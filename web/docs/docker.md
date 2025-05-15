<div align="center">

# 🐳 Docker Guide

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Docker" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>

### *Run your M3U8 Downloader Bot in a containerized environment*

</div>

---

This guide explains how to run the M3U8 Downloader Bot using Docker.

## 📋 Prerequisites

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/clipboard-check.svg" alt="Prerequisites" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="50%">Docker</th>
    <th width="50%">Docker Compose</th>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" width="50" height="50" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/layer-group.svg" width="50" height="50" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"></td>
  </tr>
  <tr>
    <td>Docker installed on your system</td>
    <td>Docker Compose installed on your system</td>
  </tr>
</table>

## 🚀 Quick Start

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/rocket.svg" alt="Quick Start" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Step 1: Get the Code 📥

<div align="center">

```bash
git clone https://github.com/Denisery/m3u8_downloader.git
cd m3u8_downloader
```

</div>

### Step 2: Configure the Bot ⚙️

Create a `.env` file with your configuration:

<div align="center">

```ini
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

</div>

### Step 3: Launch with Docker Compose 🐳

<div align="center">

```bash
docker-compose up -d
```

</div>

### Step 4: Access the Dashboard 🌐

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/browser.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

**[http://localhost:8080](http://localhost:8080)**
</div>

> 💡 **Tip:** The `-d` flag runs the container in detached mode (in the background). To see the logs, use `docker-compose logs -f`.

## 📄 Docker Compose Configuration

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/file-code.svg" alt="Docker Compose" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The `docker-compose.yml` file is configured to run the bot in a container:

<div align="center">

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

</div>

## 🔨 Dockerfile

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Dockerfile" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

The `Dockerfile` is optimized for minimal image size and security:

<div align="center">

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
CMD ["python3", "main.py"]
```

</div>

> 💡 **Note:** This Dockerfile uses a multi-stage build to reduce the final image size and runs the application as a non-root user for improved security.

## ⚙️ Environment Variables

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gear.svg" alt="Environment Variables" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The Docker setup supports all the environment variables defined in the `.env` file. See the [Configuration Guide](/docs/configuration) for more details.

## 💾 Volume Mapping

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/hard-drive.svg" alt="Volume Mapping" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th>Host Path</th>
    <th>Container Path</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td><code>./downloads</code></td>
    <td><code>/app/downloads</code></td>
    <td>Maps the downloads directory to persist downloaded files</td>
  </tr>
  <tr>
    <td><code>./.env</code></td>
    <td><code>/app/.env</code></td>
    <td>Maps the environment file for configuration</td>
  </tr>
</table>

## 🔌 Port Mapping

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/network-wired.svg" alt="Port Mapping" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th>Host Port</th>
    <th>Container Port</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td><code>8080</code></td>
    <td><code>8080</code></td>
    <td>Maps the web server port to the host</td>
  </tr>
</table>

## 🔒 Security Considerations

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/shield-halved.svg" alt="Security" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="30%">Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>👤 Non-root user</td>
    <td>The bot runs as a non-root user (<code>botuser</code>) inside the container</td>
  </tr>
  <tr>
    <td>🔍 Minimal base image</td>
    <td>Uses the slim variant of the Python image to reduce attack surface</td>
  </tr>
  <tr>
    <td>🏗️ Multi-stage build</td>
    <td>Uses a multi-stage build to reduce the final image size</td>
  </tr>
  <tr>
    <td>📦 Explicit dependencies</td>
    <td>Installs only the required dependencies</td>
  </tr>
</table>

## 🔄 Updating the Bot

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/arrow-rotate-right.svg" alt="Updating" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

To update the bot to the latest version:

### Step 1: Pull the Latest Changes 📥

<div align="center">

```bash
git pull
```

</div>

### Step 2: Rebuild and Restart the Container 🔄

<div align="center">

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

</div>

## 🔍 Troubleshooting

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/screwdriver-wrench.svg" alt="Troubleshooting" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<details open>
<summary><b>Container fails to start</b></summary>

Check the logs for errors:

<div align="center">

```bash
docker-compose logs
```

</div>
</details>

<details open>
<summary><b>Web dashboard not accessible</b></summary>

Ensure the web server is enabled in your `.env` file:

<div align="center">

```ini
ENABLE_WEB_SERVER=true
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8080
```

</div>
</details>

<details open>
<summary><b>FFmpeg not found</b></summary>

The Dockerfile installs FFmpeg, but if you're having issues, check the logs for any installation errors:

<div align="center">

```bash
docker-compose logs | grep ffmpeg
```

</div>
</details>

## 🛠️ Advanced Configuration

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/sliders.svg" alt="Advanced Configuration" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<details open>
<summary><b>Custom Network</b></summary>

To use a custom Docker network:

<div align="center">

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

</div>
</details>

<details open>
<summary><b>Resource Limits</b></summary>

To limit the container's resources:

<div align="center">

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

</div>
</details>

<details open>
<summary><b>Healthcheck</b></summary>

To add a healthcheck:

<div align="center">

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

</div>
</details>

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
