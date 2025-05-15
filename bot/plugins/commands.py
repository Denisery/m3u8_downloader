import os
import logging
import asyncio
import time
from typing import Dict, Any, List, Optional
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, MessageNotModified

# Configure logging
logger = logging.getLogger(__name__)
logger.info("Commands module loaded - command handlers should be registered")

from config.config import (
    ADMIN_USER_IDS, MAX_CONCURRENT_DOWNLOADS, TOTAL_COMPLETED_DOWNLOADS,
    RESOURCE_MONITOR_ENABLED
)
from downloader.m3u8_downloader import M3U8Downloader
from processor.video_processor import VideoProcessor
from utils.helpers import (
    is_valid_m3u8_url, generate_unique_filename, format_size,
    active_downloads, sanitize_filename
)
from utils.system_monitor import get_all_stats
from utils.resource_manager import get_resource_manager

# Command handlers
@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """
    Handle the /start command.
    """
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    logger.info(f"Start command received from user {user_id} ({user_name})")

    await message.reply_text(
        f"👋 Hello, {user_name}!\n\n"
        f"I'm an M3U8 Video Downloader Bot. I can download videos from M3U8 URLs.\n\n"
        f"Just send me an M3U8 URL, and I'll download it for you.\n\n"
        f"Use /help to see available commands."
    )

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """
    Handle the /help command.
    """
    user_id = message.from_user.id
    is_admin = user_id in ADMIN_USER_IDS

    logger.info(f"Help command received from user {user_id}")

    help_text = (
        "📖 **Available Commands:**\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/status - Check your download status\n"
        "/cancel - Cancel your current download\n"
    )

    # Add admin commands if the user is an admin
    if is_admin:
        help_text += (
            "\n**Admin Commands:**\n"
            "/stats - View detailed system and bot statistics\n"
        )

    help_text += (
        "\n**How to use:**\n"
        "1. Send me an M3U8 URL\n"
        "2. Wait for the download to complete\n"
        "3. Receive your video\n\n"
        "**Note:** I can only process one download per user at a time."
    )

    await message.reply_text(help_text)

@Client.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    """
    Handle the /status command.
    """
    user_id = message.from_user.id

    logger.info(f"Status command received from user {user_id}")

    if user_id in active_downloads:
        download = active_downloads[user_id]
        progress = download.get('progress', 0)
        status = download.get('status', 'unknown')
        filename = download.get('filename', 'unknown')
        start_time = download.get('start_time', time.time())
        elapsed = time.time() - start_time

        await message.reply_text(
            f"📥 **Download Status:**\n\n"
            f"File: `{filename}`\n"
            f"Status: {status}\n"
            f"Progress: {progress}%\n"
            f"Elapsed Time: {int(elapsed)} seconds"
        )
    else:
        await message.reply_text(
            "You don't have any active downloads."
        )

@Client.on_message(filters.command("cancel"))
async def cancel_command(client: Client, message: Message):
    """
    Handle the /cancel command.
    """
    user_id = message.from_user.id

    logger.info(f"Cancel command received from user {user_id}")

    # Check if there's an active task for this user
    if user_id in active_tasks and not active_tasks[user_id].done():
        active_tasks[user_id].cancel()

        if user_id in active_downloads:
            del active_downloads[user_id]

        await message.reply_text(
            "✅ Your download has been cancelled."
        )
    else:
        await message.reply_text(
            "You don't have any active downloads to cancel."
        )

# Initialize global dictionaries
active_tasks = {}

# Define the process_download function
async def process_download(client, message, status_message, url, filename, user_id):
    """
    Process an M3U8 download request.

    Args:
        client: The Pyrogram client
        message: The original message
        status_message: The message to update with status
        url: The M3U8 URL to download
        filename: The filename to save as
        user_id: The user ID who requested the download
    """
    try:
        # Update status
        active_downloads[user_id]['status'] = 'downloading'

        # Create downloader and processor instances
        downloader = M3U8Downloader()
        processor = VideoProcessor()

        # Download and process the video
        # This is a placeholder - implement the actual download and processing logic
        await status_message.edit_text("📥 Downloading video... 0%")

        # Simulate download progress
        for i in range(1, 101):
            active_downloads[user_id]['progress'] = i
            if i % 10 == 0:
                await status_message.edit_text(f"📥 Downloading video... {i}%")
            await asyncio.sleep(0.1)

        # Simulate processing
        active_downloads[user_id]['status'] = 'processing'
        await status_message.edit_text("🔄 Processing video...")
        await asyncio.sleep(2)

        # Simulate sending the video
        active_downloads[user_id]['status'] = 'uploading'
        await status_message.edit_text("📤 Uploading video...")
        await asyncio.sleep(2)

        # Complete
        await status_message.edit_text("✅ Download complete!")

        # Remove from active downloads
        if user_id in active_downloads:
            del active_downloads[user_id]

    except asyncio.CancelledError:
        logger.info(f"Download cancelled for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Error processing download for user {user_id}: {str(e)}")
        await status_message.edit_text(f"❌ Error: {str(e)}")

        # Remove from active downloads
        if user_id in active_downloads:
            del active_downloads[user_id]

