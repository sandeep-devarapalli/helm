FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_NO_DEV=1

WORKDIR /app
RUN pip install --no-cache-dir uv==0.11.28

COPY pyproject.toml uv.lock README.md ./
COPY services ./services
COPY alembic.ini ./alembic.ini
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONPATH="/app/services/api:/app/services/worker"

CMD ["uvicorn", "helm.main:app", "--host", "0.0.0.0", "--port", "8000"]
