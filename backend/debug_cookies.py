import os
import sys
import base64
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cookie_debugger")

def debug_cookies():
    params = os.environ.get("COOKIES_CONTENT", "")
    if not params:
        logger.error("COOKIES_CONTENT environment variable is EMPTY!")
        return

    logger.info(f"COOKIES_CONTENT length: {len(params)}")
    
    content = params
    try:
        decoded = base64.b64decode(params, validate=True).decode('utf-8')
        if "# Netscape HTTP Cookie File" in decoded or "\t" in decoded:
            content = decoded
            logger.info("Successfully decoded Base64 content.")
            logger.info(f"Decoded length: {len(content)}")
            logger.info(f"First 100 chars: {content[:100]}")
        else:
            logger.warning("Decoded content does not look like Netscape format (no header or tabs).")
            logger.info(f"First 100 chars of decoded: {decoded[:100]}")
    except Exception as e:
        logger.info(f"Content is likely NOT Base64 or decode failed: {e}")
        logger.info(f"First 100 chars of raw content: {content[:100]}")

    # Try writing to file
    try:
        fd, path = tempfile.mkstemp(suffix='.txt', text=True)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Successfully wrote to temp file: {path}")
        
        # Verify file size
        size = os.path.getsize(path)
        logger.info(f"File size: {size} bytes")
        
        # Clean up
        os.remove(path)
        logger.info("Test file deleted.")
        
    except Exception as e:
        logger.error(f"Failed to write/read temp file: {e}")

if __name__ == "__main__":
    print("--- Cookie Debugger ---")
    debug_cookies()
    print("--- End Debugger ---")
