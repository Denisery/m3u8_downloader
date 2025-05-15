<div align="center">

# 🔒 Security Features

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/shield-halved.svg" alt="Security" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Protecting your data and system with robust security measures*

</div>

---

This document outlines the security features implemented in the M3U8 Downloader Bot.

## 🛡️ Input Validation and Sanitization

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/filter.svg" alt="Validation" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### URL Validation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/link.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot implements enhanced URL validation to prevent injection attacks and ensure only valid M3U8 URLs are processed:

<div align="center">

```python
def is_valid_m3u8_url(url: str) -> bool:
    """
    Enhanced validation for M3U8 URLs with security checks.
    """
    if not url or not isinstance(url, str):
        return False

    # Basic URL validation
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False

        # Only allow http and https schemes
        if result.scheme not in ['http', 'https']:
            return False

        # Check for common URL injection patterns
        if re.search(r'[\s\'";]', url):
            return False

        # Check for localhost or private IP addresses
        hostname = result.netloc.lower()
        if hostname == 'localhost' or hostname.startswith('127.') or \
           hostname.startswith('192.168.') or hostname.startswith('10.') or \
           (hostname.startswith('172.') and 16 <= int(hostname.split('.')[1]) <= 31):
            return False
    except Exception as e:
        logger.error(f"URL validation error: {str(e)}")
        return False

    # Check if it's an m3u8 URL
    pattern = r'.*\.(m3u8|M3U8)($|\?.*)'
    return bool(re.match(pattern, url))
```

</div>

<table>
  <tr>
    <th width="30%">Security Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🔒 Scheme restriction</td>
    <td>Only http/https schemes are allowed</td>
  </tr>
  <tr>
    <td>🔍 Pattern matching</td>
    <td>Ensures URLs match valid M3U8 patterns</td>
  </tr>
  <tr>
    <td>🚫 Private network blocking</td>
    <td>Blocks localhost and private IP addresses</td>
  </tr>
  <tr>
    <td>⚠️ Injection detection</td>
    <td>Detects common URL injection patterns</td>
  </tr>
</table>

### Filename Sanitization

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/file-shield.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot sanitizes filenames to prevent path traversal attacks and other file-related vulnerabilities:

<div align="center">

```python
def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent path traversal and command injection.
    """
    # Remove path separators and potentially dangerous characters
    sanitized = re.sub(r'[\\/*?:"<>|]', '', filename)
    # Ensure the filename doesn't start with dots or dashes
    sanitized = re.sub(r'^[.\-]+', '', sanitized)
    # Limit length to prevent excessively long filenames
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    # Ensure we have a valid filename
    if not sanitized:
        sanitized = "file"
    return sanitized
```

</div>

<table>
  <tr>
    <th width="30%">Security Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🛡️ Path traversal prevention</td>
    <td>Removes path separators and dangerous characters</td>
  </tr>
  <tr>
    <td>🧹 Character sanitization</td>
    <td>Removes potentially dangerous characters</td>
  </tr>
  <tr>
    <td>📏 Length limitations</td>
    <td>Prevents buffer overflow attacks with length restrictions</td>
  </tr>
  <tr>
    <td>🎲 Randomization</td>
    <td>Uses randomized filenames to prevent enumeration</td>
  </tr>
</table>

## 🌐 Web Server Security

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/globe-shield.svg" alt="Web Security" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Authentication

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/user-lock.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The web dashboard is protected with basic authentication:

<div align="center">

```python
# Web server authentication
WEB_AUTH_ENABLED = os.getenv("WEB_AUTH_ENABLED", "true").lower() == "true"
WEB_AUTH_USERNAME = os.getenv("WEB_AUTH_USERNAME", "admin")
WEB_AUTH_PASSWORD = os.getenv("WEB_AUTH_PASSWORD", "")

# Generate a random password if not provided
if WEB_AUTH_ENABLED and not WEB_AUTH_PASSWORD:
    WEB_AUTH_PASSWORD = secrets.token_urlsafe(12)
    logger.warning(f"No WEB_AUTH_PASSWORD provided. Generated random password: {WEB_AUTH_PASSWORD}")
```

</div>

