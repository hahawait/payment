FROM python:3.12-slim

WORKDIR /application

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv
RUN uv sync --frozen

COPY src .

COPY alembic.ini .

# CMD uv run alembic revision --autogenerate && uv run alembic upgrade head && uv run uvicorn app.api.main:create_app --host 0.0.0.0 --port 8000
