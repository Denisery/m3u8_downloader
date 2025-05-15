<div align="center">

# 🚀 Installation Guide

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/download.svg" alt="Installation" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Get up and running with the M3U8 Downloader Bot*

</div>

---

This guide provides detailed instructions for installing the M3U8 Downloader Bot on different platforms.

## 📋 Prerequisites

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/clipboard-check.svg" alt="Prerequisites" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Before you begin, make sure you have the following prerequisites installed:

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

## 🖥️ Standard Installation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/terminal.svg" alt="Terminal" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Step 1: Get the Code 📥

```bash
# Clone the repository
git clone https://github.com/Denisery/m3u8_downloader.git

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

> 💡 **Note for Windows Users:** The TGCrypto package requires Microsoft Visual C++ to build on Windows. The requirements.txt file includes a platform-specific conditional to skip this dependency on Windows. If you want to use TGCrypto on Windows, you can install it from a pre-compiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#tgcrypto).

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

## 🐳 Docker Installation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Docker" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

Docker provides a consistent, cross-platform way to run the M3U8 Downloader Bot without worrying about dependencies or platform-specific issues.

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

> 💡 **Detailed Instructions**: For complete Docker setup and usage instructions, see the [Docker Guide](/docs/docker).

## 📱 Platform-Specific Instructions

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/desktop.svg" alt="Platforms" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Windows

<details>
<summary><b>Click to expand Windows-specific instructions</b></summary>

1. **Install Python**: Download and install Python from the [official website](https://www.python.org/downloads/windows/).
2. **Install FFmpeg**: 
   - Download FFmpeg from [here](https://www.gyan.dev/ffmpeg/builds/).
   - Extract the ZIP file.
   - Add the `bin` folder to your PATH environment variable.
3. **Install Git**: Download and install Git from the [official website](https://git-scm.com/download/win).
4. **Follow the standard installation steps above.**

> 💡 **Note about TGCrypto**: The TGCrypto package requires Microsoft Visual C++ to build on Windows. The requirements.txt file includes a platform-specific conditional to skip this dependency on Windows. If you want to use TGCrypto on Windows, you can install it from a pre-compiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#tgcrypto).

</details>

### macOS

<details>
<summary><b>Click to expand macOS-specific instructions</b></summary>

1. **Install Homebrew**: If you don't have Homebrew installed, install it by running:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. **Install Python**:
   ```bash
   brew install python
   ```
3. **Install FFmpeg**:
   ```bash
   brew install ffmpeg
   ```
4. **Install Git**:
   ```bash
   brew install git
   ```
5. **Follow the standard installation steps above.**

</details>

### Linux

<details>
<summary><b>Click to expand Linux-specific instructions</b></summary>

#### Ubuntu/Debian:

1. **Update package lists**:
   ```bash
   sudo apt update
   ```
2. **Install Python**:
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```
3. **Install FFmpeg**:
   ```bash
   sudo apt install ffmpeg
   ```
4. **Install Git**:
   ```bash
   sudo apt install git
   ```
5. **Follow the standard installation steps above.**

#### CentOS/RHEL:

1. **Install Python**:
   ```bash
   sudo yum install python3 python3-pip
   ```
2. **Install FFmpeg**:
   ```bash
   sudo yum install epel-release
   sudo yum install ffmpeg
   ```
3. **Install Git**:
   ```bash
   sudo yum install git
   ```
4. **Follow the standard installation steps above.**

</details>

## 🔍 Troubleshooting Installation Issues

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bug.svg" alt="Troubleshooting" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<details>
<summary><b>FFmpeg not found</b></summary>
<ul>
  <li>Make sure FFmpeg is installed and in your system PATH</li>
  <li>Try running <code>ffmpeg -version</code> in your terminal to verify the installation</li>
  <li>If using Docker, this should not be an issue as FFmpeg is included in the Docker image</li>
</ul>
</details>

<details>
<summary><b>Python package installation errors</b></summary>
<ul>
  <li>Make sure you're using Python 3.7 or higher</li>
  <li>Try upgrading pip: <code>pip install --upgrade pip</code></li>
  <li>If you're on Windows and having issues with TGCrypto, see the note above about installing from a pre-compiled wheel</li>
</ul>
</details>

<details>
<summary><b>Docker issues</b></summary>
<ul>
  <li>Make sure Docker is installed and running</li>
  <li>Check if you have permission to run Docker commands (you might need to use <code>sudo</code> on Linux)</li>
  <li>Verify that the ports you're trying to use aren't already in use</li>
</ul>
</details>

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
