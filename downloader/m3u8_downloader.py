import os
import sys
import logging
import asyncio
import tempfile
import m3u8
import platform
import subprocess
import secrets
import hashlib
from typing import Optional, Dict, List, Tuple, Any
import aiohttp
import aiofiles
from urllib.parse import urljoin
import time

from config.config import (
    DOWNLOAD_PATH, CHUNK_SIZE, MAX_DOWNLOAD_SIZE, DOWNLOAD_TIMEOUT,
    CONNECTION_POOL_MAX_CONNECTIONS, CONNECTION_POOL_MAX_KEEPALIVE,
    CONNECTION_POOL_TTL_DNS_CACHE, CONNECTION_POOL_TIMEOUT,
    CONNECTION_POOL_CONNECT_TIMEOUT,
    CACHE_ENABLED, CACHE_TTL, CACHE_MAX_SIZE
)
from utils.helpers import (
    active_downloads, fetch_content, sanitize_filename,
    create_secure_temp_dir
)
from utils.connection_pool import get_connection_pool
from utils.cache_manager import get_cache_manager
from utils.system_checks import check_ffmpeg

# Configure logging
logger = logging.getLogger(__name__)

class M3U8Downloader:
    """
    A class for downloading M3U8 playlists and their segments.
    """

    def __init__(self, user_id: int):
        """
        Initialize the M3U8 downloader with secure file handling.

        Args:
            user_id: Telegram user ID of the requester
        """
        self.user_id = user_id

        # Create a secure temporary directory with randomized name
        self.temp_dir = create_secure_temp_dir(user_id)

        # Ensure download path is secure
        self.download_path = os.path.abspath(DOWNLOAD_PATH)
        self.chunk_size = CHUNK_SIZE
        self.max_size = MAX_DOWNLOAD_SIZE
        self.timeout = DOWNLOAD_TIMEOUT
        self.start_time = 0
        self.total_segments = 0
        self.downloaded_segments = 0
        self.total_size = 0
        self.download_status = {}

        # Create download directory if it doesn't exist and set secure permissions
        try:
            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path, exist_ok=True)
                # Set secure permissions (only owner can read/write/execute)
                os.chmod(self.download_path, 0o700)
            elif os.access(self.download_path, os.W_OK):
                # If directory exists, ensure it has secure permissions
                os.chmod(self.download_path, 0o700)
        except Exception as e:
            logger.warning(f"Could not set secure permissions on download directory: {str(e)}")

    async def download_m3u8(self, url: str, output_filename: str) -> Tuple[bool, str, Optional[str]]:
        """
        Download an M3U8 playlist and all its segments with enhanced security.

        Args:
            url: M3U8 URL
            output_filename: Output filename (will be sanitized)

        Returns:
            Tuple[bool, str, Optional[str]]: (success, message, output_path if successful)
        """
        try:
            # Validate URL
            if not url or not isinstance(url, str):
                return False, "Invalid URL provided", None

            # Sanitize the output filename to prevent path traversal
            safe_filename = sanitize_filename(output_filename)
            if safe_filename != output_filename:
                logger.warning(f"Filename sanitized: {output_filename} -> {safe_filename}")
                output_filename = safe_filename

            # Ensure the output path is within the download directory
            output_path = os.path.abspath(os.path.join(self.download_path, output_filename))
            if not output_path.startswith(os.path.abspath(self.download_path)):
                logger.error(f"Path traversal attempt detected: {output_filename}")
                return False, "Invalid filename", None

            self.start_time = time.time()

            # Register this download
            active_downloads[self.user_id] = {
                'url': url,
                'filename': output_filename,
                'start_time': self.start_time,
                'progress': 0,
                'status': 'downloading'
            }

            # Try to get the M3U8 playlist from cache first if caching is enabled
            content = None
            if CACHE_ENABLED:
                cache = get_cache_manager(
                    cache_dir=os.path.join(DOWNLOAD_PATH, 'cache'),
                    ttl=CACHE_TTL,
                    max_size=CACHE_MAX_SIZE
                )
                content = await cache.get(url)
                if content:
                    logger.info(f"Using cached M3U8 content for {url}")

            # If not in cache or caching is disabled, fetch from the URL
            if not content:
                content = await fetch_content(url)
                if not content:
                    return False, "Failed to fetch M3U8 content", None

                # Cache the content if caching is enabled
                if CACHE_ENABLED:
                    await cache.set(url, content)
                    logger.info(f"Cached M3U8 content for {url}")

            playlist = m3u8.loads(content)

            # Handle master playlist (with multiple quality options)
            if playlist.is_variant:
                # Choose the highest quality stream
                playlist_url = self._get_best_playlist_url(playlist, url)
                if not playlist_url:
                    return False, "No valid streams found in the master playlist", None

                # Try to get the actual playlist from cache first if caching is enabled
                content = None
                if CACHE_ENABLED:
                    cache = get_cache_manager(
                        cache_dir=os.path.join(DOWNLOAD_PATH, 'cache'),
                        ttl=CACHE_TTL,
                        max_size=CACHE_MAX_SIZE
                    )
                    content = await cache.get(playlist_url)
                    if content:
                        logger.info(f"Using cached M3U8 content for {playlist_url}")

                # If not in cache or caching is disabled, fetch from the URL
                if not content:
                    content = await fetch_content(playlist_url)
                    if not content:
                        return False, f"Failed to fetch playlist: {playlist_url}", None

                    # Cache the content if caching is enabled
                    if CACHE_ENABLED:
                        await cache.set(playlist_url, content)
                        logger.info(f"Cached M3U8 content for {playlist_url}")

                playlist = m3u8.loads(content)
                base_url = self._get_base_url(playlist_url)
            else:
                base_url = self._get_base_url(url)

            # Download all segments
            self.total_segments = len(playlist.segments)
            if self.total_segments == 0:
                return False, "No segments found in the playlist", None

            output_path = os.path.join(self.download_path, output_filename)
            result = await self._download_segments(playlist, base_url, output_path)

            # Clean up
            self._cleanup()

            if result[0]:
                active_downloads[self.user_id]['status'] = 'completed'
                active_downloads[self.user_id]['progress'] = 100
                return True, f"Download completed: {output_filename}", output_path
            else:
                active_downloads[self.user_id]['status'] = 'failed'
                return False, result[1], None

        except Exception as e:
            logger.error(f"Error downloading M3U8: {str(e)}")
            if self.user_id in active_downloads:
                active_downloads[self.user_id]['status'] = 'failed'
            self._cleanup()
            return False, f"Error downloading M3U8: {str(e)}", None

    async def _download_segments(self, playlist: m3u8.M3U8, base_url: str, output_path: str) -> Tuple[bool, str]:
        """
        Download all segments from a playlist and merge them using the connection pool.

        Args:
            playlist: M3U8 playlist object
            base_url: Base URL for resolving relative segment URLs
            output_path: Path to save the merged file

        Returns:
            Tuple[bool, str]: (success, message)
        """
        segment_files = []
        self.downloaded_segments = 0

        try:
            # Get the connection pool
            pool = get_connection_pool(
                max_connections=CONNECTION_POOL_MAX_CONNECTIONS,
                max_keepalive_connections=CONNECTION_POOL_MAX_KEEPALIVE,
                ttl_dns_cache=CONNECTION_POOL_TTL_DNS_CACHE,
                timeout=CONNECTION_POOL_TIMEOUT,
                connection_timeout=CONNECTION_POOL_CONNECT_TIMEOUT
            )

            # Download each segment using the connection pool
            download_tasks = []

            for i, segment in enumerate(playlist.segments):
                segment_url = self._resolve_url(base_url, segment.uri)
                segment_path = os.path.join(self.temp_dir, f"segment_{i:05d}.ts")
                segment_files.append(segment_path)

                task = asyncio.create_task(
                    self._download_segment(pool, segment_url, segment_path, i)
                )
                download_tasks.append(task)

            # Wait for all downloads to complete with timeout
            try:
                await asyncio.wait_for(asyncio.gather(*download_tasks), timeout=self.timeout)
            except asyncio.TimeoutError:
                return False, f"Download timed out after {self.timeout} seconds"

            # Check if all segments were downloaded
            if self.downloaded_segments < self.total_segments:
                return False, f"Only {self.downloaded_segments}/{self.total_segments} segments were downloaded"

            # Merge segments
            return await self._merge_segments(segment_files, output_path)

        except Exception as e:
            logger.error(f"Error downloading segments: {str(e)}")
            return False, f"Error downloading segments: {str(e)}"

    async def _download_segment(self, pool, url: str, path: str, index: int) -> bool:
        """
        Download a single segment using the connection pool.

        Args:
            pool: Connection pool instance
            url: Segment URL
            path: Path to save the segment
            index: Segment index

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            async with pool.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Failed to download segment {index}: HTTP {response.status}")
                    return False

                # Check content length if available
                content_length = response.content_length
                if content_length and self.total_size + content_length > self.max_size:
                    logger.error(f"Download would exceed maximum size limit of {self.max_size} bytes")
                    return False

                async with aiofiles.open(path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(self.chunk_size):
                        await f.write(chunk)
                        self.total_size += len(chunk)

                        # Check if we've exceeded the maximum size
                        if self.total_size > self.max_size:
                            logger.error(f"Download exceeded maximum size limit of {self.max_size} bytes")
                            return False

            self.downloaded_segments += 1

            # Update progress
            if self.user_id in active_downloads:
                progress = int((self.downloaded_segments / self.total_segments) * 100)
                active_downloads[self.user_id]['progress'] = progress

            return True

        except Exception as e:
            logger.error(f"Error downloading segment {index}: {str(e)}")
            return False

    async def _merge_segments(self, segment_files: List[str], output_path: str) -> Tuple[bool, str]:
        """
        Merge downloaded segments into a single file.

        Args:
            segment_files: List of segment file paths
            output_path: Path to save the merged file

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Check if FFmpeg is available
            ffmpeg_available, ffmpeg_message = check_ffmpeg()
            if not ffmpeg_available:
                logger.error(f"FFmpeg not available: {ffmpeg_message}")
                return False, f"FFmpeg not available: {ffmpeg_message}"

            # Create a file list for ffmpeg
            file_list_path = os.path.join(self.temp_dir, "filelist.txt")

            # Use platform-safe path handling
            file_list_path = os.path.normpath(file_list_path)

            async with aiofiles.open(file_list_path, 'w') as f:
                for segment_file in segment_files:
                    if os.path.exists(segment_file):
                        # Normalize path for the current platform
                        normalized_path = os.path.normpath(segment_file)
                        # Escape backslashes in Windows paths for the filelist.txt
                        if platform.system().lower() == 'windows':
                            normalized_path = normalized_path.replace('\\', '\\\\')
                        await f.write(f"file '{normalized_path}'\n")

            # Use ffmpeg to concatenate the segments
            cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', file_list_path, '-c', 'copy', output_path
            ]

            # Create process with appropriate settings for the platform
            try:
                # For Windows, we need to set shell=True if ffmpeg is not in PATH
                if platform.system().lower() == 'windows':
                    process = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, errors='replace'
                    )
                else:
                    process = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, errors='replace'
                    )

                _, stderr = process.communicate(timeout=self.timeout)

                if process.returncode != 0:
                    logger.error(f"FFmpeg error: {stderr}")
                    return False, f"Error merging segments: FFmpeg failed with code {process.returncode}"

                return True, "Segments merged successfully"

            except subprocess.TimeoutExpired:
                process.kill()
                logger.error("FFmpeg process timed out")
                return False, "FFmpeg process timed out"

        except Exception as e:
            logger.error(f"Error merging segments: {str(e)}")
            return False, f"Error merging segments: {str(e)}"

    def _get_best_playlist_url(self, playlist: m3u8.M3U8, base_url: str) -> Optional[str]:
        """
        Get the URL of the highest quality playlist from a master playlist.

        Args:
            playlist: M3U8 master playlist
            base_url: Base URL for resolving relative URLs

        Returns:
            Optional[str]: URL of the highest quality playlist or None
        """
        if not playlist.playlists:
            return None

        # Sort playlists by bandwidth (highest first)
        sorted_playlists = sorted(
            playlist.playlists,
            key=lambda p: p.stream_info.bandwidth if p.stream_info else 0,
            reverse=True
        )

        # Return the URL of the highest bandwidth playlist
        for p in sorted_playlists:
            return self._resolve_url(base_url, p.uri)

        return None

    def _get_base_url(self, url: str) -> str:
        """
        Extract the base URL from a playlist URL.

        Args:
            url: Playlist URL

        Returns:
            str: Base URL
        """
        return url.rsplit('/', 1)[0] + '/'

    def _resolve_url(self, base_url: str, uri: str) -> str:
        """
        Resolve a relative URI against a base URL.

        Args:
            base_url: Base URL
            uri: Relative or absolute URI

        Returns:
            str: Resolved URL
        """
        if uri.startswith('http://') or uri.startswith('https://'):
            return uri
        return urljoin(base_url, uri)

    def _cleanup(self) -> None:
        """
        Securely clean up temporary files.
        """
        try:
            # Ensure the temp directory exists and is within the expected path format
            if not self.temp_dir or not os.path.exists(self.temp_dir):
                return

            # Security check: ensure the temp directory follows our naming pattern
            # This prevents accidental deletion of important directories
            if not os.path.basename(self.temp_dir).startswith(('m3u8_', 'tmp')):
                logger.warning(f"Refusing to delete suspicious temp directory: {self.temp_dir}")
                return

            # Delete all files in the temp directory first
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"Error removing file {file}: {str(e)}")

            # Then remove the directory
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)

            logger.debug(f"Temporary directory cleaned up: {self.temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {str(e)}")

    def get_progress(self) -> Dict[str, Any]:
        """
        Get the current download progress.

        Returns:
            Dict[str, Any]: Progress information
        """
        elapsed_time = time.time() - self.start_time
        progress = 0
        if self.total_segments > 0:
            progress = int((self.downloaded_segments / self.total_segments) * 100)

        return {
            'progress': progress,
            'downloaded_segments': self.downloaded_segments,
            'total_segments': self.total_segments,
            'elapsed_time': elapsed_time,
            'total_size': self.total_size
        }
