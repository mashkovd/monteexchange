# Use an official Python slim runtime as a parent image
FROM python:3.12-slim

# Install Poetry
RUN pip install poetry

# Set the working directory in the container to /app
WORKDIR /app

# Add pyproject.toml and poetry.lock file into the container at /app
ADD pyproject.toml poetry.lock /app/

# Install any needed packages specified in pyproject.toml
RUN poetry install --no-dev --no-interaction --no-ansi

# Add the current directory contents into the container at /app
ADD . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["poetry", "run", "python", "main.py"]
