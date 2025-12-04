# NYT MCP Server

This is a proof of concept for a Model Context Protocol (MCP) server for NYT data. It currently only supports article search. The client for this is Claude Desktop. A link to the instructions for setting up the Google Sheets MCP server to save search results are below. The use case in mind is:

"NYTimes article search for 'street crimes' and write to spreadsheet named 'Crimes'"

Note: This project was scaffolded swiftly with Claude Code. MCP implementation was done by a human (me).

## Demo

https://github.com/user-attachments/assets/3cc1b9e3-6c19-4b1c-abc1-2cbeb5780684

[Download hi-res video](https://drive.google.com/file/d/14icof5m-8sDIXCGc1vntQ5nGBE8f9xwx/view?usp=sharing)

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

### Run with mcp-google-sheets
Follow the instructions [here](https://github.com/xing5/mcp-google-sheets?tab=readme-ov-file#-ultra-quick-start-using-uvx), specifically the Service Account authentication.

To use this server with Claude Desktop, add to your Claude Desktop config:

```json
"google-sheets": {
      "command": "/Users/xxxx/.local/bin/uvx",
      "args": ["mcp-google-sheets@latest"],
      "env": {
        "SERVICE_ACCOUNT_PATH": "/Users/path-to-service-account-json/webrtcdemo-xxxxxx-xxxxxx.json",
        "DRIVE_FOLDER_ID": "1xxxxxxxxxx"
      }
    }
```

Note that on a Mac, the full path to uvx should be used.

