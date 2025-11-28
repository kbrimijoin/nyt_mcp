# Tests for NYT MCP Server

This directory contains tests for the NYT MCP server, specifically for the `article_search` tool.

## Setup

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Or with uv:

```bash
uv pip install -e ".[dev]"
```

Set up your environment variables in `.env`:

```bash
NYT_API_KEY=your_api_key_here
NYT_API_BASE_URL=https://api.nytimes.com/svc/search/v2
```

## Running Tests

### Unit Tests (with mocks)

Run all unit tests (excludes integration tests):

```bash
pytest -m "not integration"
```

Run with verbose output:

```bash
pytest -v -m "not integration"
```

Run specific test file:

```bash
pytest tests/test_article_search.py
```

Run specific test:

```bash
pytest tests/test_article_search.py::TestArticleSearch::test_article_search_success
```

### Integration Tests (real API calls)

**Note:** Integration tests require a valid NYT API key set in your environment.

Run only integration tests:

```bash
pytest -m integration
```

Run integration tests with verbose output:

```bash
pytest -v -m integration
```

Run all tests including integration:

```bash
pytest
```

## Test Coverage

### Unit Tests (test_article_search.py)

Tests with mocked API calls:

1. **Successful article search** - Tests the happy path with valid query
2. **Empty query handling** - Tests behavior with empty search string
3. **Special characters** - Tests handling of special characters in queries
4. **API failure handling** - Tests when the NYT API returns errors
5. **Missing environment variables** - Tests error handling for missing config
6. **HTTP request success** - Tests the underlying HTTP request helper
7. **HTTP errors** - Tests handling of HTTP errors (4xx, 5xx)
8. **Timeouts** - Tests handling of request timeouts
9. **Correct headers** - Verifies proper headers are sent
10. **Timeout configuration** - Verifies timeout parameter is set correctly

### Integration Tests (test_article_search_integration.py)

Tests with real API calls:

1. **Real API call with simple query** - Tests actual API call with "technology"
2. **Specific topic search** - Tests searching for "climate change"
3. **Direct NYT API request** - Tests the make_nyt_request helper with real API
4. **Multiple keywords** - Tests searching with multiple keywords
5. **Quoted phrases** - Tests searching with quoted search terms
6. **Invalid API key handling** - Tests behavior with invalid credentials

**Note:** Integration tests are automatically skipped if `NYT_API_KEY` is not set in the environment.
