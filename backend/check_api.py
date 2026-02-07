import urllib.request
import time
import json

url = "http://127.0.0.1:8000/api/v1/analyze/?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"

print(f"Checking {url}...")
start_time = time.time()
try:
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        end_time = time.time()
        print(f"Success! Status: {response.status}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Title: {data.get('title', 'Unknown')}")
except Exception as e:
    print(f"Error: {e}")
