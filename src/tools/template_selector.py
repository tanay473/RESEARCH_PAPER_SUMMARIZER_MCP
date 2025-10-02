from typing import Dict, List
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from src.server.mcp_server import mcp
from src.prompts.templates import (
    get_template_generation_prompt,
    get_executive_summary_prompt
)
from typing import Any
from src.prompts.fallback import get_fallback_templates

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)


def generate_dynamic_templates(paper_text: str) -> Dict[str, str]:
    """
    Use Gemini to dynamically generate analysis templates based on the paper content.
    Returns a dictionary of template_name -> template_prompt
    """
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    try:
        # Generate templates using Gemini
        prompt = get_template_generation_prompt(paper_text[:6000])
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        templates_data = json.loads(response_text)
        
        # Convert to dictionary format
        templates_dict = {}
        for template in templates_data.get("templates", []):
            templates_dict[template["name"]] = template["prompt"]
        
        return templates_dict
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text[:500]}")
        return get_fallback_templates()
    except Exception as e:
        print(f"Error generating dynamic templates: {e}")
        return get_fallback_templates()


def analyze_with_templates(paper_text: str, templates: Dict[str, str]) -> Dict[str, str]:
    """
    Analyze the paper using all generated templates.
    Returns a dictionary of template_name -> analysis_result
    """
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    analyses = {}
    
    for template_name, template_prompt in templates.items():
        try:
            # Fill in the template with paper text
            prompt = template_prompt.format(text=paper_text)
            response = model.generate_content(prompt)
            analyses[template_name] = response.text
        except Exception as e:
            analyses[template_name] = f"Error analyzing with template '{template_name}': {str(e)}"
    
    return analyses


@mcp.tool()
def select_prompt_template(context: str) -> str:
    """
    Legacy function for backward compatibility.
    Now returns a message indicating dynamic template generation is used.
    """
    return "Dynamic template generation is now used. Templates are generated based on paper content."


def generate_comprehensive_analysis(paper_text: str) -> Dict[str, Any]:
    """
    Main function that generates templates and performs comprehensive analysis.
    
    Returns:
        Dictionary containing:
        - generated_templates: The templates created for this paper
        - analyses: Analysis results for each template
        - summary: A brief overview of findings
    """
    # Generate custom templates based on paper content
    templates = generate_dynamic_templates(paper_text)
    
    # Perform analysis using all templates
    analyses = analyze_with_templates(paper_text, templates)
    
    # Generate a brief summary
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    summary_prompt = get_executive_summary_prompt(json.dumps(analyses, indent=2))
    
    try:
        summary_response = model.generate_content(summary_prompt)
        summary = summary_response.text
    except Exception as e:
        summary = f"Error generating summary: {str(e)}"
    
    return {
        "generated_templates": templates,
        "analyses": analyses,
        "summary": summary
    }
