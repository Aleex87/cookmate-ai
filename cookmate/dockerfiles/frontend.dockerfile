FROM python:3.13-slim

WORKDIR /app


RUN pip install --no-cache-dir uv

COPY  pyproject.toml .
COPY  uv.lock .

COPY cookmate ./cookmate
COPY cookmate/frontend/pyproject.toml ./cookmate/frontend/pyproject.toml

WORKDIR /app/cookmate/frontend

RUN uv sync --no-dev

WORKDIR /app/cookmate/frontend/src/frontend



CMD [ "uv", "run", "streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0" ]