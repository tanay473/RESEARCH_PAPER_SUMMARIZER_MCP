"""
Fallback templates used when dynamic template generation fails.
These provide a safety net to ensure analysis can always proceed.
"""

from typing import Dict


def get_fallback_templates() -> Dict[str, str]:
    """
    Returns fallback analysis templates for when dynamic generation fails.
    These templates cover the core aspects of research paper analysis.
    """
    return {
        "architecture_evolution": """
        Analyze the architectural innovations and design choices in this paper:
        1. What is the proposed architecture/model design?
        2. WHY did this architecture evolve? What domain needs drove these decisions?
        3. What problems in existing approaches does this architecture solve?
        4. How do the design choices connect to the problem requirements?
        5. What makes this architecture different from previous work?
        
        Paper text: {text}
        """,
        
        "mathematical_foundations": """
        Explain the mathematical and statistical foundations:
        1. What are the key equations, formulations, or statistical models?
        2. HOW does each equation contribute to the functionality?
        3. What problem does the math solve in practical terms?
        4. Connect the mathematical formalism to system behavior and performance.
        5. Why are these specific mathematical approaches necessary?
        
        Paper text: {text}
        """,
        
        "problem_and_motivation": """
        Analyze the problem context and research motivation:
        1. What is the core problem being addressed?
        2. Why were existing solutions inadequate?
        3. What gap in research does this fill?
        4. Why does this work matter to the field?
        5. What are the real-world applications or implications?
        
        Paper text: {text}
        """,
        
        "advantages_and_tradeoffs": """
        Evaluate the advantages, limitations, and trade-offs:
        1. What are the key benefits of this approach?
        2. What are the limitations or weaknesses?
        3. What are the computational costs and efficiency considerations?
        4. How does it compare to alternative approaches?
        5. What trade-offs were made in the design?
        
        Paper text: {text}
        """,
        
        "future_research": """
        Identify future research directions and scope:
        1. What questions remain open or unexplored?
        2. What improvements or extensions are suggested?
        3. What new research directions does this enable?
        4. What variations or applications could be investigated?
        5. What are the potential long-term impacts?
        
        Paper text: {text}
        """
    }


def get_legacy_prompt_templates() -> Dict[str, str]:
    """
    Legacy static templates for backward compatibility.
    Kept for reference but not actively used in the new dynamic system.
    """
    return {
        "architecture_focus": "Summarize the paper's architectural innovations, model design, and neural network structures from the provided text: {text}",
        "hardware_focus": "Summarize hardware aspects, integrations, accelerators, and optimizations from the provided text: {text}",
        "statistical_focus": "Summarize statistical modeling, probabilistic methods, and data analysis from the provided text: {text}"
    }
