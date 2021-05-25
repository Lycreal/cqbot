FROM python:3.8-slim

RUN pip install --no-cache-dir poetry

COPY pyproject.toml /app/

RUN poetry install --no-dev

COPY . /app/

WORKDIR /app

CMD poetry run python3 bot.py
