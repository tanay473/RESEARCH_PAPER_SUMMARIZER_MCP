from typing import Any, Dict, Optional

def safe_get_href(link: Any) -> str:
    href = link.get('href', '')
    return href if isinstance(href, str) else ''

def get_prompt_instruction(template_key: Optional[str], prompt_templates: Dict[str, str]) -> str:
    if not template_key or template_key not in prompt_templates:
        return prompt_templates["new_architecture"]
    return prompt_templates[template_key]
