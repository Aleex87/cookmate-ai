from utils.config import DB_DIR, OPENROUTER_BASE_URL, LLM_MODEL
from dotenv import load_dotenv

load_dotenv()

import os

from mlflow.genai import load_prompt
from sentence_transformers import SentenceTransformer
import lancedb
from pydantic_ai import Agent 
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from backend.data_models import RecipeRequest, RecipeResponse

_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
_db = lancedb.connect(DB_DIR)

def get_recipe_table(): #LLM solution, lazy loading
    return _db.open_table("recipes")

_provider = OpenAIProvider(
    base_url=OPENROUTER_BASE_URL,
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

_model = OpenAIModel(
    LLM_MODEL,
    provider=_provider,
)

print("db dir=", DB_DIR)
print("db dir=", DB_DIR.exists())
print("db dir=", list(DB_DIR.iterdir()))

def load_recipe_agent_prompt(version: int = 1) -> str:
    """
    Load the recipe agent system prompt from MLFlow. 
    Args: Version of the prompt to load from MLFlow.
    Returns: The prompt tamplate string.
    """
    prompt = load_prompt("recipe_agent_system_prompt")

    return prompt.template

_system_prompt = load_recipe_agent_prompt(version=3)

recipe_agent = Agent(
    model=_model,
    output_type=RecipeResponse,
    system_prompt=_system_prompt,
    retries=3
)


@recipe_agent.tool_plain
def retrieve_recipes(query: str, top_k: int = 3) -> str:
    """
    Search the recipe vector database for the top-K most relevant recipes
    based on the user's ingredients.

    Args:
        query: A free-text query string of ingredients (e.g. "eggs pasta tomato").
        top_k: Number of recipes to return.

    Returns:
        A formatted string containing the retrieved recipes, ready for the agent.
    """
    query_vector = _embedding_model.encode(query).tolist()
    _table = get_recipe_table()
    results = _table.search(query_vector).limit(top_k).to_list()

    lines = []
    for i, recipe in enumerate(results, start=1):
        lines.append(f"[{i}] (id: {recipe['id']}) {recipe['text']}")
    return "\n".join(lines)


async def generate_recipes(request: RecipeRequest) -> RecipeResponse:
    """
    Generate recipe suggestions based on the user's available ingredients.

    The agent will automatically call the retrieve_recipes tool when needed
    to look up recipes from the vector database.

    Args:
        request: The user's ingredient list wrapped in a RecipeRequest.

    Returns:
        A RecipeResponse withh recommended recipes.
    """
    query = ", ".join(request.ingredients)
    result = await recipe_agent.run(query)
    return result.output
  