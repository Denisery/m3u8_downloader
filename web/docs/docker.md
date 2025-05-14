# Docker Guide

This guide explains how to run the M3U8 Downloader Bot using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/m3u8_downloader.git
   cd m3u8_downloader
   ```

2. Create a `.env` file with your configuration:
   ```
   # Telegram Bot settings
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   
   # Admin settings
   ADMIN_USER_IDS=123456789,987654321
   
   # Download settings
   DOWNLOAD_PATH=downloads
   MAX_DOWNLOAD_SIZE=500MB
   MAX_CONCURRENT_DOWNLOADS=3
   
   # Web server settings
   ENABLE_WEB_SERVER=true
   WEB_SERVER_HOST=0.0.0.0
   WEB_SERVER_PORT=8080
   
   # Web server authentication
   WEB_AUTH_ENABLED=true
   WEB_AUTH_USERNAME=admin
   WEB_AUTH_PASSWORD=your_secure_password
   ```

3. Run the bot using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the web dashboard at `http://localhost:8080`

## Docker Compose Configuration

The `docker-compose.yml` file is configured to run the bot in a container:

```yaml
version: '3'

services:
  m3u8_downloader_bot:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: m3u8_downloader_bot
    restart: unless-stopped
    volumes:
      - ./downloads:/app/downloads
      - ./.env:/app/.env
    ports:
      - "8080:8080"
```

## Dockerfile

The `Dockerfile` is optimized for minimal image size and security:

```dockerfile
# Use a specific Python version for better reproducibility
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN useradd -m botuser

# Switch to the final image
FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create a non-root user
RUN useradd -m botuser

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create downloads directory and set permissions
RUN mkdir -p /app/downloads && chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Command to run the application
CMD ["python", "main.py"]
```

## Environment Variables

The Docker setup supports all the environment variables defined in the `.env` file. See the [Configuration Guide](/docs/configuration) for more details.

## Volume Mapping

The Docker Compose configuration maps the following volumes:

- `./downloads:/app/downloads`: Maps the downloads directory to persist downloaded files
- `./.env:/app/.env`: Maps the environment file for configuration

## Port Mapping

The Docker Compose configuration maps the following ports:

- `8080:8080`: Maps the web server port to the host

## Security Considerations

The Docker setup includes several security features:

1. **Non-root user**: The bot runs as a non-root user (`botuser`) inside the container
2. **Minimal base image**: Uses the slim variant of the Python image to reduce attack surface
3. **Multi-stage build**: Uses a multi-stage build to reduce the final image size
4. **Explicit dependencies**: Installs only the required dependencies

## Updating the Bot

To update the bot to the latest version:

1. Pull the latest changes:
   ```bash
   git pull
   ```

2. Rebuild and restart the container:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

## Troubleshooting

### Container fails to start

Check the logs for errors:

```bash
docker-compose logs
```

### Web dashboard not accessible

Ensure the web server is enabled in your `.env` file:

```
ENABLE_WEB_SERVER=true
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8080
```

### FFmpeg not found

The Dockerfile installs FFmpeg, but if you're having issues, check the logs for any installation errors:

```bash
docker-compose logs | grep ffmpeg
```

## Advanced Configuration

### Custom Network

To use a custom Docker network:

```yaml
version: '3'

networks:
  bot_network:
    driver: bridge

services:
  m3u8_downloader_bot:
    # ... other configuration ...
    networks:
      - bot_network
```

### Resource Limits

To limit the container's resources:

```yaml
version: '3'

services:
  m3u8_downloader_bot:
    # ... other configuration ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### Healthcheck

To add a healthcheck:

```yaml
version: '3'

services:
  m3u8_downloader_bot:
    # ... other configuration ...
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```
