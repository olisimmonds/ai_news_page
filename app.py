import streamlit as st
from src.news_fetcher import fetch_news, display_news

# Streamlit page configuration
st.set_page_config(page_title="News App", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Category", ["AI News", "Finance News", "Political News"])

# Fetch and display articles based on selected category
if page == "AI News":
    articles = fetch_news("artificial intelligence")
    display_news(articles, "AI News")

elif page == "Finance News":
    articles = fetch_news("finance")
    display_news(articles, "Finance News")

elif page == "Political News":
    articles = fetch_news("politics")
    display_news(articles, "Political News")