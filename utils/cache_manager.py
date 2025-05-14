import os
import time
import logging
import hashlib
import json
import asyncio
import aiofiles
from typing import Dict, Any, Optional, Tuple, List
import m3u8

# Configure logging
logger = logging.getLogger(__name__)

class CacheManager:
    """
    A cache manager for M3U8 content to reduce redundant downloads.
    
    This class provides caching functionality for M3U8 playlists with TTL (Time-To-Live)
    and cache invalidation mechanisms.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern for the cache manager."""
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, 
                 cache_dir: str = 'cache',
                 ttl: int = 3600,  # 1 hour default
                 max_size: int = 100 * 1024 * 1024,  # 100 MB default
                 cleanup_interval: int = 3600):  # 1 hour default
        """
        Initialize the cache manager with configurable parameters.
        
        Args:
            cache_dir: Directory to store cached files
            ttl: Time-to-live for cached items in seconds
            max_size: Maximum cache size in bytes
            cleanup_interval: Interval for cache cleanup in seconds
        """
        if self._initialized:
            return
            
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.max_size = max_size
        self.cleanup_interval = cleanup_interval
        self.cache_index: Dict[str, Dict[str, Any]] = {}
        self.lock = asyncio.Lock()
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Set secure permissions
        try:
            os.chmod(self.cache_dir, 0o700)
        except Exception as e:
            logger.warning(f"Could not set secure permissions on cache directory: {str(e)}")
        
        # Load cache index if it exists
        self._load_cache_index()
        
        # Start background cleanup task
        self.cleanup_task = asyncio.create_task(self._cleanup_task())
        
        self._initialized = True
        logger.info(f"Cache manager initialized with ttl={ttl}s, max_size={max_size} bytes")
    
    def _load_cache_index(self):
        """Load the cache index from disk."""
        index_path = os.path.join(self.cache_dir, 'cache_index.json')
        try:
            if os.path.exists(index_path):
                with open(index_path, 'r') as f:
                    self.cache_index = json.load(f)
                logger.info(f"Loaded cache index with {len(self.cache_index)} entries")
        except Exception as e:
            logger.error(f"Error loading cache index: {str(e)}")
            self.cache_index = {}
    
    async def _save_cache_index(self):
        """Save the cache index to disk."""
        index_path = os.path.join(self.cache_dir, 'cache_index.json')
        try:
            async with self.lock:
                async with aiofiles.open(index_path, 'w') as f:
                    await f.write(json.dumps(self.cache_index, indent=2))
        except Exception as e:
            logger.error(f"Error saving cache index: {str(e)}")
    
    def _get_cache_key(self, url: str) -> str:
        """
        Generate a cache key for a URL.
        
        Args:
            url: URL to generate a key for
            
        Returns:
            str: Cache key
        """
        # Create a hash of the URL
        hash_obj = hashlib.sha256(url.encode())
        return hash_obj.hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """
        Get the file path for a cache key.
        
        Args:
            key: Cache key
            
        Returns:
            str: Path to the cached file
        """
        return os.path.join(self.cache_dir, f"{key}.m3u8")
    
    async def get(self, url: str) -> Optional[str]:
        """
        Get cached content for a URL if it exists and is valid.
        
        Args:
            url: URL to get cached content for
            
        Returns:
            Optional[str]: Cached content or None if not found or expired
        """
        key = self._get_cache_key(url)
        
        async with self.lock:
            # Check if the key exists in the cache index
            if key not in self.cache_index:
                return None
            
            # Check if the cached item has expired
            cache_info = self.cache_index[key]
            if time.time() - cache_info['timestamp'] > self.ttl:
                logger.debug(f"Cache expired for {url}")
                return None
            
            # Get the cached content
            try:
                cache_path = self._get_cache_path(key)
                if not os.path.exists(cache_path):
                    logger.warning(f"Cache file missing for {url}")
                    return None
                
                async with aiofiles.open(cache_path, 'r') as f:
                    content = await f.read()
                
                logger.debug(f"Cache hit for {url}")
                return content
            except Exception as e:
                logger.error(f"Error reading cached content for {url}: {str(e)}")
                return None
    
    async def set(self, url: str, content: str) -> bool:
        """
        Cache content for a URL.
        
        Args:
            url: URL to cache content for
            content: Content to cache
            
        Returns:
            bool: True if successful, False otherwise
        """
        key = self._get_cache_key(url)
        cache_path = self._get_cache_path(key)
        
        try:
            # Write the content to the cache file
            async with aiofiles.open(cache_path, 'w') as f:
                await f.write(content)
            
            # Update the cache index
            async with self.lock:
                self.cache_index[key] = {
                    'url': url,
                    'timestamp': time.time(),
                    'size': len(content),
                    'path': cache_path
                }
            
            # Save the cache index
            await self._save_cache_index()
            
            logger.debug(f"Cached content for {url}")
            return True
        except Exception as e:
            logger.error(f"Error caching content for {url}: {str(e)}")
            return False
    
    async def invalidate(self, url: str) -> bool:
        """
        Invalidate cached content for a URL.
        
        Args:
            url: URL to invalidate
            
        Returns:
            bool: True if successful, False otherwise
        """
        key = self._get_cache_key(url)
        
        async with self.lock:
            if key not in self.cache_index:
                return False
            
            try:
                # Remove the cache file
                cache_path = self._get_cache_path(key)
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                
                # Remove the entry from the cache index
                del self.cache_index[key]
                
                # Save the cache index
                await self._save_cache_index()
                
                logger.debug(f"Invalidated cache for {url}")
                return True
            except Exception as e:
                logger.error(f"Error invalidating cache for {url}: {str(e)}")
                return False
    
    async def clear(self) -> bool:
        """
        Clear all cached content.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with self.lock:
                # Remove all cache files
                for key, info in self.cache_index.items():
                    cache_path = info.get('path')
                    if cache_path and os.path.exists(cache_path):
                        os.remove(cache_path)
                
                # Clear the cache index
                self.cache_index = {}
                
                # Save the cache index
                await self._save_cache_index()
                
                logger.info("Cache cleared")
                return True
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    async def _cleanup_task(self):
        """Background task to clean up expired and excess cache items."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_cache()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cache cleanup task: {str(e)}")
                await asyncio.sleep(60)  # Wait a minute before retrying
    
    async def _cleanup_cache(self):
        """Clean up expired and excess cache items."""
        try:
            current_time = time.time()
            total_size = 0
            items_to_remove = []
            
            # First pass: identify expired items and calculate total size
            async with self.lock:
                for key, info in self.cache_index.items():
                    if current_time - info['timestamp'] > self.ttl:
                        items_to_remove.append(key)
                    else:
                        total_size += info.get('size', 0)
            
            # Remove expired items
            for key in items_to_remove:
                await self._remove_cache_item(key)
            
            # Second pass: if still over max size, remove oldest items
            if total_size > self.max_size:
                async with self.lock:
                    # Sort items by timestamp (oldest first)
                    sorted_items = sorted(
                        self.cache_index.items(),
                        key=lambda x: x[1]['timestamp']
                    )
                    
                    # Remove oldest items until under max size
                    for key, info in sorted_items:
                        if total_size <= self.max_size:
                            break
                        
                        await self._remove_cache_item(key)
                        total_size -= info.get('size', 0)
            
            # Save the cache index
            await self._save_cache_index()
            
            logger.debug(f"Cache cleanup completed. Current size: {total_size} bytes")
        except Exception as e:
            logger.error(f"Error cleaning up cache: {str(e)}")
    
    async def _remove_cache_item(self, key: str):
        """
        Remove a cache item.
        
        Args:
            key: Cache key to remove
        """
        try:
            async with self.lock:
                if key in self.cache_index:
                    # Remove the cache file
                    cache_path = self._get_cache_path(key)
                    if os.path.exists(cache_path):
                        os.remove(cache_path)
                    
                    # Remove the entry from the cache index
                    del self.cache_index[key]
        except Exception as e:
            logger.error(f"Error removing cache item {key}: {str(e)}")
    
    async def stop(self):
        """Stop the cache manager and clean up resources."""
        if hasattr(self, 'cleanup_task') and self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Save the cache index
        await self._save_cache_index()
        
        logger.info("Cache manager stopped")

# Global cache manager instance
cache_manager = None

def get_cache_manager(
    cache_dir: str = 'cache',
    ttl: int = 3600,
    max_size: int = 100 * 1024 * 1024,
    cleanup_interval: int = 3600
) -> CacheManager:
    """
    Get or create the global cache manager instance.
    
    Args:
        cache_dir: Directory to store cached files
        ttl: Time-to-live for cached items in seconds
        max_size: Maximum cache size in bytes
        cleanup_interval: Interval for cache cleanup in seconds
        
    Returns:
        CacheManager: The global cache manager instance
    """
    global cache_manager
    
    if cache_manager is None:
        cache_manager = CacheManager(
            cache_dir=cache_dir,
            ttl=ttl,
            max_size=max_size,
            cleanup_interval=cleanup_interval
        )
    
    return cache_manager

async def close_cache_manager():
    """Close the global cache manager."""
    global cache_manager
    
    if cache_manager:
        await cache_manager.stop()
        cache_manager = None
