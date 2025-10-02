FALL_BACK_TEMPLATE = {
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
