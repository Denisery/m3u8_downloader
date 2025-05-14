<div align="center">

# 📹 M3U8 Downloader Bot

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/video.svg" alt="Video Icon" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Transform streaming videos into downloadable files with just one click*

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Python](https://img.shields.io/badge/Made_With-Python-1F425F?style=for-the-badge&logo=python&logoColor=white&color=306998)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/Powered_By-FFmpeg-4285F4?style=for-the-badge&logo=ffmpeg&logoColor=white&color=007808)](https://ffmpeg.org/)

<img src="https://img.shields.io/badge/Easy_Setup-89CFF0" alt="Easy Setup"/> <img src="https://img.shields.io/badge/Beginner_Friendly-A7C7E7" alt="Beginner Friendly"/> <img src="https://img.shields.io/badge/Video_Processing-6495ED" alt="Video Processing"/> <img src="https://img.shields.io/badge/Telegram_Integration-0096FF" alt="Telegram Integration"/> <img src="https://img.shields.io/badge/Streaming_Media-318CE7" alt="Streaming Media"/>

</div>

---

## 📑 Table of Contents

- [📹 M3U8 Downloader Bot](#-m3u8-downloader-bot)
  - [📑 Table of Contents](#-table-of-contents)
  - [🌟 Introduction](#-introduction)
    - [What is an M3U8 File?](#what-is-an-m3u8-file)
    - [What This Bot Does](#what-this-bot-does)
  - [✨ Features](#-features)
  - [📋 Requirements](#-requirements)
  - [🚀 Installation Guide](#-installation-guide)
  - [🐳 Docker Deployment](#-docker-deployment)
  - [⚙️ Configuration](#️-configuration)
  - [🎮 How to Use](#-how-to-use)
  - [🤖 Bot Commands](#-bot-commands)
  - [📊 Web Dashboard](#-web-dashboard)
  - [📁 Project Structure](#-project-structure)
  - [🔍 Troubleshooting](#-troubleshooting)
  - [📜 License](#-license)
  - [🙏 Acknowledgements](#-acknowledgements)

---

## 🌟 Introduction

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/folder-open.svg" alt="Video Folder" width="100" height="100" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### What is an M3U8 File?

**M3U8** files are playlist files used for streaming media content. When you watch videos online, many streaming services break the video into small chunks and use M3U8 files to tell your player how to access these chunks in the right order.

> 💡 **Think of it like this:** Instead of downloading one large video file, streaming services send you a "recipe" (the M3U8 file) that tells your player how to collect and play all the small video pieces.

### What This Bot Does

This Telegram bot allows you to:
1. **Download** complete videos from M3U8 streaming URLs
2. **Convert** them into standard video files
3. **Send** them directly to you via Telegram

Perfect for saving webinars, tutorials, or any streaming content for offline viewing!

---

## ✨ Features

### 📥 One-Click Downloads
Simply send an M3U8 URL to the bot and receive a complete video file in return.

### 🎞️ Quality Selection
Choose from multiple quality options when available in master playlists.

### 📊 Live Progress Updates
Watch as your download progresses with real-time status updates.

### 🔄 Multi-User Support
Handle multiple download requests from different users simultaneously.

### 🎬 Advanced Processing
Automatic video processing with FFmpeg for optimal quality and compatibility.

### 🖼️ Thumbnail Generation
Automatic creation of video thumbnails for easy identification.

### 📊 System Monitoring Dashboard
Web-based dashboard showing system resources, bot statistics, and performance metrics.

### 👮 Admin Controls
Special commands and web interface for monitoring and managing the bot's operations.

### 🛠️ Modular Architecture
Clean, modular code design makes it easy to extend and customize.

---

## 📋 Requirements

<table>
  <tr>
    <th width="33%">Python 3.7+</th>
    <th width="33%">FFmpeg</th>
    <th width="33%">Telegram API</th>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/python.svg" width="50" height="50" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/film.svg" width="50" height="50" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/telegram.svg" width="50" height="50" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"></td>
  </tr>
  <tr>
    <td>The programming language that powers the bot</td>
    <td>Required for video processing and conversion</td>
    <td>Credentials for bot communication (API ID, Hash, Token)</td>
  </tr>
  <tr>
    <td><a href="https://www.python.org/downloads/">Download Python</a></td>
    <td><a href="https://ffmpeg.org/download.html">Download FFmpeg</a></td>
    <td><a href="https://my.telegram.org/apps">Get API Credentials</a></td>
  </tr>
</table>

> 💡 **New to Telegram Bots?** Follow our [step-by-step guide](#getting-telegram-api-credentials) to get your API credentials.

---

## 🚀 Installation Guide

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/download.svg" alt="Download Folder" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Step 1: Get the Code 📥

```bash
# Clone the repository
git clone https://github.com/yourusername/m3u8_downloader.git

# Navigate to the project folder
cd m3u8_downloader
```

### Step 2: Create a Virtual Environment 🔮

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### Step 3: Install Dependencies 📦

```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Set Up Configuration ⚙️

**Windows:**
```bash
# Copy the example environment file
copy .env.example .env

# Edit the .env file with your details
notepad .env
```

**macOS/Linux:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your details
nano .env
```

---

## 🐳 Docker Deployment

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Docker" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

Docker provides a consistent, cross-platform way to run the M3U8 Downloader Bot without worrying about dependencies or platform-specific issues.

### Benefits of Using Docker

- **Cross-Platform Compatibility**: Works identically on Windows, macOS, and Linux
- **No Local Dependencies**: No need to install Python, FFmpeg, or other dependencies
- **Simplified Setup**: Get up and running with just a few commands
- **Isolated Environment**: Keep the bot and its dependencies contained
- **Easy Updates**: Simple process to update to newer versions

### Quick Start with Docker

```bash
# Build the Docker image
docker build -t m3u8-downloader .

# Run the container
docker run -d --name m3u8-bot \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e BOT_TOKEN=your_bot_token \
  -e ADMIN_USER_IDS=your_user_id \
  -v $(pwd)/downloads:/app/downloads \
  m3u8-downloader
```

### Using Docker Compose (Recommended)

```bash
# Create a .env file with your credentials first, then:
docker-compose up -d
```

> 💡 **Detailed Instructions**: For complete Docker setup and usage instructions, see the Docker Guide in the web documentation at `/docs/docker`.

---

## ⚙️ Configuration

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gear.svg" alt="Settings" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Edit your `.env` file with the following settings:

```ini
# Telegram API credentials
# Get these from https://my.telegram.org/apps
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Download settings
DOWNLOAD_PATH=downloads
MAX_DOWNLOAD_SIZE=524288000  # 500 MB
CHUNK_SIZE=1048576  # 1 MB

# Bot settings
ADMIN_USER_IDS=123456789,987654321  # Your Telegram user ID(s)
MAX_CONCURRENT_DOWNLOADS=5
DOWNLOAD_TIMEOUT=3600  # 1 hour

# Web server settings
ENABLE_WEB_SERVER=true  # Set to false to disable the web server
WEB_SERVER_HOST=0.0.0.0  # Listen on all interfaces
WEB_SERVER_PORT=8080  # Web server port
```

### Getting Telegram API Credentials

<details>
<summary>Click to expand step-by-step instructions</summary>

1. Visit [my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Fill in the form with any name and title
4. Select "Other" as app platform
5. Click "Create Application"
6. Note your **API ID** and **API Hash**
7. To create a bot and get a **Bot Token**:
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` and follow the instructions
   - Copy the token provided

</details>

> 💡 **Tip:** To find your Telegram user ID for the ADMIN_USER_IDS setting, message [@userinfobot](https://t.me/userinfobot) on Telegram.

---

## 🎮 How to Use

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/play.svg" alt="Play" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Starting the Bot

**Standard Method:**
```bash
# Run the bot
python main.py
```

**Using Docker:**
```bash
# Run with Docker Compose
docker-compose up -d
```

You should see a message confirming the bot is running.

### Using the Bot on Telegram

1. **Find your bot** on Telegram using the username you created
2. Send **/start** to initialize the bot
3. Send an **M3U8 URL** to the bot
4. Wait for the bot to **process** the video
5. Receive your **downloaded video**!

---

## 🤖 Bot Commands

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/robot.svg" alt="Robot" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/start</code></td>
    <td>Initialize the bot and see welcome message</td>
  </tr>
  <tr>
    <td><code>/help</code></td>
    <td>Display available commands and instructions</td>
  </tr>
  <tr>
    <td><code>/status</code></td>
    <td>Check the progress of your current download</td>
  </tr>
  <tr>
    <td><code>/cancel</code></td>
    <td>Cancel your active download</td>
  </tr>
  <tr>
    <td><code>/stats</code></td>
    <td>View detailed system information and bot statistics (admin only)</td>
  </tr>
</table>

### Enhanced Admin Statistics Command

The `/stats` command provides administrators with comprehensive information about the system and bot performance:

- **System Information**: Operating system details, Python version, and FFmpeg version
- **Resource Usage**: Real-time CPU, memory, and disk usage statistics
- **Bot Performance**: Uptime, active downloads, and total completed downloads
- **Active Downloads**: List of current downloads with progress information

This command is only accessible to users whose Telegram IDs are listed in the `ADMIN_USER_IDS` configuration setting.

## 📊 Web Dashboard & Documentation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gauge-high.svg" alt="Dashboard" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The M3U8 Downloader Bot includes a web-based dashboard that provides real-time monitoring of system resources and bot statistics, as well as comprehensive documentation.

### Features

- **System Information**: OS details, Python version, FFmpeg version
- **Resource Usage**: Real-time CPU, memory, and disk usage with visual indicators
- **Bot Statistics**: Uptime, active downloads, completed downloads
- **Auto-Refresh**: Dashboard automatically refreshes every 30 seconds
- **Comprehensive Documentation**: Detailed guides on setup, configuration, security, and more
- **Mobile-Friendly Design**: Responsive layout works on all devices
- **Dark Mode Support**: Automatic theme switching based on system preferences

### Accessing the Dashboard & Documentation

The dashboard is available at `http://your-server-ip:8080` by default. You can configure the host and port in your `.env` file.

The documentation is accessible at `http://your-server-ip:8080/docs` and includes:

- **Overview**: Introduction to the M3U8 Downloader Bot
- **Security Guide**: Security features and best practices
- **Docker Guide**: Running the bot with Docker
- **Cross-Platform Guide**: Cross-platform compatibility information
- **Configuration Guide**: Configuration options and settings

### Configuration

You can customize the web server settings in your `.env` file:

```ini
# Web server settings
ENABLE_WEB_SERVER=true  # Set to false to disable the web server
WEB_SERVER_HOST=0.0.0.0  # Listen on all interfaces
WEB_SERVER_PORT=8080  # Web server port
```

### Security Considerations

- The web dashboard includes built-in authentication for security
- Configure authentication in your `.env` file:
  ```ini
  # Web server authentication
  WEB_AUTH_ENABLED=true
  WEB_AUTH_USERNAME=admin
  WEB_AUTH_PASSWORD=your_secure_password
  ```
- For additional security, consider using a reverse proxy with HTTPS
- For Docker deployments, you can limit access by not publishing the port to the host

For more security information, see the Security Guide in the web documentation at `/docs/security`.

## 🔍 Troubleshooting

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bug.svg" alt="Debug" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<details>
<summary><b>Bot not responding?</b></summary>
<ul>
  <li>Verify your API credentials in the <code>.env</code> file</li>
  <li>Check if the bot is running in your terminal</li>
  <li>Make sure you've started a chat with your bot on Telegram</li>
</ul>
</details>

<details>
<summary><b>Download fails?</b></summary>
<ul>
  <li>Ensure the M3U8 URL is valid and publicly accessible</li>
  <li>Check if the URL requires authentication or is geo-restricted</li>
  <li>Verify that the file size doesn't exceed your <code>MAX_DOWNLOAD_SIZE</code> setting</li>
</ul>
</details>

<details>
<summary><b>FFmpeg errors?</b></summary>
<ul>
  <li>Confirm FFmpeg is properly installed on your system</li>
  <li>Make sure FFmpeg is in your system PATH</li>
  <li>Try running <code>ffmpeg -version</code> in your terminal to verify the installation</li>
  <li>Consider using Docker to avoid FFmpeg installation issues (see <a href="#-docker-deployment">Docker Deployment</a>)</li>
</ul>
</details>

<details>
<summary><b>Video not playing?</b></summary>
<ul>
  <li>Some M3U8 streams use encryption or DRM that can't be downloaded</li>
  <li>Try a different media player (VLC is recommended)</li>
  <li>Check if the original stream is accessible from your location</li>
</ul>
</details>

---

## 📜 License

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/regular/copyright.svg" alt="License" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgements

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/award.svg" alt="Credits" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### [Pyrogram](https://docs.pyrogram.org/)
Elegant Telegram MTProto API framework

### [m3u8](https://github.com/globocom/m3u8)
Python m3u8 parser and toolkit

### [FFmpeg](https://ffmpeg.org/)
Complete multimedia solution

---

<div align="center">
  <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/triangle-exclamation.svg" alt="Warning" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

## ⚠️ Disclaimer and Legal Warning

<div align="center">

```
⚠️ IMPORTANT: USE THIS BOT AT YOUR OWN RISK ⚠️
```

</div>

> **This bot is provided for educational and personal use only owner are:**

<table>
  <tr>
    <td align="center" width="80px">⚠️</td>
    <td><strong>NOT</strong> responsible for any misuse or illegal activities conducted using this tool</td>
  </tr>
  <tr>
    <td align="center">⛔</td>
    <td><strong>DO NOT</strong> endorse downloading copyrighted content without proper authorization</td>
  </tr>
  <tr>
    <td align="center">⚖️</td>
    <td>Cannot be held liable for any legal consequences resulting from improper use</td>
  </tr>
</table>

### 📜 Copyright and Fair Use Guidelines

<details open>
<summary><b>Important Guidelines</b></summary>

* ✅ **Always** obtain permission from content creators before downloading their videos
* 🔒 **Respect** copyright laws and intellectual property rights
* 📱 **Only** download videos with explicit permission from the content owners
* 📄 Be aware that downloading certain content may violate the Terms of Service of the respective platforms

</details>

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
