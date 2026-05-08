FROM python:3.13-slim

WORKDIR /app/cookmate

COPY cookmate-backend cookmate-backend

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir uv

WORKDIR /app/cookmate/cookmate-backend/backend

RUN uv sync --no-dev

CMD [ "uv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000" ]