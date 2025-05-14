import os
import logging
import asyncio
import time
from typing import Dict, Any, List, Optional
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, MessageNotModified

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

# Configure logging
logger = logging.getLogger(__name__)

# Track active tasks
active_tasks: Dict[int, asyncio.Task] = {}

# Command handlers
@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """
    Handle the /start command.
    """
    user_id = message.from_user.id
    user_name = message.from_user.first_name

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

    # Add web dashboard info for admins
    if is_admin:
        from config.config import WEB_SERVER_HOST, WEB_SERVER_PORT, ENABLE_WEB_SERVER
        if ENABLE_WEB_SERVER:
            help_text += (
                f"\n\n**Web Dashboard:**\n"
                f"A web dashboard is available at http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}\n"
                f"It shows system information and bot statistics."
            )

    await message.reply_text(help_text)

@Client.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    """
    Handle the /status command.
    """
    user_id = message.from_user.id

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

# Admin commands
@Client.on_message(filters.command("stats") & filters.user(ADMIN_USER_IDS))
async def stats_command(client: Client, message: Message):
    """
    Handle the /stats command (admin only).
    Shows system information and bot statistics.
    """
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
        f"FFmpeg: {bot_stats['ffmpeg_version']}\n\n"
    )

    # Format resource usage
    resources_text = (
        f"📈 **Resource Usage:**\n\n"
        f"CPU: {system_stats['cpu']['percent']}% ({system_stats['cpu']['count']} cores)\n"
        f"Memory: {system_stats['memory']['used_formatted']} / {system_stats['memory']['total_formatted']} ({system_stats['memory']['percent']}%)\n"
        f"Disk: {system_stats['disk']['used_formatted']} / {system_stats['disk']['total_formatted']} ({system_stats['disk']['percent']}%)\n\n"
    )

    # Format bot statistics
    bot_text = (
        f"📊 **Bot Statistics:**\n\n"
        f"Uptime: {bot_stats['uptime_formatted']}\n"
        f"Active Downloads: {bot_stats['active_downloads']}\n"
        f"Total Downloads: {bot_stats['total_downloads']}\n"
        f"Completed Downloads: {bot_stats['completed_downloads']}\n\n"
    )

    # Add resource manager statistics if enabled
    if RESOURCE_MONITOR_ENABLED:
        resource_mgr = get_resource_manager()
        resource_stats = resource_mgr.get_stats()

        resource_mgr_text = (
            f"🔄 **Resource Manager:**\n\n"
            f"CPU Threshold: {resource_stats['cpu_threshold']}%\n"
            f"Memory Threshold: {resource_stats['memory_threshold']}%\n"
            f"Max Concurrent Tasks: {resource_stats['max_concurrent_tasks']}\n"
            f"Current Concurrent Tasks: {resource_stats['current_concurrent_tasks']}\n"
            f"Queued Tasks: {resource_stats['queued_tasks']}\n"
            f"Throttling: {'Yes' if resource_stats['throttling'] else 'No'}\n\n"
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
@Client.on_message(filters.text & filters.private & ~filters.command)
async def handle_url(client: Client, message: Message):
    """
    Handle M3U8 URLs sent by users with enhanced security.
    """
    # Get and sanitize the URL
    url = message.text.strip()
    user_id = message.from_user.id

    # Log the request for security monitoring
    logger.info(f"URL request from user {user_id}: {url[:50]}{'...' if len(url) > 50 else ''}")

    # Check if the URL is valid with enhanced security checks
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

    # Generate a unique and secure filename
    filename = generate_unique_filename(user_id)

    # Log the download start for security auditing
    logger.info(f"Starting download for user {user_id}: {filename}")

    # Use resource manager if enabled, otherwise create a regular task
    if RESOURCE_MONITOR_ENABLED:
        # Get the resource manager
        resource_mgr = get_resource_manager()

        # Create a task using the resource manager
        download_task = asyncio.create_task(
            resource_mgr.run_task(
                process_download,
                client, message, status_message, url, filename, user_id
            )
        )

        logger.info(f"Download task for user {user_id} scheduled with resource manager")
    else:
        # Create a regular task
        download_task = asyncio.create_task(
            process_download(client, message, status_message, url, filename, user_id)
        )

        logger.info(f"Download task for user {user_id} scheduled without resource manager")

    # Store the task
    active_tasks[user_id] = download_task

    # Add callback to clean up when the task is done
    download_task.add_done_callback(
        lambda t: cleanup_task(t, user_id)
    )

async def process_download(client: Client, message: Message, status_message: Message,
                          url: str, filename: str, user_id: int):
    """
    Process an M3U8 download.

    Args:
        client: Pyrogram client
        message: Original message with the URL
        status_message: Message to update with status
        url: M3U8 URL
        filename: Output filename
        user_id: User ID
    """
    try:
        # Update status
        await status_message.edit_text(
            "⏳ Starting download...\n\n"
            "This may take a while depending on the video size."
        )

        # Create downloader
        downloader = M3U8Downloader(user_id)

        # Start download
        success, msg, output_path = await downloader.download_m3u8(url, filename)

        if not success or not output_path:
            await status_message.edit_text(
                f"❌ Download failed: {msg}"
            )
            return

        # Get video info
        await status_message.edit_text(
            "🔄 Processing video..."
        )

        video_info = await VideoProcessor.get_video_info(output_path)

        # Create thumbnail with secure path handling
        thumbnail_filename = sanitize_filename(f"thumb_{filename.replace('.mp4', '.jpg')}")
        thumbnail_path = os.path.abspath(os.path.join(os.path.dirname(output_path), thumbnail_filename))

        # Security check: ensure the thumbnail path is within the download directory
        if not thumbnail_path.startswith(os.path.abspath(os.path.dirname(output_path))):
            logger.error(f"Path traversal attempt detected in thumbnail path: {thumbnail_filename}")
            thumbnail_path = os.path.join(os.path.dirname(output_path), "thumbnail.jpg")

        await VideoProcessor.create_thumbnail(output_path, thumbnail_path)

        # Send the video
        await status_message.edit_text(
            "📤 Uploading video to Telegram..."
        )

        # Format video information
        duration = int(video_info.get('duration', 0))
        width = video_info.get('width', 0)
        height = video_info.get('height', 0)
        file_size = video_info.get('size', 0)

        # Send as video if possible, otherwise as document
        try:
            if os.path.exists(output_path):
                if os.path.exists(thumbnail_path):
                    await client.send_video(
                        chat_id=message.chat.id,
                        video=output_path,
                        duration=duration,
                        width=width,
                        height=height,
                        thumb=thumbnail_path,
                        caption=f"📹 **Video Downloaded**\n\n"
                                f"🔗 **Source:** M3U8 Stream\n"
                                f"⏱️ **Duration:** {duration} seconds\n"
                                f"📏 **Resolution:** {width}x{height}\n"
                                f"📦 **Size:** {format_size(file_size)}",
                        reply_to_message_id=message.id
                    )
                else:
                    await client.send_video(
                        chat_id=message.chat.id,
                        video=output_path,
                        duration=duration,
                        width=width,
                        height=height,
                        caption=f"📹 **Video Downloaded**\n\n"
                                f"🔗 **Source:** M3U8 Stream\n"
                                f"⏱️ **Duration:** {duration} seconds\n"
                                f"📏 **Resolution:** {width}x{height}\n"
                                f"📦 **Size:** {format_size(file_size)}",
                        reply_to_message_id=message.id
                    )

                # Increment completed downloads counter
                global TOTAL_COMPLETED_DOWNLOADS
                TOTAL_COMPLETED_DOWNLOADS += 1

                await status_message.edit_text(
                    "✅ Download completed and video sent!"
                )
            else:
                await status_message.edit_text(
                    "❌ Error: Output file not found."
                )
        except Exception as e:
            logger.error(f"Error sending video: {str(e)}")

            # Try sending as document if video sending fails
            try:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=output_path,
                    caption=f"📹 **Video Downloaded**\n\n"
                            f"🔗 **Source:** M3U8 Stream\n"
                            f"⏱️ **Duration:** {duration} seconds\n"
                            f"📏 **Resolution:** {width}x{height}\n"
                            f"📦 **Size:** {format_size(file_size)}",
                    reply_to_message_id=message.id
                )

                # Increment completed downloads counter
                global TOTAL_COMPLETED_DOWNLOADS
                TOTAL_COMPLETED_DOWNLOADS += 1

                await status_message.edit_text(
                    "✅ Download completed and sent as document!"
                )
            except Exception as doc_e:
                logger.error(f"Error sending document: {str(doc_e)}")
                await status_message.edit_text(
                    f"❌ Error sending file: {str(doc_e)}"
                )

        # Clean up files securely
        try:
            # Security check: ensure we're only deleting files in the download directory
            download_dir = os.path.abspath(os.path.dirname(output_path))

            if os.path.exists(output_path) and os.path.abspath(output_path).startswith(download_dir):
                os.remove(output_path)
                logger.debug(f"Removed output file: {output_path}")
            else:
                logger.warning(f"Skipped removal of suspicious output path: {output_path}")

            if os.path.exists(thumbnail_path) and os.path.abspath(thumbnail_path).startswith(download_dir):
                os.remove(thumbnail_path)
                logger.debug(f"Removed thumbnail file: {thumbnail_path}")
            else:
                logger.warning(f"Skipped removal of suspicious thumbnail path: {thumbnail_path}")

        except Exception as e:
            logger.error(f"Error cleaning up files: {str(e)}")

    except asyncio.CancelledError:
        # Handle cancellation
        await status_message.edit_text(
            "❌ Download cancelled by user."
        )
        raise
    except Exception as e:
        logger.error(f"Error processing download: {str(e)}")
        await status_message.edit_text(
            f"❌ An error occurred: {str(e)}"
        )
    finally:
        # Clean up active downloads
        if user_id in active_downloads:
            del active_downloads[user_id]

def cleanup_task(task, user_id):
    """
    Clean up a completed task.

    Args:
        task: The completed task
        user_id: User ID
    """
    if user_id in active_tasks:
        del active_tasks[user_id]

    # Handle any exceptions
    if not task.cancelled() and task.exception():
        logger.error(f"Task for user {user_id} failed with exception: {task.exception()}")
