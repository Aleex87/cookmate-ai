from pydantic import BaseModel, Field


class RecipeRequest(BaseModel):
    ingredients: list[str] = Field(
        description="List of ingredients available to the user."
    )


class Recipe(BaseModel):
    title: str = Field(
        description="The name of the recipe."
    )
    steps: list[str] = Field(
        description="A list of short cooking steps. Each step should be a clear instruction."
    )


class RecipeResponse(BaseModel):
    recipes: list[Recipe] = Field(
        description="A list of exactly three recipe suggestions."
    )