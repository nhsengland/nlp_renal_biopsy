import ollama

def use_llm_to_compare(entity1: str, entity2: str, model: str = 'gemma2:2b', provider: str = 'ollama') -> bool:
    """Compare two medical entities using specified LLM."""
    query = f"""Are the phrases "{entity1}" and "{entity2}" the exact same, synonyms, or similar phrases? 
    Allow some deviation in phrasing if necessary. Only answer True or False."""
    
    if provider == 'ollama':
        response = ollama.generate(
            model=model,
            prompt=query,
            options={'temperature': 0, 'num_predict': 2}
        )
        return "True" in response['response']
    
    else:
        raise ValueError(f"Unsupported provider: {provider}")