"""Unit tests for src/news_fetcher.py.

Covers:
- _format_date: ISO 8601 parsing, edge cases, None/empty input.
- fetch_news: successful fetch, missing API key, network errors, HTTP errors.
- display_article: None-field fallbacks, missing image placeholder, image rendering.

Uses only the standard library (unittest + unittest.mock) so no extra
dependencies are needed beyond what is already in requirements.txt.
Streamlit is replaced with a MagicMock before the module under test is
imported, so no running Streamlit server is required.
"""
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests

# ---------------------------------------------------------------------------
# Streamlit mock — must be injected before src.news_fetcher is imported.
# ---------------------------------------------------------------------------

_ST_MOCK: MagicMock = MagicMock(name="streamlit")
_ST_MOCK.cache_data = lambda **kwargs: (lambda func: func)
sys.modules["streamlit"] = _ST_MOCK

# Remove any previously cached import of the module so the mock takes effect.
for _key in list(sys.modules):
    if _key.startswith("src"):
        del sys.modules[_key]

import src.news_fetcher as _nf  # noqa: E402 — must come after mock injection


def _reset_st() -> None:
    """Reset the shared streamlit mock and restore cache_data."""
    _ST_MOCK.reset_mock()
    _ST_MOCK.cache_data = lambda **kwargs: (lambda func: func)


# ---------------------------------------------------------------------------
# _format_date
# ---------------------------------------------------------------------------


class TestFormatDate(unittest.TestCase):
    """Tests for the _format_date private helper."""

    def setUp(self) -> None:
        _reset_st()

    def test_valid_iso_date_with_z_suffix(self) -> None:
        from src.news_fetcher import _format_date

        self.assertEqual(_format_date("2026-04-03T12:00:00Z"), "3 Apr 2026")

    def test_valid_iso_date_with_utc_offset(self) -> None:
        from src.news_fetcher import _format_date

        self.assertEqual(_format_date("2026-04-03T12:00:00+00:00"), "3 Apr 2026")

    def test_single_digit_day_has_no_leading_zero(self) -> None:
        from src.news_fetcher import _format_date

        result = _format_date("2026-01-05T00:00:00Z")
        self.assertEqual(result, "5 Jan 2026")
        self.assertFalse(result.startswith("0"), "Day should not have a leading zero")

    def test_double_digit_day(self) -> None:
        from src.news_fetcher import _format_date

        self.assertEqual(_format_date("2026-12-25T00:00:00Z"), "25 Dec 2026")

    def test_empty_string_returns_unknown_date(self) -> None:
        from src.news_fetcher import _format_date

        self.assertEqual(_format_date(""), "Unknown date")

    def test_none_returns_unknown_date(self) -> None:
        from src.news_fetcher import _format_date

        self.assertEqual(_format_date(None), "Unknown date")

    def test_invalid_string_falls_back_to_first_ten_chars(self) -> None:
        from src.news_fetcher import _format_date

        self.assertEqual(_format_date("2026-04-03 not parseable"), "2026-04-03")

    def test_short_garbage_string_returned_as_is(self) -> None:
        from src.news_fetcher import _format_date

        # Fewer than 10 chars: raw[:10] is just the full raw value.
        self.assertEqual(_format_date("bad"), "bad")


# ---------------------------------------------------------------------------
# fetch_news
# ---------------------------------------------------------------------------


