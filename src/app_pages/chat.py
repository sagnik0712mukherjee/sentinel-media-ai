import streamlit as st

from src.agents.rag_chat_agent import RAGChatAgent
from src.rag.retriever import Retriever


def render_chat_page():
    st.header("💬 Chat with Your Media")

    if "agent_context" not in st.session_state:
        st.warning("Run AI analysis first.")
        return

    user_query = st.text_input("Ask a question")

    if user_query:
        retriever = Retriever()

        transcript = st.session_state.agent_context["audio"].full_transcript
        retrieved_context = retriever.retrieve(
                                media_id=st.session_state.media_id,
                                transcript_text=transcript,
                                query=user_query,
                            )


        agent = RAGChatAgent(
            media_id=st.session_state.media_id,
            session_id=st.session_state.chat_session_id,
            retrieved_context=retrieved_context,
            user_question=user_query,
        )

        response = agent.run()

        st.markdown("### 🤖 Answer")
        st.write(response.answer)
