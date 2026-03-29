import json
import os
from datetime import datetime
from typing import Any

AUDIT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "audit")
os.makedirs(AUDIT_DIR, exist_ok=True)


class AuditLogger:
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.log_file = os.path.join(AUDIT_DIR, f"{workflow_id}.json")
        self.entries = []
        self._load_existing()

    def _load_existing(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                self.entries = json.load(f)

    def log(self, agent: str, action: str, details: Any, status: str = "success"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "workflow_id": self.workflow_id,
            "agent": agent,
            "action": action,
            "details": details,
            "status": status
        }
        self.entries.append(entry)
        self._save()
        return entry

    def _save(self):
        with open(self.log_file, "w") as f:
            json.dump(self.entries, f, indent=2, default=str)

    def get_trail(self):
        return self.entries

    def get_summary(self):
        total = len(self.entries)
        by_agent = {}
        by_status = {}
        for e in self.entries:
            by_agent[e["agent"]] = by_agent.get(e["agent"], 0) + 1
            by_status[e["status"]] = by_status.get(e["status"], 0) + 1
        return {
            "workflow_id": self.workflow_id,
            "total_actions": total,
            "by_agent": by_agent,
            "by_status": by_status,
            "first_action": self.entries[0]["timestamp"] if self.entries else None,
            "last_action": self.entries[-1]["timestamp"] if self.entries else None
        }
