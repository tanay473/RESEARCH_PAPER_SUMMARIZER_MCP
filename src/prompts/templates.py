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