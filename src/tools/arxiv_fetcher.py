from typing import List, Dict
import arxiv
import requests
from io import BytesIO
from pypdf import PdfReader
from pathlib import Path
import google.generativeai as genai
from typing import Any
import os 
from dotenv import load_dotenv
from src.server.mcp_server import mcp
from src.tools.template_selector import generate_dynamic_templates, analyze_with_templates
from src.prompts.templates import (
    get_template_selection_prompt,
    get_focused_summary_prompt,
    get_holistic_summary_prompt
)
import json


# Load environment variables from .env file
load_dotenv()

# Configure Gemini API using environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)


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


def extract_pdf_text(local_path: str, max_pages: int = 10) -> str:
    """Extract text from stored PDF."""
    try:
        with open(local_path, 'rb') as f:
            reader = PdfReader(BytesIO(f.read()))
        text = "".join([page.extract_text() or "" for page in reader.pages[:max_pages]])
        return text[:8000]  # Increased limit for better analysis
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def select_best_template_and_generate_summary(
    paper_text: str, 
    templates: Dict[str, str], 
    analyses: Dict[str, str]
) -> Dict[str, str]:
    """
    Use Gemini to select the most appropriate template and generate a comprehensive summary.
    
    Returns:
        Dictionary containing:
        - selected_template: The name of the chosen template
        - selection_reasoning: Why this template was chosen
        - focused_summary: Final summary using the selected template
        - holistic_summary: A holistic summary covering all templates
    """
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Step 1: Select the best template
    template_selection_prompt = get_template_selection_prompt(
        json.dumps(analyses, indent=2)
    )
    
    try:
        selection_response = model.generate_content(template_selection_prompt)
        selection_text = selection_response.text.strip()
        
        # Clean markdown code blocks
        if selection_text.startswith("```json"):
            selection_text = selection_text[7:]
        if selection_text.startswith("```"):
            selection_text = selection_text[3:]
        if selection_text.endswith("```"):
            selection_text = selection_text[:-3]
        selection_text = selection_text.strip()
        
        selection_data = json.loads(selection_text)
        selected_template = selection_data.get("selected_template", list(templates.keys())[0])
        selection_reasoning = selection_data.get("reasoning", "Template selected based on content analysis")
    except Exception as e:
        print(f"Error in template selection: {e}")
        selected_template = list(templates.keys())[0]
        selection_reasoning = "Default template selected due to selection error"
    
    # Step 2: Generate comprehensive summary based on selected template
    primary_summary_prompt = get_focused_summary_prompt(
        selected_template,
        paper_text,
        analyses.get(selected_template, "No analysis available")
    )
    
    try:
        summary_response = model.generate_content(primary_summary_prompt)
        comprehensive_summary = summary_response.text
    except Exception as e:
        comprehensive_summary = f"Error generating primary summary: {str(e)}"
    
    # Step 3: Generate holistic summary covering all aspects
    holistic_summary_prompt = get_holistic_summary_prompt(
        json.dumps(analyses, indent=2)
    )
    
    try:
        holistic_response = model.generate_content(holistic_summary_prompt)
        all_aspects_summary = holistic_response.text
    except Exception as e:
        all_aspects_summary = f"Error generating holistic summary: {str(e)}"
    
    return {
        "selected_template": selected_template,
        "selection_reasoning": selection_reasoning,
        "focused_summary": comprehensive_summary,
        "holistic_summary": all_aspects_summary
    }


@mcp.tool()
def fetch_arxiv_papers(keywords: str, max_results: int = 5, author: str = '') -> List[Dict[str, Any]]:
    """
    Fetch papers, store PDF, extract text, dynamically generate custom templates, 
    perform comprehensive analysis, select best template, and generate summaries using Gemini.
    """
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
            
            if extracted_text and "Error" not in extracted_text:
                # Step 1: Dynamically generate templates based on paper content
                print(f"Generating dynamic templates for: {result.title}")
                custom_templates = generate_dynamic_templates(extracted_text)
                
                # Step 2: Analyze using the generated templates
                print(f"Analyzing paper with {len(custom_templates)} custom templates...")
                analyses = analyze_with_templates(extracted_text, custom_templates)
                
                # Step 3: Select best template and generate summaries
                print(f"Selecting best template and generating summaries...")
                summary_results = select_best_template_and_generate_summary(
                    extracted_text, 
                    custom_templates, 
                    analyses
                )
                
                papers.append({
                    "title": str(result.title),
                    "authors": ", ".join(str(author.name) for author in result.authors),
                    "pdf_url": pdf_url,
                    "local_pdf_path": local_path,
                    "extracted_text_snippet": extracted_text[:500],
                    
                    # Template generation results
                    "generated_templates": custom_templates,
                    
                    # Individual template analyses
                    "template_analyses": analyses,
                    
                    # Summary results
                    "best_template": summary_results["selected_template"],
                    "template_selection_reasoning": summary_results["selection_reasoning"],
                    "focused_summary": summary_results["focused_summary"],
                    "holistic_summary": summary_results["holistic_summary"]
                })
            else:
                papers.append({
                    "title": str(result.title),
                    "authors": ", ".join(str(author.name) for author in result.authors),
                    "pdf_url": pdf_url,
                    "local_pdf_path": local_path,
                    "error": "Failed to extract text from PDF"
                })

    return papers

