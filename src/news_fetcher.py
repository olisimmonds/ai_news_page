import requests
import datetime
import os
import streamlit as st
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Now you can access your API key
API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

# Fetch news based on query
def fetch_news(query):
    last_week = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat() + "Z"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevance",
        "from": last_week,
        "apiKey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        articles=response.json().get("articles", [])
        articles.sort(key=lambda x: x["publishedAt"], reverse=True)
        return articles
    else:
        return []
    
def display_article(article):
    if article.get("urlToImage"):
        st.image(article["urlToImage"], use_container_width=True)

    st.markdown(f"### {article['title']}")
    st.write(f"**Source:** {article['source']['name']}")
    st.write(f"📅 {article['publishedAt'][:10]}")
    st.write(article["description"])  # Short description
    st.markdown(f"[🔗 Read More]({article['url']})", unsafe_allow_html=True)
    st.divider()  # Add a horizontal line for separation

def display_news(articles, title):
    st.title(title)
    if articles:
        cols = st.columns(3)
        for index, article in enumerate(articles[:15]):  # Show only top 15 articles
            with cols[index % 3]:
                display_article(article)
    else:
        st.write("No news articles found.")