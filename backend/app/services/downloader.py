import yt_dlp
import logging
import os
import tempfile
import random
import time
import base64
from typing import Dict, Any, List
from app.core.config import settings as app_settings

logger = logging.getLogger(__name__)

class MediaExtractor:
    def __init__(self):
        self.cookie_file_path = None
        if app_settings.COOKIES_CONTENT:
            self.cookie_file_path = self._write_cookies_file(app_settings.COOKIES_CONTENT)

        self.ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'verbose': True,
            'noplaylist': True,
            'extract_flat': False,
            'simulate': True,
            'skip_download': True,
            'ignore_no_formats_error': True,  # Don't crash if some formats are missing
            'check_formats': False,          # Don't stricter validate formats
            'allowed_extractors': ['default', 'youtube', 'pinterest', 'instagram', 'twitter'], 
            'socket_timeout': 30,
            # Force IPv4 to avoid common IPv6 blocks in datacenters
            'source_address': '0.0.0.0', 
            'outtmpl': '%(title)s.%(ext)s',
            # Anti-bot measures
            # 'user_agent': '...', # REMOVED: Let yt-dlp pick the correct UA for the client (ios/android)
            'sleep_interval': random.randint(2, 5),
            # Removed specific player_client args to let new yt-dlp version handle defaults
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

        if self.cookie_file_path:
            self.ydl_opts['cookiefile'] = self.cookie_file_path

        if app_settings.PROXY_URL:
            self.ydl_opts['proxy'] = app_settings.PROXY_URL
            logger.info("Using Proxy for yt-dlp")

    def download_media(self, url: str, format_id: str, output_dir: str, progress_hook=None) -> str:
        """
        Download media to the specified directory.
        Returns the path to the downloaded file.
        """
        opts = self.ydl_opts.copy()
        opts['simulate'] = False
        opts['skip_download'] = False
        opts['paths'] = {'home': output_dir}
        if progress_hook:
            opts['progress_hooks'] = [progress_hook]

        if format_id == 'best':
            opts['format'] = 'bestvideo+bestaudio/best'
        else:
            opts['format'] = format_id

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # yt-dlp might return a list if it's a playlist (disabled) or just info
                # The filename can be tricky to predict exactly because of merging.
                # We often use 'prepare_filename' but it might differ after merge.
                # A robust way is to finding the file in the dir since we make a unique dir.
                return ydl.prepare_filename(info)
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            raise ValueError(f"Download failed: {str(e)}")


    def extract_info(self, url: str) -> Dict[str, Any]:
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return self._process_info(info)
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            raise ValueError(f"Failed to extract media info: {str(e)}")

    def _process_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the data from yt-dlp into our MediaData format.
        """
        formats = []
        seen_resolutions = set()

        raw_formats = info.get('formats', [])
        
        # Sort best to worst
        raw_formats.sort(key=lambda x: (x.get('height') or 0, x.get('tbr') or 0), reverse=True)

        for f in raw_formats:
            # Skip formats without video or audio if we want mixed, 
            # but yt-dlp separates them often. 
            # For now, let's list distinct video qualities and audio.
            
            ext = f.get('ext')
            height = f.get('height')
            format_id = f.get('format_id')
            filesize = f.get('filesize')
            
            # Simple filtering logic
            if height: # Video
                res_str = f"{height}p"
                
                # Filter out storyboards/mhtml which often appear when main formats are blocked
                if ext in ['mhtml', 'html', 'htm']:
                    continue
                if 'storyboard' in f.get('format_note', '') or 'storyboard' in f.get('protocol', ''):
                    continue

                # Removed 'ext != webm' check to allow VP9/AV1 formats which are standard now
                if res_str not in seen_resolutions: 
                    formats.append({
                        "resolution": res_str,
                        "ext": ext,
                        "size": self._format_size(filesize),
                        "format_id": format_id,
                        "type": "video"
                    })
                    seen_resolutions.add(res_str)
            elif f.get('acodec') != 'none' and f.get('vcodec') == 'none': # Audio only
                 formats.append({
                        "resolution": "Audio",
                        "ext": ext,
                        "size": self._format_size(filesize),
                        "format_id": format_id,
                        "type": "audio"
                    })

        # Add "Best" option
        formats.insert(0, {
            "resolution": "Best Quality",
            "ext": info.get('ext', 'mp4'),
            "size": "Variable",
            "format_id": "best",
            "type": "best"
        })

        return {
            "title": info.get('title'),
            "thumbnail": info.get('thumbnail'),
            "duration": self._format_duration(info.get('duration')),
            "platform": info.get('extractor_key'),
            "formats": formats
        }

    def _format_size(self, size: int) -> str:
        if not size:
            return "Unknown"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def _format_duration(self, seconds: int) -> str:
        if not seconds:
            return "0:00"
        # Convert to int to handle float values from yt-dlp
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"

    def _write_cookies_file(self, content: str) -> str:
        """
        Write cookies content to a temporary file.
        Supports both direct text and Base64 encoded content (safer for Env Vars).
        """
        try:
            # Try to decode Base64 first
            try:
                decoded = base64.b64decode(content).decode('utf-8')
                # Check if it looks like a Netscape cookie file (starts with # usually, or contains tab separators)
                if "# Netscape HTTP Cookie File" in decoded or "\t" in decoded:
                    content = decoded
                    logger.info(f"Successfully decoded Base64 cookies. Length: {len(content)}")
            except Exception as e:
                logger.warning(f"Base64 decode failed or not needed: {e}")
                # If decode fails, assume it's raw text
                pass

            fd, path = tempfile.mkstemp(suffix='.txt', text=True)
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Debug: Read back to ensure it wrote correctly
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                logger.info(f"Cookies file created at {path}. First line: {first_line[:50]}...")

            return path
        except Exception as e:
            logger.error(f"Failed to create cookies file: {e}")
            return None

extractor = MediaExtractor()
