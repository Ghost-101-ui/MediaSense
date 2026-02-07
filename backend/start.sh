#!/bin/bash
# Quick deployment script for Railway/Render

# Install system dependencies
apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
