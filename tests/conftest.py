"""Pytest configuration for the ai_news_page test suite.

When running under pytest, this file is picked up automatically. The
streamlit mock is already injected at module level in test_news_fetcher.py
so that it works with both pytest and plain ``python -m unittest``. This
conftest provides no additional fixtures; it exists as a hook for future
pytest-specific configuration (e.g. markers, plugins).
"""
