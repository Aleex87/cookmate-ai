import json 
import lancedb
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from src.cookmate.utils.config import PROCESSED_DATA_DIR, DB_DIR

load_dotenv()

embedding_model = get_registry().get("cohere").create(
    name="embed-multilingual-v3.0"
)

class RecipeModel(LanceModel):
    id: str
    title: str 
    ingredients: str
    instructions: str
    text: str = embedding_model.SourceField()
    vector: Vector(embedding_model.ndims()) = embedding_model.VectorField()  #type ignore

# Load jason
with open(PROCESSED_DATA_DIR / "recipes_clean.json") as f:
    recipes = json.load(f)

records = []

for recipe in recipes:
    records.append(
        {
            "id": recipe["id"],
            "title": recipe["title"],
            "ingredients": ", ".join(recipe["ingredients"]),
            "instructions": " ".join(recipe["instructions"]),
            "text": recipe["text"],
        }
    )

DB_DIR.mkdir(parents=True, exist_ok=True)

vector_db = lancedb.connect(DB_DIR)

table = vector_db.create_table(
        "recipes",
        schema=RecipeModel,
        data=records,
        mode="overwrite",
)

print(f"Create table with {table.count_rows()} recipes")
