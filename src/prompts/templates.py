"""
Prompt templates for dynamic analysis generation and summarization.
These prompts guide Gemini in analyzing and summarizing research papers.
"""


# Meta-prompt for generating custom analysis templates
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


# Prompt for selecting the best template
TEMPLATE_SELECTION_PROMPT = """
You are analyzing a research paper. You have generated multiple analysis templates and their corresponding analyses.

Available templates and their analyses:
{analyses}

Your task:
1. Review all the analyses above
2. Determine which template/aspect provides the MOST valuable insights for understanding this paper
3. Explain why this aspect is most critical

Respond in JSON format:
{{
  "selected_template": "template_name",
  "reasoning": "Explanation of why this template is most valuable for this specific paper"
}}
"""


# Prompt for generating focused summary based on selected template
FOCUSED_SUMMARY_PROMPT = """
You are summarizing a research paper with focus on: {selected_template}

Paper text:
{paper_text}

Analysis from the selected perspective:
{selected_analysis}

Generate a comprehensive, well-structured summary that:
1. Clearly explains the main contribution
2. Focuses on the {aspect_name} aspects
3. Uses clear, technical language
4. Provides specific details and insights
5. Is suitable for researchers in this field

Length: 300-500 words
"""


# Prompt for generating holistic summary covering all aspects
HOLISTIC_SUMMARY_PROMPT = """
You are creating a holistic summary of a research paper by synthesizing multiple analytical perspectives.

All analyses:
{all_analyses}

Create a comprehensive summary that:
1. **Overview**: What is this paper about? (2-3 sentences)
2. **Architecture & Design**: Key architectural innovations and why they evolved
3. **Mathematical Foundations**: How the math/statistics enable functionality
4. **Key Advantages**: Main benefits and performance improvements
5. **Limitations & Trade-offs**: Important constraints or costs
6. **Future Directions**: Promising research opportunities

Structure your response with clear sections. Be specific and technical.
Length: 400-600 words
"""


# Prompt for generating executive summary
EXECUTIVE_SUMMARY_PROMPT = """
Based on these analyses of a research paper, provide a brief executive summary (3-4 sentences):

{analyses}

Focus on:
- The core innovation or contribution
- Why it matters
- Key results or advantages
"""


def get_template_generation_prompt(paper_text: str) -> str:
    """Returns formatted prompt for generating dynamic templates."""
    return TEMPLATE_GENERATION_PROMPT.format(text=paper_text)


def get_template_selection_prompt(analyses: str) -> str:
    """Returns formatted prompt for selecting best template."""
    return TEMPLATE_SELECTION_PROMPT.format(analyses=analyses)


def get_focused_summary_prompt(
    selected_template: str,
    paper_text: str,
    selected_analysis: str
) -> str:
    """Returns formatted prompt for generating focused summary."""
    aspect_name = selected_template.replace('_', ' ')
    return FOCUSED_SUMMARY_PROMPT.format(
        selected_template=selected_template,
        paper_text=paper_text[:6000],
        selected_analysis=selected_analysis,
        aspect_name=aspect_name
    )


def get_holistic_summary_prompt(all_analyses: str) -> str:
    """Returns formatted prompt for generating holistic summary."""
    return HOLISTIC_SUMMARY_PROMPT.format(all_analyses=all_analyses)


def get_executive_summary_prompt(analyses: str) -> str:
    """Returns formatted prompt for generating executive summary."""
    return EXECUTIVE_SUMMARY_PROMPT.format(analyses=analyses)
