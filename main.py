import os
import sys
import logging
import asyncio
import platform
from pyrogram import idle
from bot.client import BotClient
from config.config import (
    DOWNLOAD_PATH, ENABLE_WEB_SERVER,
    CONNECTION_POOL_MAX_CONNECTIONS, CONNECTION_POOL_MAX_KEEPALIVE,
    CONNECTION_POOL_TTL_DNS_CACHE, CONNECTION_POOL_TIMEOUT,
    CONNECTION_POOL_CONNECT_TIMEOUT,
    CACHE_ENABLED, CACHE_TTL, CACHE_MAX_SIZE,
    RESOURCE_MONITOR_ENABLED, RESOURCE_CPU_THRESHOLD, RESOURCE_MEMORY_THRESHOLD,
    RESOURCE_CHECK_INTERVAL, MAX_CONCURRENT_DOWNLOADS
)
from utils.system_checks import check_ffmpeg, get_platform_info
from utils.connection_pool import get_connection_pool, close_connection_pool
from utils.cache_manager import get_cache_manager, close_cache_manager
from utils.resource_manager import get_resource_manager, close_resource_manager
from web.server import WebServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_system_requirements():
    """
    Check if the system meets all requirements to run the bot.

    Returns:
        bool: True if all requirements are met, False otherwise
    """
    # Log platform information
    platform_info = get_platform_info()
    logger.info(f"Running on {platform_info['system']} {platform_info['release']} ({platform_info['machine']})")
    logger.info(f"Python version: {platform_info['python_version']}")

    # Check for FFmpeg
    ffmpeg_available, ffmpeg_message = check_ffmpeg()
    if ffmpeg_available:
        logger.info(f"FFmpeg check: {ffmpeg_message}")
    else:
        logger.error(f"FFmpeg check failed: {ffmpeg_message}")
        logger.error("FFmpeg is required for video processing. Please install FFmpeg:")

        if platform_info['system'].lower() == 'windows':
            logger.error("  - Download from: https://ffmpeg.org/download.html")
            logger.error("  - Add the bin folder to your PATH environment variable")
        elif platform_info['system'].lower() == 'darwin':  # macOS
            logger.error("  - Install with Homebrew: brew install ffmpeg")
            logger.error("  - Or download from: https://ffmpeg.org/download.html")
        elif platform_info['system'].lower() == 'linux':
            logger.error("  - Ubuntu/Debian: sudo apt install ffmpeg")
            logger.error("  - Fedora: sudo dnf install ffmpeg")
            logger.error("  - Arch Linux: sudo pacman -S ffmpeg")

        return False

    return True

async def main():
    """
    Main function to start the bot.
    """
    try:
        # Check system requirements
        if not check_system_requirements():
            logger.error("System requirements check failed. Please fix the issues and try again.")
            return

        # Create download directory if it doesn't exist
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)

        # Initialize the connection pool
        logger.info("Initializing connection pool...")
        pool = get_connection_pool(
            max_connections=CONNECTION_POOL_MAX_CONNECTIONS,
            max_keepalive_connections=CONNECTION_POOL_MAX_KEEPALIVE,
            ttl_dns_cache=CONNECTION_POOL_TTL_DNS_CACHE,
            timeout=CONNECTION_POOL_TIMEOUT,
            connection_timeout=CONNECTION_POOL_CONNECT_TIMEOUT
        )
        logger.info(f"Connection pool initialized with max_connections={CONNECTION_POOL_MAX_CONNECTIONS}")

        # Initialize the cache manager if enabled
        if CACHE_ENABLED:
            logger.info("Initializing cache manager...")
            cache_dir = os.path.join(DOWNLOAD_PATH, 'cache')
            cache = get_cache_manager(
                cache_dir=cache_dir,
                ttl=CACHE_TTL,
                max_size=CACHE_MAX_SIZE
            )
            logger.info(f"Cache manager initialized with ttl={CACHE_TTL}s, max_size={CACHE_MAX_SIZE} bytes")

        # Initialize the resource manager if enabled
        if RESOURCE_MONITOR_ENABLED:
            logger.info("Initializing resource manager...")
            resource_mgr = get_resource_manager(
                cpu_threshold=RESOURCE_CPU_THRESHOLD,
                memory_threshold=RESOURCE_MEMORY_THRESHOLD,
                check_interval=RESOURCE_CHECK_INTERVAL,
                max_concurrent_tasks=MAX_CONCURRENT_DOWNLOADS
            )
            logger.info(f"Resource manager initialized with cpu_threshold={RESOURCE_CPU_THRESHOLD}%, "
                       f"memory_threshold={RESOURCE_MEMORY_THRESHOLD}%, "
                       f"max_concurrent_tasks={MAX_CONCURRENT_DOWNLOADS}")

        # Create and start the bot client
        bot_client = BotClient()
        bot = bot_client.get_client()

        # Start the bot
        bot_info = await bot_client.start()
        logger.info(f"Bot started as @{bot_info.username}")

        # Start the web server if enabled
        web_server = None
        if ENABLE_WEB_SERVER:
            web_server = WebServer()
            await web_server.start()

        # Keep the bot running
        await idle()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
    finally:
        # Stop the bot
        if 'bot_client' in locals() and bot_client:
            await bot_client.stop()

        # Stop the web server
        if 'web_server' in locals() and web_server:
            await web_server.stop()

        # Close the connection pool
        logger.info("Closing connection pool...")
        await close_connection_pool()
        logger.info("Connection pool closed")

        # Close the cache manager if enabled
        if CACHE_ENABLED:
            logger.info("Closing cache manager...")
            await close_cache_manager()
            logger.info("Cache manager closed")

        # Close the resource manager if enabled
        if RESOURCE_MONITOR_ENABLED:
            logger.info("Closing resource manager...")
            await close_resource_manager()
            logger.info("Resource manager closed")



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted")
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
