from pydantic import BaseModel

class Recipe(BaseModel):
    title: str
    steps: list[str]

class RecipeResponse(BaseModel):
    recipes: list[Recipe]

class RecipeRequest(BaseModel):
    ingredients: list[str]