import json
import re
import google.generativeai as genai
# from google import genai
from config import GEMINI_MODEL, AGENT_PERSONAS
from tools.workflow_tools import (
    verify_employee_details, check_budget, get_vendor_quotes,
    extract_meeting_decisions, draft_contract
)
from utils.audit_logger import AuditLogger


class DataRetrievalAgent:
    def __init__(self, audit_logger: AuditLogger):
        self.model = genai.GenerativeModel(
            GEMINI_MODEL,
            system_instruction=AGENT_PERSONAS["data_retrieval"]
        )
        self.audit = audit_logger
        self.name = "DataRetrievalAgent"

    def retrieve(self, workflow_type: str, input_data: dict) -> dict:
        self.audit.log(self.name, "start_retrieval", {
            "workflow_type": workflow_type,
            "input": input_data
        })
        collected = {}

        try:
            if workflow_type == "employee_onboarding":
                result = verify_employee_details(
                    input_data.get("employee_id", "EMP001"),
                    input_data.get("name", "New Employee"),
                    input_data.get("department", "Engineering")
                )
                collected["employee_record"] = result
                self.audit.log(self.name, "verify_employee", result)

            elif workflow_type == "procurement_to_payment":
                budget = check_budget(
                    input_data.get("department", "Engineering"),
                    float(input_data.get("amount", 5000)),
                    input_data.get("cost_center", "CC-001")
                )
                collected["budget_check"] = budget
                self.audit.log(self.name, "check_budget", budget)

                quotes = get_vendor_quotes(
                    input_data.get("item", "Laptop"),
                    int(input_data.get("quantity", 1))
                )
                collected["vendor_quotes"] = quotes
                self.audit.log(self.name, "get_vendor_quotes", quotes)

            elif workflow_type == "meeting_intelligence":
                decisions = extract_meeting_decisions(
                    input_data.get("meeting_notes", "")
                )
                collected["meeting_data"] = decisions
                self.audit.log(self.name, "extract_meeting_data", decisions)

            elif workflow_type == "contract_lifecycle":
                contract = draft_contract(
                    input_data.get("parties", ["Company A", "Company B"]),
                    input_data.get("contract_type", "Service Agreement"),
                    input_data.get("terms", {})
                )
                collected["contract_draft"] = contract
                self.audit.log(self.name, "draft_contract", contract)

        except Exception as tool_err:
            self.audit.log(self.name, "tool_error", {"error": str(tool_err)}, status="warning")

        try:
            prompt = f"""
You are reviewing data collected for a {workflow_type} workflow.
Data collected: {json.dumps(collected, indent=2)}
Original request: {json.dumps(input_data, indent=2)}

Validate the data quality briefly. Respond ONLY in this exact JSON (no markdown, no extra text):
{{"valid": true, "completeness_score": 85, "missing_fields": [], "warnings": [], "summary": "Data looks good"}}
"""
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Strip markdown code fences if present
            text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                validation = json.loads(match.group())
            else:
                raise ValueError("No JSON found in response")
        except Exception as gemini_err:
            self.audit.log(self.name, "gemini_validation_fallback", {"error": str(gemini_err)}, status="warning")
            validation = {
                "valid": True,
                "completeness_score": 80,
                "missing_fields": [],
                "warnings": [],
                "summary": "Data collected successfully (validation skipped)"
            }

        collected["validation"] = validation
        self.audit.log(self.name, "validate_data", validation)
        return collected
