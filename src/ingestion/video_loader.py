"""
Video Loader
------------

Handles ingestion of local video files
and standardizes storage paths.
"""

import os
import shutil
from uuid import uuid4


class VideoLoader:
    """
    Loads and prepares local video files
    for processing.
    """

    def __init__(self, workspace_dir: str = "workspace/videos"):
        self.workspace_dir = workspace_dir
        os.makedirs(self.workspace_dir, exist_ok=True)

    # --------------------------------------------------

    def load(self, video_path: str) -> dict:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        media_id = str(uuid4())
        ext = os.path.splitext(video_path)[-1]

        dest_path = os.path.join(
            self.workspace_dir, f"{media_id}{ext}"
        )

        shutil.copy(video_path, dest_path)

        return {
            "media_id": media_id,
            "video_path": dest_path,
        }
