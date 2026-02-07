from fastapi import APIRouter
from app.api.endpoints import analyze, download

api_router = APIRouter()
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
api_router.include_router(download.router, prefix="/download", tags=["download"])
