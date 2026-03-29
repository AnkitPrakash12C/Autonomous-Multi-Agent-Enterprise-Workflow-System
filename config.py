import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-2.5-flash"

WORKFLOW_TYPES = {
    "employee_onboarding": {
        "name": "Employee Onboarding",
        "description": "End-to-end onboarding for new employees",
        "steps": [
            "verify_employee_details",
            "create_accounts",
            "assign_equipment",
            "schedule_orientation",
            "assign_buddy",
            "send_welcome_email",
            "verify_completion"
        ],
        "sla_hours": 48
    },
    "procurement_to_payment": {
        "name": "Procurement to Payment",
        "description": "Full procurement lifecycle from request to payment",
        "steps": [
            "validate_purchase_request",
            "check_budget_availability",
            "get_vendor_quotes",
            "approval_routing",
            "raise_purchase_order",
            "goods_receipt_check",
            "invoice_matching",
            "trigger_payment",
            "verify_completion"
        ],
        "sla_hours": 72
    },
    "contract_lifecycle": {
        "name": "Contract Lifecycle Management",
        "description": "Contract creation, review, approval and execution",
        "steps": [
            "intake_contract_request",
            "draft_contract",
            "legal_review",
            "stakeholder_approval",
            "counterparty_signature",
            "execute_contract",
            "store_and_notify",
            "verify_completion"
        ],
        "sla_hours": 120
    },
    "meeting_intelligence": {
        "name": "Meeting Intelligence",
        "description": "Extract decisions, create tasks, assign owners from meetings",
        "steps": [
            "ingest_meeting_notes",
            "extract_decisions",
            "identify_action_items",
            "assign_owners",
            "set_deadlines",
            "send_notifications",
            "track_completion",
            "verify_completion"
        ],
        "sla_hours": 24
    }
}

AGENT_PERSONAS = {
    "orchestrator": "You are the Orchestrator Agent for an enterprise workflow automation system. Coordinate specialized agents, track workflow state, detect failures, trigger recovery, and maintain an auditable decision trail. Be precise, structured, and business-focused.",
    "data_retrieval": "You are the Data Retrieval Agent. Gather, validate, and structure data needed for enterprise workflows. Check employee databases, vendor systems, budget systems, and document repositories. Flag any data inconsistencies.",
    "decision": "You are the Decision Agent. Apply business rules, compliance checks, and approval logic to workflow data. Determine if conditions are met, who needs to approve, and what the next action should be. Reason step by step.",
    "action": "You are the Action Agent. Execute approved workflow steps including creating accounts, sending emails, updating records, raising POs, and triggering downstream systems. Report exactly what action was taken.",
    "verification": "You are the Verification Agent. Independently validate that each workflow step completed successfully. Check outputs match expected outcomes, flag discrepancies, and confirm SLA compliance. You are the quality gate."
}
