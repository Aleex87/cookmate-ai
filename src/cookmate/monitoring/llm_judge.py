import json

from dotenv import load_dotenv
import lancedb
import mlflow
from pydantic import BaseModel, Field
from mlflow.genai import evaluate
from mlflow.genai.scorers import Completeness, Correctness, Fluency
from sentence_transformers import SentenceTransformer

#from cookmate.utils.config import DB_DIR, EVALUATION_DATASET_PATH, RECIPES_JSON_PATH
from utils.config import DB_DIR, EVALUATION_DATASET_PATH, RECIPES_JSON_PATH

load_dotenv()

# load evalutation_dataset.json 
def load_evaluation_dataset() -> list[dict]:
    "Load evaluation dataset from JSON file."
    with open(EVALUATION_DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# load recipes_clean.json   
def load_recipe_lookup() -> dict:
    "Load clean recipes adn create a lookup dictionary by recipes id"
    with open(RECIPES_JSON_PATH, "r", encoding="utf-8") as f:
        recipes = json.load(f)
    
    return {recipe["id"]: recipe for recipe in recipes}

class RetrievedRecipe(BaseModel):
    "Structured recipe record used for evaluation"
    id: str = Field(description="Unique recipe identifier from the recipe database.")
    title: str = Field(description="Recipe title.")
    ingredients: list[str] = Field(description="List of ingredients required by the recipe.")
    instructions: list[str] = Field(description="Step-by-step cooking instructions.")

class RetrievalOutput(BaseModel):
    """Structured retrieval output used for MLflow evaluation."""
    recipes: list[RetrievedRecipe] = Field(
        description="List of recipes retrieved from the vector database.")


def retrieve_recipes(
    ingredients: list[str],
    recipe_lookup: dict,
    embedding_model: SentenceTransformer,
    limit: int = 3,
) -> dict:
    """
    Retrieve recipes from LanceDB using ingredient query embeddings.

    Args:
        ingredients (list[str]): User-provided ingredients
        recipe_lookup (dict): Lookup dictionary with full recipe records by id.
        embedding_model (SentenceTransformer): Embedding model used for query encoding
        limit (int): Number of recipes to retrieve
    Returns:
        dict: Validated structured retrieval output with recipe details.
    """
    db = lancedb.connect(DB_DIR)
    recipes_table = db.open_table("recipes")

    query_text = ", ".join(ingredients)
    query_vector = embedding_model.encode(query_text).tolist()

    retrieved_rows = (
        recipes_table
        .search(query_vector)
        .limit(limit)
        .to_pandas()
    )

    retrieved_recipe_ids = retrieved_rows["id"].tolist()

    retrieved_recipes = [
        RetrievedRecipe(
            id=recipe_lookup[recipe_id]["id"],
            title=recipe_lookup[recipe_id]["title"],
            ingredients=recipe_lookup[recipe_id]["ingredients"],
            instructions=recipe_lookup[recipe_id]["instructions"],
        )
        for recipe_id in retrieved_recipe_ids
    ]

    retrieval_output = RetrievalOutput(recipes=retrieved_recipes)

    return retrieval_output.model_dump()

def run_judge() -> None:
    """Run MLflow evaluation using real LanceDB retrieval outputs."""
    evaluation_dataset = load_evaluation_dataset()
    recipe_lookup = load_recipe_lookup()

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    eval_data = []

    for item in evaluation_dataset:
        ingredients = item["inputs"]["ingredients"]

        output = retrieve_recipes(
            ingredients=ingredients,
            recipe_lookup=recipe_lookup,
            embedding_model=embedding_model,
            limit=3,
        )

        eval_data.append(
            {
                "inputs": {
                    "ingredients": ingredients
                },
                "outputs": output,
                "expectations": {
                    "expected_facts": [
                        "The output should contain recipes related to the input ingredients.",
                        "The output should include recipe titles.",
                        "The output should include recipe ingredients.",
                        "The output should include recipe instructions.",
                        "The output should not invent recipes outside the recipe database."
                    ]
                },
            }
        )

    mlflow.set_experiment("cookmate-llm-judge")

    llm_judge = "openrouter:/openai/gpt-oss-20b:free"

    with mlflow.start_run(run_name="cookmate-retrieval-evaluation"):
        mlflow.log_param("judge_model", llm_judge)
        mlflow.log_param("embedding_model", "all-MiniLM-L6-v2")
        mlflow.log_param("retrieval_limit", 3)

        results = evaluate(
            data=eval_data,
            scorers=[
                Correctness(model=llm_judge),
                    ],
        )

        print("Evaluation results:")
        print(results)
        print("Metrics:")
        print(results.metrics)



if __name__ == "__main__":
    run_judge()