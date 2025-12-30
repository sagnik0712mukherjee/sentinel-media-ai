import streamlit as st

from src.orchestration.workflow_runner import WorkflowRunner


def render_media_dashboard():
    st.header("📊 Media Dashboard")

    if "media_id" not in st.session_state:
        st.warning("No media uploaded yet.")
        return

    st.write(f"**Media ID:** {st.session_state.media_id}")

    if st.button("🧠 Run AI Analysis"):
        with st.spinner("Running agentic pipeline..."):
            runner = WorkflowRunner(media_id=st.session_state.media_id)

            context = runner.run(
                audio_path=st.session_state.audio_path,
                frame_paths=st.session_state.frame_paths,
            )

            st.session_state.agent_context = context

        st.success("✅ AI analysis completed!")

    if "agent_context" in st.session_state:
        st.subheader("Agent Outputs Available")
        for key in st.session_state.agent_context.keys():
            st.markdown(f"- **{key.capitalize()} Agent**")
