FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# Попробуйте сначала без системных зависимостей
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-root --no-interaction

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]