FROM python:3.8-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry install --no-interaction --no-cache

