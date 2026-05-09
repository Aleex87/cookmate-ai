FROM python:3.13-slim

WORKDIR /app


RUN pip install --no-cache-dir uv

COPY  pyproject.toml .
COPY  uv.lock .

COPY src ./src


WORKDIR /app/src/cookmate/cookmate-backend/backend

RUN uv sync --package coockmate-backend --no-dev

CMD [ "uv", "run", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000" ]