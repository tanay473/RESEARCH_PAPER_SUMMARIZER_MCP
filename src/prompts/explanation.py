def explain_concept(concept: str, detail_level: str = "medium") -> str:
    levels = {
        "simple": "Explain this concept in simple terms for beginners.",
        "medium": "Provide a balanced explanation with some technical details.",
        "advanced": "Give a detailed, technical explanation suitable for experts."
    }
    instruction = levels.get(detail_level.lower(), levels["medium"])
    return f"{instruction}\n\nConcept: {concept}"
