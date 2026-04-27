from pathlib import Path

def get_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists() and (parent / "src").exists():
            return parent
    raise RuntimeError("Project root not found")


BASE_DIR = get_project_root()

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DB_DIR = BASE_DIR / "db"

# specific file
RAW_DATA_FILE = RAW_DATA_DIR / "3A2M.csv"