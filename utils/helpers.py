import os
import re
import time
import logging
import asyncio
import secrets
import hashlib
from typing import Optional, Dict, Any, List
import aiohttp
import aiofiles
from urllib.parse import urlparse, urljoin
import html

from config.config import (
    CONNECTION_POOL_MAX_CONNECTIONS, CONNECTION_POOL_MAX_KEEPALIVE,
    CONNECTION_POOL_TTL_DNS_CACHE, CONNECTION_POOL_TIMEOUT,
    CONNECTION_POOL_CONNECT_TIMEOUT
)
from utils.connection_pool import get_connection_pool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Active downloads tracking
active_downloads: Dict[int, Dict[str, Any]] = {}

def is_valid_m3u8_url(url: str) -> bool:
    """
    Enhanced validation for M3U8 URLs with security checks.

    Args:
        url: The URL to check

    Returns:
        bool: True if the URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False

    # Basic URL validation
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False

        # Only allow http and https schemes
        if result.scheme not in ['http', 'https']:
            return False

        # Check for common URL injection patterns
        if re.search(r'[\s\'";]', url):
            return False

        # Check for localhost or private IP addresses
        hostname = result.netloc.lower()
        if hostname == 'localhost' or hostname.startswith('127.') or \
           hostname.startswith('192.168.') or hostname.startswith('10.') or \
           (hostname.startswith('172.') and 16 <= int(hostname.split('.')[1]) <= 31):
            return False
    except Exception as e:
        logger.error(f"URL validation error: {str(e)}")
        return False

    # Check if it's an m3u8 URL
    pattern = r'.*\.(m3u8|M3U8)($|\?.*)'
    return bool(re.match(pattern, url))

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent path traversal and command injection.

    Args:
        filename: Filename to sanitize

    Returns:
        str: Sanitized filename
    """
    # Remove path separators and potentially dangerous characters
    sanitized = re.sub(r'[\\/*?:"<>|]', '', filename)
    # Ensure the filename doesn't start with dots or dashes
    sanitized = re.sub(r'^[.\-]+', '', sanitized)
    # Limit length to prevent excessively long filenames
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    # Ensure we have a valid filename
    if not sanitized:
        sanitized = "file"
    return sanitized

def generate_unique_filename(user_id: int, extension: str = 'mp4') -> str:
    """
    Generate a unique and secure filename based on user ID and timestamp.

    Args:
        user_id: Telegram user ID
        extension: File extension (default: mp4)

    Returns:
        str: Unique filename
    """
    # Sanitize the extension
    extension = sanitize_filename(extension)
    if not extension:
        extension = "mp4"

    # Generate a random token for additional security
    random_token = secrets.token_hex(4)
    timestamp = int(time.time())

    # Create a filename with user_id, timestamp and random token
    return f"{user_id}_{timestamp}_{random_token}.{extension}"

def format_size(size_bytes: int) -> str:
    """
    Format bytes to human-readable size.

    Args:
        size_bytes: Size in bytes

    Returns:
        str: Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        int: Size of the file in bytes
    """
    try:
        return os.path.getsize(file_path)
    except (FileNotFoundError, OSError):
        return 0

def create_secure_temp_dir(user_id: int) -> str:
    """
    Create a secure temporary directory with random name.

    Args:
        user_id: User ID

    Returns:
        str: Path to temporary directory
    """
    import tempfile

    # Generate a random token
    random_token = secrets.token_hex(8)

    # Create a hash of the user ID and token
    hash_obj = hashlib.sha256(f"{user_id}_{random_token}".encode())
    dir_name = hash_obj.hexdigest()[:16]

    # Create the temporary directory
    temp_dir = tempfile.mkdtemp(prefix=f"m3u8_{dir_name}_")

    # Set secure permissions (only owner can read/write/execute)
    try:
        os.chmod(temp_dir, 0o700)
    except Exception as e:
        logger.warning(f"Could not set secure permissions on temp dir: {str(e)}")

    return temp_dir

async def fetch_content(url: str, headers: Optional[Dict[str, str]] = None,
                    max_size: int = 10 * 1024 * 1024) -> Optional[str]:
    """
    Fetch content from a URL with enhanced security checks using the connection pool.

    Args:
        url: URL to fetch
        headers: Optional HTTP headers
        max_size: Maximum content size in bytes (default: 10MB)

    Returns:
        Optional[str]: Content as string or None if failed
    """
    # Validate URL before proceeding
    if not is_valid_m3u8_url(url):
        logger.error(f"Invalid M3U8 URL: {url}")
        return None

    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    try:
        # Get the connection pool
        pool = get_connection_pool(
            max_connections=CONNECTION_POOL_MAX_CONNECTIONS,
            max_keepalive_connections=CONNECTION_POOL_MAX_KEEPALIVE,
            ttl_dns_cache=CONNECTION_POOL_TTL_DNS_CACHE,
            timeout=CONNECTION_POOL_TIMEOUT,
            connection_timeout=CONNECTION_POOL_CONNECT_TIMEOUT
        )

        # Use the connection pool to make the request
        async with pool.get(url, headers=headers, allow_redirects=True, max_redirects=5) as response:
            if response.status == 200:
                # Check content type
                content_type = response.headers.get('Content-Type', '')
                if not ('text/plain' in content_type or
                        'application/x-mpegurl' in content_type or
                        'application/vnd.apple.mpegurl' in content_type or
                        'audio/mpegurl' in content_type or
                        'audio/x-mpegurl' in content_type):
                    logger.warning(f"Unexpected content type for M3U8: {content_type} from {url}")

                # Check content length
                content_length = response.content_length
                if content_length and content_length > max_size:
                    logger.error(f"Content too large: {content_length} bytes (max: {max_size})")
                    return None

                # Read with size limit
                content = await response.read()
                if len(content) > max_size:
                    logger.error(f"Content too large: {len(content)} bytes (max: {max_size})")
                    return None

                return content.decode('utf-8', errors='replace')
            else:
                logger.error(f"Failed to fetch URL {url}, status code: {response.status}")
                return None
    except aiohttp.ClientError as e:
        logger.error(f"Client error fetching URL {url}: {str(e)}")
        return None
    except asyncio.TimeoutError:
        logger.error(f"Timeout fetching URL {url}")
        return None
    except Exception as e:
        logger.error(f"Error fetching URL {url}: {str(e)}")
        return None
