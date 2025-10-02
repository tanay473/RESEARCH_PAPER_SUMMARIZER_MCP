# MCP Research Paper Summarizer

A simple MCP server in Python for fetching and summarizing research papers from arXiv and company sites. Works with LM Studio and Claude Desktop.

## What It Does
This tool grabs papers based on keywords and creates smart summaries using different templates (like for new AI architectures or hardware stuff). It picks the best template automatically and can try others if needed.

## Features
- Fetch papers from arXiv.
- Auto-select summary templates based on paper content.
- Sample alternative summaries if the first pick seems off.
- Explain concepts from papers at simple, medium, or advanced levels.
- Runs locally or as a server.

## Setup
1. Clone the repo:
   ```
   git clone https://github.com/tanay473/RESEARCH_PAPER_SUMMARIZER_MCP.git
   cd mcp-research-summarizer
   ```

2. Install stuff:
   ```
   pip install mcp arxiv requests beautifulsoup4
   ```

3. Run it:
   ```
   python mcp_arxiv.py
   ```

## How to Use
- In LM Studio or Claude Desktop, add the server via config (check docs/GENERIC_SETUP.md).
- Ask things like: "Summarize recent papers on transformers" or "Explain attention mechanisms simply."

## Config Example (for LM Studio)
Put this in mcp.json:
```json
{
  "mcpServers": {
    "research-paper-server": {
      "name": "Research Paper Server",
      "transport": "stdio",
      "command": "python mcp_arxiv.py",
      "working_directory": "/your/project/path"
    }
  }
}
```
## Setup 
for further setup refer the setup.md in the repo and setup the server

## limitations
cannot get the papers from the specific companies if they are not avaliable on arxiv 
## Note
This was just a demo to test the MCP for reducing the burden of manual prompting to summarize the research paper 
so with this it generates the dynamic templates covering the different aspects of research paper for better summary (kind of Automation for my daily usage)
So give it a try ....

## Contributing
Fork it, make changes, and send a pull request. Open issues for bugs or ideas.


