import yt_dlp
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MediaExtractor:
    def __init__(self):
        self.ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'verbose': True,
            'noplaylist': True,  # Single video only
            'extract_flat': False, # Need full info for formats
            'simulate': True, # Do not download video
            'skip_download': True,
            'allowed_extractors': ['default', 'youtube', 'pinterest', 'instagram', 'twitter'], 
            'socket_timeout': 10,
            'outtmpl': '%(title)s.%(ext)s',
        }

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
                if res_str not in seen_resolutions and ext != 'webm': # Prefer mp4 for compatibility
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

extractor = MediaExtractor()
