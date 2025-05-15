<div align="center">

# 📈 Scalability Guide

<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/chart-line.svg" alt="Scalability" width="180" height="180" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>

### *Optimize performance and resource usage for your M3U8 Downloader Bot*

</div>

---

This guide explains the scalability features of the M3U8 Downloader Bot and how they help improve performance and resource usage.

## 📑 Table of Contents

- [🔄 Connection Pooling](#-connection-pooling)
- [💾 Caching System](#-caching-system)
- [⚖️ Dynamic Resource Allocation](#️-dynamic-resource-allocation)
- [⚙️ Configuration Options](#️-configuration-options)
- [📊 Monitoring](#-monitoring)

## 🔄 Connection Pooling

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/arrows-rotate.svg" alt="Connection Pooling" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Connection pooling is a technique that reuses existing connections instead of creating new ones for each request. This significantly improves performance when downloading M3U8 segments, which typically involve many HTTP requests to the same server.

### Benefits

<table>
  <tr>
    <th width="30%">Benefit</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>⏱️ <strong>Reduced Latency</strong></td>
    <td>Eliminates the overhead of establishing new connections</td>
  </tr>
  <tr>
    <td>🚀 <strong>Improved Throughput</strong></td>
    <td>Allows for more efficient use of network resources</td>
  </tr>
  <tr>
    <td>⚖️ <strong>Better Resource Management</strong></td>
    <td>Controls the number of concurrent connections</td>
  </tr>
</table>

### How It Works

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gears.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The connection pool manager maintains a pool of HTTP connections that can be reused for multiple requests. When a request is made, the manager either provides an existing idle connection or creates a new one if needed. After the request is completed, the connection is returned to the pool for future use.

## 💾 Caching System

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/database.svg" alt="Caching System" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The caching system stores M3U8 playlist content to reduce redundant downloads and improve performance.

### Benefits

<table>
  <tr>
    <th width="30%">Benefit</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>📉 <strong>Reduced Bandwidth Usage</strong></td>
    <td>Avoids downloading the same content multiple times</td>
  </tr>
  <tr>
    <td>⚡ <strong>Faster Response Times</strong></td>
    <td>Serves cached content immediately without network requests</td>
  </tr>
  <tr>
    <td>🔋 <strong>Reduced Server Load</strong></td>
    <td>Minimizes requests to the source server</td>
  </tr>
</table>

### How It Works

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/memory.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

When an M3U8 playlist is requested, the system first checks if it exists in the cache and is still valid (not expired). If found, it returns the cached content. Otherwise, it fetches the content from the source, stores it in the cache, and then returns it.

The cache uses a Time-To-Live (TTL) mechanism to ensure content freshness. Cached items older than the TTL are considered stale and will be refetched from the source.

### Cache Invalidation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/trash.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="30%">Invalidation Trigger</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>⏱️ <strong>TTL Expiration</strong></td>
    <td>When the Time-To-Live period expires</td>
  </tr>
  <tr>
    <td>📊 <strong>Size Limit</strong></td>
    <td>When the cache size exceeds the configured maximum</td>
  </tr>
  <tr>
    <td>🔄 <strong>Application Restart</strong></td>
    <td>When the application is restarted</td>
  </tr>
</table>

## ⚖️ Dynamic Resource Allocation

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/scale-balanced.svg" alt="Dynamic Resource Allocation" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Dynamic resource allocation monitors system resources and adjusts the workload accordingly to prevent system overload.

### Benefits

<table>
  <tr>
    <th width="30%">Benefit</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🛡️ <strong>Prevents System Overload</strong></td>
    <td>Throttles tasks when system resources are constrained</td>
  </tr>
  <tr>
    <td>⚡ <strong>Optimizes Performance</strong></td>
    <td>Maximizes throughput based on available resources</td>
  </tr>
  <tr>
    <td>🔄 <strong>Improves Stability</strong></td>
    <td>Ensures the application remains responsive under heavy load</td>
  </tr>
</table>

### How It Works

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/microchip.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The resource manager monitors CPU and memory usage at regular intervals. When usage exceeds configured thresholds, it enters "throttling mode" and reduces the number of concurrent tasks. When resource usage returns to normal levels, it resumes normal operation.

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/diagram-project.svg" width="120" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Tasks are queued and executed based on available resources, ensuring that the system remains stable even under heavy load.

## ⚙️ Configuration Options

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/sliders.svg" alt="Configuration" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

You can configure the scalability features through environment variables or the `.env` file:

### Connection Pool Settings

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/network-wired.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<div align="center">

```ini
CONNECTION_POOL_MAX_CONNECTIONS=100  # Maximum number of connections in the pool
CONNECTION_POOL_MAX_KEEPALIVE=30     # Maximum number of keepalive connections
CONNECTION_POOL_TTL_DNS_CACHE=300    # Time-to-live for DNS cache entries in seconds
CONNECTION_POOL_TIMEOUT=30           # Total request timeout in seconds
CONNECTION_POOL_CONNECT_TIMEOUT=10   # Connection establishment timeout in seconds
```

</div>

### Cache Settings

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/database.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<div align="center">

```ini
CACHE_ENABLED=true           # Set to false to disable caching
CACHE_TTL=3600               # Cache time-to-live in seconds (1 hour)
CACHE_MAX_SIZE=104857600     # Maximum cache size in bytes (100 MB)
```

</div>

### Resource Allocation Settings

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/microchip.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<div align="center">

```ini
RESOURCE_MONITOR_ENABLED=true      # Set to false to disable resource monitoring
RESOURCE_CPU_THRESHOLD=80.0        # CPU usage threshold percentage
RESOURCE_MEMORY_THRESHOLD=80.0     # Memory usage threshold percentage
RESOURCE_CHECK_INTERVAL=5          # Resource check interval in seconds
```

</div>

## 📊 Monitoring

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/chart-simple.svg" alt="Monitoring" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

You can monitor the scalability features through the web dashboard or the `/stats` command (admin only).

### Web Dashboard

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gauge-high.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

The web dashboard displays real-time statistics for:

<table>
  <tr>
    <th width="30%">Metric</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🔄 <strong>Connection Pool</strong></td>
    <td>Active connections, idle connections, and connection usage</td>
  </tr>
  <tr>
    <td>💾 <strong>Cache Status</strong></td>
    <td>Cache hit rate, item count, and memory usage</td>
  </tr>
  <tr>
    <td>⚖️ <strong>Resource Manager</strong></td>
    <td>CPU/memory usage, throttling status, and task queue</td>
  </tr>
</table>

### Admin Command

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/terminal.svg" width="40" height="40" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

Administrators can use the `/stats` command to view detailed statistics about the scalability features, including:

<table>
  <tr>
    <th width="30%">Statistic</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>🔄 <strong>Connection Pool</strong></td>
    <td>Detailed connection statistics, including creation/reuse counts</td>
  </tr>
  <tr>
    <td>💾 <strong>Cache</strong></td>
    <td>Hit/miss ratios, memory usage, and item expiration data</td>
  </tr>
  <tr>
    <td>⚖️ <strong>Resource Manager</strong></td>
    <td>Throttling history, resource usage trends, and task completion times</td>
  </tr>
</table>

## 💡 Best Practices

<div align="center">
<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/lightbulb.svg" alt="Best Practices" width="80" height="80" style="filter: invert(1) sepia(1) saturate(5) hue-rotate(300deg);"/>
</div>

<table>
  <tr>
    <th width="30%">Practice</th>
    <th width="70%">Description</th>
  </tr>
  <tr>
    <td>⚖️ <strong>Adjust Thresholds</strong></td>
    <td>Set CPU and memory thresholds based on your server's capabilities</td>
  </tr>
  <tr>
    <td>💾 <strong>Optimize Cache Size</strong></td>
    <td>Set the cache size based on available memory and expected workload</td>
  </tr>
  <tr>
    <td>📊 <strong>Monitor Performance</strong></td>
    <td>Regularly check the dashboard to ensure optimal performance</td>
  </tr>
  <tr>
    <td>🔄 <strong>Tune Connection Pool</strong></td>
    <td>Adjust connection pool settings based on network conditions and server capabilities</td>
  </tr>
</table>

---

<div align="center">
<p>Made with ❤️ for video enthusiasts everywhere</p>
</div>
