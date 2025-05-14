import os
import logging
import subprocess
import platform
import shutil
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def check_ffmpeg() -> Tuple[bool, Optional[str]]:
    """
    Check if FFmpeg is installed and available in the system PATH.
    
    Returns:
        Tuple[bool, Optional[str]]: (is_available, version_or_error_message)
    """
    try:
        # First try using shutil which is cross-platform
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            # Get version info
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Extract the first line which contains the version
                version = result.stdout.split('\n')[0]
                logger.info(f"FFmpeg found: {version}")
                return True, version
        
        # If shutil.which failed, try platform-specific approaches
        system = platform.system().lower()
        
        if system == "windows":
            # On Windows, check common installation paths
            common_paths = [
                r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
                r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
                r"C:\ffmpeg\bin\ffmpeg.exe"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    logger.info(f"FFmpeg found at: {path}")
                    return True, f"FFmpeg found at: {path}"
                    
            return False, "FFmpeg not found. Please install FFmpeg and add it to your PATH."
            
        elif system in ["linux", "darwin"]:  # Linux or macOS
            # Try common package manager paths
            common_paths = [
                "/usr/bin/ffmpeg",
                "/usr/local/bin/ffmpeg",
                "/opt/local/bin/ffmpeg",
                "/opt/homebrew/bin/ffmpeg"  # Homebrew on Apple Silicon
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    logger.info(f"FFmpeg found at: {path}")
                    return True, f"FFmpeg found at: {path}"
                    
            return False, "FFmpeg not found. Please install FFmpeg using your package manager."
            
        else:
            return False, f"Unsupported operating system: {system}"
            
    except Exception as e:
        logger.error(f"Error checking FFmpeg: {str(e)}")
        return False, f"Error checking FFmpeg: {str(e)}"

def get_platform_info() -> dict:
    """
    Get information about the current platform.
    
    Returns:
        dict: Platform information
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