# Admin commands
@Client.on_message(filters.command("stats") & filters.user(ADMIN_USER_IDS))
async def stats_command(client: Client, message: Message):
    """
    Handle the /stats command (admin only).
    Shows system information and bot statistics.
    """
    user_id = message.from_user.id
    logger.info(f"Stats command received from admin {user_id}")

    # Get all stats
    all_stats = get_all_stats()

    # Extract stats for easier access
    platform_info = all_stats['platform']
    system_stats = all_stats['system']
    bot_stats = all_stats['bot']

    # Format system information
    system_text = (
        f"🖥️ **System Information:**\n\n"
        f"OS: {platform_info['system']} {platform_info['release']}\n"
        f"Machine: {platform_info['machine']}\n"
        f"Python: {platform_info['python_version']}\n"
        f"FFmpeg: {bot_stats.get('ffmpeg_version', 'Unknown')}\n\n"
    )

    # Format resource usage
    resources_text = (
        f"📊 **Resource Usage:**\n\n"
        f"CPU: {system_stats['cpu']['percent']}%\n"
        f"Memory: {system_stats['memory']['percent']}% ({system_stats['memory']['used_formatted']} / {system_stats['memory']['total_formatted']})\n"
        f"Disk: {system_stats['disk']['percent']}% ({system_stats['disk']['used_formatted']} / {system_stats['disk']['total_formatted']})\n\n"
    )

    # Format bot statistics
    bot_text = (
        f"🤖 **Bot Statistics:**\n\n"
        f"Uptime: {bot_stats.get('uptime_formatted', 'Unknown')}\n"
        f"Active Downloads: {bot_stats.get('active_downloads', len(active_downloads))}\n"
        f"Completed Downloads: {bot_stats.get('completed_downloads', TOTAL_COMPLETED_DOWNLOADS)}\n\n"
    )

    # Add resource manager statistics if enabled
    if RESOURCE_MONITOR_ENABLED:
        resource_mgr_stats = all_stats.get('resource_manager', {})
        if resource_mgr_stats and resource_mgr_stats.get('enabled', False) != False:
            resource_mgr_text = (
                f"🔄 **Resource Manager:**\n\n"
                f"CPU Threshold: {resource_mgr_stats.get('cpu_threshold', 'N/A')}%\n"
                f"Memory Threshold: {resource_mgr_stats.get('memory_threshold', 'N/A')}%\n"
                f"Max Concurrent Tasks: {resource_mgr_stats.get('max_concurrent_tasks', 'N/A')}\n"
                f"Current Concurrent Tasks: {resource_mgr_stats.get('current_concurrent_tasks', 'N/A')}\n"
                f"Queued Tasks: {resource_mgr_stats.get('queued_tasks', 'N/A')}\n"
                f"Throttling: {'Yes' if resource_mgr_stats.get('throttling', False) else 'No'}\n\n"
            )

            bot_text += resource_mgr_text

    # Add active downloads details
    active_downloads_text = ""
    if active_downloads:
        active_downloads_text = "**Active Downloads:**\n"
        for user_id, download in active_downloads.items():
            status = download.get('status', 'unknown')
            progress = download.get('progress', 0)
            filename = download.get('filename', 'unknown')
            active_downloads_text += f"User {user_id}: {filename} ({status} - {progress}%)\n"

    # Combine all sections
    stats_text = system_text + resources_text + bot_text + active_downloads_text

    await message.reply_text(stats_text)

# URL handler
@Client.on_message(filters.text & filters.private & ~filters.command(["start", "help", "status", "cancel", "stats"]))
async def handle_url(client: Client, message: Message):
    """
    Handle M3U8 URLs sent by users.
    """
    # Get and sanitize the URL
    url = message.text.strip()
    user_id = message.from_user.id

    # Skip if the message starts with a slash (potential command)
    if url.startswith('/'):
        logger.info(f"Skipping message that starts with / from user {user_id}")
        return

    logger.info(f"Received potential URL from user {user_id}: {url[:50]}{'...' if len(url) > 50 else ''}")

    # Check if the URL is valid
    if not is_valid_m3u8_url(url):
        await message.reply_text(
            "❌ This doesn't look like a valid M3U8 URL.\n\n"
            "Please send a valid HTTP or HTTPS M3U8 URL (ending with .m3u8)."
        )
        return

    # Check if the user already has an active download
    if user_id in active_downloads and active_downloads[user_id].get('status') == 'downloading':
        await message.reply_text(
            "⚠️ You already have an active download.\n\n"
            "Please wait for it to complete or use /cancel to cancel it."
        )
        return

    # Check if we've reached the maximum number of concurrent downloads
    active_count = sum(1 for d in active_downloads.values() if d.get('status') == 'downloading')
    if active_count >= MAX_CONCURRENT_DOWNLOADS:
        await message.reply_text(
            "⚠️ The bot is currently at maximum capacity.\n\n"
            "Please try again later."
        )
        return

    # Start the download process
    status_message = await message.reply_text(
        "🔍 Analyzing M3U8 URL...",
        quote=True
    )

    # Generate a unique filename
    filename = generate_unique_filename(url)

    logger.info(f"Starting download for user {user_id}: {filename}")

    # Add to active downloads
    active_downloads[user_id] = {
        'status': 'analyzing',
        'progress': 0,
        'filename': filename,
        'start_time': time.time()
    }



    # Create a task for the download process
    download_task = asyncio.create_task(
        process_download(client, message, status_message, url, filename, user_id)
    )

    # Store the task in the global active_tasks dictionary
    active_tasks[user_id] = download_task
