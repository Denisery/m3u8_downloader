import os
import secrets
import logging
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Telegram API credentials
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Download settings
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads")
MAX_DOWNLOAD_SIZE = int(os.getenv("MAX_DOWNLOAD_SIZE", 500 * 1024 * 1024))  # 500 MB default
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024 * 1024))  # 1 MB default

# Bot settings
ADMIN_USER_IDS = list(map(int, os.getenv("ADMIN_USER_IDS", "").split(","))) if os.getenv("ADMIN_USER_IDS") else []
MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", 5))
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", 3600))  # 1 hour default

# Web server settings
ENABLE_WEB_SERVER = os.getenv("ENABLE_WEB_SERVER", "true").lower() == "true"
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "0.0.0.0")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", 8080))

# Web server authentication
WEB_AUTH_ENABLED = os.getenv("WEB_AUTH_ENABLED", "true").lower() == "true"
WEB_AUTH_USERNAME = os.getenv("WEB_AUTH_USERNAME", "admin")
WEB_AUTH_PASSWORD = os.getenv("WEB_AUTH_PASSWORD", "")

# Generate a random password if not provided
if WEB_AUTH_ENABLED and not WEB_AUTH_PASSWORD:
    WEB_AUTH_PASSWORD = secrets.token_urlsafe(12)
    logger.warning(f"No WEB_AUTH_PASSWORD provided. Generated random password: {WEB_AUTH_PASSWORD}")

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Bot start time (for uptime calculation)
import time
BOT_START_TIME = time.time()

# Statistics tracking
TOTAL_COMPLETED_DOWNLOADS = 0

# Connection pool settings
CONNECTION_POOL_MAX_CONNECTIONS = int(os.getenv("CONNECTION_POOL_MAX_CONNECTIONS", 100))
CONNECTION_POOL_MAX_KEEPALIVE = int(os.getenv("CONNECTION_POOL_MAX_KEEPALIVE", 30))
CONNECTION_POOL_TTL_DNS_CACHE = int(os.getenv("CONNECTION_POOL_TTL_DNS_CACHE", 300))
CONNECTION_POOL_TIMEOUT = int(os.getenv("CONNECTION_POOL_TIMEOUT", 30))
CONNECTION_POOL_CONNECT_TIMEOUT = int(os.getenv("CONNECTION_POOL_CONNECT_TIMEOUT", 10))

# Cache settings
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour default
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", 100 * 1024 * 1024))  # 100 MB default

# Resource allocation settings
RESOURCE_MONITOR_ENABLED = os.getenv("RESOURCE_MONITOR_ENABLED", "true").lower() == "true"
RESOURCE_CPU_THRESHOLD = float(os.getenv("RESOURCE_CPU_THRESHOLD", 80.0))  # 80% CPU usage threshold
RESOURCE_MEMORY_THRESHOLD = float(os.getenv("RESOURCE_MEMORY_THRESHOLD", 80.0))  # 80% memory usage threshold
RESOURCE_CHECK_INTERVAL = int(os.getenv("RESOURCE_CHECK_INTERVAL", 5))  # Check every 5 seconds
