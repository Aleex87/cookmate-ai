from mlflow import load_prompt
from sentence_transformers import SentenceTransformer
import lancedb

from cookmate.utils.config import DB_DIR


_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
_db = lancedb.connect(DB_DIR)
_table = _db.open_table("recipes")


def load_recipe_agent_prompt(version: int = 1) -> str:
    """
    Load the recipe agent system prompt from MLFlow. 
    Args: Version of the prompt to load from MLFlow.
    Returns: The prompt tamplate string.
    """
    prompt = load_prompt(f"prompts:/recipe_agent_system_prompt/{version}")

    return prompt.template


def retrieve_recipes(query: str, top_k: int = 3) -> list[dict]:
    """
    Search the recipe vector database for the top-K most relevant recipes.

    Args:
        query: A free-text query string (e.g. "eggs pasta tomato").
        top_k: Number of recipes to return.

    Returns:
        A list of recipe dicts, each with 'id' and 'text' fields.
    """
    query_vector = _embedding_model.encode(query).tolist()
    results = _table.search(query_vector).limit(top_k).to_list()
    return [{"id": r["id"], "text": r["text"]} for r in results]