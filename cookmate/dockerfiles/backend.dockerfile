FROM python:3.13-slim

WORKDIR /app


RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock .

COPY data/processed/recipes_clean.json ./data/processed/recipes_clean.json
COPY prompts ./prompts
COPY mlflow.db ./mlflow.db
COPY cookmate ./cookmate
COPY cookmate/backend/pyproject.toml ./cookmate/backend/pyproject.toml

WORKDIR /app/cookmate/backend

RUN uv sync --no-dev 

WORKDIR /app

RUN uv run python -u cookmate/setup/ingestion.py

WORKDIR /app/cookmate/backend

CMD ["uv", "run", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]