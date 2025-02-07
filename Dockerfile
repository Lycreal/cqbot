FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --frozen
