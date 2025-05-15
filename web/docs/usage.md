<div align="center">

# 🎮 Usage Guide

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/play.svg" alt="Usage" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Learn how to use the M3U8 Downloader Bot effectively*

</div>

---

This guide provides detailed instructions on how to use the M3U8 Downloader Bot to download and process M3U8 video streams.

## 🚀 Starting the Bot

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/rocket-launch.svg" alt="Starting" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Standard Method

```bash
# Activate your virtual environment first
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run the bot
python main.py
# OR
python3 main.py
```

### Using Docker

```bash
# Run with Docker Compose
docker-compose up -d
```

You should see a message confirming the bot is running.

## 🤖 Interacting with the Bot

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/robot.svg" alt="Bot" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Basic Workflow

<table>
  <tr>
    <th width="20%">Step</th>
    <th width="80%">Description</th>
  </tr>
  <tr>
    <td align="center">1️⃣</td>
    <td><strong>Find your bot</strong> on Telegram using the username you created with BotFather</td>
  </tr>
  <tr>
    <td align="center">2️⃣</td>
    <td>Send <code>/start</code> to initialize the bot</td>
  </tr>
  <tr>
    <td align="center">3️⃣</td>
    <td>Send an <strong>M3U8 URL</strong> to the bot</td>
  </tr>
  <tr>
    <td align="center">4️⃣</td>
    <td>Wait for the bot to <strong>process</strong> the video</td>
  </tr>
  <tr>
    <td align="center">5️⃣</td>
    <td>Receive your <strong>downloaded video</strong>!</td>
  </tr>
</table>

### Available Commands

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

## 📥 Downloading Videos

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/download.svg" alt="Downloading" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Sending M3U8 URLs

To download a video, simply send the M3U8 URL to the bot. The URL should look something like this:
```
https://example.com/path/to/video.m3u8
```

### Quality Selection

If the M3U8 URL is a master playlist with multiple quality options, the bot will ask you to select a quality:

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/list.svg" alt="Quality Selection" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="20%">Option</th>
    <th width="80%">Description</th>
  </tr>
  <tr>
    <td align="center">🔍</td>
    <td><strong>Auto</strong>: The bot will automatically select the highest quality</td>
  </tr>
  <tr>
    <td align="center">🎬</td>
    <td><strong>Manual</strong>: You can select from available quality options</td>
  </tr>
</table>

### Download Progress

The bot will show you the download progress in real-time:

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/spinner.svg" alt="Progress" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="20%">Status</th>
    <th width="80%">Description</th>
  </tr>
  <tr>
    <td align="center">📋</td>
    <td><strong>Analyzing</strong>: The bot is analyzing the M3U8 file</td>
  </tr>
  <tr>
    <td align="center">📥</td>
    <td><strong>Downloading</strong>: The bot is downloading the video segments</td>
  </tr>
  <tr>
    <td align="center">🔄</td>
    <td><strong>Processing</strong>: The bot is processing the downloaded segments</td>
  </tr>
  <tr>
    <td align="center">📤</td>
    <td><strong>Uploading</strong>: The bot is uploading the processed video to Telegram</td>
  </tr>
  <tr>
    <td align="center">✅</td>
    <td><strong>Completed</strong>: The download is complete</td>
  </tr>
</table>

### Canceling Downloads

If you need to cancel a download, you can use the `/cancel` command. The bot will stop the download and clean up any temporary files.

## 📊 Admin Features

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/user-shield.svg" alt="Admin" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

If you're an admin (your Telegram user ID is listed in the `ADMIN_USER_IDS` configuration), you have access to additional features:

### Stats Command

The `/stats` command provides comprehensive information about the system and bot performance:

<table>
  <tr>
    <th width="30%">Information</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>System Information</td>
    <td>Operating system details, Python version, and FFmpeg version</td>
  </tr>
  <tr>
    <td>Resource Usage</td>
    <td>Real-time CPU, memory, and disk usage statistics</td>
  </tr>
  <tr>
    <td>Bot Performance</td>
    <td>Uptime, active downloads, and total completed downloads</td>
  </tr>
  <tr>
    <td>Active Downloads</td>
    <td>List of current downloads with progress information</td>
  </tr>
</table>

### Web Dashboard

Admins can also access the web dashboard for more detailed monitoring. See the [Web Dashboard](#-web-dashboard) section below.

## 📊 Web Dashboard

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gauge-high.svg" alt="Dashboard" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The M3U8 Downloader Bot includes a web-based dashboard that provides real-time monitoring of system resources and bot statistics.

### Accessing the Dashboard

The dashboard is available at `http://localhost:8080` or `http://your-server-ip:8080` by default. You can configure the host and port in your `.env` file.

### Dashboard Features

<table>
  <tr>
    <th width="30%">Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>System Information</td>
    <td>OS details, Python version, FFmpeg version</td>
  </tr>
  <tr>
    <td>Resource Usage</td>
    <td>Real-time CPU, memory, and disk usage with visual indicators</td>
  </tr>
  <tr>
    <td>Bot Statistics</td>
    <td>Uptime, active downloads, completed downloads</td>
  </tr>
  <tr>
    <td>Auto-Refresh</td>
    <td>Dashboard automatically refreshes every 30 seconds</td>
  </tr>
  <tr>
    <td>Mobile-Friendly Design</td>
    <td>Responsive layout works on all devices</td>
  </tr>
  <tr>
    <td>Dark Mode Support</td>
    <td>Automatic theme switching based on system preferences</td>
  </tr>
</table>

### Dashboard Authentication

The web dashboard includes built-in authentication for security. You can configure authentication in your `.env` file:

```ini
# Web server authentication
WEB_AUTH_ENABLED=true
WEB_AUTH_USERNAME=admin
WEB_AUTH_PASSWORD=your_secure_password
```

## 🔒 Security Considerations

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/shield-halved.svg" alt="Security" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

When using the M3U8 Downloader Bot, keep these security considerations in mind:

- Only download videos that you have permission to download
- Keep your API credentials secure
- Enable web authentication for the dashboard
- Consider using a reverse proxy with HTTPS for the web dashboard
- Regularly update the bot to get the latest security fixes

For more security information, see the [Security Guide](/docs/security).

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
