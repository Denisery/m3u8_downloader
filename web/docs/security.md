# Security Features

This document outlines the security features implemented in the M3U8 Downloader Bot.

## Input Validation and Sanitization

### URL Validation

The bot implements enhanced URL validation to prevent injection attacks and ensure only valid M3U8 URLs are processed:

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

Key security features:
- Scheme restriction (only http/https allowed)
- Pattern matching for valid M3U8 URLs
- Blocking of localhost and private IP addresses
- Detection of common URL injection patterns

### Filename Sanitization

The bot sanitizes filenames to prevent path traversal attacks and other file-related vulnerabilities:

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

Key security features:
- Path traversal prevention
- Removal of potentially dangerous characters
- Length limitations to prevent buffer overflow attacks
- Randomized filenames to prevent enumeration

## Web Server Security

### Authentication

The web dashboard is protected with basic authentication:

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

Key security features:
- Basic authentication for the web dashboard
- Auto-generated secure passwords
- Configurable username and password
- Clear logging of authentication status

### Security Headers

The web server adds security headers to all responses to protect against common web vulnerabilities:

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

Key security features:
- Content Security Policy (CSP) to prevent XSS attacks
- X-Content-Type-Options to prevent MIME sniffing
- X-Frame-Options to prevent clickjacking
- X-XSS-Protection for additional XSS protection
- Strict-Transport-Security to enforce HTTPS
- Referrer-Policy to control information leakage
- Cache-Control to prevent sensitive data caching

## File Security

### Secure Temporary Directories

The bot creates secure temporary directories for downloads:

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

Key security features:
- Randomized directory names using cryptographic functions
- Secure permissions (0700) to restrict access
- Validation of paths to prevent directory traversal
- Secure cleanup of temporary files

### Download Path Security

The bot ensures that all file operations are performed within the expected directories:

```python
# Ensure the output path is within the download directory
output_path = os.path.abspath(os.path.join(self.download_path, output_filename))
if not output_path.startswith(os.path.abspath(self.download_path)):
    logger.error(f"Path traversal attempt detected: {output_filename}")
    return False, "Invalid filename", None
```

Key security features:
- Absolute path resolution to prevent path confusion
- Path traversal detection and prevention
- Secure permissions on download directories
- Validation before file operations

## Network Security

### Content Fetching

The bot implements secure content fetching with various security checks:

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

Key security features:
- Content type validation
- Size limitations to prevent DoS attacks
- Timeout controls
- SSL enforcement
- Redirect limitations
- Error handling for network failures

## How to Use These Features

### Enabling Web Authentication

To enable web authentication, set the following environment variables:

```
WEB_AUTH_ENABLED=true
WEB_AUTH_USERNAME=admin
WEB_AUTH_PASSWORD=your_secure_password
```

If you don't provide a password, a secure random password will be generated and logged at startup.

### Securing File Paths

The application automatically secures file paths. No additional configuration is needed.

### Generating a Secret Key

To set a custom secret key for security features:

```
SECRET_KEY=your_random_secret_key
```

If you don't provide a secret key, a secure random key will be generated at startup.

## Security Best Practices

1. **Run as a non-root user**: When deploying with Docker, the application runs as a non-root user by default.

2. **Use HTTPS**: When exposing the web dashboard, place it behind a reverse proxy with HTTPS.

3. **Limit access**: Configure your firewall to restrict access to the web dashboard.

4. **Regular updates**: Keep the application and its dependencies updated.

5. **Monitor logs**: Regularly check logs for suspicious activity.

6. **Set strong passwords**: Use strong passwords for the web dashboard.

7. **Limit admin users**: Only add trusted users to the ADMIN_USER_IDS list.
