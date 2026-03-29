import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
os.makedirs(STATE_DIR, exist_ok=True)


class WorkflowState:
    def __init__(self, workflow_id: str, workflow_type: str, input_data: Dict):
        self.workflow_id = workflow_id
        self.workflow_type = workflow_type
        self.input_data = input_data
        self.status = "running"
        self.current_step = 0
        self.steps_completed = []
        self.steps_failed = []
        self.retry_counts = {}
        self.collected_data = {}
        self.decisions = []
        self.actions_taken = []
        self.errors = []
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.human_approvals_needed = []
        self.human_approvals_received = []

    def to_dict(self) -> Dict:
        return self.__dict__.copy()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.updated_at = datetime.now().isoformat()

    def add_error(self, step: str, error: str):
        self.errors.append({"step": step, "error": error, "timestamp": datetime.now().isoformat()})
        self.steps_failed.append(step)
        self.updated_at = datetime.now().isoformat()

    def increment_retry(self, step: str) -> int:
        self.retry_counts[step] = self.retry_counts.get(step, 0) + 1
        return self.retry_counts[step]

    def save(self, state_dir: str = STATE_DIR):
        path = os.path.join(state_dir, f"{self.workflow_id}_state.json")
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)

    @classmethod
    def load(cls, workflow_id: str, state_dir: str = STATE_DIR) -> Optional["WorkflowState"]:
        path = os.path.join(state_dir, f"{workflow_id}_state.json")
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj

    @classmethod
    def list_all(cls, state_dir: str = STATE_DIR):
        files = [f for f in os.listdir(state_dir) if f.endswith("_state.json")]
        states = []
        for f in files:
            path = os.path.join(state_dir, f)
            with open(path, "r") as fp:
                states.append(json.load(fp))
        return sorted(states, key=lambda x: x.get("created_at", ""), reverse=True)
