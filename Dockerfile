# =============================================================================
# M3U8 Downloader Bot - Multi-stage Dockerfile
# =============================================================================
# This Dockerfile creates an optimized container for the M3U8 Downloader Bot
# with cross-platform compatibility considerations.
#
# Features:
# - Multi-stage build to minimize final image size
# - Proper handling of platform-specific dependencies
# - FFmpeg pre-installed for video processing
# - Efficient layer caching for faster builds
# - Cross-platform compatibility considerations
# =============================================================================

# =============================================================================
# STAGE 1: Build dependencies
# =============================================================================
FROM python:3.10-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
# Note: We're installing all dependencies regardless of platform
# since we're building in a Linux container
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: Final image
# =============================================================================
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install FFmpeg and other runtime dependencies
# We use --no-install-recommends to keep the image size small
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set environment variables
# These can be overridden at runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOWNLOAD_PATH=/app/downloads \
    MAX_DOWNLOAD_SIZE=524288000 \
    CHUNK_SIZE=1048576 \
    MAX_CONCURRENT_DOWNLOADS=5 \
    DOWNLOAD_TIMEOUT=3600 \
    ENABLE_WEB_SERVER=true \
    WEB_SERVER_HOST=0.0.0.0 \
    WEB_SERVER_PORT=8080

# Expose web server port
EXPOSE 8080

# Create download directory
RUN mkdir -p /app/downloads && \
    chmod 777 /app/downloads

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Command to run the application
CMD ["python3", "main.py"]

# =============================================================================
# USAGE INSTRUCTIONS
# =============================================================================
#
# Build the Docker image:
#   docker build -t m3u8-downloader .
#
# Run the container:
#   docker run -d --name m3u8-bot \
#     -e API_ID=your_api_id \
#     -e API_HASH=your_api_hash \
#     -e BOT_TOKEN=your_bot_token \
#     -e ADMIN_USER_IDS=your_user_id \
#     -v $(pwd)/downloads:/app/downloads \
#     m3u8-downloader
#
# Environment Variables:
#   - API_ID: Your Telegram API ID (required)
#   - API_HASH: Your Telegram API Hash (required)
#   - BOT_TOKEN: Your Telegram Bot Token (required)
#   - ADMIN_USER_IDS: Comma-separated list of admin user IDs (required)
#   - DOWNLOAD_PATH: Path to store downloads (default: /app/downloads)
#   - MAX_DOWNLOAD_SIZE: Maximum download size in bytes (default: 500MB)
#   - MAX_CONCURRENT_DOWNLOADS: Maximum concurrent downloads (default: 5)
#   - DOWNLOAD_TIMEOUT: Download timeout in seconds (default: 3600)
#   - ENABLE_WEB_SERVER: Enable/disable web server (default: true)
#   - WEB_SERVER_PORT: Web server port (default: 8080)
#
# Persistent Storage:
#   The container uses a volume mount for the downloads directory to persist
#   downloaded videos between container restarts.
#
# Health Check:
#   You can add a health check to monitor the container:
#   docker run ... --health-cmd "python -c 'import sys; sys.exit(0)'" \
#     --health-interval=30s --health-timeout=10s --health-retries=3 \
#     m3u8-downloader
# =============================================================================
