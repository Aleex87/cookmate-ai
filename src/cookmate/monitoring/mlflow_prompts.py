from pathlib import Path
from mlflow.genai import register_prompt
from cookmate.utils.config import BASE_DIR

PROMPT_PATH= BASE_DIR / "prompts" / "recipe_agent_system_prompt.md"

def read_prompt(prompt_path : Path) -> str:
    "Read a prompt file and return its content as a string"
    return prompt_path.read_text(encoding="utf-8")

def register_recipe_agent_prompt() -> None:
    "Register the recipe agent system prompt in MLflow"
    prompt_template= read_prompt(PROMPT_PATH)

    registered_prompt = register_prompt(
        name= "recipe_agent_system_prompt",
        template= prompt_template,
        commit_message="Initial recipe agent system prompt",
        tags= {
                "project": "cookmate-ai",
                "agent": "recipe_agent",
                "prompt_type": "system_prompt",
        },
    )

    print("Prompt registered successfully.")
    print(f"Name: {registered_prompt.name}")
    print(f"Version: {registered_prompt.version}")

if __name__ == "__main__":
    register_recipe_agent_prompt()
    