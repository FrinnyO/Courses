FROM python:3.12-slim

WORKDIR /code

RUN apt-get update \
    && apt-get install -y gcc libpq-dev libjpeg-dev zlib1g-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

ENV PYTHONPATH=/code
ENV PYTHONUNBUFFERED=1

EXPOSE 8000