# Generic MCP Server Configuration Guide
This guide provides a user-agnostic setup for configuring an MCP (Model Context Protocol) server, which allows local AI tools like LM Studio or Claude Desktop to connect to custom Python scripts (e.g., for tasks like research paper summarization). It's designed for any user on Windows, macOS, or Linux, with placeholders for personalization. The config is typically stored in a JSON file (e.g., `mcp.json` or `mcp-config.json`).

MCP servers enable AI models to use your custom tools and prompts. Choose "stdio" transport for direct local execution or "http" for running the server independently.

## Prerequisites (For All Users)- 
Install the AI app: LM Studio or Claude Desktop (latest version recommended).
- Python 3.8+ installed, with dependencies for your script (e.g., `pip install mcp arxiv requests beautifulsoup4`).
- Your MCP server script (e.g., `mcp_script.py`) in a known directory.
- For HTTP transport, install Uvicorn if needed (`pip install uvicorn`) to run the server.

## Key Configuration Parameters- 
- **name/id**: Unique name for your server (e.g., "my-mcp-server").
- **description**: Brief explanation of the server's function.
- **transport**: "stdio" (local execution) or "http" (remote endpoint).
- **command**: Command to run the script (e.g., "python mcp_script.py").
- **working_directory/workingDir**: Full path to your script's folder (e.g., "/path/to/your/project").
- **url/endpoint** (HTTP only): Server URL (e.g., "http://localhost:8000").
- **version**: Optional (e.g., "1.0.0").

Use absolute paths to avoid issues. Placeholders like `<YOUR_SCRIPT_NAME>` can be replaced with your details.

## Setup for LM StudioLM Studio uses a `mcp.json` file for MCP configs.

### Steps1. Open LM Studio and go to the "Program" tab (>_ icon).
2. Click "Install" > "Edit mcp.json" to open the editor.
3. Add your server under "mcpServers".
4. Save, restart LM Studio, and connect via the Program tab.
5. Test by prompting a model that uses your MCP tools.

### Sample Config (stdio)
```json
{
  "mcpServers": {
    "my-mcp-server": {
      "name": "My MCP Server",
      "description": "Custom tools for AI tasks.",
      "version": "1.0.0",
      "transport": "stdio",
      "command": "python <YOUR_SCRIPT_NAME>.py",
      "working_directory": "<YOUR_WORKING_DIR>"
    }
  }
}
```

### Sample Config (http)Run your script first (e.g., `uvicorn <YOUR_SCRIPT_NAME>:app --host 0.0.0.0 --port 8000`).

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "name": "My MCP Server",
      "transport": "http",
      "url": "http://localhost:8000"
    }
  }
}
```

## Setup for Claude Desktop
Claude Desktop (Anthropic's app) integrates MCP via a config file or API settings. Check Anthropic docs for exact paths, as it may vary.

### Steps
1. Open Claude Desktop and navigate to Settings > Extensions > MCP (or API integrations).
2. Create/edit `mcp-config.json` in Claude's config folder (e.g., `~/Library/Application Support/Claude/mcp-config.json` on macOS or equivalent).
3. Add your server details.
4. Restart the app and enable the MCP extension.
5. Test in a chat by invoking your tools (e.g., "Use MCP to summarize a paper").

### Sample Config (stdio)
```json
{
  "servers": [
    {
      "id": "my-mcp-server",
      "name": "My MCP Server",
      "description": "Custom tools for AI tasks.",
      "transport": "stdio",
      "command": "python <YOUR_SCRIPT_NAME>.py",
      "workingDir": "<YOUR_WORKING_DIR>"
    }
  ]
}
```

### Sample Config (http) Run your script as a server first.
```json
{
  "servers": [
    {
      "id": "my-mcp-server",
      "name": "My MCP Server",
      "transport": "http",
      "endpoint": "http://localhost:8000"
    }
  ]
}
```

## Troubleshooting Tips
- **Path Errors**: Use full absolute paths in "command" (e.g., "python /full/path/to/<YOUR_SCRIPT_NAME>.py").
- **Connection Issues**: Ensure the script runs without errors standalone. For HTTP, verify the port is open (test with `curl http://localhost:8000`).
- **Logs**: Enable debug logs in the app settings and check for errors.
- **Updates**: Ensure your app and MCP SDK are up-to-date (e.g., `pip install --upgrade mcp`).
- **Platform Differences**: On macOS/Linux, use forward slashes in paths; on Windows, use double backslashes (e.g., "C:\\\\path\\\\to\\\\dir").
- If the server fails to start, clear app cache or reinstall the MCP plugin.

This guide is generic and can be adapted for any MCP-compatible app. Replace placeholders with your specifics, and consult official docs for app-specific variations.