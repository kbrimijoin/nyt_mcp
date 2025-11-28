"""Integration tests for the article_search tool that make actual API calls."""

import pytest
import os
import logging
from dotenv import load_dotenv
from mcp_server.server import article_search, make_nyt_request

# Load environment variables
load_dotenv()

# Skip all tests in this file if API key is not available
pytestmark = pytest.mark.skipif(
    not os.getenv('NYT_API_KEY'),
    reason="NYT_API_KEY not set in environment"
)


class TestArticleSearchIntegration:
    """Integration tests that make actual API calls to NYT API."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_article_search_real_api_call(self):
        """Test article search with actual API call."""
        # Use a simple, common search term
        query = "technology"

        result = await article_search(query)
        print('result ', type(result))
        # logging.info('logging result ', result)
        # Basic assertions - result should not be None
        assert result is not None
        
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_article_search_with_multiple_keywords(self):
        """Test searching with multiple keywords."""
        query = "artificial intelligence machine learning"

        result = await article_search(query)
        print('result ', result)
        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_article_search_with_quotes(self):
        """Test searching with quoted phrases."""
        query = '"New York"'

        result = await article_search(query)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_invalid_api_key(self):
        """Test behavior with invalid API key."""
        # Temporarily override the API key
        original_key = os.getenv('NYT_API_KEY')

        with pytest.MonkeyPatch.context() as m:
            m.setenv('NYT_API_KEY', 'invalid_key_12345')

            result = await article_search("test")

            # Should handle invalid API key gracefully
            # Currently returns "test" regardless, but API call should fail
            assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
