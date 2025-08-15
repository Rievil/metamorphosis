# Use slim Python image
FROM python:3.12-slim

# Do not buffer stdout/stderr and avoid writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install build and Postgres client dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY backend ./backend

# Install Python dependencies
RUN pip install --no-cache-dir .

# Default environment variables
ENV PORT=8000 \
    DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres \
    SECRET_KEY=changeme

EXPOSE 8000

# Start the FastAPI server
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]
