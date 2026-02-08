from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
import os
import base64

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to MediaSense API"}

@app.get("/debug/cookies")
def debug_cookies():
    """
    Debug endpoint to check if COOKIES_CONTENT is loaded correctly.
    WARNING: This exposes parts of your cookies. Disable in production or use with caution.
    """
    params = os.environ.get("COOKIES_CONTENT", "")
    if not params:
        return {"status": "error", "message": "COOKIES_CONTENT is EMPTY"}

    result = {
        "status": "ok",
        "length": len(params),
        "is_base64": False,
        "content_snippet": params[:50] + "..." if len(params) > 50 else params
    }

    try:
        decoded = base64.b64decode(params, validate=True).decode('utf-8')
        result["is_base64"] = True
        result["decoded_length"] = len(decoded)
        result["decoded_snippet"] = decoded[:100] + "..." if len(decoded) > 100 else decoded
        
        if "# Netscape HTTP Cookie File" in decoded or "\t" in decoded:
            result["format_check"] = "Looks like Netscape format (GOOD)"
        else:
            result["format_check"] = "Does NOT look like Netscape format (BAD)"
            
    except Exception as e:
        result["is_base64"] = False
        result["decode_error"] = str(e)
        
    return result
