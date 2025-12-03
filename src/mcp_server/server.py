"""Main MCP server implementation."""

import os
from typing import Any
import httpx
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("NYT")

async def make_nyt_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NYT API with proper error handling."""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def article_search(query: str) -> dict:
    """Search NYT articles

    Args:
        query: keywords to search on
        filter: filter search results
    """
    base_url = os.getenv('NYT_API_BASE_URL')
    api_key = os.getenv('NYT_API_KEY')

    if not base_url or not api_key:
        raise KeyError("NYT_API_BASE_URL or NYT_API_KEY environment variables are not set.")

    url = f"{os.getenv('NYT_API_BASE_URL')}/articlesearch.json?q={query}&api-key={os.getenv('NYT_API_KEY')}"

    data = await make_nyt_request(url)

    if not data or 'status' not in data or data['status'] != 'OK' or not data['response'] or not data['response']['docs']:
        return "Unable to perform article search."

    return data['response']['docs']


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()