from fastapi import FastAPI

from cookmate.backend.agents import generate_recipes
from cookmate.backend.data_models import RecipeRequest, RecipeResponse

app = FastAPI(title="Cookmate AI")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recipes", response_model=RecipeResponse)
async def get_recipes(request: RecipeRequest) -> RecipeResponse:
    return await generate_recipes(request)
