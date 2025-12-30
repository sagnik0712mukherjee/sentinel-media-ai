import streamlit as st

from src.app_pages.upload import render_upload_page
from src.app_pages.media_dashboard import render_media_dashboard
from src.app_pages.insights import render_insights_page
from src.app_pages.chat import render_chat_page


# ---------------------------------------------------------
# Page Config (DO THIS FIRST)
# ---------------------------------------------------------

st.set_page_config(
    page_title="Sentinel Media AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Global Styling (subtle, clean)
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }
        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    """
    # 🎬 Sentinel Media AI
    **AI that watches, listens, thinks, and decides**
    ---
    """
)


# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("## 🧭 Navigation")

    page = st.radio(
        label="",
        options=[
            "📤 Upload Media",
            "📊 Media Dashboard",
            "🧠 Insights",
            "💬 Chat",
        ],
    )

    st.markdown("---")

    st.markdown(
        """
        ### ℹ️ About
        Sentinel Media AI is an **agentic, multimodal AI system**
        that analyzes video & audio using multiple collaborating agents.
        """
    )

    st.markdown("---")

    st.markdown(
        """
        **Built with ❤️ using:**
        - Agentic AI
        - RAG
        - Streamlit
        - OpenAI
        - Elasticsearch
        """
    )


# ---------------------------------------------------------
# Page Routing
# ---------------------------------------------------------

if page == "📤 Upload Media":
    render_upload_page()

elif page == "📊 Media Dashboard":
    render_media_dashboard()

elif page == "🧠 Insights":
    render_insights_page()

elif page == "💬 Chat":
    render_chat_page()


# ---------------------------------------------------------
# Footer (soft branding)
# ---------------------------------------------------------

st.markdown(
    """
    ---
    <div style="text-align:center; color:gray;">
        Sentinel Media AI • Agentic Multimodal Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True,
)
