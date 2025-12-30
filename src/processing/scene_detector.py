"""
Scene Detector
--------------

Provides simple time-based scene segmentation
for videos.
"""

from typing import List, Tuple

import cv2


class SceneDetector:
    """
    Detects scenes based on fixed time windows.
    """

    def __init__(self, scene_duration_seconds: int = 30):
        self.scene_duration_seconds = scene_duration_seconds

    def detect(self, video_path: str) -> List[Tuple[int, int]]:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Unable to open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_seconds = int(total_frames / fps)

        scenes = []
        start = 0

        while start < duration_seconds:
            end = min(start + self.scene_duration_seconds, duration_seconds)
            scenes.append((start, end))
            start = end

        cap.release()
        return scenes
