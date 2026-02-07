from typing import Dict, Any, Optional
import uuid

class TaskManager:
    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def create_task(self) -> str:
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = {
            "status": "pending",
            "progress": 0,
            "filename": None,
            "error": None,
            "filepath": None
        }
        return task_id

    def update_task(self, task_id: str, **kwargs):
        if task_id in self._tasks:
            self._tasks[task_id].update(kwargs)

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self._tasks.get(task_id)

    def fail_task(self, task_id: str, error: str):
        self.update_task(task_id, status="failed", error=error)

task_manager = TaskManager()
