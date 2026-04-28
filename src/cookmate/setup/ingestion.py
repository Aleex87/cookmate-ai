import json
from sentence_transformers import SentenceTransformer
import lancedb

from src.cookmate.utils.config import PROCESSED_DATA_DIR, DB_DIR


# load data
with open(PROCESSED_DATA_DIR / "recipes_clean.json", encoding="utf-8") as f:
    data = json.load(f)


# model (locale)
model = SentenceTransformer("all-MiniLM-L6-v2")


# prepare
texts = [r["text"] for r in data]
ids = [r["id"] for r in data]


# embeddings (batch)
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True
)


# create records
records = []
for i in range(len(data)):
    records.append({
        "id": ids[i],
        "text": texts[i],
        "vector": embeddings[i].tolist()
    })


# DB
DB_DIR.mkdir(parents=True, exist_ok=True)
db = lancedb.connect(DB_DIR)

table = db.create_table(
    "recipes",
    data=records,
    mode="overwrite"
)

print("Rows:", table.count_rows())