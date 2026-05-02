from mlflow import load_prompt

def load_recipe_agent_prompt(version: int = 1) -> str:
    """
    Load the recipe agent system prompt from MLFlow. 
    Args: Version of the prompt to load from MLFlow.
    Returns: The prompt tamplate string.
    """
    prompt = load_prompt(f"prompts:/recipe_agent_system_prompt/{version}")

    return prompt.template
