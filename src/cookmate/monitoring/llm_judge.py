import json
import os
from pathlib import Path
from dotenv import load_dotenv
import mlflow
from mlflow.genai import evaluate
from mlflow.genai.scorers import Correctness

load_dotenv()

DATASET_PATH = Path(__file__).parent / "evaluation_dataset.json"


def load_dataset():
    """Load evaluation dataset from JSON file."""
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def fake_agent(ingredients: list[str]) -> str:
    """
    Temporary fake agent.

    This simulates a response from the real system.
    Later we will replace this with the real backend agent.
    """
    return f"Suggested recipes using: {', '.join(ingredients)}"


def run_judge():
    import os
    print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
    print("OPENAI_API_BASE:", os.getenv("OPENAI_API_BASE"))

    
    
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

    with mlflow.start_run():
        results = evaluate(
            data=eval_data,
            scorers=[Correctness(model="openai/gpt-3.5-turbo")],
        )

        print("Evaluation results:")
        print(results)
        

if __name__ == "__main__":
    run_judge()