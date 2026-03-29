import json
import re
import google.generativeai as genai
# from google import genai
from config import GEMINI_MODEL, AGENT_PERSONAS
from tools.workflow_tools import (
    create_system_accounts, assign_equipment, raise_purchase_order,
    send_notification, legal_review
)
from utils.audit_logger import AuditLogger


class ActionAgent:
    def __init__(self, audit_logger: AuditLogger):
        self.model = genai.GenerativeModel(
            GEMINI_MODEL,
            system_instruction=AGENT_PERSONAS["action"]
        )
        self.audit = audit_logger
        self.name = "ActionAgent"

    def execute(self, workflow_type: str, decision: dict, collected_data: dict, input_data: dict) -> dict:
        self.audit.log(self.name, "start_execution", {
            "workflow_type": workflow_type,
            "next_actions": decision.get("next_actions", [])
        })
        results = {}

        try:
            if workflow_type == "employee_onboarding":
                accounts = create_system_accounts(
                    input_data.get("employee_id", "EMP001"),
                    input_data.get("name", "Employee"),
                    input_data.get("department", "Engineering")
                )
                results["accounts_created"] = accounts
                self.audit.log(self.name, "create_accounts", accounts)

                equipment = assign_equipment(
                    input_data.get("employee_id", "EMP001"),
                    input_data.get("department", "Engineering")
                )
                results["equipment_assigned"] = equipment
                self.audit.log(self.name, "assign_equipment", equipment)

                notif = send_notification(
                    recipient=input_data.get("name", "Employee"),
                    subject="Welcome to the Company!",
                    body=f"Your accounts have been created. Email: {accounts.get('email_created', 'N/A')}",
                    channel="email"
                )
                results["welcome_email"] = notif
                self.audit.log(self.name, "send_welcome_email", notif)

            elif workflow_type == "procurement_to_payment":
                quotes = collected_data.get("vendor_quotes", {})
                recommended_vendor = quotes.get("recommended", "Default Vendor")
                amount = float(input_data.get("amount", 5000))
                po = raise_purchase_order(
                    vendor=recommended_vendor,
                    item=input_data.get("item", "Equipment"),
                    quantity=int(input_data.get("quantity", 1)),
                    amount=amount
                )
                results["purchase_order"] = po
                self.audit.log(self.name, "raise_purchase_order", po)

                notif = send_notification(
                    recipient="finance@company.com",
                    subject=f"PO Raised: {po.get('po_number', 'N/A')}",
                    body=f"Purchase Order raised for {po.get('vendor')}. Amount: ₹{po.get('total_amount')}",
                    channel="email"
                )
                results["po_notification"] = notif
                self.audit.log(self.name, "notify_finance", notif)

            elif workflow_type == "contract_lifecycle":
                contract_id = collected_data.get("contract_draft", {}).get("contract_id", "CTR-00000")
                review = legal_review(contract_id)
                results["legal_review"] = review
                self.audit.log(self.name, "legal_review", review)

                notif = send_notification(
                    recipient="legal@company.com",
                    subject=f"Contract {contract_id} Ready",
                    body=f"Contract reviewed and {'approved' if review.get('approved') else 'needs revision'}.",
                    channel="email"
                )
                results["legal_notification"] = notif
                self.audit.log(self.name, "notify_legal", notif)

            elif workflow_type == "meeting_intelligence":
                meeting_data = collected_data.get("meeting_data", {})
                action_items = meeting_data.get("action_items", [])
                notifications_sent = []
                for item in action_items:
                    notif = send_notification(
                        recipient=item.get("owner", "Team"),
                        subject=f"Action Item Assigned: {item.get('task', '')}",
                        body=f"Task: {item.get('task')}. Deadline: {item.get('deadline')}",
                        channel="slack"
                    )
                    notifications_sent.append(notif)
                    self.audit.log(self.name, f"assign_task", {"task": item.get("task"), "notif": notif})
                results["task_notifications"] = notifications_sent

        except Exception as tool_err:
            self.audit.log(self.name, "action_tool_error", {"error": str(tool_err)}, status="warning")
            results["partial_error"] = str(tool_err)

        # Gemini summary — safe fallback
        try:
            prompt = f"""
You executed workflow actions for {workflow_type}.
Results: {json.dumps(results, indent=2)}

Write a brief executive summary. Respond ONLY in this exact JSON:
{{"summary": "Brief summary here", "completed_count": 3, "follow_up_items": [], "status": "completed"}}
"""
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
            match = re.search(r'\{.*\}', text, re.DOTALL)
            summary = json.loads(match.group()) if match else None
            if not summary:
                raise ValueError("No JSON")
        except Exception as e:
            self.audit.log(self.name, "summary_fallback", {"error": str(e)}, status="warning")
            summary = {
                "summary": f"Workflow actions for {workflow_type} completed. {len(results)} steps executed successfully.",
                "completed_count": len(results),
                "follow_up_items": [],
                "status": "completed"
            }

        results["execution_summary"] = summary
        self.audit.log(self.name, "execution_complete", summary)
        return results