<table>
  <tr>
    <th width="30%">Security Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🔑 Basic authentication</td>
    <td>Protects the web dashboard with username/password</td>
  </tr>
  <tr>
    <td>🔐 Auto-generated passwords</td>
    <td>Creates secure random passwords if none provided</td>
  </tr>
  <tr>
    <td>⚙️ Configurable credentials</td>
    <td>Allows custom username and password configuration</td>
  </tr>
  <tr>
    <td>📝 Authentication logging</td>
    <td>Provides clear logging of authentication status</td>
  </tr>
</table>

### Security Headers

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/shield.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The web server adds security headers to all responses to protect against common web vulnerabilities:

<div align="center">

```python
@web.middleware
async def security_headers_middleware(self, request, handler):
    """
    Middleware to add security headers to all responses.
    """
    response = await handler(request)

    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'

    return response
```

</div>

<table>
  <tr>
    <th width="30%">Security Header</th>
    <th width="70%">Protection</th>
  </tr>
  <tr>
    <td>🛡️ Content Security Policy</td>
    <td>Prevents XSS attacks by controlling resource loading</td>
  </tr>
  <tr>
    <td>🔍 X-Content-Type-Options</td>
    <td>Prevents MIME type sniffing security exploits</td>
  </tr>
  <tr>
    <td>🖼️ X-Frame-Options</td>
    <td>Prevents clickjacking attacks by disabling framing</td>
  </tr>
  <tr>
    <td>🔒 X-XSS-Protection</td>
    <td>Provides additional XSS protection in supported browsers</td>
  </tr>
  <tr>
    <td>🔐 Strict-Transport-Security</td>
    <td>Enforces HTTPS connections for enhanced security</td>
  </tr>
  <tr>
    <td>🔏 Referrer-Policy</td>
    <td>Controls information leakage in HTTP referrers</td>
  </tr>
  <tr>
    <td>📦 Cache-Control</td>
    <td>Prevents sensitive data caching in browsers</td>
  </tr>
</table>

## 📁 File Security

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/folder-closed.svg" alt="File Security" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Secure Temporary Directories

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/folder-tree.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot creates secure temporary directories for downloads:

<div align="center">

```python
def create_secure_temp_dir(user_id: int) -> str:
    """
    Create a secure temporary directory with random name.
    """
    import tempfile

    # Generate a random token
    random_token = secrets.token_hex(8)

    # Create a hash of the user ID and token
    hash_obj = hashlib.sha256(f"{user_id}_{random_token}".encode())
    dir_name = hash_obj.hexdigest()[:16]

    # Create the temporary directory
    temp_dir = tempfile.mkdtemp(prefix=f"m3u8_{dir_name}_")

    # Set secure permissions (only owner can read/write/execute)
    try:
        os.chmod(temp_dir, 0o700)
    except Exception as e:
        logger.warning(f"Could not set secure permissions on temp dir: {str(e)}")

    return temp_dir
```

</div>

<table>
  <tr>
    <th width="30%">Security Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🎲 Randomized names</td>
    <td>Uses cryptographic functions to generate unpredictable directory names</td>
  </tr>
  <tr>
    <td>🔒 Secure permissions</td>
    <td>Sets 0700 permissions to restrict access to owner only</td>
  </tr>
  <tr>
    <td>🛡️ Path validation</td>
    <td>Validates paths to prevent directory traversal attacks</td>
  </tr>
  <tr>
    <td>🧹 Secure cleanup</td>
    <td>Ensures proper cleanup of temporary files after use</td>
  </tr>
</table>

### Download Path Security

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/download.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot ensures that all file operations are performed within the expected directories:

<div align="center">

```python
# Ensure the output path is within the download directory
output_path = os.path.abspath(os.path.join(self.download_path, output_filename))
if not output_path.startswith(os.path.abspath(self.download_path)):
    logger.error(f"Path traversal attempt detected: {output_filename}")
    return False, "Invalid filename", None
```

</div>

<table>
  <tr>
    <th width="30%">Security Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🔍 Absolute path resolution</td>
    <td>Prevents path confusion by resolving to absolute paths</td>
  </tr>
  <tr>
    <td>🚫 Path traversal detection</td>
    <td>Detects and prevents path traversal attempts</td>
  </tr>
  <tr>
    <td>🔒 Secure permissions</td>
    <td>Sets appropriate permissions on download directories</td>
  </tr>
  <tr>
    <td>✅ Pre-operation validation</td>
    <td>Validates paths before performing file operations</td>
  </tr>
</table>

