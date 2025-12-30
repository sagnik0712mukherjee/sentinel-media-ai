import cv2
import os
import shutil
from typing import List, Tuple
import uuid


class FrameSampler:
    def __init__(self, interval_seconds: int = 5, base_output_dir: str = "data/tmp/frames"):
        self.interval_seconds = interval_seconds
        self.base_output_dir = base_output_dir
        os.makedirs(self.base_output_dir, exist_ok=True)

    def sample(self, video_path: str) -> Tuple[List[str], callable]:
        """
        Samples frames from a video and returns:
        - list of frame paths
        - cleanup function to delete them safely
        """

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Unable to open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = max(int(fps * self.interval_seconds), 1)

        # Create isolated temp directory per run
        run_id = uuid.uuid4().hex
        output_dir = os.path.join(self.base_output_dir, run_id)
        os.makedirs(output_dir, exist_ok=True)

        frame_count = 0
        saved_frames = []

        success, frame = cap.read()
        while success:
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(
                    output_dir, f"frame_{frame_count}.jpg"
                )
                cv2.imwrite(frame_path, frame)
                saved_frames.append(frame_path)

            success, frame = cap.read()
            frame_count += 1

        cap.release()

        def cleanup():
            shutil.rmtree(output_dir, ignore_errors=True)

        return saved_frames, cleanup
