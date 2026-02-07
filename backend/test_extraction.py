from app.services.downloader import extractor
import sys

# Test with a known safer URL (e.g. a simple public video or even a non-video URL that yt-dlp might handle info for, but let's stick to a safe youtube video)
# "Me at the zoo" - the first video on YouTube, usually safe.
url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 

try:
    print(f"Testing extraction for: {url}")
    data = extractor.extract_info(url)
    print("Extraction successful!")
    print(f"Title: {data.get('title')}")
    print(f"Formats found: {len(data.get('formats', []))}")
except Exception as e:
    print(f"Extraction failed: {e}")
    sys.exit(1)
