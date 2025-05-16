FROM python:3.12-slim

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Add dependency files
COPY pyproject.toml uv.lock /app/

# Install dependencies using uv
RUN uv sync

# Copy the rest of the application code
COPY . /app

# Expose port
EXPOSE 80

# Run the application
CMD ["uv", "run", "main.py"]