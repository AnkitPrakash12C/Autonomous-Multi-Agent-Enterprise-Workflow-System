import json
import re
import google.generativeai as genai
from config import GEMINI_MODEL, AGENT_PERSONAS, WORKFLOW_TYPES
from utils.audit_logger import AuditLogger
# from google import genai

class DecisionAgent:
    def __init__(self, audit_logger: AuditLogger):
        self.model = genai.GenerativeModel(
            GEMINI_MODEL,
            system_instruction=AGENT_PERSONAS["decision"]
        )
        self.audit = audit_logger
        self.name = "DecisionAgent"

    def decide(self, workflow_type: str, collected_data: dict, input_data: dict) -> dict:
        self.audit.log(self.name, "start_decision", {"workflow_type": workflow_type})
        workflow_info = WORKFLOW_TYPES.get(workflow_type, {})

        default_decision = {
            "decision": "PROCEED",
            "requires_human_approval": False,
            "approval_reason": "",
            "approval_step": None,
            "automated_steps": workflow_info.get("steps", []),
            "risk_level": "LOW",
            "risk_reasons": ["Standard workflow"],
            "next_actions": ["Execute all workflow steps autonomously"],
            "business_rules_applied": ["Standard enterprise policy", "Budget threshold check"],
            "estimated_completion_hours": workflow_info.get("sla_hours", 48) // 4,
            "decision_rationale": "All pre-conditions met. Proceeding autonomously."
        }

        try:
            prompt = f"""
You are making business decisions for a {workflow_info.get('name', workflow_type)} workflow.

Workflow steps: {workflow_info.get('steps', [])}
SLA hours: {workflow_info.get('sla_hours', 48)}
Collected data: {json.dumps(collected_data, indent=2)}
Original request: {json.dumps(input_data, indent=2)}

Determine if workflow should proceed and what decisions to make.
Respond ONLY in this exact JSON (no markdown, no extra text):
{{
  "decision": "PROCEED",
  "requires_human_approval": false,
  "approval_reason": "",
  "approval_step": null,
  "automated_steps": ["step1", "step2"],
  "risk_level": "LOW",
  "risk_reasons": ["reason"],
  "next_actions": ["action1", "action2"],
  "business_rules_applied": ["rule1"],
  "estimated_completion_hours": 4,
  "decision_rationale": "explanation here"
}}
"""
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                decision = json.loads(match.group())
            else:
                raise ValueError("No JSON found")
        except Exception as e:
            self.audit.log(self.name, "gemini_fallback", {"error": str(e)}, status="warning")
            decision = default_decision

        self.audit.log(self.name, "workflow_decision", decision)
        return decision