## 🌐 Network Security

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/network-wired.svg" alt="Network Security" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Content Fetching

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/cloud-arrow-down.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The bot implements secure content fetching with various security checks:

<div align="center">

```python
async def fetch_content(url: str, headers: Optional[Dict[str, str]] = None,
                max_size: int = 10 * 1024 * 1024) -> Optional[str]:
    """
    Fetch content from a URL with enhanced security checks.
    """
    # Validate URL before proceeding
    if not is_valid_m3u8_url(url):
        logger.error(f"Invalid M3U8 URL: {url}")
        return None

    # ... (additional code)

    try:
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, allow_redirects=True,
                                  max_redirects=5, ssl=True) as response:
                if response.status == 200:
                    # Check content type
                    content_type = response.headers.get('Content-Type', '')
                    if not ('text/plain' in content_type or
                            'application/x-mpegurl' in content_type or
                            'application/vnd.apple.mpegurl' in content_type or
                            'audio/mpegurl' in content_type or
                            'audio/x-mpegurl' in content_type):
                        logger.warning(f"Unexpected content type for M3U8: {content_type} from {url}")

                    # Check content length
                    content_length = response.content_length
                    if content_length and content_length > max_size:
                        logger.error(f"Content too large: {content_length} bytes (max: {max_size})")
                        return None

                    # ... (additional code)
```

</div>

<table>
  <tr>
    <th width="30%">Security Feature</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>📝 Content type validation</td>
    <td>Verifies that responses have appropriate MIME types</td>
  </tr>
  <tr>
    <td>📏 Size limitations</td>
    <td>Prevents DoS attacks by limiting download sizes</td>
  </tr>
  <tr>
    <td>⏱️ Timeout controls</td>
    <td>Prevents hanging connections with configurable timeouts</td>
  </tr>
  <tr>
    <td>🔒 SSL enforcement</td>
    <td>Ensures secure connections with SSL/TLS</td>
  </tr>
  <tr>
    <td>↩️ Redirect limitations</td>
    <td>Limits the number of redirects to prevent redirect loops</td>
  </tr>
  <tr>
    <td>⚠️ Error handling</td>
    <td>Robust error handling for network failures</td>
  </tr>
</table>

## 🛠️ How to Use These Features

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/screwdriver-wrench.svg" alt="How to Use" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Enabling Web Authentication

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/lock.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

To enable web authentication, set the following environment variables:

<div align="center">

```ini
WEB_AUTH_ENABLED=true
WEB_AUTH_USERNAME=admin
WEB_AUTH_PASSWORD=your_secure_password
```

</div>

> 💡 **Tip:** If you don't provide a password, a secure random password will be generated and logged at startup.

### Securing File Paths

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/folder-closed.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The application automatically secures file paths. No additional configuration is needed.

### Generating a Secret Key

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/key.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

To set a custom secret key for security features:

<div align="center">

```ini
SECRET_KEY=your_random_secret_key
```

</div>

> 💡 **Tip:** If you don't provide a secret key, a secure random key will be generated at startup.

## 💡 Security Best Practices

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
    <td align="center">👤</td>
    <td><strong>Run as a non-root user</strong></td>
    <td>When deploying with Docker, the application runs as a non-root user by default</td>
  </tr>
  <tr>
    <td align="center">🔒</td>
    <td><strong>Use HTTPS</strong></td>
    <td>When exposing the web dashboard, place it behind a reverse proxy with HTTPS</td>
  </tr>
  <tr>
    <td align="center">🔥</td>
    <td><strong>Limit access</strong></td>
    <td>Configure your firewall to restrict access to the web dashboard</td>
  </tr>
  <tr>
    <td align="center">🔄</td>
    <td><strong>Regular updates</strong></td>
    <td>Keep the application and its dependencies updated</td>
  </tr>
  <tr>
    <td align="center">📊</td>
    <td><strong>Monitor logs</strong></td>
    <td>Regularly check logs for suspicious activity</td>
  </tr>
  <tr>
    <td align="center">🔑</td>
    <td><strong>Set strong passwords</strong></td>
    <td>Use strong passwords for the web dashboard</td>
  </tr>
  <tr>
    <td align="center">👮</td>
    <td><strong>Limit admin users</strong></td>
    <td>Only add trusted users to the ADMIN_USER_IDS list</td>
  </tr>
</table>

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
