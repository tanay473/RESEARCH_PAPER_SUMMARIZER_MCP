# Importing automatically registers tools and prompts via decorators
from src.server.mcp_server import mcp
import src.tools.arxiv_fetcher
import src.prompts.templates
import src.prompts.fallback

if __name__ == "__main__":
    mcp.run(transport="stdio")
