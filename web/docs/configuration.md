<div align="center">

# ⚙️ Configuration Guide

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/sliders.svg" alt="Configuration" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Customize your M3U8 Downloader Bot to fit your needs*

</div>

---

The M3U8 Downloader Bot can be configured using environment variables. This guide explains all available configuration options.

## 🛠️ Configuration Methods

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/wrench.svg" alt="Methods" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

You can configure the bot using one of the following methods:

<table>
  <tr>
    <th width="33%">Environment Variables</th>
    <th width="33%">.env File</th>
    <th width="33%">Docker Environment</th>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/terminal.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/file-lines.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"></td>
  </tr>
  <tr>
    <td>Set environment variables directly in your system</td>
    <td>Create a <code>.env</code> file in the root directory of the project</td>
    <td>Set environment variables in your Docker Compose file</td>
  </tr>
</table>

## 🔑 Required Configuration

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/key.svg" alt="Required" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

These settings are required for the bot to function:

### 🤖 Telegram Bot Settings

<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
    <th>Default</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>API_ID</code></td>
    <td>Telegram API ID from <a href="https://my.telegram.org">my.telegram.org</a></td>
    <td>None</td>
    <td><code>123456</code></td>
  </tr>
  <tr>
    <td><code>API_HASH</code></td>
    <td>Telegram API Hash from <a href="https://my.telegram.org">my.telegram.org</a></td>
    <td>None</td>
    <td><code>abcdef1234567890abcdef1234567890</code></td>
  </tr>
  <tr>
    <td><code>BOT_TOKEN</code></td>
    <td>Telegram Bot Token from <a href="https://t.me/BotFather">@BotFather</a></td>
    <td>None</td>
    <td><code>123456789:ABCDefGhIJKlmnOPQRstUVwxYZ</code></td>
  </tr>
</table>

## 🔧 Optional Configuration

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gears.svg" alt="Optional" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

These settings are optional and have default values:

### 👮 Admin Settings

<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
    <th>Default</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>ADMIN_USER_IDS</code></td>
    <td>Comma-separated list of Telegram user IDs who have admin access</td>
    <td>Empty</td>
    <td><code>123456789,987654321</code></td>
  </tr>
</table>

### 📥 Download Settings

<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
    <th>Default</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>DOWNLOAD_PATH</code></td>
    <td>Path where downloaded files are stored</td>
    <td><code>downloads</code></td>
    <td><code>/app/downloads</code></td>
  </tr>
  <tr>
    <td><code>MAX_DOWNLOAD_SIZE</code></td>
    <td>Maximum file size for downloads (in bytes or with suffix KB, MB, GB)</td>
    <td><code>500MB</code></td>
    <td><code>1GB</code></td>
  </tr>
  <tr>
    <td><code>MAX_CONCURRENT_DOWNLOADS</code></td>
    <td>Maximum number of concurrent downloads</td>
    <td><code>3</code></td>
    <td><code>5</code></td>
  </tr>
  <tr>
    <td><code>DOWNLOAD_TIMEOUT</code></td>
    <td>Timeout for downloads in seconds</td>
    <td><code>300</code></td>
    <td><code>600</code></td>
  </tr>
  <tr>
    <td><code>CHUNK_SIZE</code></td>
    <td>Chunk size for downloads in bytes</td>
    <td><code>1048576</code> (1MB)</td>
    <td><code>2097152</code> (2MB)</td>
  </tr>
</table>

### 🌐 Web Server Settings

<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
    <th>Default</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>ENABLE_WEB_SERVER</code></td>
    <td>Whether to enable the web server</td>
    <td><code>true</code></td>
    <td><code>false</code></td>
  </tr>
  <tr>
    <td><code>WEB_SERVER_HOST</code></td>
    <td>Host to bind the web server</td>
    <td><code>0.0.0.0</code></td>
    <td><code>127.0.0.1</code></td>
  </tr>
  <tr>
    <td><code>WEB_SERVER_PORT</code></td>
    <td>Port for the web server</td>
    <td><code>8080</code></td>
    <td><code>9000</code></td>
  </tr>
</table>

### 🔒 Web Server Authentication

<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
    <th>Default</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>WEB_AUTH_ENABLED</code></td>
    <td>Whether to enable authentication for the web server</td>
    <td><code>true</code></td>
    <td><code>false</code></td>
  </tr>
  <tr>
    <td><code>WEB_AUTH_USERNAME</code></td>
    <td>Username for web server authentication</td>
    <td><code>admin</code></td>
    <td><code>user</code></td>
  </tr>
  <tr>
    <td><code>WEB_AUTH_PASSWORD</code></td>
    <td>Password for web server authentication</td>
    <td>Auto-generated</td>
    <td><code>your_secure_password</code></td>
  </tr>
</table>

### 🛡️ Security Settings

<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
    <th>Default</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>SECRET_KEY</code></td>
    <td>Secret key for security features</td>
    <td>Auto-generated</td>
    <td><code>your_random_secret_key</code></td>
  </tr>
