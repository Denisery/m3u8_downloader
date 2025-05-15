<div align="center">

# 🔌 API Documentation

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/plug.svg" alt="API" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Integrate with the M3U8 Downloader Bot programmatically*

</div>

---

The M3U8 Downloader Bot provides a RESTful API that allows you to interact with the bot programmatically. This documentation covers the available endpoints, authentication, and usage examples.

## 🔑 Authentication

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/key.svg" alt="Authentication" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

All API endpoints require authentication using an API key. You can configure the API key in your `.env` file:

```ini
# API settings
API_ENABLED=true
API_KEY=your_secure_api_key
```

To authenticate your requests, include the API key in the `Authorization` header:

```
Authorization: Bearer your_secure_api_key
```

## 🌐 Base URL

The API is available at the same host and port as the web dashboard, with `/api` as the base path:

```
http://your-server-ip:8080/api
```

## 📋 Available Endpoints

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/list.svg" alt="Endpoints" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### Status Endpoint

<table>
  <tr>
    <th width="20%">Method</th>
    <th width="30%">Endpoint</th>
    <th width="50%">Description</th>
  </tr>
  <tr>
    <td><code>GET</code></td>
    <td><code>/api/status</code></td>
    <td>Get the current status of the bot</td>
  </tr>
</table>

#### Response

```json
{
  "status": "online",
  "uptime": "3 days, 2 hours, 15 minutes",
  "version": "1.0.0",
  "active_downloads": 2,
  "completed_downloads": 150,
  "system_info": {
    "cpu_usage": 25.5,
    "memory_usage": 512.3,
    "disk_usage": 10240.5
  }
}
```

### Download Endpoint

<table>
  <tr>
    <th width="20%">Method</th>
    <th width="30%">Endpoint</th>
    <th width="50%">Description</th>
  </tr>
  <tr>
    <td><code>POST</code></td>
    <td><code>/api/download</code></td>
    <td>Start a new download</td>
  </tr>
</table>

#### Request Body

```json
{
  "url": "https://example.com/path/to/video.m3u8",
  "quality": "auto",
  "callback_url": "https://your-server.com/callback"
}
```

#### Response

```json
{
  "download_id": "abc123",
  "status": "queued",
  "estimated_time": "unknown",
  "message": "Download queued successfully"
}
```

### Download Status Endpoint

<table>
  <tr>
    <th width="20%">Method</th>
    <th width="30%">Endpoint</th>
    <th width="50%">Description</th>
  </tr>
  <tr>
    <td><code>GET</code></td>
    <td><code>/api/download/:id</code></td>
    <td>Get the status of a specific download</td>
  </tr>
</table>

#### Response

```json
{
  "download_id": "abc123",
  "status": "downloading",
  "progress": 45.2,
  "estimated_time": "2 minutes",
  "url": "https://example.com/path/to/video.m3u8",
  "size": "125.4 MB",
  "created_at": "2023-05-15T12:34:56Z",
  "updated_at": "2023-05-15T12:40:23Z"
}
```

### Cancel Download Endpoint

<table>
  <tr>
    <th width="20%">Method</th>
    <th width="30%">Endpoint</th>
    <th width="50%">Description</th>
  </tr>
  <tr>
    <td><code>DELETE</code></td>
    <td><code>/api/download/:id</code></td>
    <td>Cancel a specific download</td>
  </tr>
</table>

#### Response

```json
{
  "download_id": "abc123",
  "status": "cancelled",
  "message": "Download cancelled successfully"
}
```

### List Downloads Endpoint

<table>
  <tr>
    <th width="20%">Method</th>
    <th width="30%">Endpoint</th>
    <th width="50%">Description</th>
  </tr>
  <tr>
    <td><code>GET</code></td>
    <td><code>/api/downloads</code></td>
    <td>List all downloads</td>
  </tr>
</table>

#### Query Parameters

<table>
  <tr>
    <th width="20%">Parameter</th>
    <th width="20%">Type</th>
    <th width="20%">Default</th>
    <th width="40%">Description</th>
  </tr>
  <tr>
    <td><code>status</code></td>
    <td>string</td>
    <td>all</td>
    <td>Filter by status (queued, downloading, processing, completed, failed, cancelled)</td>
  </tr>
  <tr>
    <td><code>limit</code></td>
    <td>integer</td>
    <td>10</td>
    <td>Number of results to return</td>
  </tr>
  <tr>
    <td><code>offset</code></td>
    <td>integer</td>
    <td>0</td>
    <td>Offset for pagination</td>
  </tr>
</table>

#### Response

```json
{
  "total": 152,
  "limit": 10,
  "offset": 0,
  "downloads": [
    {
      "download_id": "abc123",
      "status": "downloading",
      "progress": 45.2,
      "url": "https://example.com/path/to/video.m3u8",
      "created_at": "2023-05-15T12:34:56Z"
    },
    {
      "download_id": "def456",
      "status": "completed",
      "progress": 100,
      "url": "https://example.com/path/to/another-video.m3u8",
      "created_at": "2023-05-15T11:22:33Z"
    }
  ]
}
```

## 📊 Webhook Callbacks

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bell.svg" alt="Webhooks" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The API supports webhook callbacks to notify your application when a download status changes. To use this feature, include a `callback_url` parameter when starting a download.

### Callback Payload

```json
{
  "download_id": "abc123",
  "status": "completed",
  "progress": 100,
  "url": "https://example.com/path/to/video.m3u8",
  "size": "125.4 MB",
  "download_url": "https://your-server.com/downloads/abc123.mp4",
  "created_at": "2023-05-15T12:34:56Z",
  "completed_at": "2023-05-15T12:45:12Z"
}
```

## 💻 Code Examples

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/code.svg" alt="Code" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

### cURL

```bash
# Start a download
curl -X POST "http://your-server-ip:8080/api/download" \
  -H "Authorization: Bearer your_secure_api_key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/path/to/video.m3u8", "quality": "auto"}'

# Check download status
curl -X GET "http://your-server-ip:8080/api/download/abc123" \
  -H "Authorization: Bearer your_secure_api_key"

# Cancel a download
curl -X DELETE "http://your-server-ip:8080/api/download/abc123" \
  -H "Authorization: Bearer your_secure_api_key"
```

### Python

```python
import requests

API_URL = "http://your-server-ip:8080/api"
API_KEY = "your_secure_api_key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Start a download
response = requests.post(
    f"{API_URL}/download",
    headers=headers,
    json={
        "url": "https://example.com/path/to/video.m3u8",
        "quality": "auto"
    }
)
download_id = response.json()["download_id"]
print(f"Download started with ID: {download_id}")

# Check download status
response = requests.get(
    f"{API_URL}/download/{download_id}",
    headers=headers
)
print(f"Download status: {response.json()['status']}")
```

### JavaScript

```javascript
const API_URL = "http://your-server-ip:8080/api";
const API_KEY = "your_secure_api_key";

const headers = {
  "Authorization": `Bearer ${API_KEY}`,
  "Content-Type": "application/json"
};

// Start a download
fetch(`${API_URL}/download`, {
  method: "POST",
  headers: headers,
  body: JSON.stringify({
    url: "https://example.com/path/to/video.m3u8",
    quality: "auto"
  })
})
.then(response => response.json())
.then(data => {
  const downloadId = data.download_id;
  console.log(`Download started with ID: ${downloadId}`);
  
  // Check download status
  return fetch(`${API_URL}/download/${downloadId}`, {
    method: "GET",
    headers: headers
  });
})
.then(response => response.json())
.then(data => {
  console.log(`Download status: ${data.status}`);
});
```

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
