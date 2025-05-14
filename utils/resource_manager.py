import os
import time
import logging
import asyncio
import psutil
from typing import Dict, Any, Optional, Callable, List, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class ResourceManager:
    """
    A resource manager for dynamic resource allocation based on system load.
    
    This class monitors system resources and adjusts resource usage for optimal performance.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern for the resource manager."""
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, 
                 cpu_threshold: float = 80.0,
                 memory_threshold: float = 80.0,
                 check_interval: int = 5,
                 max_concurrent_tasks: int = 5):
        """
        Initialize the resource manager with configurable parameters.
        
        Args:
            cpu_threshold: CPU usage threshold percentage
            memory_threshold: Memory usage threshold percentage
            check_interval: Resource check interval in seconds
            max_concurrent_tasks: Maximum number of concurrent tasks
        """
        if self._initialized:
            return
            
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.check_interval = check_interval
        self.max_concurrent_tasks = max_concurrent_tasks
        self.current_concurrent_tasks = 0
        self.throttling = False
        self.lock = asyncio.Lock()
        self.task_queue: List[Tuple[asyncio.Future, Callable, List, Dict]] = []
        self.running_tasks: List[asyncio.Task] = []
        
        # Start background monitoring task
        self.monitor_task = asyncio.create_task(self._monitor_resources())
        
        self._initialized = True
        logger.info(f"Resource manager initialized with cpu_threshold={cpu_threshold}%, "
                   f"memory_threshold={memory_threshold}%, max_concurrent_tasks={max_concurrent_tasks}")
    
    async def _monitor_resources(self):
        """Background task to monitor system resources and adjust resource usage."""
        while True:
            try:
                # Get current resource usage
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # Log resource usage
                logger.debug(f"Resource usage: CPU={cpu_percent}%, Memory={memory_percent}%")
                
                # Check if we need to throttle
                if cpu_percent > self.cpu_threshold or memory_percent > self.memory_threshold:
                    if not self.throttling:
                        logger.warning(f"Resource threshold exceeded: CPU={cpu_percent}%, "
                                      f"Memory={memory_percent}%. Throttling tasks.")
                        self.throttling = True
                else:
                    if self.throttling:
                        logger.info(f"Resource usage normalized: CPU={cpu_percent}%, "
                                   f"Memory={memory_percent}%. Resuming normal operation.")
                        self.throttling = False
                
                # Process the task queue if we have capacity
                await self._process_task_queue()
                
                # Wait for the next check
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error monitoring resources: {str(e)}")
                await asyncio.sleep(self.check_interval)
    
    async def _process_task_queue(self):
        """Process the task queue based on available resources."""
        async with self.lock:
            # Calculate how many tasks we can run
            available_slots = self.max_concurrent_tasks - self.current_concurrent_tasks
            
            # If throttling, reduce available slots
            if self.throttling:
                available_slots = max(1, available_slots // 2)
            
            # Process tasks from the queue
            for _ in range(min(available_slots, len(self.task_queue))):
                future, func, args, kwargs = self.task_queue.pop(0)
                
                # Create and start the task
                task = asyncio.create_task(self._run_task(future, func, args, kwargs))
                self.running_tasks.append(task)
                self.current_concurrent_tasks += 1
    
    async def _run_task(self, future: asyncio.Future, func: Callable, args: List, kwargs: Dict):
        """
        Run a task and set its result in the future.
        
        Args:
            future: Future to set the result in
            func: Function to run
            args: Function arguments
            kwargs: Function keyword arguments
        """
        try:
            result = await func(*args, **kwargs)
            if not future.done():
                future.set_result(result)
        except Exception as e:
            if not future.done():
                future.set_exception(e)
        finally:
            async with self.lock:
                self.current_concurrent_tasks -= 1
                if task := asyncio.current_task():
                    if task in self.running_tasks:
                        self.running_tasks.remove(task)
    
    async def run_task(self, func: Callable, *args, **kwargs) -> Any:
        """
        Run a task with resource management.
        
        Args:
            func: Function to run
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Any: Function result
        """
        # Create a future for the task result
        future = asyncio.get_running_loop().create_future()
        
        # Add the task to the queue
        async with self.lock:
            self.task_queue.append((future, func, args, kwargs))
        
        # Process the task queue
        await self._process_task_queue()
        
        # Wait for the task to complete
        return await future
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the resource manager.
        
        Returns:
            Dict[str, Any]: Resource manager statistics
        """
        return {
            "cpu_threshold": self.cpu_threshold,
            "memory_threshold": self.memory_threshold,
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "current_concurrent_tasks": self.current_concurrent_tasks,
            "throttling": self.throttling,
            "queued_tasks": len(self.task_queue),
            "running_tasks": len(self.running_tasks)
        }
    
    async def stop(self):
        """Stop the resource manager and clean up resources."""
        if hasattr(self, 'monitor_task') and self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        
        # Cancel all running tasks
        for task in self.running_tasks:
            task.cancel()
        
        # Clear the task queue
        async with self.lock:
            for future, _, _, _ in self.task_queue:
                if not future.done():
                    future.cancel()
            self.task_queue.clear()
        
        logger.info("Resource manager stopped")

# Global resource manager instance
resource_manager = None

def get_resource_manager(
    cpu_threshold: float = 80.0,
    memory_threshold: float = 80.0,
    check_interval: int = 5,
    max_concurrent_tasks: int = 5
) -> ResourceManager:
    """
    Get or create the global resource manager instance.
    
    Args:
        cpu_threshold: CPU usage threshold percentage
        memory_threshold: Memory usage threshold percentage
        check_interval: Resource check interval in seconds
        max_concurrent_tasks: Maximum number of concurrent tasks
        
    Returns:
        ResourceManager: The global resource manager instance
    """
    global resource_manager
    
    if resource_manager is None:
        resource_manager = ResourceManager(
            cpu_threshold=cpu_threshold,
            memory_threshold=memory_threshold,
            check_interval=check_interval,
            max_concurrent_tasks=max_concurrent_tasks
        )
    
    return resource_manager

async def close_resource_manager():
    """Close the global resource manager."""
    global resource_manager
    
    if resource_manager:
        await resource_manager.stop()
        resource_manager = None