class TestFetchNews(unittest.TestCase):
    """Tests for fetch_news, with requests.get mocked out."""

    def setUp(self) -> None:
        _reset_st()
        # Store the real API_KEY so we can restore it in tearDown.
        self._original_api_key = _nf.API_KEY

    def tearDown(self) -> None:
        _nf.API_KEY = self._original_api_key

    @staticmethod
    def _mock_response(articles: list, raise_http_error: bool = False) -> MagicMock:
        resp = MagicMock()
        resp.json.return_value = {"articles": articles}
        if raise_http_error:
            resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        else:
            resp.raise_for_status.return_value = None
        return resp

    def test_missing_api_key_returns_empty_list(self) -> None:
        _nf.API_KEY = ""
        self.assertEqual(_nf.fetch_news("ai"), [])

    def test_successful_fetch_returns_articles_sorted_descending(self) -> None:
        _nf.API_KEY = "test-key-123"
        articles = [
            {"title": "Older", "publishedAt": "2026-04-01T08:00:00Z"},
            {"title": "Newer", "publishedAt": "2026-04-03T12:00:00Z"},
        ]
        with patch("src.news_fetcher.requests.get", return_value=self._mock_response(articles)):
            result = _nf.fetch_news("artificial intelligence")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Newer")
        self.assertEqual(result[1]["title"], "Older")

    def test_network_exception_returns_empty_list(self) -> None:
        _nf.API_KEY = "test-key-123"
        with patch(
            "src.news_fetcher.requests.get",
            side_effect=requests.exceptions.ConnectionError("timeout"),
        ):
            self.assertEqual(_nf.fetch_news("ai"), [])

    def test_http_error_returns_empty_list(self) -> None:
        _nf.API_KEY = "test-key-123"
        with patch(
            "src.news_fetcher.requests.get",
            return_value=self._mock_response([], raise_http_error=True),
        ):
            self.assertEqual(_nf.fetch_news("ai"), [])

    def test_request_passes_query_and_api_key(self) -> None:
        _nf.API_KEY = "my-secret-key"
        mock_get = MagicMock(return_value=self._mock_response([]))
        with patch("src.news_fetcher.requests.get", mock_get):
            _nf.fetch_news("finance")

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"]["apiKey"], "my-secret-key")
        self.assertEqual(kwargs["params"]["q"], "finance")

    def test_empty_response_returns_empty_list(self) -> None:
        _nf.API_KEY = "test-key-123"
        with patch(
            "src.news_fetcher.requests.get",
            return_value=self._mock_response([]),
        ):
            self.assertEqual(_nf.fetch_news("obscure topic"), [])


# ---------------------------------------------------------------------------
# display_article
# ---------------------------------------------------------------------------


class TestDisplayArticle(unittest.TestCase):
    """Tests for None-field handling and rendering in display_article."""

    def setUp(self) -> None:
        _reset_st()

    @staticmethod
    def _article(**overrides) -> dict:
        """Return a fully populated article dict with optional field overrides."""
        base: dict = {
            "title": "Test Headline",
            "description": "A short description.",
            "source": {"name": "Test Source"},
            "publishedAt": "2026-04-03T12:00:00Z",
            "url": "https://example.com/article",
            "urlToImage": "https://example.com/image.jpg",
        }
        base.update(overrides)
        return base

    def test_none_title_renders_fallback(self) -> None:
        from src.news_fetcher import display_article

        display_article(self._article(title=None))

        markdown_texts = [str(c) for c in _ST_MOCK.markdown.call_args_list]
        self.assertTrue(
            any("No title" in t for t in markdown_texts),
            "Expected 'No title' fallback in markdown calls",
        )

    def test_none_description_renders_fallback(self) -> None:
        from src.news_fetcher import display_article

        display_article(self._article(description=None))

        write_texts = [str(c) for c in _ST_MOCK.write.call_args_list]
        self.assertTrue(
            any("No description available." in t for t in write_texts),
            "Expected 'No description available.' fallback in write calls",
        )

    def test_missing_image_shows_placeholder_html(self) -> None:
        from src.news_fetcher import display_article

        display_article(self._article(urlToImage=None))

        _ST_MOCK.image.assert_not_called()

        markdown_calls = [str(c) for c in _ST_MOCK.markdown.call_args_list]
        self.assertTrue(
            any("\U0001f4f0" in c for c in markdown_calls),  # 📰
            "Expected placeholder HTML (📰 emoji) in markdown calls",
        )

    def test_present_image_url_calls_st_image(self) -> None:
        from src.news_fetcher import display_article

        display_article(self._article(urlToImage="https://example.com/img.jpg"))

        _ST_MOCK.image.assert_called_once_with(
            "https://example.com/img.jpg", use_container_width=True
        )

    def test_missing_source_shows_unknown_source(self) -> None:
        from src.news_fetcher import display_article

        display_article(self._article(source={}))

        caption_texts = [str(c) for c in _ST_MOCK.caption.call_args_list]
        self.assertTrue(
            any("Unknown source" in t for t in caption_texts),
            "Expected 'Unknown source' in caption calls",
        )

    def test_read_more_link_contains_article_url(self) -> None:
        from src.news_fetcher import display_article

        display_article(self._article(url="https://bbc.co.uk/story"))

        markdown_calls = [str(c) for c in _ST_MOCK.markdown.call_args_list]
        self.assertTrue(
            any("https://bbc.co.uk/story" in c for c in markdown_calls),
            "Expected article URL in a markdown call",
        )


if __name__ == "__main__":
    unittest.main()
