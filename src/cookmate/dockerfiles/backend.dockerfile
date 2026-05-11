FROM python:3.13-slim

WORKDIR /app


RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock .

COPY data/processed/recipes_clean.json ./data/processed/recipes_clean.json
COPY prompts ./prompts
COPY mlflow.db ./mlflow.db
COPY src ./src

RUN uv sync --package cookmate-backend --no-dev

RUN uv run --package cookmate-backend python src/cookmate/setup/ingestion.py

WORKDIR /app/src/cookmate/cookmate-backend/backend

CMD ["uv", "run", "--package", "cookmate-backend", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]