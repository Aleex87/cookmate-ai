from fastapi import FastAPI

from backend.agents import generate_recipes
from backend.data_models import RecipeRequest, RecipeResponse
from fastapi import APIRouter



app = FastAPI(title="Cookmate AI")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recipes", response_model=RecipeResponse)
async def get_recipes(request: RecipeRequest) -> RecipeResponse:
    return await generate_recipes(request)
