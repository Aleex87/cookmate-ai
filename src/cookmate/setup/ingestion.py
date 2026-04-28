from src.cookmate.utils.config import PROCESSED_DATA_DIR, DB_DIR
from sentence_transformers import SentenceTransformer
import json 
import lancedb

# Load jason
with open(PROCESSED_DATA_DIR / "recipes_clean.json") as f:
    data = json.load(f)

print(len(data))
print(data[0])
