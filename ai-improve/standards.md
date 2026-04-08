# Standards

## Code Quality
- Modular, readable, maintainable
- Clear function structure with type hints
- No unnecessary complexity
- Constants defined at module level, not as magic numbers/strings
- Descriptive variable and function names

## Error Handling
- All API calls wrapped in try/except
- Graceful degradation with user-friendly error messages
- No silent failures

## Performance
- Use Streamlit's `@st.cache_data` for API responses
- Avoid redundant API calls
- Efficient data handling

## UI/UX
- Clean, modern, consistent design
- Good spacing and layout
- Loading spinners for async operations
- Responsive column layout
- Safe rendering (handle None values)

## Testing
- Core functionality covered with unit tests
- Mock external API calls in tests
- Edge cases handled (empty results, API errors, None fields)

## General
- Production-ready quality
- Clear inline documentation
- requirements.txt kept up to date
- .env.example provided for onboarding
