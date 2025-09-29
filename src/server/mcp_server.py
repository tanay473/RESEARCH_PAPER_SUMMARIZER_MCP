from mcp.server.fastmcp import FastMCP

# Create shared MCP instance
mcp = FastMCP(
    name="Research Paper MCP Server",
    instructions="Fetches papers from arXiv and whitepapers, provides summarizations via context-based templates."
)

'''here we can create a N number of instances and then we can run those suitable instances in the main.py'''