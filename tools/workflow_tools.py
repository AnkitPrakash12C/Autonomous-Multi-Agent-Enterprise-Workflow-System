import random
import uuid
from datetime import datetime, timedelta


def verify_employee_details(employee_id: str, name: str, department: str) -> dict:
    return {
        "verified": True,
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "joining_date": datetime.now().strftime("%Y-%m-%d"),
        "manager": "Rajesh Kumar",
        "location": "Bangalore"
    }


def create_system_accounts(employee_id: str, name: str, department: str) -> dict:
    email = f"{name.lower().replace(' ', '.')}@company.com"
    return {
        "email_created": email,
        "slack_account": f"@{name.lower().replace(' ', '_')}",
        "jira_account": f"JIRA-{employee_id}",
        "github_added": True,
        "vpn_access": True,
        "hr_portal": True
    }


def assign_equipment(employee_id: str, department: str) -> dict:
    equipment_map = {
        "Engineering": ["MacBook Pro 14", "External Monitor", "Mechanical Keyboard", "Mouse"],
        "Sales": ["Dell Laptop", "iPhone 15", "Headset"],
        "HR": ["Dell Laptop", "Headset"],
        "Finance": ["ThinkPad", "External Monitor"],
    }
    equipment = equipment_map.get(department, ["Dell Laptop", "Headset"])
    return {
        "assigned": equipment,
        "ticket_id": f"IT-{random.randint(10000, 99999)}",
        "delivery_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    }


def check_budget(department: str, amount: float, cost_center: str) -> dict:
    available = random.uniform(amount * 0.5, amount * 3)
    has_budget = available >= amount
    return {
        "department": department,
        "cost_center": cost_center,
        "requested_amount": amount,
        "available_budget": round(available, 2),
        "approved": has_budget,
        "budget_code": f"BDG-{random.randint(1000, 9999)}"
    }


def get_vendor_quotes(item: str, quantity: int) -> dict:
    vendors = [
        {"vendor": "TechSupply Co.", "unit_price": round(random.uniform(100, 500), 2), "delivery_days": 5},
        {"vendor": "QuickProcure Ltd.", "unit_price": round(random.uniform(100, 500), 2), "delivery_days": 3},
        {"vendor": "EnterpriseGoods Inc.", "unit_price": round(random.uniform(100, 500), 2), "delivery_days": 7},
    ]
    for v in vendors:
        v["total"] = round(v["unit_price"] * quantity, 2)
    vendors.sort(key=lambda x: x["total"])
    return {"item": item, "quantity": quantity, "quotes": vendors, "recommended": vendors[0]["vendor"]}


def raise_purchase_order(vendor: str, item: str, quantity: int, amount: float) -> dict:
    return {
        "po_number": f"PO-{random.randint(100000, 999999)}",
        "vendor": vendor,
        "item": item,
        "quantity": quantity,
        "total_amount": amount,
        "status": "raised",
        "expected_delivery": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    }


def extract_meeting_decisions(meeting_notes: str) -> dict:
    return {
        "decisions": [
            "Launch new product feature by Q3 end",
            "Hire 3 more engineers in backend team",
            "Migrate infrastructure to AWS by December"
        ],
        "action_items": [
            {"task": "Finalize feature spec", "owner": "Product Team", "deadline": "Next Friday"},
            {"task": "Post job descriptions", "owner": "HR Team", "deadline": "This week"},
            {"task": "Create migration plan", "owner": "DevOps Team", "deadline": "Two weeks"}
        ],
        "participants": ["CEO", "CTO", "Product Lead", "HR Head"],
        "meeting_date": datetime.now().strftime("%Y-%m-%d")
    }


def send_notification(recipient: str, subject: str, body: str, channel: str = "email") -> dict:
    return {
        "sent": True,
        "recipient": recipient,
        "channel": channel,
        "message_id": f"MSG-{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.now().isoformat()
    }


def draft_contract(parties: list, contract_type: str, terms: dict) -> dict:
    return {
        "contract_id": f"CTR-{random.randint(10000, 99999)}",
        "parties": parties,
        "type": contract_type,
        "version": "1.0",
        "drafted_at": datetime.now().isoformat(),
        "status": "draft",
        "clauses": ["Standard liability", "Confidentiality", "IP ownership", "Termination clause"],
        "next_step": "Legal review"
    }


def legal_review(contract_id: str) -> dict:
    approved = random.random() > 0.2
    return {
        "contract_id": contract_id,
        "reviewed_by": "Legal Team",
        "approved": approved,
        "comments": "Approved with standard terms" if approved else "Clause 4 needs revision",
        "reviewed_at": datetime.now().isoformat()
    }
