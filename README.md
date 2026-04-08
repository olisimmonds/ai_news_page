# AI News

Using the free [NewsAPI](https://newsapi.org) API, this Streamlit application aggregates news stories from reputable sources and displays them in a clean, card-based layout. It covers AI, finance, and politics and refreshes results every 10 minutes to avoid hitting API rate limits.

![screenshot](https://github.com/user-attachments/assets/7089af43-4f3a-4768-923e-8b714939e04f)

## Setup

1. **Clone the repo** and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the project root (copy from the provided example):
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and replace the placeholder with your NewsAPI key:
   ```
   NEWSAPI_KEY=your_key_here
   ```
   Get a free key at [newsapi.org](https://newsapi.org/register).

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Running Tests

The test suite uses Python's built-in `unittest` framework — no extra dependencies required:

```bash
python -m unittest discover -s tests -v
```

## Project Structure

```
.
├── app.py               # Streamlit entry point and sidebar navigation
├── src/
│   └── news_fetcher.py  # API fetch, caching, date formatting, and card rendering
├── tests/
│   └── test_news_fetcher.py  # Unit tests (20 tests)
├── requirements.txt
└── .env.example
```
