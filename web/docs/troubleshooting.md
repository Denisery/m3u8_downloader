<div align="center">

# 🔍 Troubleshooting Guide

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bug.svg" alt="Troubleshooting" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Solutions for common issues with the M3U8 Downloader Bot*

</div>

---

This guide provides solutions for common issues you might encounter when using the M3U8 Downloader Bot.

## 🤖 Bot Issues

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/robot.svg" alt="Bot Issues" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Bot Not Responding

<details open>
<summary><b>If the bot is not responding to your messages:</b></summary>

<table>
  <tr>
    <th width="30%">Possible Cause</th>
    <th width="70%">Solution</th>
  </tr>
  <tr>
    <td>Bot is not running</td>
    <td>
      <ul>
        <li>Check if the bot process is running on your server</li>
        <li>Start the bot using <code>python main.py</code> or <code>docker-compose up -d</code></li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Incorrect API credentials</td>
    <td>
      <ul>
        <li>Verify your API credentials in the <code>.env</code> file</li>
        <li>Make sure <code>API_ID</code>, <code>API_HASH</code>, and <code>BOT_TOKEN</code> are correct</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Network issues</td>
    <td>
      <ul>
        <li>Check your internet connection</li>
        <li>Ensure your server can connect to Telegram's servers</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Bot was blocked or deleted</td>
    <td>
      <ul>
        <li>Make sure you haven't blocked the bot</li>
        <li>Try searching for the bot on Telegram again</li>
      </ul>
    </td>
  </tr>
</table>

</details>

### Bot Crashes on Startup

<details open>
<summary><b>If the bot crashes immediately after starting:</b></summary>

<table>
  <tr>
    <th width="30%">Possible Cause</th>
    <th width="70%">Solution</th>
  </tr>
  <tr>
    <td>Missing dependencies</td>
    <td>
      <ul>
        <li>Make sure all dependencies are installed: <code>pip install -r requirements.txt</code></li>
        <li>Check for any error messages related to missing packages</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Configuration errors</td>
    <td>
      <ul>
        <li>Verify that your <code>.env</code> file exists and contains all required variables</li>
        <li>Check for syntax errors in your <code>.env</code> file</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Port conflicts</td>
    <td>
      <ul>
        <li>If the web server is enabled, make sure the specified port is not already in use</li>
        <li>Try changing the <code>WEB_SERVER_PORT</code> in your <code>.env</code> file</li>
      </ul>
    </td>
  </tr>
</table>

</details>

## 📥 Download Issues

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/download.svg" alt="Download Issues" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Download Fails

<details open>
<summary><b>If your download fails or gets stuck:</b></summary>

<table>
  <tr>
    <th width="30%">Possible Cause</th>
    <th width="70%">Solution</th>
  </tr>
  <tr>
    <td>Invalid M3U8 URL</td>
    <td>
      <ul>
        <li>Make sure the URL is a valid M3U8 URL</li>
        <li>Try opening the URL in a web browser or media player to verify it works</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Geo-restricted content</td>
    <td>
      <ul>
        <li>Some content may be restricted to certain geographic regions</li>
        <li>Check if you can access the content directly from your location</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Authentication required</td>
    <td>
      <ul>
        <li>Some M3U8 streams require authentication</li>
        <li>The bot cannot download streams that require authentication</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>File size limit exceeded</td>
    <td>
      <ul>
        <li>Check if the file size exceeds your <code>MAX_DOWNLOAD_SIZE</code> setting</li>
        <li>Increase the limit in your <code>.env</code> file if needed</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Network issues</td>
    <td>
      <ul>
        <li>Check your internet connection</li>
        <li>Some servers may have rate limiting or connection restrictions</li>
      </ul>
    </td>
  </tr>
</table>

</details>

### Video Processing Fails

<details open>
<summary><b>If the video processing stage fails:</b></summary>

<table>
  <tr>
    <th width="30%">Possible Cause</th>
    <th width="70%">Solution</th>
  </tr>
  <tr>
    <td>FFmpeg issues</td>
    <td>
      <ul>
        <li>Make sure FFmpeg is properly installed on your system</li>
        <li>Try running <code>ffmpeg -version</code> to verify the installation</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Corrupted segments</td>
    <td>
      <ul>
        <li>Some segments in the M3U8 playlist may be corrupted</li>
        <li>Try downloading the video again</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Disk space issues</td>
    <td>
      <ul>
        <li>Check if you have enough disk space for the processed video</li>
        <li>Free up space if needed</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Unsupported codec</td>
    <td>
      <ul>
        <li>Some videos may use codecs that are not supported by FFmpeg</li>
        <li>Try updating FFmpeg to the latest version</li>
      </ul>
    </td>
  </tr>
