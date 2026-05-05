import json

from dotenv import load_dotenv
import lancedb
import mlflow
from mlflow.genai import evaluate
from mlflow.genai.scorers import Completeness, Correctness, Fluency
from sentence_transformers import SentenceTransformer

from cookmate.utils.config import DB_DIR, EVALUATION_DATASET_PATH, RECIPES_JSON_PATH


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








DATASET_PATH = Path(__file__).parent / "evaluation_dataset.json"


def load_dataset():
    """Load evaluation dataset from JSON file."""
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def fake_agent(ingredients: list[str]) -> dict:
    """
    Temporary fake agent.

    This simulates the expected structure of the future recipe agent.
    """
    return {
        "recipes": [
            {
                "title": "Simple pasta with eggs",
                "ingredients": ingredients,
                "description": "A simple recipe idea based on the provided ingredients.",
            }
        ]
    }

def run_judge():
     

    dataset = load_dataset()

    # Prepare evaluation format
    eval_data = []

    for item in dataset:
        ingredients = item["inputs"]["ingredients"]
        expected = item["expectations"]["description"]

        output = fake_agent(ingredients)

        eval_data.append(
        {
        "inputs": {
            "ingredients": ingredients
            },
        "outputs": output,
        "expectations": {
            "expected_response": expected
            },
        }
    )

    # Start MLflow experiment
    mlflow.set_experiment("cookmate-llm-judge")
    llm_judge = "openrouter:/openai/gpt-oss-20b:free"

    with mlflow.start_run():
        results = evaluate(
            data=eval_data,
            scorers=[
                Correctness(model=llm_judge),
    ],
)

        print("Evaluation results:")
        print(results)
        

if __name__ == "__main__":
    run_judge()