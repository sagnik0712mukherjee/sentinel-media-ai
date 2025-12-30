"""
Sample Pipeline Run
-------------------

Demonstrates an end-to-end execution
of the agentic media intelligence pipeline.
"""

from src.ingestion.video_loader import VideoLoader
from src.ingestion.audio_extractor import AudioExtractor
from src.processing.frame_sampler import FrameSampler
from src.orchestration.workflow_runner import WorkflowRunner


def main():
    print("🚀 Starting sample run")

    # --------------------------------------------------
    # Ingest video
    # --------------------------------------------------
    video_loader = VideoLoader()
    video_info = video_loader.load("sample_video.mp4")  # replace path

    media_id = video_info["media_id"]
    video_path = video_info["video_path"]

    print(f"Media ID: {media_id}")

    # --------------------------------------------------
    # Extract audio
    # --------------------------------------------------
    audio_extractor = AudioExtractor()
    audio_path = audio_extractor.extract(video_path, media_id)

    print(f"Audio extracted: {audio_path}")

    # --------------------------------------------------
    # Sample frames (NEW)
    # --------------------------------------------------
    frame_sampler = FrameSampler()
    frame_paths, cleanup_frames = frame_sampler.sample(video_path)

    print(f"Sampled {len(frame_paths)} frames")

    # --------------------------------------------------
    # Run agentic workflow
    # --------------------------------------------------
    runner = WorkflowRunner(media_id=media_id)

    try:
        context = runner.run(
            audio_path=audio_path,
            frame_paths=frame_paths,
        )

        print("\n🧠 AGENT OUTPUT SUMMARY")
        print("-" * 40)

        for key, value in context.items():
            print(f"\n[{key.upper()}]")
            print(value)

    finally:
        # 🔥 ALWAYS clean up frames
        cleanup_frames()

    print("\n✅ Sample run completed successfully")


if __name__ == "__main__":
    main()
