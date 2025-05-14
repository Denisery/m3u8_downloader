import os
import time
import logging
import platform
import psutil
from typing import Dict, Any

from config.config import (
    BOT_START_TIME, TOTAL_COMPLETED_DOWNLOADS,
    CACHE_ENABLED, RESOURCE_MONITOR_ENABLED
)
from utils.helpers import active_downloads, format_size
from utils.system_checks import check_ffmpeg, get_platform_info
from utils.connection_pool import get_connection_pool
from utils.cache_manager import get_cache_manager
from utils.resource_manager import get_resource_manager

# Configure logging
logger = logging.getLogger(__name__)

def get_system_stats() -> Dict[str, Any]:
    """
    Get system statistics including CPU, memory, and disk usage.

    Returns:
        Dict[str, Any]: System statistics
    """
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count(logical=True)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_used = memory.used
        memory_total = memory.total
        memory_percent = memory.percent

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_used = disk.used
        disk_total = disk.total
        disk_percent = disk.percent

        # Format values
        memory_used_formatted = format_size(memory_used)
        memory_total_formatted = format_size(memory_total)
        disk_used_formatted = format_size(disk_used)
        disk_total_formatted = format_size(disk_total)

        return {
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count
            },
            'memory': {
                'used': memory_used,
                'total': memory_total,
                'percent': memory_percent,
                'used_formatted': memory_used_formatted,
                'total_formatted': memory_total_formatted
            },
            'disk': {
                'used': disk_used,
                'total': disk_total,
                'percent': disk_percent,
                'used_formatted': disk_used_formatted,
                'total_formatted': disk_total_formatted
            }
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {str(e)}")
        return {
            'cpu': {'percent': 0, 'count': 0},
            'memory': {
                'used': 0, 'total': 0, 'percent': 0,
                'used_formatted': '0 B', 'total_formatted': '0 B'
            },
            'disk': {
                'used': 0, 'total': 0, 'percent': 0,
                'used_formatted': '0 B', 'total_formatted': '0 B'
            },
            'error': str(e)
        }

def get_bot_stats() -> Dict[str, Any]:
    """
    Get bot statistics including uptime, active downloads, etc.

    Returns:
        Dict[str, Any]: Bot statistics
    """
    try:
        # Calculate uptime
        uptime_seconds = time.time() - BOT_START_TIME
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format uptime
        uptime_formatted = ""
        if days > 0:
            uptime_formatted += f"{int(days)}d "
        if hours > 0 or days > 0:
            uptime_formatted += f"{int(hours)}h "
        if minutes > 0 or hours > 0 or days > 0:
            uptime_formatted += f"{int(minutes)}m "
        uptime_formatted += f"{int(seconds)}s"

        # Get active downloads
        active_count = sum(1 for d in active_downloads.values() if d.get('status') == 'downloading')

        # Get FFmpeg version
        ffmpeg_available, ffmpeg_message = check_ffmpeg()
        ffmpeg_version = ffmpeg_message if ffmpeg_available else "Not available"

        return {
            'uptime_seconds': uptime_seconds,
            'uptime_formatted': uptime_formatted,
            'active_downloads': active_count,
            'total_downloads': len(active_downloads),
            'completed_downloads': TOTAL_COMPLETED_DOWNLOADS,
            'ffmpeg_version': ffmpeg_version
        }
    except Exception as e:
        logger.error(f"Error getting bot stats: {str(e)}")
        return {
            'uptime_seconds': 0,
            'uptime_formatted': '0s',
            'active_downloads': 0,
            'total_downloads': 0,
            'completed_downloads': 0,
            'ffmpeg_version': 'Unknown',
            'error': str(e)
        }

def get_all_stats() -> Dict[str, Any]:
    """
    Get all statistics including system, bot, connection pool, cache, and resource manager stats.

    Returns:
        Dict[str, Any]: All statistics
    """
    # Get platform info
    platform_info = get_platform_info()

    # Get system stats
    system_stats = get_system_stats()

    # Get bot stats
    bot_stats = get_bot_stats()

    # Initialize additional stats
    connection_pool_stats = {}
    cache_stats = {}
    resource_manager_stats = {}

    # Get connection pool stats
    try:
        pool = get_connection_pool()
        connection_pool_stats = pool.get_stats()
    except Exception as e:
        logger.error(f"Error getting connection pool stats: {str(e)}")
        connection_pool_stats = {"error": str(e)}

    # Get cache stats if enabled
    if CACHE_ENABLED:
        try:
            cache = get_cache_manager()
            # We don't have a get_stats method for cache yet, so just provide basic info
            cache_stats = {
                "enabled": True,
                "cache_dir": cache.cache_dir,
                "ttl": cache.ttl,
                "max_size": cache.max_size,
                "items_count": len(cache.cache_index)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            cache_stats = {"error": str(e)}
    else:
        cache_stats = {"enabled": False}

    # Get resource manager stats if enabled
    if RESOURCE_MONITOR_ENABLED:
        try:
            resource_mgr = get_resource_manager()
            resource_manager_stats = resource_mgr.get_stats()
        except Exception as e:
            logger.error(f"Error getting resource manager stats: {str(e)}")
            resource_manager_stats = {"error": str(e)}
    else:
        resource_manager_stats = {"enabled": False}

    return {
        'platform': platform_info,
        'system': system_stats,
        'bot': bot_stats,
        'connection_pool': connection_pool_stats,
        'cache': cache_stats,
        'resource_manager': resource_manager_stats
    }
