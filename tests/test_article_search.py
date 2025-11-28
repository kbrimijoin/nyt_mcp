"""Tests for the article_search tool."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import os
from mcp_server.server import article_search, make_nyt_request


class TestArticleSearch:
    """Test suite for article_search functionality."""

    @pytest.mark.asyncio
    async def test_article_search_success(self):
        """Test successful article search with valid query."""
        # Mock environment variables
        with patch.dict(os.environ, {
            'NYT_API_BASE_URL': 'https://api.nytimes.com/svc/search/v2',
            'NYT_API_KEY': 'test_api_key'
        }):
            # Mock the HTTP request
            mock_response = {
                "status": "OK",
                "response": {
                    "docs": [
                        {
                            "abstract": "Test article abstract",
                            "headline": {"main": "Test Headline"},
                            "web_url": "https://www.nytimes.com/test-article"
                        }
                    ]
                }
            }

            with patch('mcp_server.server.make_nyt_request', new_callable=AsyncMock) as mock_request:
                mock_request.return_value = mock_response

                result = await article_search("climate change")

                # Verify the request was made with correct URL
                mock_request.assert_called_once()
                call_args = mock_request.call_args[0][0]
                assert "articlesearch.json" in call_args
                assert "q=climate change" in call_args
                assert "api-key=test_api_key" in call_args

                # Verify result
                assert result is not None

    @pytest.mark.asyncio
    async def test_article_search_empty_query(self):
        """Test article search with empty query string."""
        with patch.dict(os.environ, {
            'NYT_API_BASE_URL': 'https://api.nytimes.com/svc/search/v2',
            'NYT_API_KEY': 'test_api_key'
        }):
            with patch('mcp_server.server.make_nyt_request', new_callable=AsyncMock) as mock_request:
                mock_request.return_value = {"response": {"docs": []}}

                result = await article_search("")

                # Should still make request even with empty query
                mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_article_search_special_characters(self):
        """Test article search with special characters in query."""
        with patch.dict(os.environ, {
            'NYT_API_BASE_URL': 'https://api.nytimes.com/svc/search/v2',
            'NYT_API_KEY': 'test_api_key'
        }):
            with patch('mcp_server.server.make_nyt_request', new_callable=AsyncMock) as mock_request:
                mock_request.return_value = {"response": {"docs": []}}

                query_with_special_chars = "test & query"
                result = await article_search(query_with_special_chars)

                # Verify the query was passed through
                mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_article_search_api_failure(self):
        """Test article search when API returns None (failure)."""
        with patch.dict(os.environ, {
            'NYT_API_BASE_URL': 'https://api.nytimes.com/svc/search/v2',
            'NYT_API_KEY': 'test_api_key'
        }):
            with patch('mcp_server.server.make_nyt_request', new_callable=AsyncMock) as mock_request:
                mock_request.return_value = None

                result = await article_search("test query")

                # Should handle None response gracefully
                assert result is not None

    @pytest.mark.asyncio
    async def test_article_search_missing_env_vars(self):
        """Test article search when environment variables are missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises((KeyError, TypeError)):
                await article_search("test query")


class TestMakeNYTRequest:
    """Test suite for make_nyt_request helper function."""

    @pytest.mark.asyncio
    async def test_make_nyt_request_success(self):
        """Test successful HTTP request."""
        test_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        mock_response_data = {"status": "OK", "response": {"docs": []}}

        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock()
            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            mock_client.return_value.__aenter__.return_value.get = mock_get

            result = await make_nyt_request(test_url)

            assert result == mock_response_data
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_make_nyt_request_http_error(self):
        """Test HTTP request with error response."""
        test_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock()
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("HTTP Error")
            mock_get.return_value = mock_response

            mock_client.return_value.__aenter__.return_value.get = mock_get

            result = await make_nyt_request(test_url)

            assert result is None

    @pytest.mark.asyncio
    async def test_make_nyt_request_timeout(self):
        """Test HTTP request timeout."""
        test_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock(side_effect=Exception("Timeout"))
            mock_client.return_value.__aenter__.return_value.get = mock_get

            result = await make_nyt_request(test_url)

            assert result is None

    @pytest.mark.asyncio
    async def test_make_nyt_request_correct_headers(self):
        """Test that correct headers are sent with the request."""
        test_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock()
            mock_response = MagicMock()
            mock_response.json.return_value = {}
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            mock_client.return_value.__aenter__.return_value.get = mock_get

            await make_nyt_request(test_url)

            # Verify headers were passed
            call_kwargs = mock_get.call_args[1]
            assert 'headers' in call_kwargs
            assert call_kwargs['headers']['User-Agent'] == "weather-app/1.0"
            assert call_kwargs['headers']['Accept'] == "application/geo+json"

    @pytest.mark.asyncio
    async def test_make_nyt_request_timeout_parameter(self):
        """Test that timeout parameter is set correctly."""
        test_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

        with patch('httpx.AsyncClient') as mock_client:
            mock_get = AsyncMock()
            mock_response = MagicMock()
            mock_response.json.return_value = {}
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            mock_client.return_value.__aenter__.return_value.get = mock_get

            await make_nyt_request(test_url)

            # Verify timeout was set
            call_kwargs = mock_get.call_args[1]
            assert call_kwargs['timeout'] == 30.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
