from fastapi import FastAPI

from cookmate.backend.data_models import RecipeRequest, RecipeResponse, Recipe

app = FastAPI(title="Cookmate AI=")

@app.get("/health")
def health():
    return {"status": {"ok"}}

@app.post("/recipes", response_model=RecipeResponse)
def get_recipes(request: RecipeRequest) -> RecipeResponse:
    return RecipeResponse(
        recipes=[
            Recipe(
                title="Pasta with eggs",
                steps=[
                    "Boil pasta in salted water until al dente.",
                    "Beat eggs in a bowl and season with salt and pepper.",
                    "Drain pasta and immediately mix with eggs off the heat."
                ]
            ),
            Recipe(
                title="Tomato pasta",
                steps=[
                    "Boil pasta in salted water.",
                    "Heat olive oil and add chopped tomatoes.",
                    "Mix pasta with tomato sauce and serve."
                ]
            )
        ]
    )