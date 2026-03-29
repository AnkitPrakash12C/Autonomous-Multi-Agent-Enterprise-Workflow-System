import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents.orchestrator import OrchestratorAgent
from config import WORKFLOW_TYPES


def main():
    print("\n" + "="*60)
    print("  ⚡ Enterprise Workflow AI - PS2 Hackathon Demo")
    print("="*60)

    print("\nAvailable Workflows:")
    for i, (key, val) in enumerate(WORKFLOW_TYPES.items(), 1):
        print(f"  {i}. {val['name']}")

    choice = input("\nSelect workflow (1-4): ").strip()
    idx = int(choice) - 1
    workflow_type = list(WORKFLOW_TYPES.keys())[idx]

    print(f"\n✅ Selected: {WORKFLOW_TYPES[workflow_type]['name']}")
    print("\nUsing default demo input data...\n")

    demo_inputs = {
        "employee_onboarding": {"name": "Priya Mehta", "employee_id": "EMP2026099", "department": "Engineering"},
        "procurement_to_payment": {"item": "Dell Server", "quantity": 2, "amount": 180000, "department": "Engineering", "cost_center": "CC-001"},
        "meeting_intelligence": {"meeting_notes": "Q4 planning. Decision: Expand to 3 new cities. Arjun to lead ops. Budget ₹50L approved. Timeline: 6 months."},
        "contract_lifecycle": {"parties": ["ABC Corp", "XYZ Ltd"], "contract_type": "Service Agreement", "value": 2500000}
    }

    input_data = demo_inputs[workflow_type]

    def progress_cb(step, message, agent):
        print(f"  [{agent}] {message}")

    print("🚀 Launching autonomous workflow...\n")
    orchestrator = OrchestratorAgent()
    result = orchestrator.run_workflow(workflow_type, input_data, progress_callback=progress_cb)

    print("\n" + "="*60)
    print(f"  Workflow ID : {result.get('workflow_id')}")
    print(f"  Status      : {result.get('status')}")
    print(f"  Quality     : {result.get('verification', {}).get('quality_score', 'N/A')}/100")
    print(f"  Audit Events: {result.get('audit_summary', {}).get('total_actions', 0)}")
    print("="*60)
    print(f"\n📋 Summary: {result.get('executive_summary', 'No summary.')}\n")


if __name__ == "__main__":
    main()