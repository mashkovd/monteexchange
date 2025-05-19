FROM python:3.12-slim

# Install dependencies: curl for healthchecks
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files first (for better layer caching)
COPY pyproject.toml uv.lock /app/

# Install dependencies using uv
RUN uv sync

# Copy the application code
COPY . /app

# Expose port for health check
EXPOSE 8080

# Environment variables
ENV PYTHONUNBUFFERED=1

# Healthcheck using the health endpoint from main.py
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

# Run the application
CMD ["python", "-m", "main"]
