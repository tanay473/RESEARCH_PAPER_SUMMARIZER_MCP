from typing import Dict, List
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from src.server.mcp_server import mcp
from typing import Any

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)


# Meta-prompt for Gemini to generate custom analysis templates
TEMPLATE_GENERATION_PROMPT = """
You are an expert research paper analyzer. Based on the following paper excerpt, generate 3-5 focused analysis templates that will help deeply understand this specific paper.

Paper excerpt:
{text}

Generate templates that cover these aspects:
1. **Architecture & Design Evolution**: Analyze the architectural innovations, model design choices, and WHY this architecture evolved. Explain the domain needs and problems that drove these specific design decisions. What was inadequate in previous approaches?

2. **Mathematical & Statistical Foundations**: Explain the statistical equations, mathematical formulations, and their functional role. Connect the math to the practical functionality - HOW do these equations enable the system to work? What problem does each equation solve?

3. **Problem Context & Motivation**: Identify the core problem being solved, the gap in existing research, and why this work matters to the field.

4. **Advantages & Trade-offs**: Analyze the benefits, limitations, computational costs, performance gains, and practical trade-offs of the proposed approach compared to alternatives.

5. **Future Research Directions & Scope**: Identify open questions, potential improvements, unexplored variations, and promising research directions suggested by or enabled by this work.

Return your response as a JSON object with this structure:
{{
  "templates": [
    {{
      "name": "architecture_evolution",
      "description": "Brief description of what this template analyzes",
      "prompt": "Detailed prompt that instructs the AI to analyze this specific aspect of the paper in depth"
    }},
    ...
  ]
}}

Make each template prompt specific, detailed, and actionable. The prompts should guide deep analysis, not just summarization.
"""


def generate_dynamic_templates(paper_text: str) -> Dict[str, str]:
    """
    Use Gemini to dynamically generate analysis templates based on the paper content.
    Returns a dictionary of template_name -> template_prompt
    """
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    try:
        # Generate templates using Gemini
        prompt = TEMPLATE_GENERATION_PROMPT.format(text=paper_text[:6000])  # Use more context
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


def get_fallback_templates() -> Dict[str, str]:
    """
    Fallback templates in case dynamic generation fails.
    """
    return {
        "architecture_evolution": """
        Analyze the architectural innovations and design choices in this paper:
        1. What is the proposed architecture/model design?
        2. WHY did this architecture evolve? What domain needs drove these decisions?
        3. What problems in existing approaches does this architecture solve?
        4. How do the design choices connect to the problem requirements?
        
        Paper text: {text}
        """,
        
        "mathematical_foundations": """
        Explain the mathematical and statistical foundations:
        1. What are the key equations, formulations, or statistical models?
        2. HOW does each equation contribute to the functionality?
        3. What problem does the math solve in practical terms?
        4. Connect the mathematical formalism to system behavior and performance.
        
        Paper text: {text}
        """,
        
        "problem_and_motivation": """
        Analyze the problem context and research motivation:
        1. What is the core problem being addressed?
        2. Why were existing solutions inadequate?
        3. What gap in research does this fill?
        4. Why does this work matter to the field?
        
        Paper text: {text}
        """,
        
        "advantages_and_tradeoffs": """
        Evaluate the advantages, limitations, and trade-offs:
        1. What are the key benefits of this approach?
        2. What are the limitations or weaknesses?
        3. What are the computational costs and efficiency considerations?
        4. How does it compare to alternative approaches?
        
        Paper text: {text}
        """,
        
        "future_research": """
        Identify future research directions and scope:
        1. What questions remain open or unexplored?
        2. What improvements or extensions are suggested?
        3. What new research directions does this enable?
        4. What variations or applications could be investigated?
        
        Paper text: {text}
        """
    }


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
    summary_prompt = f"""
    Based on these analyses of a research paper, provide a brief executive summary (3-4 sentences):
    
    {json.dumps(analyses, indent=2)}
    """
    
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
