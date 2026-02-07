# MediaSense

**Universal Media Downloader** - Secure, Fast, Premium.

## Features
- **Auto-Detection**: Pasting a link automatically detects the platform and media type.
- **Multi-Platform Support**: YouTube, Pinterest, Instagram, X (Twitter).
- **High Quality**: Downloads in best available resolution (up to 8K) and bitrate.
- **Secure**: No background scraping, no login required, privacy-focused.
- **Ad-Friendly UI**: Premium design ready for monetization.

## Tech Stack
- **Frontend**: Next.js 15, React, Tailwind CSS, Framer Motion.
- **Backend**: FastAPI, yt-dlp, FFmpeg.

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- FFmpeg installed and in system PATH.

### Backend Setup
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # Or manually: pip install fastapi uvicorn yt-dlp ffmpeg-python python-multipart
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Server will run at `http://localhost:8000`.

### Frontend Setup
1. Navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   App will run at `http://localhost:3000`.

## Configuration
- Backend settings in `backend/app/core/config.py`.
- Frontend API URL is currently set to `http://localhost:8000/api/v1`.

## Deployment
- **Frontend**: Deploy to Vercel or Netlify.
- **Backend**: Deploy to VPS, Railway, or Render (requires FFmpeg).

## License
MIT