</table>

</details>

## 🖥️ System Issues

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/desktop.svg" alt="System Issues" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### FFmpeg Errors

<details open>
<summary><b>If you encounter FFmpeg-related errors:</b></summary>

<table>
  <tr>
    <th width="30%">Possible Cause</th>
    <th width="70%">Solution</th>
  </tr>
  <tr>
    <td>FFmpeg not installed</td>
    <td>
      <ul>
        <li>Install FFmpeg using your system's package manager</li>
        <li>Windows: Download from <a href="https://ffmpeg.org/download.html">ffmpeg.org</a> and add to PATH</li>
        <li>macOS: <code>brew install ffmpeg</code></li>
        <li>Linux: <code>apt install ffmpeg</code> or equivalent</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>FFmpeg not in PATH</td>
    <td>
      <ul>
        <li>Make sure FFmpeg is in your system PATH</li>
        <li>Try running <code>ffmpeg -version</code> to verify</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Outdated FFmpeg version</td>
    <td>
      <ul>
        <li>Some features may require a newer version of FFmpeg</li>
        <li>Update FFmpeg to the latest version</li>
      </ul>
    </td>
  </tr>
</table>

</details>

### Web Dashboard Issues

<details open>
<summary><b>If the web dashboard is not working:</b></summary>

<table>
  <tr>
    <th width="30%">Possible Cause</th>
    <th width="70%">Solution</th>
  </tr>
  <tr>
    <td>Web server disabled</td>
    <td>
      <ul>
        <li>Check if <code>ENABLE_WEB_SERVER</code> is set to <code>true</code> in your <code>.env</code> file</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Port conflicts</td>
    <td>
      <ul>
        <li>Make sure the specified port is not already in use</li>
        <li>Try changing the <code>WEB_SERVER_PORT</code> in your <code>.env</code> file</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Authentication issues</td>
    <td>
      <ul>
        <li>If authentication is enabled, make sure you're using the correct username and password</li>
        <li>Check your <code>WEB_AUTH_USERNAME</code> and <code>WEB_AUTH_PASSWORD</code> settings</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Firewall blocking access</td>
    <td>
      <ul>
        <li>Make sure your firewall allows access to the web server port</li>
        <li>If running on a remote server, check if the port is open to external connections</li>
      </ul>
    </td>
  </tr>
</table>

</details>

## 🐳 Docker Issues

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/docker.svg" alt="Docker Issues" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(175deg);"/>
</div>

<details open>
<summary><b>If you're having issues with Docker:</b></summary>

<table>
  <tr>
    <th width="30%">Possible Cause</th>
    <th width="70%">Solution</th>
  </tr>
  <tr>
    <td>Docker not running</td>
    <td>
      <ul>
        <li>Make sure Docker is installed and running</li>
        <li>Try running <code>docker --version</code> to verify</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Permission issues</td>
    <td>
      <ul>
        <li>On Linux, you might need to run Docker commands with <code>sudo</code></li>
        <li>Or add your user to the <code>docker</code> group: <code>sudo usermod -aG docker $USER</code></li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Volume mounting issues</td>
    <td>
      <ul>
        <li>Make sure the paths in your volume mounts exist</li>
        <li>Check for permission issues on the host directories</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Environment variables not set</td>
    <td>
      <ul>
        <li>Make sure all required environment variables are set in your Docker Compose file or <code>.env</code> file</li>
      </ul>
    </td>
  </tr>
</table>

</details>

## 📞 Getting Help

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/headset.svg" alt="Getting Help" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

If you've tried the solutions above and are still experiencing issues, you can get help through the following channels:

<table>
  <tr>
    <th width="30%">Channel</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>GitHub Issues</td>
    <td>
      <ul>
        <li>Create an issue on the <a href="https://github.com/Denisery/m3u8_downloader/issues">GitHub repository</a></li>
        <li>Include detailed information about your issue and the steps to reproduce it</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Contact Maintainers</td>
    <td>
      <ul>
        <li>Reach out to the project maintainers directly</li>
        <li>See the <a href="/docs/contributing">Contributing Guide</a> for contact information</li>
      </ul>
    </td>
  </tr>
</table>

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
