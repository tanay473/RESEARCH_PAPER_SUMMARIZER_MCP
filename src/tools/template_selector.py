from typing import Dict
from src.prompts.templates import prompt_templates
from src.server.mcp_server import mcp

@mcp.tool()
def select_prompt_template(context: str) -> str:
    ctx = context.lower()
    if any(k in ctx for k in ["statistic", "probabil", "data analysis"]):
        return "statistical_domain_architecture"
    elif any(k in ctx for k in ["hardware", "chip", "accelerator"]):
        return "hardware_and_architecture"
    elif any(k in ctx for k in ["architecture", "model design"]):
        return "new_architecture"
    return "new_architecture"

def sample_alternative_templates(paper_text: str, chosen_key: str, context: str) -> Dict[str, str]:
    recommended_key = select_prompt_template(context)
    if chosen_key != recommended_key:
        samples = {
            key: f"{template}\n\nPaper content:\n{paper_text}"
            for key, template in prompt_templates.items()
        }
        samples["warning"] = f"Chosen template '{chosen_key}' may be unsuitable. Recommended: '{recommended_key}'."
        return samples
    return {"message": "Chosen template is suitable; no sampling needed."}
