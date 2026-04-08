import datetime
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv("NEWSAPI_KEY", "")
BASE_URL: str = "https://newsapi.org/v2/everything"
MAX_ARTICLES: int = 15
DAYS_BACK: int = 7

# Inline HTML placeholder rendered when an article has no image.
_PLACEHOLDER_HTML: str = (
    '<div style="'
    "width:100%;height:160px;"
    "background:linear-gradient(135deg,#e8eaf6 0%,#c5cae9 100%);"
    "border-radius:4px;display:flex;align-items:center;"
    "justify-content:center;font-size:2.5rem;"
    'margin-bottom:0.5rem;">📰</div>'
)


@st.cache_data(ttl=600)
def fetch_news(query: str) -> list[dict]:
    """Fetch news articles from NewsAPI for the given query.

    Results are cached for 10 minutes to avoid hitting API rate limits.
    Returns an empty list on any error.
    """
    if not API_KEY:
        st.error("NEWSAPI_KEY is not set. Please add it to your .env file.")
        return []

    from_date = (
        datetime.datetime.now() - datetime.timedelta(days=DAYS_BACK)
    ).isoformat() + "Z"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevance",
        "from": from_date,
        "apiKey": API_KEY,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        articles: list[dict] = response.json().get("articles", [])
        articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
        return articles
    except requests.exceptions.RequestException as exc:
        st.error(f"Failed to fetch news: {exc}")
        return []


def _format_date(raw: str) -> str:
    """Parse an ISO 8601 date string and return a human-readable date."""
    try:
        dt = datetime.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.strftime("%-d %b %Y")
    except (ValueError, AttributeError):
        return raw[:10] if raw else "Unknown date"


def display_article(article: dict) -> None:
    """Render a single news article card with a bordered container."""
    image_url: str | None = article.get("urlToImage")
    title: str = article.get("title") or "No title"
    description: str = article.get("description") or "No description available."
    source: str = article.get("source", {}).get("name", "Unknown source")
    published: str = _format_date(article.get("publishedAt", ""))
    url: str = article.get("url", "#")

    with st.container(border=True):
        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.markdown(_PLACEHOLDER_HTML, unsafe_allow_html=True)
        st.markdown(f"**{title}**")
        st.caption(f"{source} · {published}")
        st.write(description)
        st.markdown(f"[Read more →]({url})")


def display_news(articles: list[dict], title: str) -> None:
    """Render a grid of news articles under the given heading."""
    st.title(title)

    if not articles:
        st.info("No news articles found.")
        return

    shown = articles[:MAX_ARTICLES]
    st.caption(f"Showing {len(shown)} articles")

    cols = st.columns(3)
    for index, article in enumerate(shown):
        with cols[index % 3]:
            display_article(article)
