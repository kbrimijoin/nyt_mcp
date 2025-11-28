# NYT MCP Server

A Model Context Protocol (MCP) server for NYT data.

## Setup

1. Create a virtual environment:
```bash
uv venv --python 3.12
source .venv/bin/activate  # On Windows: venv\Scripts\activate
uv pip install pip
```

2. Install dependencies:
```bash
pip install -e .
```

## Running the Server

```bash
python src/mcp_server/server.py
```

Or use the installed script:
```bash
nyt-mcp-server
```

## Development

The server implements the Model Context Protocol and can be integrated with MCP clients like Claude Desktop.

### Project Structure

```
nyt_mcp/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       └── server.py
├── pyproject.toml
└── README.md
```

### Adding Tools

Edit `src/mcp_server/server.py` to add new tools:

1. Add tool definition in `list_tools()`
2. Add tool implementation in `call_tool()`

## Configuration

To use this server with Claude Desktop, add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "nyt": {
      "command": "python",
      "args": ["/path/to/nyt_mcp/src/mcp_server/server.py"]
    }
  }
}
```
