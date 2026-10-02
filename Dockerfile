# Stage 1 - Builder
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

# Stage 2 - Production Runtime
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app
COPY --from=builder /app /app

EXPOSE 8000
CMD ["python", "-m", "enterprise_data_agent.server"]