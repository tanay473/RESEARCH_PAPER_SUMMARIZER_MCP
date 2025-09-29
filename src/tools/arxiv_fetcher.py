from typing import List, Dict
import arxiv
from src.server.mcp_server import mcp

@mcp.tool()
def fetch_arxiv_papers(keywords: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Fetch research papers from arXiv based on keywords."""
    client = arxiv.Client()
    search = arxiv.Search(
        query=keywords,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers: List[Dict[str, str]] = []
    for result in client.results(search):
        papers.append({
            "title": str(result.title),
            "authors": ", ".join(str(author.name) for author in result.authors),
            "summary": str(result.summary),
            "pdf_url": str(result.pdf_url),
            "published": str(result.published),
        })

    return papers
