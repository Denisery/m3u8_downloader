# Cross-Platform Compatibility Guide

The M3U8 Downloader Bot is designed to work on multiple platforms, including Windows, Linux, and macOS. This guide explains how to ensure compatibility across different operating systems.

## Platform-Specific Considerations

### Windows

Windows users may encounter specific issues when running the bot:

#### TGCrypto Dependency

The `TGCrypto` package requires Microsoft Visual C++ to build on Windows. To avoid this issue, the bot's requirements.txt file includes a platform-specific conditional:

```
# Telegram API
pyrogram>=2.0.106,<3.0.0
# TGCrypto is optional on Windows but recommended on other platforms
tgcrypto>=1.2.5,<2.0.0; sys_platform != 'win32'
```

This ensures that Windows users can install the dependencies without requiring Microsoft Visual C++.

#### Path Handling

Windows uses backslashes (`\`) for file paths, while Unix-based systems use forward slashes (`/`). The bot handles this difference using `os.path` functions:

```python
import os

# Platform-independent path joining
output_path = os.path.join(self.download_path, output_filename)
```

#### Command Execution

When executing external commands like FFmpeg, the bot detects the platform and adjusts the command accordingly:

```python
import platform

def get_ffmpeg_command(input_file, output_file):
    """
    Get the FFmpeg command based on the platform.
    """
    base_command = ['ffmpeg', '-i', input_file, '-c', 'copy', output_file]
    
    if platform.system() == 'Windows':
        # Use shell=True on Windows
        return ' '.join(base_command), True
    else:
        # Use shell=False on Unix-based systems
        return base_command, False
```

### Linux

Linux is the primary development platform for the bot and generally has the best compatibility.

#### FFmpeg Installation

On Linux, FFmpeg can be installed using the package manager:

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install ffmpeg

# CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

#### File Permissions

The bot sets appropriate file permissions on Linux:

```python
# Set secure permissions (only owner can read/write/execute)
try:
    os.chmod(temp_dir, 0o700)
except Exception as e:
    logger.warning(f"Could not set secure permissions on temp dir: {str(e)}")
```

### macOS

macOS is similar to Linux in terms of compatibility, with a few differences:

#### FFmpeg Installation

On macOS, FFmpeg can be installed using Homebrew:

```bash
brew install ffmpeg
```

## Cross-Platform Implementation

### System Checks

The bot includes system checks to ensure compatibility:

```python
def check_ffmpeg():
    """
    Check if FFmpeg is installed and get its version.
    """
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['ffmpeg', '-version'], 
                                   capture_output=True, 
                                   text=True, 
                                   shell=True)
        else:
            result = subprocess.run(['ffmpeg', '-version'], 
                                   capture_output=True, 
                                   text=True)
        
        if result.returncode == 0:
            # Extract version from output
            version_match = re.search(r'ffmpeg version (\S+)', result.stdout)
            if version_match:
                return True, version_match.group(1)
            return True, "Unknown version"
        else:
            return False, None
    except Exception as e:
        logger.error(f"Error checking FFmpeg: {str(e)}")
        return False, None
```

### Platform Detection

The bot detects the platform and adjusts its behavior accordingly:

```python
def get_platform_info():
    """
    Get platform information.
    """
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
    }
```

### Temporary Directory Handling

The bot uses the `tempfile` module for cross-platform temporary directory creation:

```python
import tempfile

# Create a temporary directory
temp_dir = tempfile.mkdtemp(prefix=f"m3u8_{user_id}_")
```

## Docker for Cross-Platform Deployment

Docker provides a consistent environment across platforms. See the [Docker Guide](/docs/docker) for more details.

## Troubleshooting Cross-Platform Issues

### Windows-Specific Issues

#### FFmpeg Not Found

Ensure FFmpeg is installed and added to your PATH:

1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the files to a folder (e.g., `C:\ffmpeg`)
3. Add the `bin` folder to your PATH:
   - Right-click on "This PC" or "My Computer" and select "Properties"
   - Click on "Advanced system settings"
   - Click on "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add the path to the `bin` folder (e.g., `C:\ffmpeg\bin`)
   - Click "OK" on all dialogs

#### TGCrypto Installation Errors

If you encounter errors installing TGCrypto:

1. Skip TGCrypto installation on Windows:
   ```bash
   pip install -r requirements.txt
   ```

2. The bot will work without TGCrypto, but with slightly reduced performance.

### Linux-Specific Issues

#### Permission Denied

If you encounter permission issues:

1. Ensure the user running the bot has appropriate permissions:
   ```bash
   sudo chown -R yourusername:yourusername /path/to/m3u8_downloader
   ```

2. Make the Python script executable:
   ```bash
   chmod +x main.py
   ```

### macOS-Specific Issues

#### FFmpeg Installation

If you encounter issues with FFmpeg on macOS:

1. Try installing with Homebrew:
   ```bash
   brew install ffmpeg
   ```

2. If Homebrew is not installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

## Best Practices for Cross-Platform Development

1. **Use os.path for file paths**: Always use `os.path.join()` for path construction
2. **Check platform before platform-specific code**: Use `platform.system()` to detect the platform
3. **Handle file permissions appropriately**: Be aware of different permission models
4. **Use try-except for platform-specific operations**: Catch exceptions for operations that might fail on certain platforms
5. **Test on all target platforms**: Regularly test the bot on Windows, Linux, and macOS
6. **Use Docker for consistent deployment**: Docker provides a consistent environment across platforms
