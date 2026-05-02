from mlflow import load_prompt

def load_recipe_agent_prompt(version: int = 1) -> str:
    """
    Load the recipe agent system prompt from MLFlow. 
    Args: Version of the prompt to load from MLFlow.
    Returns: The prompt tamplate string.
    """
    prompt = load_prompt(f"prompts:/recipe_agent_system_prompt/{version}")

    return prompt.template

def generate_recipes_placeholder(ingredients: list[str]) -> str:
    """
    Temporary placeholder function for recipe genertation, this funcion is ment to be removed
    later end replaced with the full RAG + LLM pipleine.
    argsuments: ingredients (list[str]): this is the list of the imput ingerdients
    return: Placeholer responce
    """
    prompt = load_recipe_agent_prompt(version=1)
    return f"""
        [debug placeholder]
        loaded prompt: {prompt[:200]}.........
        ingredient recived: {ingredients}
    """
