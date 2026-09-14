# 📈 Equity Research & News Summarization Dashboard

An interactive, AI-powered financial intelligence tool built with Streamlit, LangChain, Groq LLM, and NewsAPI. This application fetches real-time market news, synthesizes key market takeaways into structured executive summaries, generates audio overviews, and allows exporting reports.

---

## 🚀 Live Demo

- **Streamlit Web Application:** [Live Dashboard](https://project-9-frq3nh5nskwhdeieqxg9sa.streamlit.app/)

---

## ✨ Features

- 🔍 **Real-Time News Fetching:** Dynamic query, language, and date range filtering powered by NewsAPI.
- 🤖 **LLM-Powered Analysis:** LangChain integration with Groq to categorize market findings into structured themes, key insights, market impacts, and geopolitical angles.
- 🎧 **Audio Overview:** Automated Text-to-Speech generation (`gTTS`) providing an audio briefing of the summary.
- 📥 **Export Capability:** One-click download of the generated summary report as a `.txt` file.
- 🖼️ **Visual News Feed:** Grid layout rendering article images and direct link cards for full-text reading.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** Streamlit
- **LLM Orchestration:** LangChain
- **LLM Provider:** Groq API (`openai/gpt-oss-20b`)
- **Data Source:** NewsAPI
- **Audio Processing:** gTTS (Google Text-to-Speech)
- **Environment & Deployment:** Streamlit Community Cloud & GitHub

---

## 🔐 Configuration & Secrets Management

To run locally or on Streamlit Cloud, secure your secrets in `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key"
NEWS_API_KEY = "your_news_api_key"
