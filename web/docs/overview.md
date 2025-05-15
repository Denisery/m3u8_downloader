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

The M3U8 Downloader Bot is a Telegram bot that allows you to download and process M3U8 video streams. It's designed to be easy to use, highly configurable, and secure.

## ✨ Features

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/star.svg" alt="Features" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### 📥 One-Click Downloads
Simply send an M3U8 URL to the bot and receive a complete video file in return.

### 🌐 Cross-Platform
Works seamlessly on Windows, Linux, and macOS.

### 🔒 Secure
Implements various security measures to protect against common attacks.

### 🔄 Scalable
Designed to handle multiple concurrent downloads efficiently.

### ⚙️ Configurable
Easily configurable through environment variables.

### 📊 Web Dashboard
Includes a web dashboard for monitoring system statistics.

### 📚 Comprehensive Documentation
Detailed documentation to help you get started.

## 🔄 How It Works

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gears.svg" alt="How It Works" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="20%">Step</th>
    <th width="80%">Description</th>
  </tr>
  <tr>
    <td align="center">1️⃣</td>
    <td><strong>URL Submission</strong>: Send an M3U8 URL to the bot.</td>
  </tr>
  <tr>
    <td align="center">2️⃣</td>
    <td><strong>Validation</strong>: The bot validates the URL to ensure it's a valid M3U8 URL.</td>
  </tr>
  <tr>
    <td align="center">3️⃣</td>
    <td><strong>Download</strong>: The bot downloads all segments from the M3U8 playlist.</td>
  </tr>
  <tr>
    <td align="center">4️⃣</td>
    <td><strong>Processing</strong>: The downloaded segments are processed and combined into a single video file.</td>
  </tr>
  <tr>
    <td align="center">5️⃣</td>
    <td><strong>Delivery</strong>: The processed video is sent back to you through Telegram.</td>
  </tr>
</table>

## 🚀 Getting Started

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/rocket.svg" alt="Getting Started" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Prerequisites

<table>
  <tr>
    <th width="33%">Python 3.8+</th>
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
</table>

### Installation

#### Step 1: Get the Code 📥

```bash
# Clone the repository
git clone https://github.com/Denisery/m3u8_downloader.git
cd m3u8_downloader
```

#### Step 2: Install Dependencies 📦

```bash
# Install all required packages
pip install -r requirements.txt
```

#### Step 3: Set Up Configuration ⚙️

Create a `.env` file with your configuration:

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
```

#### Step 4: Run the Bot ▶️

```bash
python main.py
# OR
python3 main.py
```

### 🐳 Docker Installation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Docker" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

You can also run the bot using Docker:

```bash
docker-compose up -d
```

> 💡 **Tip:** Using Docker provides a consistent environment and eliminates the need to install dependencies directly on your system.

## 🎮 Usage

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/play.svg" alt="Usage" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Using the Bot on Telegram

1. **Find your bot** on Telegram using the username you created
2. Send **/start** to initialize the bot
3. Send an **M3U8 URL** to the bot
4. Wait for the bot to **process** the video
5. Receive your **downloaded video**!

## 🤖 Bot Commands

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/robot.svg" alt="Bot Commands" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
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

## ⚙️ Configuration

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gear.svg" alt="Configuration" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot can be configured using environment variables. See the [Configuration Guide](/docs/configuration) for more details.

## 🔒 Security

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/shield-halved.svg" alt="Security" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot implements various security measures to protect against common attacks. See the [Security Guide](/docs/security) for more details.

## 💻 Cross-Platform Compatibility

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/desktop.svg" alt="Cross-Platform" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot is designed to work on Windows, Linux, and macOS. See the [Cross-Platform Guide](/docs/cross-platform) for more details.

## 🐳 Docker Guide

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Docker" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

The bot can be run using Docker. See the [Docker Guide](/docs/docker) for more details.

## 🤝 Contributing

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/code-pull-request.svg" alt="Contributing" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Contributions are welcome! Please see our [Contributing Guide](/docs/CONTRIBUTING) for more details.

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
