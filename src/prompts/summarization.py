from typing import Optional
from src.server.mcp_server import mcp
from src.prompts.templates import prompt_templates
from src.utils.helpers import get_prompt_instruction
from src.tools.template_selector import select_prompt_template, sample_alternative_templates

@mcp.prompt(name="Summarize Research Paper")
def summarize_paper(paper_text: str, context: str, template_key: Optional[str] = None) -> str:
    """Generate a summarization prompt after selecting or sampling templates based on context."""
    if template_key is None:
        template_key = select_prompt_template(context)
    samples = sample_alternative_templates(paper_text, template_key, context) #type:ignore
    if "warning" in samples:
        return "\n\n".join([f"Sample for {k}: {v}" for k, v in samples.items() if k != "warning"]) + f"\n\n{samples['warning']}"
    instruction = get_prompt_instruction(template_key, prompt_templates)
    return f"{instruction}\n\nPaper content:\n{paper_text}"
