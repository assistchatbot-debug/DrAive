"""
Redis Cache Manager for DrAivBot
High-performance session caching with automatic fallback to Supabase
"""
import json
import logging
from typing import Optional, Dict, Any
from redis import asyncio as aioredis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class RedisCache:
    """
    Redis cache manager with automatic fallback

    Features:
    - In-memory caching for hot sessions
    - Automatic TTL (24 hours)
    - Graceful fallback to Supabase
    - Connection pooling
    """

    def __init__(self, redis_url: str):
        """
        Initialize Redis connection

        Args:
            redis_url: Redis connection URL (redis://host:port/db)
        """
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None
        self._connected = False

    async def connect(self) -> bool:
        """
        Connect to Redis server

        Returns:
            True if connected, False otherwise
        """
        try:
            self.redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=50,
                socket_connect_timeout=5,
                socket_keepalive=True,
                health_check_interval=30
            )

            # Test connection
            await self.redis.ping()
            self._connected = True
            logger.info("✅ Redis connected successfully")
            return True

        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}. Using Supabase only.")
            self._connected = False
            return False

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
            self._connected = False
            logger.info("Redis disconnected")

    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self._connected

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get value from Redis

        Args:
            key: Cache key

        Returns:
            Cached data or None
        """
        if not self._connected:
            return None

        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None

        except RedisError as e:
            logger.warning(f"Redis GET error: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Dict[str, Any],
        ttl: int = 86400  # 24 hours
    ) -> bool:
        """
        Set value in Redis with TTL

        Args:
            key: Cache key
            value: Data to cache
            ttl: Time to live in seconds (default 24h)

        Returns:
            True if successful, False otherwise
        """
        if not self._connected:
            return False

        try:
            serialized = json.dumps(value, default=str)
            await self.redis.setex(key, ttl, serialized)
            return True

        except RedisError as e:
            logger.warning(f"Redis SET error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete key from Redis

        Args:
            key: Cache key

        Returns:
            True if successful, False otherwise
        """
        if not self._connected:
            return False

        try:
            await self.redis.delete(key)
            return True

        except RedisError as e:
            logger.warning(f"Redis DELETE error: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in Redis

        Args:
            key: Cache key

        Returns:
            True if exists, False otherwise
        """
        if not self._connected:
            return False

        try:
            return await self.redis.exists(key) > 0

        except RedisError as e:
            logger.warning(f"Redis EXISTS error: {e}")
            return False

    async def expire(self, key: str, ttl: int) -> bool:
        """
        Update TTL for key

        Args:
            key: Cache key
            ttl: New TTL in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self._connected:
            return False

        try:
            await self.redis.expire(key, ttl)
            return True

        except RedisError as e:
            logger.warning(f"Redis EXPIRE error: {e}")
            return False

    async def keys(self, pattern: str = "*") -> list:
        """
        Get all keys matching pattern

        Args:
            pattern: Key pattern (default: all keys)

        Returns:
            List of matching keys
        """
        if not self._connected:
            return []

        try:
            return await self.redis.keys(pattern)

        except RedisError as e:
            logger.warning(f"Redis KEYS error: {e}")
            return []

    async def flush_db(self) -> bool:
        """
        Flush all keys from current database
        ⚠️ Use with caution!

        Returns:
            True if successful, False otherwise
        """
        if not self._connected:
            return False

        try:
            await self.redis.flushdb()
            logger.warning("⚠️ Redis database flushed!")
            return True

        except RedisError as e:
            logger.error(f"Redis FLUSHDB error: {e}")
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """
        Get Redis statistics

        Returns:
            Dictionary with stats
        """
        if not self._connected:
            return {
                "connected": False,
                "error": "Not connected to Redis"
            }

        try:
            info = await self.redis.info()
            return {
                "connected": True,
                "used_memory": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }

        except RedisError as e:
            logger.error(f"Redis INFO error: {e}")
            return {
                "connected": False,
                "error": str(e)
            }


# Singleton instance
_redis_cache: Optional[RedisCache] = None


async def get_redis_cache() -> Optional[RedisCache]:
    """
    Get Redis cache singleton instance

    Returns:
        RedisCache instance or None if disabled
    """
    global _redis_cache
    return _redis_cache


async def init_redis_cache(redis_url: Optional[str]) -> Optional[RedisCache]:
    """
    Initialize Redis cache

    Args:
        redis_url: Redis connection URL or None to disable

    Returns:
        RedisCache instance or None
    """
    global _redis_cache

    if not redis_url:
        logger.info("Redis caching disabled (no REDIS_URL provided)")
        return None

    _redis_cache = RedisCache(redis_url)
    connected = await _redis_cache.connect()

    if not connected:
        logger.warning("Redis cache initialization failed, continuing without cache")
        _redis_cache = None

    return _redis_cache


async def close_redis_cache():
    """Close Redis connection"""
    global _redis_cache
    if _redis_cache:
        await _redis_cache.disconnect()
        _redis_cache = None
