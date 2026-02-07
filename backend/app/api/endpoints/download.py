import os
import threading
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.downloader import extractor
from app.services.storage import storage
from app.services.task_manager import task_manager

router = APIRouter()

class DownloadRequest(BaseModel):
    url: str
    format_id: str

class DownloadResponse(BaseModel):
    task_id: str
    status: str

def process_download(task_id: str, url: str, format_id: str):
    try:
        task_dir, _ = storage.create_temp_dir()
        # We use the existing task_id for tracking, but create storage for it.
        # Actually storage.create_temp_dir returns a NEW uuid. 
        # Let's fix storage to accept an ID or just use the one from task_manager.
        
        # Override storage logic slightly here or update storage service?
        # Let's just use the path from storage.create_temp_dir but map it.
        # Wait, better:
        task_dir_path = storage.base_dir / task_id
        task_dir_path.mkdir(exist_ok=True)
        
        task_manager.update_task(task_id, status="processing", progress=0)

        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    p = d.get('_percent_str', '0%').replace('%','')
                    task_manager.update_task(task_id, progress=float(p))
                except:
                    pass
            elif d['status'] == 'finished':
                task_manager.update_task(task_id, progress=100, status="completed")

        filepath = extractor.download_media(url, format_id, str(task_dir_path), progress_hook)
        filename = os.path.basename(filepath)
        
        task_manager.update_task(task_id, status="completed", filepath=filepath, filename=filename)
        
        # Schedule cleanup? handled by separate cleaner or retention policy
        
    except Exception as e:
        task_manager.fail_task(task_id, str(e))

@router.post("/", response_model=DownloadResponse)
async def start_download(req: DownloadRequest, background_tasks: BackgroundTasks):
    task_id = task_manager.create_task()
    background_tasks.add_task(process_download, task_id, req.url, req.format_id)
    return {"task_id": task_id, "status": "pending"}

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/file/{task_id}")
async def get_file(task_id: str):
    task = task_manager.get_task(task_id)
    if not task or task['status'] != 'completed' or not task['filepath']:
        raise HTTPException(status_code=404, detail="File not ready or found")
    
    return FileResponse(
        path=task['filepath'], 
        filename=task['filename'], 
        media_type='application/octet-stream'
    )
