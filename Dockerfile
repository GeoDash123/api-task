# Build stage
FROM python:3.13-slim AS builder

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./

# Create virtual environment and install dependencies with uv
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python -e .

# Runtime stage
FROM python:3.13-slim

# Install runtime dependencies for psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')"
