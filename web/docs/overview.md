# M3U8 Downloader Bot

The M3U8 Downloader Bot is a Telegram bot that allows you to download and process M3U8 video streams. It's designed to be easy to use, highly configurable, and secure.

## Features

- **Easy to Use**: Simply send an M3U8 URL to the bot, and it will download and process the video for you.
- **Cross-Platform**: Works on Windows, Linux, and macOS.
- **Secure**: Implements various security measures to protect against common attacks.
- **Scalable**: Designed to handle multiple concurrent downloads efficiently.
- **Configurable**: Easily configurable through environment variables.
- **Web Dashboard**: Includes a web dashboard for monitoring system statistics.
- **Comprehensive Documentation**: Detailed documentation to help you get started.

## How It Works

1. **URL Submission**: Send an M3U8 URL to the bot.
2. **Validation**: The bot validates the URL to ensure it's a valid M3U8 URL.
3. **Download**: The bot downloads all segments from the M3U8 playlist.
4. **Processing**: The downloaded segments are processed and combined into a single video file.
5. **Delivery**: The processed video is sent back to you through Telegram.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- FFmpeg
- Telegram Bot Token

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/m3u8_downloader.git
   cd m3u8_downloader
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
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
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

### Docker Installation

You can also run the bot using Docker:

```bash
docker-compose up -d
```

## Usage

1. Start a chat with your bot on Telegram.
2. Send an M3U8 URL to the bot.
3. Wait for the bot to download and process the video.
4. Receive the processed video file.

## Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Get help information
- `/cancel` - Cancel the current download
- `/stats` - Get system statistics (admin only)

## Configuration

The bot can be configured using environment variables. See the [Configuration Guide](/docs/configuration) for more details.

## Security

The bot implements various security measures to protect against common attacks. See the [Security Guide](/docs/security) for more details.

## Cross-Platform Compatibility

The bot is designed to work on Windows, Linux, and macOS. See the [Cross-Platform Guide](/docs/cross-platform) for more details.

## Docker Guide

The bot can be run using Docker. See the [Docker Guide](/docs/docker) for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
