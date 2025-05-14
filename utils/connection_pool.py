import logging
import asyncio
import aiohttp
from typing import Dict, Optional, Any, List
import time
import ssl
from aiohttp.client import ClientTimeout

# Configure logging
logger = logging.getLogger(__name__)

class ConnectionPool:
    """
    A connection pool manager for handling HTTP requests efficiently.
    
    This class manages a pool of aiohttp ClientSession objects to reuse connections
    and improve performance for multiple concurrent HTTP requests.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern for the connection pool."""
        if cls._instance is None:
            cls._instance = super(ConnectionPool, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, 
                 max_connections: int = 100, 
                 max_keepalive_connections: int = 30,
                 ttl_dns_cache: int = 300,
                 timeout: int = 30,
                 connection_timeout: int = 10,
                 ssl_verify: bool = True):
        """
        Initialize the connection pool with configurable parameters.
        
        Args:
            max_connections: Maximum number of connections in the pool
            max_keepalive_connections: Maximum number of keepalive connections
            ttl_dns_cache: Time-to-live for DNS cache entries in seconds
            timeout: Total request timeout in seconds
            connection_timeout: Connection establishment timeout in seconds
            ssl_verify: Whether to verify SSL certificates
        """
        if self._initialized:
            return
            
        self.max_connections = max_connections
        self.max_keepalive_connections = max_keepalive_connections
        self.ttl_dns_cache = ttl_dns_cache
        self.timeout = timeout
        self.connection_timeout = connection_timeout
        self.ssl_verify = ssl_verify
        
        # Create a TCP connector with connection pooling
        self.connector = aiohttp.TCPConnector(
            limit=self.max_connections,
            limit_per_host=self.max_keepalive_connections,
            ttl_dns_cache=self.ttl_dns_cache,
            ssl=ssl_verify,
            force_close=False,
            enable_cleanup_closed=True
        )
        
        # Create a client session with the connector
        self.session = aiohttp.ClientSession(
            connector=self.connector,
            timeout=ClientTimeout(
                total=self.timeout,
                connect=self.connection_timeout
            ),
            raise_for_status=False
        )
        
        # Track active requests
        self.active_requests = 0
        self.request_times: List[float] = []
        self.max_request_times = 100  # Keep track of the last 100 request times
        
        self._initialized = True
        logger.info(f"Connection pool initialized with max_connections={max_connections}, "
                   f"max_keepalive_connections={max_keepalive_connections}")
    
    async def close(self):
        """Close the connection pool and release resources."""
        if hasattr(self, 'session') and self.session:
            await self.session.close()
            logger.info("Connection pool closed")
    
    async def get(self, url: str, headers: Optional[Dict[str, str]] = None, 
                 allow_redirects: bool = True, max_redirects: int = 5,
                 timeout: Optional[int] = None) -> aiohttp.ClientResponse:
        """
        Perform a GET request using the connection pool.
        
        Args:
            url: URL to request
            headers: Optional HTTP headers
            allow_redirects: Whether to follow redirects
            max_redirects: Maximum number of redirects to follow
            timeout: Optional timeout override for this specific request
            
        Returns:
            aiohttp.ClientResponse: Response object
        """
        start_time = time.time()
        self.active_requests += 1
        
        try:
            # Use custom timeout if provided
            if timeout:
                timeout_obj = ClientTimeout(total=timeout, connect=self.connection_timeout)
                response = await self.session.get(
                    url, 
                    headers=headers, 
                    allow_redirects=allow_redirects,
                    max_redirects=max_redirects,
                    timeout=timeout_obj
                )
            else:
                response = await self.session.get(
                    url, 
                    headers=headers, 
                    allow_redirects=allow_redirects,
                    max_redirects=max_redirects
                )
            
            return response
        finally:
            self.active_requests -= 1
            request_time = time.time() - start_time
            
            # Track request times for performance monitoring
            self.request_times.append(request_time)
            if len(self.request_times) > self.max_request_times:
                self.request_times.pop(0)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the connection pool.
        
        Returns:
            Dict[str, Any]: Connection pool statistics
        """
        avg_request_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
        
        return {
            "active_requests": self.active_requests,
            "max_connections": self.max_connections,
            "avg_request_time": avg_request_time,
            "connector_stats": {
                "limit": self.connector.limit,
                "limit_per_host": self.connector.limit_per_host,
                "acquired_connections": len(self.connector._acquired),
                "num_pools": len(self.connector._conns)
            }
        }

# Global connection pool instance
connection_pool = None

def get_connection_pool(
    max_connections: int = 100,
    max_keepalive_connections: int = 30,
    ttl_dns_cache: int = 300,
    timeout: int = 30,
    connection_timeout: int = 10,
    ssl_verify: bool = True
) -> ConnectionPool:
    """
    Get or create the global connection pool instance.
    
    Args:
        max_connections: Maximum number of connections in the pool
        max_keepalive_connections: Maximum number of keepalive connections
        ttl_dns_cache: Time-to-live for DNS cache entries in seconds
        timeout: Total request timeout in seconds
        connection_timeout: Connection establishment timeout in seconds
        ssl_verify: Whether to verify SSL certificates
        
    Returns:
        ConnectionPool: The global connection pool instance
    """
    global connection_pool
    
    if connection_pool is None:
        connection_pool = ConnectionPool(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            ttl_dns_cache=ttl_dns_cache,
            timeout=timeout,
            connection_timeout=connection_timeout,
            ssl_verify=ssl_verify
        )
    
    return connection_pool

async def close_connection_pool():
    """Close the global connection pool."""
    global connection_pool
    
    if connection_pool:
        await connection_pool.close()
        connection_pool = None
