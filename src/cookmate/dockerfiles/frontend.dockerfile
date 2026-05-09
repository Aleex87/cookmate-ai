FROM python:3.13-slim

WORKDIR /app


RUN pip install --no-cache-dir uv

COPY  pyproject.toml .
COPY  uv.lock .

COPY src ./src

RUN uv sync --package coockmate-frontend --no-dev

WORKDIR /app/src/cookmate/cookmate-frontend/frontend



CMD [ "uv", "run", "streamlit", "run", "app.py", "--server.port", "8501", "--server.addfress", "0.0.0.0" ]