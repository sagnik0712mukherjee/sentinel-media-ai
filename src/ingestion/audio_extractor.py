"""
Audio Extractor
---------------

Extracts audio track from video files
for speech-to-text processing.
"""

import os
from moviepy import VideoFileClip


class AudioExtractor:
    """
    Extracts audio from video files.
    """

    def __init__(self, output_dir: str = "workspace/audio"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # --------------------------------------------------

    def extract(self, video_path: str, media_id: str) -> str:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        audio_path = os.path.join(
            self.output_dir, f"{media_id}.wav"
        )

        clip = VideoFileClip(video_path)

        if clip.audio is None:
            raise RuntimeError("No audio track found in video")

        # New moviepy-compatible call
        clip.audio.write_audiofile(
            audio_path,
            codec="pcm_s16le",
        )

        clip.close()

        return audio_path
