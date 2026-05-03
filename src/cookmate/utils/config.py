from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3] #get_project_root()

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DB_DIR = BASE_DIR / "db"

# specific file
RAW_DATA_FILE = RAW_DATA_DIR / "3A2M.csv"

# OpenRouter / LLM
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "meta-llama/llama-3.3-70b-instruct:free"