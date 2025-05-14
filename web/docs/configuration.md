# Configuration Guide

The M3U8 Downloader Bot can be configured using environment variables. This guide explains all available configuration options.

## Configuration Methods

You can configure the bot using one of the following methods:

1. **Environment Variables**: Set environment variables directly in your system
2. **.env File**: Create a `.env` file in the root directory of the project
3. **Docker Environment**: Set environment variables in your Docker Compose file

## Required Configuration

These settings are required for the bot to function:

### Telegram Bot Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) | None | `123456` |
| `API_HASH` | Telegram API Hash from [my.telegram.org](https://my.telegram.org) | None | `abcdef1234567890abcdef1234567890` |
| `BOT_TOKEN` | Telegram Bot Token from [@BotFather](https://t.me/BotFather) | None | `123456789:ABCDefGhIJKlmnOPQRstUVwxYZ` |

## Optional Configuration

These settings are optional and have default values:

### Admin Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ADMIN_USER_IDS` | Comma-separated list of Telegram user IDs who have admin access | Empty | `123456789,987654321` |

### Download Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DOWNLOAD_PATH` | Path where downloaded files are stored | `downloads` | `/app/downloads` |
| `MAX_DOWNLOAD_SIZE` | Maximum file size for downloads (in bytes or with suffix KB, MB, GB) | `500MB` | `1GB` |
| `MAX_CONCURRENT_DOWNLOADS` | Maximum number of concurrent downloads | `3` | `5` |
| `DOWNLOAD_TIMEOUT` | Timeout for downloads in seconds | `300` | `600` |
| `CHUNK_SIZE` | Chunk size for downloads in bytes | `1048576` (1MB) | `2097152` (2MB) |

### Web Server Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ENABLE_WEB_SERVER` | Whether to enable the web server | `true` | `false` |
| `WEB_SERVER_HOST` | Host to bind the web server | `0.0.0.0` | `127.0.0.1` |
| `WEB_SERVER_PORT` | Port for the web server | `8080` | `9000` |

### Web Server Authentication

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `WEB_AUTH_ENABLED` | Whether to enable authentication for the web server | `true` | `false` |
| `WEB_AUTH_USERNAME` | Username for web server authentication | `admin` | `user` |
| `WEB_AUTH_PASSWORD` | Password for web server authentication | Auto-generated | `your_secure_password` |

### Security Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `SECRET_KEY` | Secret key for security features | Auto-generated | `your_random_secret_key` |

## Example .env File

Here's an example `.env` file with all available configuration options:

```
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

## Configuration Loading

The bot loads configuration in the following order:

1. Default values
2. `.env` file
3. Environment variables

This means that environment variables take precedence over the `.env` file, which takes precedence over default values.

## Configuration Validation

The bot validates the configuration at startup and logs any issues:

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

## Dynamic Configuration

Some configuration options can be changed at runtime through admin commands:

- `/set_max_downloads <number>` - Set the maximum number of concurrent downloads
- `/set_download_timeout <seconds>` - Set the download timeout

## Configuration Best Practices

1. **Use environment variables for sensitive information**: Don't hardcode sensitive information in your code
2. **Set appropriate limits**: Configure `MAX_DOWNLOAD_SIZE` and `MAX_CONCURRENT_DOWNLOADS` based on your server's capabilities
3. **Enable web authentication**: Always enable web authentication in production
4. **Use a strong password**: Use a strong password for web authentication
5. **Limit admin access**: Only add trusted users to the `ADMIN_USER_IDS` list

## Troubleshooting

### Configuration Not Applied

If your configuration changes are not being applied:

1. Check that you're using the correct variable names
2. Ensure your `.env` file is in the correct location
3. Restart the bot after making changes

### Web Server Not Starting

If the web server is not starting:

1. Check that `ENABLE_WEB_SERVER` is set to `true`
2. Ensure the port is not already in use
3. Check the logs for any errors

### Admin Commands Not Working

If admin commands are not working:

1. Ensure your user ID is in the `ADMIN_USER_IDS` list
2. Check that the IDs are comma-separated without spaces
3. Restart the bot after making changes
