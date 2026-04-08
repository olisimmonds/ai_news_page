# Tasks

## Phase: Analyse
- [x] Read and understand all source files
- [x] Document issues and improvement opportunities (see progress.md)

## Phase: Plan
- [x] Prioritise tasks by impact
- [x] Break refactor into small, safe steps

## Phase: Refactor
- [x] Add `requirements.txt`
- [x] Add `.env.example`
- [x] Add `@st.cache_data` to `fetch_news` to avoid redundant API calls
- [x] Wrap API call in try/except for network error handling
- [x] Fix fragile date formatting (use `datetime.fromisoformat` instead of `[:10]` slice)
- [x] Guard against None values in `article["description"]` and `article["title"]`
- [x] Extract magic numbers to named constants (`MAX_ARTICLES`, `DAYS_BACK`)
- [x] Add type hints to all functions
- [x] Add `__pycache__` and `*.pyc` to `.gitignore`
- [x] Add loading spinner in `app.py`
- [x] Simplify category dispatch using a dict in `app.py`
- [ ] Split `news_fetcher.py` into `fetcher.py` and `ui.py` (deferred — low priority for current size)

## Phase: UI
- [x] Improve article card styling — wrapped each article in `st.container(border=True)`
- [x] Handle missing images with a placeholder — `_PLACEHOLDER_HTML` gradient div shown when `urlToImage` is absent
- [x] Add article count indicator (done — via `st.caption`)
- [x] Set page icon (📰) and better page title ("AI News") in `set_page_config`
- [x] Inject CSS to cap content width at 1400 px on wide screens

## Phase: Test
- [x] Add `tests/` directory
- [x] Unit test `fetch_news` with mocked requests
- [x] Unit test `_format_date` edge cases
- [x] Unit test None-field handling in `display_article`

## Phase: Polish
- [x] Update README with setup instructions
- [x] Final code review pass
