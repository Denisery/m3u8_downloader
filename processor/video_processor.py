import os
import sys
import logging
import asyncio
import subprocess
import platform
import json
from typing import Dict, Any, Tuple, Optional

from utils.system_checks import check_ffmpeg

# Configure logging
logger = logging.getLogger(__name__)

class VideoProcessor:
    """
    A class for processing video files.
    """

    @staticmethod
    async def get_video_info(file_path: str) -> Dict[str, Any]:
        """
        Get information about a video file using ffprobe.

        Args:
            file_path: Path to the video file

        Returns:
            Dict[str, Any]: Video information
        """
        try:
            # Check if FFmpeg is available
            ffmpeg_available, ffmpeg_message = check_ffmpeg()
            if not ffmpeg_available:
                logger.error(f"FFmpeg not available: {ffmpeg_message}")
                return {
                    'duration': 0,
                    'width': 0,
                    'height': 0,
                    'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                    'format': 'unknown',
                    'error': f"FFmpeg not available: {ffmpeg_message}"
                }

            # Normalize file path for the current platform
            file_path = os.path.normpath(file_path)

            cmd = [
                'ffprobe', '-v', 'error', '-show_entries',
                'format=duration,size,bit_rate:stream=width,height,codec_name,codec_type',
                '-of', 'json', file_path
            ]

            # Use different approaches based on platform
            if platform.system().lower() == 'windows':
                # On Windows, we need to handle potential path issues
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
            else:
                # Standard approach for Unix-like systems
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='replace')
                logger.error(f"FFprobe error: {error_msg}")
                return {
                    'duration': 0,
                    'width': 0,
                    'height': 0,
                    'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                    'format': 'unknown',
                    'error': f"FFprobe error: {error_msg}"
                }

            data = json.loads(stdout.decode('utf-8', errors='replace'))

            # Extract relevant information
            info = {
                'duration': float(data.get('format', {}).get('duration', 0)),
                'size': int(data.get('format', {}).get('size', 0)),
                'bit_rate': int(data.get('format', {}).get('bit_rate', 0)),
                'format': data.get('format', {}).get('format_name', 'unknown'),
                'streams': []
            }

            # Process streams
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'video':
                    info['width'] = int(stream.get('width', 0))
                    info['height'] = int(stream.get('height', 0))
                    info['video_codec'] = stream.get('codec_name', 'unknown')
                elif stream.get('codec_type') == 'audio':
                    info['audio_codec'] = stream.get('codec_name', 'unknown')

                info['streams'].append({
                    'codec_type': stream.get('codec_type', 'unknown'),
                    'codec_name': stream.get('codec_name', 'unknown'),
                    'width': int(stream.get('width', 0)) if 'width' in stream else None,
                    'height': int(stream.get('height', 0)) if 'height' in stream else None
                })

            return info

        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return {
                'duration': 0,
                'width': 0,
                'height': 0,
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                'format': 'unknown',
                'error': str(e)
            }

    @staticmethod
    async def convert_video(input_path: str, output_path: str, target_format: str = 'mp4',
                           max_size: Optional[int] = None) -> Tuple[bool, str]:
        """
        Convert a video file to a different format or resize it.

        Args:
            input_path: Path to the input video file
            output_path: Path to save the output video file
            target_format: Target video format (default: mp4)
            max_size: Maximum file size in bytes (optional)

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Check if FFmpeg is available
            ffmpeg_available, ffmpeg_message = check_ffmpeg()
            if not ffmpeg_available:
                logger.error(f"FFmpeg not available: {ffmpeg_message}")
                return False, f"FFmpeg not available: {ffmpeg_message}"

            # Normalize file paths for the current platform
            input_path = os.path.normpath(input_path)
            output_path = os.path.normpath(output_path)

            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            # Base command for conversion
            cmd = ['ffmpeg', '-y', '-i', input_path, '-c:v', 'libx264', '-c:a', 'aac']

            # If max_size is specified, adjust bitrate accordingly
            if max_size:
                # Get video info
                info = await VideoProcessor.get_video_info(input_path)
                duration = info.get('duration', 0)

                if duration > 0:
                    # Calculate target bitrate (80% of max_size for video, 20% for audio)
                    # Convert to kilobits
                    target_bitrate = int((max_size * 8 * 0.8) / duration / 1000)
                    audio_bitrate = int((max_size * 8 * 0.2) / duration / 1000)

                    # Add bitrate parameters
                    cmd.extend(['-b:v', f'{target_bitrate}k', '-b:a', f'{audio_bitrate}k'])

            # Add output path
            cmd.append(output_path)

            # Run the command with platform-specific settings
            if platform.system().lower() == 'windows':
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
            else:
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='replace')
                logger.error(f"FFmpeg error: {error_msg}")
                return False, f"Error converting video: FFmpeg failed with code {process.returncode}"

            # Verify the output file exists
            if not os.path.exists(output_path):
                return False, "Error: Output file was not created"

            return True, "Video converted successfully"

        except Exception as e:
            logger.error(f"Error converting video: {str(e)}")
            return False, f"Error converting video: {str(e)}"

    @staticmethod
    async def create_thumbnail(video_path: str, thumbnail_path: str,
                              time_offset: float = 5.0) -> Tuple[bool, str]:
        """
        Create a thumbnail from a video file.

        Args:
            video_path: Path to the video file
            thumbnail_path: Path to save the thumbnail
            time_offset: Time offset in seconds (default: 5.0)

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Check if FFmpeg is available
            ffmpeg_available, ffmpeg_message = check_ffmpeg()
            if not ffmpeg_available:
                logger.error(f"FFmpeg not available: {ffmpeg_message}")
                return False, f"FFmpeg not available: {ffmpeg_message}"

            # Normalize file paths for the current platform
            video_path = os.path.normpath(video_path)
            thumbnail_path = os.path.normpath(thumbnail_path)

            # Ensure output directory exists
            thumbnail_dir = os.path.dirname(thumbnail_path)
            if thumbnail_dir and not os.path.exists(thumbnail_dir):
                os.makedirs(thumbnail_dir, exist_ok=True)

            # Get video info to check duration
            info = await VideoProcessor.get_video_info(video_path)
            duration = info.get('duration', 0)

            # If video is shorter than time_offset, use the middle point
            if duration > 0 and duration < time_offset:
                time_offset = duration / 2

            # Create thumbnail command
            cmd = [
                'ffmpeg', '-y', '-ss', str(time_offset), '-i', video_path,
                '-vframes', '1', '-q:v', '2', thumbnail_path
            ]

            # Run the command with platform-specific settings
            if platform.system().lower() == 'windows':
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
            else:
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='replace')
                logger.error(f"FFmpeg error: {error_msg}")
                return False, f"Error creating thumbnail: FFmpeg failed with code {process.returncode}"

            # Verify the output file exists
            if not os.path.exists(thumbnail_path):
                return False, "Error: Thumbnail file was not created"

            return True, "Thumbnail created successfully"

        except Exception as e:
            logger.error(f"Error creating thumbnail: {str(e)}")
            return False, f"Error creating thumbnail: {str(e)}"
