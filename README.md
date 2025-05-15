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
  - [✨ Key Features](#-key-features)
  - [📋 Prerequisites](#-prerequisites)
  - [🚀 Quick Installation](#-quick-installation)
  - [📚 Documentation](#-documentation)
  - [📜 License](#-license)
  - [🤝 Contributing](#-contributing)

---

## 🌟 Introduction

The M3U8 Downloader Bot is a Telegram bot that allows you to download and convert streaming videos from M3U8 URLs into standard video files. Perfect for saving webinars, tutorials, or any streaming content for offline viewing!

## ✨ Key Features

- **📥 One-Click Downloads**: Simply send an M3U8 URL to the bot and receive a complete video file
- **🎞️ Quality Selection**: Choose from multiple quality options when available in master playlists
- **📊 Live Progress Updates**: Watch as your download progresses with real-time status updates
- **🔄 Multi-User Support**: Handle multiple download requests from different users simultaneously
- **🎬 Advanced Processing**: Automatic video processing with FFmpeg for optimal quality
- **📊 System Monitoring**: Web-based dashboard showing system resources and bot statistics
- **💻 Cross-Platform**: Works seamlessly on Windows, Linux, and macOS

## 📋 Prerequisites

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
</table>

## 🚀 Quick Installation

```bash
# Clone the repository
git clone https://github.com/Denisery/m3u8_downloader.git
cd m3u8_downloader

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure the bot
cp .env.example .env
# Edit .env with your Telegram API credentials

# Run the bot
python main.py
```

For Docker users:
```bash
docker-compose up -d
```

## 📚 Documentation

Detailed documentation is available in the web/docs directory:

- [📖 Overview](/web/docs/overview.md) - Introduction to the M3U8 Downloader Bot
- [🚀 Installation Guide](/web/docs/installation.md) - Complete installation instructions for all platforms
- [⚙️ Configuration Guide](/web/docs/configuration.md) - All configuration options and environment variables
- [🎮 Usage Guide](/web/docs/usage.md) - Detailed usage instructions with examples
- [✨ Features](/web/docs/features.md) - In-depth explanation of all features
- [🔍 Troubleshooting](/web/docs/troubleshooting.md) - Solutions for common issues
- [🤝 Contributing](/web/docs/contributing.md) - Guidelines for contributing to the project
- [🔌 API Documentation](/web/docs/api.md) - API documentation for programmatic integration
- [🔒 Security Guide](/web/docs/security.md) - Security features and best practices
- [🐳 Docker Guide](/web/docs/docker.md) - Running the bot with Docker
- [💻 Cross-Platform Guide](/web/docs/cross-platform.md) - Cross-platform compatibility information
- [🔄 Scalability Guide](/web/docs/scalability.md) - Scalability features and configuration

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](/web/docs/contributing.md) for more details.

---

<div align="center">

⚠️ **DISCLAIMER**: This tool is provided for educational and personal use only. Always respect copyright laws and terms of service when downloading content.

<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
