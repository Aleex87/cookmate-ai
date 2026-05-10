FROM python:3.13-slim

WORKDIR /app


RUN pip install --no-cache-dir uv

COPY  pyproject.toml .
COPY  uv.lock .

COPY src ./src

RUN uv sync --package cookmate-backend --no-dev

WORKDIR /app/src/cookmate/cookmate-backend/backend


CMD [ "uv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000" ]