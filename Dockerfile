FROM python:3.12-slim-bookworm

WORKDIR /app

# Install uv
RUN pip install uv

# Copy the rest of your project files
COPY . .

# Create necessary
RUN uv sync

# Set the entrypoint to run your main script using uv
ENTRYPOINT ["uv", "run", "./main.py"]