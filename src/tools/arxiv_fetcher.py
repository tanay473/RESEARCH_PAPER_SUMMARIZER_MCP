from typing import List, Dict
import arxiv
import requests
from io import BytesIO
from pypdf import PdfReader
from pathlib import Path
import google.generativeai as genai
from typing import Any
import os 
from src.server.mcp_server import mcp


# Configure Gemini API using environment variable
genai.configure(api_key='AIzaSyChUXPd5Uk67ifo_G6hONVDBIBrLJWbkyc')


# Define templates for diverse aspects
prompt_templates = {
    "architecture_focus": "Summarize the paper's architectural innovations, model design, and neural network structures from the provided text: {text}",
    "hardware_focus": "Summarize hardware aspects, integrations, accelerators, and optimizations from the provided text: {text}",
    "statistical_focus": "Summarize statistical modeling, probabilistic methods, and data analysis from the provided text: {text}"
}


def download_pdf(pdf_url: str, download_dir: str = "./pdfs") -> str:
    """Download and store PDF locally."""
    try:
        response = requests.get(pdf_url, timeout=20)
        response.raise_for_status()
        Path(download_dir).mkdir(parents=True, exist_ok=True)
        filename = pdf_url.split('/')[-1]
        file_path = Path(download_dir) / filename
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return str(file_path)
    except Exception as e:
        return f"Error downloading PDF: {str(e)}"


def extract_pdf_text(local_path: str, max_pages: int = 5) -> str:
    """Extract text from stored PDF."""
    try:
        with open(local_path, 'rb') as f:
            reader = PdfReader(BytesIO(f.read()))
        text = "".join([page.extract_text() or "" for page in reader.pages[:max_pages]])
        return text[:5000]  # Limit for API efficiency
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def select_primary_template(extracted_text: str) -> str:
    """Keyword-based template selection."""
    text_lower = extracted_text.lower()
    if any(k in text_lower for k in ["statistic", "probabil", "data analysis", "modeling"]):
        return "statistical_focus"
    elif any(k in text_lower for k in ["hardware", "chip", "accelerator", "integration"]):
        return "hardware_focus"
    else:
        return "architecture_focus"  # Default


def summarize_with_gemini(extracted_text: str, template_key: str) -> str:
    """Use Gemini API to generate a summary with the given template."""
    model = genai.GenerativeModel('gemini-2.5-flash')  # Or 'gemini-1.5-pro' for advanced tasks
    prompt = prompt_templates[template_key].format(text=extracted_text)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {str(e)}"


@mcp.tool()
def fetch_arxiv_papers(keywords: str, max_results: int = 5, author: str = '') -> List[Dict[str, Any]]:
    """Fetch papers, store PDF, extract text, select template, and generate multi-template summaries via Gemini."""
    client = arxiv.Client()
    query = f'ti:"{keywords}"'
    if author:
        query += f' AND au:"{author}"'
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)


    papers: List[Dict[str, Any]] = []
    for result in client.results(search):
        if result.title.strip().lower() == keywords.strip().lower():
            pdf_url = str(result.pdf_url)
            local_path = download_pdf(pdf_url)  # Download and store
            extracted_text = extract_pdf_text(local_path) if "Error" not in local_path else ""
            primary_template = select_primary_template(extracted_text)
            
            # Generate summaries for all templates using Gemini (diverse aspects)
            summaries = {}
            for key in prompt_templates:
                summaries[key] = summarize_with_gemini(extracted_text, key)
            
            papers.append({
                "title": str(result.title),
                "authors": ", ".join(str(author.name) for author in result.authors),
                "pdf_url": pdf_url,
                "local_pdf_path": local_path,
                "extracted_text_snippet": extracted_text[:500],
                "primary_template": primary_template,
                "multi_summaries": summaries  # Gemini-generated summaries
            })


    return papers

