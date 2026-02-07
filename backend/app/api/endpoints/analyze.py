from fastapi import APIRouter, HTTPException, Query
from app.services.downloader import extractor
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Format(BaseModel):
    resolution: str
    ext: str
    size: str
    format_id: str
    type: str

class MediaResponse(BaseModel):
    title: str
    thumbnail: str
    duration: str
    platform: str
    formats: List[Format]

@router.get("/", response_model=MediaResponse)
async def analyze_url(url: str = Query(..., title="Media URL", min_length=5)):
    """
    Analyze a URL and return available media formats.
    """
    try:
        data = extractor.extract_info(url)
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during analysis")
