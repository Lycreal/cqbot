FROM python:3.8-slim

WORKDIR /app

COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN pip install --no-cache-dir poetry &&\
    poetry install --no-cache
