import os
import shutil
import time
import uuid
import logging
from pathlib import Path
from threading import Thread

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, base_dir: str = "temp_downloads", retention_seconds: int = 300):
        self.base_dir = Path(base_dir)
        self.retention_seconds = retention_seconds
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Start cleanup thread or use a scheduler in real production
        # For this scope, we'll check on access or use a simplistic background loop if needed.
        # But actually, FastAPI background tasks can handle cleanup after serving.
        
    def create_temp_dir(self) -> Path:
        """Create a unique directory for a download task."""
        task_id = str(uuid.uuid4())
        task_dir = self.base_dir / task_id
        task_dir.mkdir(exist_ok=True)
        return task_dir, task_id

    def get_file_path(self, task_id: str, filename: str) -> Path:
        return self.base_dir / task_id / filename

    def cleanup(self, task_id: str):
        """Delete the temporary directory for a task."""
        task_dir = self.base_dir / task_id
        try:
            if task_dir.exists():
                shutil.rmtree(task_dir)
                logger.info(f"Cleaned up task {task_id}")
        except Exception as e:
            logger.error(f"Failed to cleanup {task_id}: {e}")

storage = StorageService()
