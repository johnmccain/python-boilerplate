FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Install dependencies only (cache the layer for faster builds)
RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main && \
    rm -rf /root/.cache/poetry

COPY server ./server
COPY scripts ./scripts
COPY python_boilerplate ./python_boilerplate
RUN chmod +x ./scripts/entrypoint.sh

RUN poetry install --no-interaction --no-ansi --only main

EXPOSE 8080

CMD ["./scripts/entrypoint.sh"]
