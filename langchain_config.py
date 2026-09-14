import os
import streamlit as st
from newsapi import NewsApiClient
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

def fetch_and_summarize(query, from_date=None, language='en'):
    """
    Fetches news articles via NewsAPI and summarizes them using Groq LLM.
    Returns:
        tuple: (summary_text, list_of_image_dictionaries)
    """
    # 1. Safely retrieve API keys (checks environment variables first, then Streamlit secrets)
    groq_key = os.getenv("GROQ_API_KEY") or (st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets else None)
    news_key = os.getenv("NEWS_API_KEY") or (st.secrets.get("NEWS_API_KEY") if hasattr(st, "secrets") and "NEWS_API_KEY" in st.secrets else None)

    if not news_key or not groq_key:
        raise ValueError("API Keys are missing! Ensure environment variables or Streamlit secrets are set.")

    # 2. Initialize NewsAPI client
    newsapi = NewsApiClient(api_key=news_key)
    
    # 3. Query articles from NewsAPI
    response = newsapi.get_everything(
        q=query,
        from_param=from_date,
        language=language,
        sort_by='relevancy',
        page_size=10
    )

    articles = response.get('articles', [])
    if not articles:
        return "No relevant news articles found for the specified query.", []

    compiled_texts = []
    images = []

    # 4. Process top 5 relevant articles
    for idx, art in enumerate(articles[:5]):
        title = art.get('title', 'No Title')
        desc = art.get('description', '') or ''
        url = art.get('url', '#')
        img_url = art.get('urlToImage')

        compiled_texts.append(f"Article {idx+1}: {title} - {desc}")
        
        # Collect valid image metadata for visual UI
        if img_url:
            images.append({"title": title, "url": img_url, "link": url})

    context = "\n".join(compiled_texts)

    # 5. Initialize Groq LLM model via LangChain integration
    llm = ChatGroq(
        temperature=0.3,
        model_name="llama-3.1-8b-instant",
        groq_api_key=groq_key
    )

    # 6. Define prompt structure for equity analyst summary
    prompt = PromptTemplate(
        input_variables=["query", "context"],
        template="""
        You are an expert equity research analyst. Given the search query and the news article excerpts, 
        provide a clear, executive-level summary highlighting market impact, geopolitical issues, and major takeaways.

        Query: {query}
        Article Excerpts:
        {context}
        """
    )

    # 7. Execute chain (Prompt -> Groq LLM)
    chain = prompt | llm
    result = chain.invoke({"query": query, "context": context})

    return result.content, images
