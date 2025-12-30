import streamlit as st
from uuid import uuid4

from src.ingestion.video_loader import VideoLoader
from src.ingestion.youtube_loader import YouTubeLoader
from src.ingestion.audio_extractor import AudioExtractor
from src.processing.frame_sampler import FrameSampler


def render_upload_page():
    st.header("📤 Upload Media")

    upload_type = st.radio(
        "Choose input type",
        ["Upload Video File", "YouTube URL"],
    )

    if upload_type == "Upload Video File":
        uploaded_file = st.file_uploader(
            "Upload a video file", type=["mp4", "mov", "mkv"]
        )

        if uploaded_file:
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            if st.button("Process Video"):
                _process_video(temp_path)

    else:
        youtube_url = st.text_input("Enter YouTube URL")

        if youtube_url and st.button("Process YouTube Video"):
            yt_loader = YouTubeLoader()
            video_info = yt_loader.load(youtube_url)
            _process_video(video_info["video_path"], video_info["media_id"])


def _process_video(video_path: str, media_id: str | None = None):
    st.info("Processing video...")

    if not media_id:
        media_id = str(uuid4())

    audio_extractor = AudioExtractor()
    frame_sampler = FrameSampler()

    # -----------------------------
    # Audio extraction
    # -----------------------------
    audio_path = audio_extractor.extract(video_path, media_id)

    # -----------------------------
    # Frame sampling (NEW)
    # -----------------------------
    frame_paths, cleanup_frames = frame_sampler.sample(video_path)

    # -----------------------------
    # Store in session state
    # -----------------------------
    st.session_state.media_id = media_id
    st.session_state.video_path = video_path
    st.session_state.audio_path = audio_path
    st.session_state.frame_paths = frame_paths
    st.session_state.cleanup_frames = cleanup_frames
    st.session_state.chat_session_id = str(uuid4())

    st.success("✅ Media processed successfully!")
    st.info("Go to Media Dashboard →")
