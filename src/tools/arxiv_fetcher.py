from typing import List, Dict
import arxiv
import requests
from io import BytesIO
from pypdf import PdfReader
from src.server.mcp_server import mcp

@mcp.tool()
def fetch_arxiv_papers(keywords: str, max_results: int = 5, author: str = '') -> List[Dict[str, str]]:
    """Fetch research papers from arXiv based on keywords, with optional author matching and PDF summary extraction."""
    client = arxiv.Client()
    
    # Build query: Use keywords for title search, add author if provided
    query = f'ti:"{keywords}"'
    if author:
        query += f' AND au:"{author}"'
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers: List[Dict[str, str]] = []
    for result in client.results(search):
        # Exact title match filter (case-insensitive)
        if result.title.strip().lower() == keywords.strip().lower():
            pdf_url = str(result.pdf_url)
            pdf_summary = extract_pdf_summary(pdf_url)  # New: Extract from PDF
            
            papers.append({
                "title": str(result.title),
                "authors": ", ".join(str(author.name) for author in result.authors),
                "summary": str(result.summary),  # Keep arXiv summary if needed
                "pdf_url": pdf_url,
                "published": str(result.published),
                "pdf_summary": pdf_summary  # New field: Extracted PDF text
            })

    return papers

def extract_pdf_summary(pdf_url: str, max_pages: int = 2, max_chars: int = 10000) -> str:
    """Extract a summary from the PDF's first few pages."""
    try:
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages[:max_pages]:
            text += page.extract_text() or ""
        
        return text[:max_chars] + ("..." if len(text) > max_chars else "")
    except Exception as e:
        return f"Error extracting PDF summary: {str(e)}"