</table>

## 📄 Example .env File

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/file-code.svg" alt="Example File" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Here's an example `.env` file with all available configuration options:

<div align="center">

```ini
# Telegram Bot settings
API_ID=123456
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=123456789:ABCDefGhIJKlmnOPQRstUVwxYZ

# Admin settings
ADMIN_USER_IDS=123456789,987654321

# Download settings
DOWNLOAD_PATH=downloads
MAX_DOWNLOAD_SIZE=500MB
MAX_CONCURRENT_DOWNLOADS=3
DOWNLOAD_TIMEOUT=300
CHUNK_SIZE=1048576

# Web server settings
ENABLE_WEB_SERVER=true
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8080

# Web server authentication
WEB_AUTH_ENABLED=true
WEB_AUTH_USERNAME=admin
WEB_AUTH_PASSWORD=your_secure_password

# Security settings
SECRET_KEY=your_random_secret_key
```

</div>

> 💡 **Tip:** You can copy this example and modify it to fit your needs.

## 🔄 Configuration Loading

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/arrow-down-a-z.svg" alt="Loading Order" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot loads configuration in the following order:

<table>
  <tr>
    <th width="10%">Priority</th>
    <th width="30%">Source</th>
    <th width="60%">Description</th>
  </tr>
  <tr>
    <td align="center">1️⃣</td>
    <td>Environment Variables</td>
    <td>Highest priority, overrides all other sources</td>
  </tr>
  <tr>
    <td align="center">2️⃣</td>
    <td><code>.env</code> File</td>
    <td>Medium priority, overrides default values</td>
  </tr>
  <tr>
    <td align="center">3️⃣</td>
    <td>Default Values</td>
    <td>Lowest priority, used if no other source is specified</td>
  </tr>
</table>

This means that environment variables take precedence over the `.env` file, which takes precedence over default values.

## ✅ Configuration Validation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/check-double.svg" alt="Validation" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot validates the configuration at startup and logs any issues:

<div align="center">

```
[INFO] Loading configuration...
[INFO] API_ID: ********
[INFO] API_HASH: ********
[INFO] BOT_TOKEN: ********
[INFO] ADMIN_USER_IDS: [123456789, 987654321]
[INFO] MAX_CONCURRENT_DOWNLOADS: 3
[INFO] Web server enabled: True
[INFO] Web server host: 0.0.0.0
[INFO] Web server port: 8080
[INFO] Web authentication enabled: True
```

</div>

## 🔄 Dynamic Configuration

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bolt.svg" alt="Dynamic" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Some configuration options can be changed at runtime through admin commands:

<table>
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/set_max_downloads &lt;number&gt;</code></td>
    <td>Set the maximum number of concurrent downloads</td>
  </tr>
  <tr>
    <td><code>/set_download_timeout &lt;seconds&gt;</code></td>
    <td>Set the download timeout</td>
  </tr>
</table>

## 💡 Configuration Best Practices

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/lightbulb.svg" alt="Best Practices" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="10%">Tip</th>
    <th width="90%">Description</th>
  </tr>
  <tr>
    <td align="center">🔒</td>
    <td><strong>Use environment variables for sensitive information</strong>: Don't hardcode sensitive information in your code</td>
  </tr>
  <tr>
    <td align="center">⚖️</td>
    <td><strong>Set appropriate limits</strong>: Configure <code>MAX_DOWNLOAD_SIZE</code> and <code>MAX_CONCURRENT_DOWNLOADS</code> based on your server's capabilities</td>
  </tr>
  <tr>
    <td align="center">🔐</td>
    <td><strong>Enable web authentication</strong>: Always enable web authentication in production</td>
  </tr>
  <tr>
    <td align="center">🔑</td>
    <td><strong>Use a strong password</strong>: Use a strong password for web authentication</td>
  </tr>
  <tr>
    <td align="center">👮</td>
    <td><strong>Limit admin access</strong>: Only add trusted users to the <code>ADMIN_USER_IDS</code> list</td>
  </tr>
</table>

## 🔍 Troubleshooting

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bug.svg" alt="Troubleshooting" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Configuration Not Applied

<details open>
<summary><b>If your configuration changes are not being applied:</b></summary>

1. ✅ Check that you're using the correct variable names
2. 📁 Ensure your `.env` file is in the correct location
3. 🔄 Restart the bot after making changes

</details>

### Web Server Not Starting

<details open>
<summary><b>If the web server is not starting:</b></summary>

1. ⚙️ Check that `ENABLE_WEB_SERVER` is set to `true`
2. 🔌 Ensure the port is not already in use
3. 📋 Check the logs for any errors

</details>

### Admin Commands Not Working

<details open>
<summary><b>If admin commands are not working:</b></summary>

1. 👤 Ensure your user ID is in the `ADMIN_USER_IDS` list
2. 📝 Check that the IDs are comma-separated without spaces
3. 🔄 Restart the bot after making changes

</details>

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
