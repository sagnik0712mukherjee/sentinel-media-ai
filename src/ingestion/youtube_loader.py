"""
YouTube Loader
--------------

Downloads videos from YouTube URLs
for ingestion into the pipeline.
"""

import os
from uuid import uuid4

from yt_dlp import YoutubeDL


class YouTubeLoader:
    """
    Downloads and prepares YouTube videos.
    """

    def __init__(self, workspace_dir: str = "workspace/videos"):
        self.workspace_dir = workspace_dir
        os.makedirs(self.workspace_dir, exist_ok=True)

    # --------------------------------------------------

    def load(self, youtube_url: str) -> dict:
        media_id = str(uuid4())
        output_path = os.path.join(self.workspace_dir, media_id)

        ydl_opts = {
            "outtmpl": f"{output_path}.%(ext)s",
            "format": "mp4/bestaudio+best",
            "quiet": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            video_ext = info.get("ext", "mp4")

        return {
            "media_id": media_id,
            "video_path": f"{output_path}.{video_ext}",
            "title": info.get("title"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
        }
