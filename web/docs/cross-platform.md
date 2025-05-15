<div align="center">

# 💻 Cross-Platform Compatibility Guide

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/display.svg" alt="Cross-Platform" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Run your M3U8 Downloader Bot on any operating system*

</div>

---

The M3U8 Downloader Bot is designed to work on multiple platforms, including Windows, Linux, and macOS. This guide explains how to ensure compatibility across different operating systems.

## 🖥️ Platform-Specific Considerations

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/computer.svg" alt="Platforms" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/windows.svg" width="25" height="25" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/> Windows

Windows users may encounter specific issues when running the bot:

#### TGCrypto Dependency

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/puzzle-piece.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The `TGCrypto` package requires Microsoft Visual C++ to build on Windows. To avoid this issue, the bot's requirements.txt file includes a platform-specific conditional:

<div align="center">

```python
# Telegram API
pyrogram>=2.0.106,<3.0.0
# TGCrypto is optional on Windows but recommended on other platforms
tgcrypto>=1.2.5,<2.0.0; sys_platform != 'win32'
```

</div>

> 💡 **Tip:** This ensures that Windows users can install the dependencies without requiring Microsoft Visual C++.

#### Path Handling

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/folder-tree.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Windows uses backslashes (`\`) for file paths, while Unix-based systems use forward slashes (`/`). The bot handles this difference using `os.path` functions:

<div align="center">

```python
import os

# Platform-independent path joining
output_path = os.path.join(self.download_path, output_filename)
```

</div>

#### Command Execution

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/terminal.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

When executing external commands like FFmpeg, the bot detects the platform and adjusts the command accordingly:

<div align="center">

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

</div>

### <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/linux.svg" width="25" height="25" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/> Linux

Linux is the primary development platform for the bot and generally has the best compatibility.

#### FFmpeg Installation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/film.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

On Linux, FFmpeg can be installed using the package manager:

<table>
  <tr>
    <th>Distribution</th>
    <th>Command</th>
  </tr>
  <tr>
    <td>Debian/Ubuntu</td>
    <td>
      <code>sudo apt-get update</code><br>
      <code>sudo apt-get install ffmpeg</code>
    </td>
  </tr>
  <tr>
    <td>CentOS/RHEL</td>
    <td>
      <code>sudo yum install epel-release</code><br>
      <code>sudo yum install ffmpeg</code>
    </td>
  </tr>
  <tr>
    <td>Fedora</td>
    <td>
      <code>sudo dnf install ffmpeg</code>
    </td>
  </tr>
</table>

#### File Permissions

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/lock.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot sets appropriate file permissions on Linux:

<div align="center">

```python
# Set secure permissions (only owner can read/write/execute)
try:
    os.chmod(temp_dir, 0o700)
except Exception as e:
    logger.warning(f"Could not set secure permissions on temp dir: {str(e)}")
```

</div>

### <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/apple.svg" width="25" height="25" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/> macOS

macOS is similar to Linux in terms of compatibility, with a few differences:

#### FFmpeg Installation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/apple.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

On macOS, FFmpeg can be installed using Homebrew:

<div align="center">

```bash
brew install ffmpeg
```

</div>

## 🔄 Cross-Platform Implementation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/code.svg" alt="Implementation" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### System Checks

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/check-circle.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot includes system checks to ensure compatibility:

<div align="center">

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

</div>

### Platform Detection

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/magnifying-glass.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot detects the platform and adjusts its behavior accordingly:

<div align="center">

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

</div>

### Temporary Directory Handling

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/folder.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot uses the `tempfile` module for cross-platform temporary directory creation:

<div align="center">

```python
import tempfile

# Create a temporary directory
temp_dir = tempfile.mkdtemp(prefix=f"m3u8_{user_id}_")
```

</div>

## 🐳 Docker for Cross-Platform Deployment

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Docker" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

Docker provides a consistent environment across platforms. See the [Docker Guide](/docs/docker) for more details.

> 💡 **Tip:** Using Docker eliminates most cross-platform issues by providing a consistent Linux-based environment regardless of the host operating system.

## 🔍 Troubleshooting Cross-Platform Issues

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/screwdriver-wrench.svg" alt="Troubleshooting" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Windows-Specific Issues

<details open>
<summary><b>FFmpeg Not Found</b></summary>

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

</details>

<details open>
<summary><b>TGCrypto Installation Errors</b></summary>

If you encounter errors installing TGCrypto:

1. Skip TGCrypto installation on Windows:
   ```bash
   pip install -r requirements.txt
   ```

2. The bot will work without TGCrypto, but with slightly reduced performance.

</details>

### Linux-Specific Issues

<details open>
<summary><b>Permission Denied</b></summary>

If you encounter permission issues:

1. Ensure the user running the bot has appropriate permissions:
   ```bash
   sudo chown -R Denisery:Denisery /path/to/m3u8_downloader
   ```

2. Make the Python script executable:
   ```bash
   chmod +x main.py
   ```

</details>

### macOS-Specific Issues

<details open>
<summary><b>FFmpeg Installation</b></summary>

If you encounter issues with FFmpeg on macOS:

1. Try installing with Homebrew:
   ```bash
   brew install ffmpeg
   ```

2. If Homebrew is not installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

</details>

## 💡 Best Practices for Cross-Platform Development

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/lightbulb.svg" alt="Best Practices" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="10%">Icon</th>
    <th width="30%">Practice</th>
    <th width="60%">Description</th>
  </tr>
  <tr>
    <td align="center">🔄</td>
    <td><strong>Use os.path for file paths</strong></td>
    <td>Always use <code>os.path.join()</code> for path construction to ensure compatibility across platforms</td>
  </tr>
  <tr>
    <td align="center">🔍</td>
    <td><strong>Check platform before platform-specific code</strong></td>
    <td>Use <code>platform.system()</code> to detect the platform before executing platform-specific code</td>
  </tr>
  <tr>
    <td align="center">🔒</td>
    <td><strong>Handle file permissions appropriately</strong></td>
    <td>Be aware of different permission models between Windows and Unix-based systems</td>
  </tr>
  <tr>
    <td align="center">⚠️</td>
    <td><strong>Use try-except for platform-specific operations</strong></td>
    <td>Catch exceptions for operations that might fail on certain platforms</td>
  </tr>
  <tr>
    <td align="center">🧪</td>
    <td><strong>Test on all target platforms</strong></td>
    <td>Regularly test the bot on Windows, Linux, and macOS to ensure compatibility</td>
  </tr>
  <tr>
    <td align="center">🐳</td>
    <td><strong>Use Docker for consistent deployment</strong></td>
    <td>Docker provides a consistent environment across platforms, eliminating many compatibility issues</td>
  </tr>
</table>

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
