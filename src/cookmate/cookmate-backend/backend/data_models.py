from pydantic import BaseModel, Field


class Recipe(BaseModel):
    title: str = Field(
        description="The name of the recipe.",
        examples=["Pasta with eggs"]
    )
    steps: list[str] = Field(
        description="Ordered list of cooking instructions, one step per item.",
        examples=[["Boil pasta", "Beat eggs", "Combine and serve"]]
    )


class RecipeResponse(BaseModel):
    recipes: list[Recipe] = Field(
        description="List of recommended recipes the user can make with their ingredients.",
        examples=[[
            {
                "title": "Pasta with eggs",
                "steps": ["Boil pasta", "Beat eggs", "Combine and serve"]
            }
        ]]
    )


class RecipeRequest(BaseModel):
    ingredients: list[str] = Field(
        description="List of ingredients the user has available at home.",
        examples=[["eggs", "pasta", "tomato"]]
    )