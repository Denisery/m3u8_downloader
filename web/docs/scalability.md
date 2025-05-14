# Scalability Guide

This guide explains the scalability features of the M3U8 Downloader Bot and how they help improve performance and resource usage.

## Table of Contents

- [Connection Pooling](#connection-pooling)
- [Caching System](#caching-system)
- [Dynamic Resource Allocation](#dynamic-resource-allocation)
- [Configuration Options](#configuration-options)
- [Monitoring](#monitoring)

## Connection Pooling

Connection pooling is a technique that reuses existing connections instead of creating new ones for each request. This significantly improves performance when downloading M3U8 segments, which typically involve many HTTP requests to the same server.

### Benefits

- **Reduced Latency**: Eliminates the overhead of establishing new connections
- **Improved Throughput**: Allows for more efficient use of network resources
- **Better Resource Management**: Controls the number of concurrent connections

### How It Works

The connection pool manager maintains a pool of HTTP connections that can be reused for multiple requests. When a request is made, the manager either provides an existing idle connection or creates a new one if needed. After the request is completed, the connection is returned to the pool for future use.

## Caching System

The caching system stores M3U8 playlist content to reduce redundant downloads and improve performance.

### Benefits

- **Reduced Bandwidth Usage**: Avoids downloading the same content multiple times
- **Faster Response Times**: Serves cached content immediately without network requests
- **Reduced Server Load**: Minimizes requests to the source server

### How It Works

When an M3U8 playlist is requested, the system first checks if it exists in the cache and is still valid (not expired). If found, it returns the cached content. Otherwise, it fetches the content from the source, stores it in the cache, and then returns it.

The cache uses a Time-To-Live (TTL) mechanism to ensure content freshness. Cached items older than the TTL are considered stale and will be refetched from the source.

### Cache Invalidation

The cache is automatically invalidated in the following cases:
- When the TTL expires
- When the cache size exceeds the configured maximum
- When the application is restarted

## Dynamic Resource Allocation

Dynamic resource allocation monitors system resources and adjusts the workload accordingly to prevent system overload.

### Benefits

- **Prevents System Overload**: Throttles tasks when system resources are constrained
- **Optimizes Performance**: Maximizes throughput based on available resources
- **Improves Stability**: Ensures the application remains responsive under heavy load

### How It Works

The resource manager monitors CPU and memory usage at regular intervals. When usage exceeds configured thresholds, it enters "throttling mode" and reduces the number of concurrent tasks. When resource usage returns to normal levels, it resumes normal operation.

Tasks are queued and executed based on available resources, ensuring that the system remains stable even under heavy load.

## Configuration Options

You can configure the scalability features through environment variables or the `.env` file:

### Connection Pool Settings

```
CONNECTION_POOL_MAX_CONNECTIONS=100  # Maximum number of connections in the pool
CONNECTION_POOL_MAX_KEEPALIVE=30     # Maximum number of keepalive connections
CONNECTION_POOL_TTL_DNS_CACHE=300    # Time-to-live for DNS cache entries in seconds
CONNECTION_POOL_TIMEOUT=30           # Total request timeout in seconds
CONNECTION_POOL_CONNECT_TIMEOUT=10   # Connection establishment timeout in seconds
```

### Cache Settings

```
CACHE_ENABLED=true           # Set to false to disable caching
CACHE_TTL=3600               # Cache time-to-live in seconds (1 hour)
CACHE_MAX_SIZE=104857600     # Maximum cache size in bytes (100 MB)
```

### Resource Allocation Settings

```
RESOURCE_MONITOR_ENABLED=true      # Set to false to disable resource monitoring
RESOURCE_CPU_THRESHOLD=80.0        # CPU usage threshold percentage
RESOURCE_MEMORY_THRESHOLD=80.0     # Memory usage threshold percentage
RESOURCE_CHECK_INTERVAL=5          # Resource check interval in seconds
```

## Monitoring

You can monitor the scalability features through the web dashboard or the `/stats` command (admin only).

### Web Dashboard

The web dashboard displays real-time statistics for:
- Connection pool usage
- Cache status and item count
- Resource manager status and task queue

### Admin Command

Administrators can use the `/stats` command to view detailed statistics about the scalability features, including:
- Connection pool statistics
- Cache statistics
- Resource manager status and throttling information

## Best Practices

- **Adjust Thresholds**: Set CPU and memory thresholds based on your server's capabilities
- **Optimize Cache Size**: Set the cache size based on available memory and expected workload
- **Monitor Performance**: Regularly check the dashboard to ensure optimal performance
- **Tune Connection Pool**: Adjust connection pool settings based on network conditions and server capabilities
