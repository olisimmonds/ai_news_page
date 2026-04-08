import streamlit as st
from src.news_fetcher import fetch_news, display_news

st.set_page_config(page_title="AI News", page_icon="📰", layout="wide")

# Constrain content width on very large screens for readability.
st.markdown(
    "<style>.block-container{max-width:1400px;padding-top:1.5rem;}</style>",
    unsafe_allow_html=True,
)

CATEGORIES: dict[str, str] = {
    "AI News": "artificial intelligence",
    "Finance News": "finance",
    "Political News": "politics",
}

page = st.sidebar.radio("Category", list(CATEGORIES.keys()))

query = CATEGORIES[page]

with st.spinner("Fetching latest news..."):
    articles = fetch_news(query)

display_news(articles, page)
