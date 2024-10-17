# Stage 1: Build Stage
FROM python:3.12-slim AS build

# Install uv in the build stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies for building
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Copy dependency files
COPY pyproject.toml uv.lock .

# Install dependencies with uv sync inside the virtual environment
RUN uv sync --frozen --no-cache

# set the working directory
WORKDIR /code

ENV PATH="/.venv/bin:${PATH}"

# Run the application.
CMD ["fastapi", "dev", "app/main.py", "--port", "80", "--host", "0.0.0.0"]