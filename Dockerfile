FROM python:3.12-slim-bookworm

WORKDIR /app

# Postgres deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy the rest of your project files
COPY . .

# Create necessary
RUN uv sync --no-dev

# Set the entrypoint to run your main script using uv
ENTRYPOINT ["uv", "run", "--no-dev", "./main.py"]