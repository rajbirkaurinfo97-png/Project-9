import streamlit as st
import os
import io
from dotenv import load_dotenv
from gtts import gTTS
from langchain_config import fetch_and_summarize

# Load environment variables if running locally or in Colab
load_dotenv()

# Page configuration
st.set_page_config(page_title="Equity Research News Tool", layout="wide", page_icon="📈")

# Main Title & Subtitle
st.title("📈 Equity Research & News Summarization Dashboard")
st.markdown("Powered by **LangChain**, **Groq LLM**, and **NewsAPI**.")

# ------------------------------------------------------------------------------
# SIDEBAR CONTROLS (Inputs, Dates, Languages)
# ------------------------------------------------------------------------------
st.sidebar.header("🔍 Search & Filter Controls")

# Input Query
query = st.sidebar.text_input("Research Topic / Query", value="Russia Ukraine war impact on market")

# Date Filter (Default set to broad search)
from_date = st.sidebar.date_input("From Date", value=None, help="Select starting date for news search")

# Language Selection
language = st.sidebar.selectbox("Language", options=["en", "es", "fr", "de"], index=0, help="Select language of news articles")

# Submit Button
fetch_button = st.sidebar.button("Fetch & Summarize", type="primary")

# ------------------------------------------------------------------------------
# MAIN CONTENT AREA
# ------------------------------------------------------------------------------
if fetch_button:
    if not query.strip():
        st.error("Please enter a valid research topic.")
    else:
        with st.spinner("Fetching news articles and generating summary with Groq..."):
            try:
                # Format date parameter
                date_str = from_date.strftime('%Y-%m-%d') if from_date else None
                
                # Fetch summary and image metadata from backend
                summary, images = fetch_and_summarize(query, from_date=date_str, language=language)

                # 1. Executive Summary Output
                st.subheader("💡 Executive Summary")
                st.write(summary)

                # 2. Audio Overview Feature (Google TTS)
                st.subheader("🔊 Audio Overview")
                tts = gTTS(text=summary[:500], lang=language)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp.getvalue(), format="audio/mp3")

                # 3. Export Summary Option
                st.subheader("📥 Export Summary")
                st.download_button(
                    label="Download Summary (.txt)",
                    data=summary,
                    file_name=f"{query.replace(' ', '_')}_summary.txt",
                    mime="text/plain"
                )

                # 4. Related Images & Visuals Section
                if images:
                    st.subheader("🖼️ Related News Visuals")
                    cols = st.columns(min(len(images), 3))
                    for idx, img in enumerate(images[:3]):
                        with cols[idx]:
                            st.image(img['url'], caption=img['title'], use_container_width=True)
                            st.markdown(f"[Read Full Article]({img['link']})")

            except Exception as e:
                st.error(f"An error occurred while running the research pipeline: {e}")
