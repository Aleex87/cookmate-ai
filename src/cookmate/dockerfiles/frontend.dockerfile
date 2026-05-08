FROM python:3.13-slim

WORKDIR /app

COPY cookmate-frontend frontend

RUN pip install --no-cache-dir uv

WORKDIR /app/cookmate

RUN uv sync --no-dev

CMD [ "uv", "run", "steamlit", "run", "app.py", "--server.port", "8501", "--server.adress", "0.0.0.0" ]