from fastapi import FastAPI, HTTPException

from cookmate.backend.src.backend.agents import generate_recipes
from cookmate.backend.src.backend.data_models import RecipeRequest, RecipeResponse


app = FastAPI(title="Cookmate AI")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recipes", response_model=RecipeResponse)
async def get_recipes(request: RecipeRequest) -> RecipeResponse:
    try:
        return await generate_recipes(request)
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Recipe generation failed: {type(error).__name__}",
        ) from error