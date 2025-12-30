import streamlit as st


def render_insights_page():
    st.header("🧠 Insights")

    context = st.session_state.get("agent_context")
    if not context:
        st.warning("Run AI analysis first.")
        return

    reasoning = context.get("reasoning")
    emotion = context.get("emotion")
    risk = context.get("risk")

    if reasoning and reasoning.success:
        st.subheader("📌 Key Insights")
        if reasoning.insights:
            for insight in reasoning.insights:
                st.markdown(f"- {insight.insight}")
        else:
            st.markdown("_No insights generated._")

        st.subheader("🧠 Summary / Intent")
        if reasoning.summary:
            st.markdown(reasoning.summary)
        else:
            st.markdown("_No summary available._")

        st.subheader("🧭 Key Themes")
        if reasoning.key_themes:
            st.markdown(", ".join(reasoning.key_themes))
        else:
            st.markdown("_No key themes detected._")

        st.subheader("📋 Conclusions / Decisions")
        if reasoning.decisions:
            for d in reasoning.decisions:
                st.markdown(f"- {d}")
        else:
            st.markdown("_No decisions inferred._")

    if emotion:
        st.subheader("🎭 Emotion Analysis")
        st.write(f"**Dominant Emotion:** {emotion.dominant_emotion}")

        for spike in emotion.emotion_spikes:
            st.markdown(
                f"- {spike.emotion} at {spike.timestamp}s (intensity {spike.intensity})"
            )

    if risk and risk.success:
        st.subheader("⚠️ Risk Assessment")

        if risk.overall_risk_level:
            st.write(f"**Overall Risk Level:** {risk.overall_risk_level}")

        if risk.risk_flags:
            for flag in risk.risk_flags:
                st.markdown(f"**Category:** {flag.category}")
                st.markdown(f"- Severity: {flag.severity}")
                st.markdown(f"- Description: {flag.description}")
                st.markdown("---")
        else:
            st.markdown("_No significant risks detected._")
