"""
Session Manager for DrAivBot
Hybrid approach: Redis cache + Supabase persistent storage

Architecture:
- Hot sessions → Redis (fast access)
- Cold sessions → Supabase (persistent backup)
- Automatic sync between Redis and Supabase
- Graceful fallback if Redis unavailable
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json
import logging

from bot.core.database import get_pool
from bot.core.redis_cache import get_redis_cache
from bot.config import SESSION_TIMEOUT_HOURS

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Hybrid session manager with Redis cache + Supabase persistent storage

    Features:
    - Fast Redis cache for hot sessions (< 50ms)
    - Persistent Supabase storage for cold sessions
    - Automatic cache invalidation (24h TTL)
    - Graceful fallback if Redis unavailable
    - Thread-safe async operations

    Performance:
    - Redis hit: ~10ms
    - Redis miss → Supabase: ~50ms
    - Direct Supabase (no Redis): ~50ms
    """

    @staticmethod
    def _get_cache_key(telegram_id: int) -> str:
        """Generate Redis cache key"""
        return f"session:{telegram_id}"

    @staticmethod
    async def get_session(telegram_id: int) -> Dict[str, Any]:
        """
        Get session for telegram user (Redis → Supabase)

        Flow:
        1. Try Redis cache (fast)
        2. If miss → Load from Supabase
        3. Store in Redis for next access
        4. If expired → Create new session
        """
        cache = await get_redis_cache()
        cache_key = SessionManager._get_cache_key(telegram_id)

        # Try Redis first
        if cache and cache.is_connected():
            cached_session = await cache.get(cache_key)
            if cached_session:
                logger.debug(f"✅ Redis HIT: session:{telegram_id}")
                return cached_session

        # Redis miss → Load from Supabase
        logger.debug(f"⚠️ Redis MISS: session:{telegram_id} → Loading from Supabase")

        pool = await get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT id, user_id, company_id, state, data, expires_at
                FROM sessions
                WHERE telegram_id = $1
                  AND expires_at > NOW()
            """, telegram_id)

            if row:
                # Session exists in Supabase
                session_data = {
                    "id": str(row['id']),
                    "telegram_id": telegram_id,
                    "user_id": str(row['user_id']) if row['user_id'] else None,
                    "company_id": str(row['company_id']) if row['company_id'] else None,
                    "state": row['state'],
                    "data": row['data'] if row['data'] else {},
                    "expires_at": row['expires_at']
                }

                # Store in Redis for next access
                if cache and cache.is_connected():
                    await cache.set(cache_key, session_data, ttl=SESSION_TIMEOUT_HOURS * 3600)
                    logger.debug(f"✅ Cached to Redis: session:{telegram_id}")

                return session_data
            else:
                # Session expired or not exists → Create new
                return await SessionManager.create_session(telegram_id)

    @staticmethod
    async def create_session(telegram_id: int, **kwargs) -> Dict[str, Any]:
        """
        Create new session (write to both Redis + Supabase)
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            expires_at = datetime.utcnow() + timedelta(hours=SESSION_TIMEOUT_HOURS)

            row = await conn.fetchrow("""
                INSERT INTO sessions (
                    telegram_id, user_id, company_id, state, data, expires_at
                )
                VALUES (
                    $1, $2::uuid, $3::uuid, $4, $5, $6
                )
                ON CONFLICT (telegram_id) DO UPDATE
                SET user_id = EXCLUDED.user_id,
                    company_id = EXCLUDED.company_id,
                    state = EXCLUDED.state,
                    data = EXCLUDED.data,
                    expires_at = EXCLUDED.expires_at,
                    updated_at = NOW()
                RETURNING id, user_id, company_id, state, data, expires_at
            """,
                telegram_id,
                kwargs.get("user_id"),
                kwargs.get("company_id"),
                kwargs.get("state", "MENU"),
                json.dumps(kwargs.get("data", {})),
                expires_at
            )

            session_data = {
                "id": str(row['id']),
                "telegram_id": telegram_id,
                "user_id": str(row['user_id']) if row['user_id'] else None,
                "company_id": str(row['company_id']) if row['company_id'] else None,
                "state": row['state'],
                "data": row['data'] if row['data'] else {},
                "expires_at": row['expires_at']
            }

            # Store in Redis
            cache = await get_redis_cache()
            if cache and cache.is_connected():
                cache_key = SessionManager._get_cache_key(telegram_id)
                await cache.set(cache_key, session_data, ttl=SESSION_TIMEOUT_HOURS * 3600)
                logger.debug(f"✅ New session cached: session:{telegram_id}")

            return session_data

    @staticmethod
    async def update_session(
        telegram_id: int,
        state: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        company_id: Optional[str] = None
    ) -> None:
        """
        Update session (invalidate Redis + update Supabase)
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            updates = []
            params = [telegram_id]
            param_idx = 2

            if state is not None:
                updates.append(f"state = ${param_idx}")
                params.append(state)
                param_idx += 1

            if data is not None:
                updates.append(f"data = ${param_idx}::jsonb")
                params.append(json.dumps(data))
                param_idx += 1

            if user_id is not None:
                updates.append(f"user_id = ${param_idx}::uuid")
                params.append(user_id)
                param_idx += 1

            if company_id is not None:
                updates.append(f"company_id = ${param_idx}::uuid")
                params.append(company_id)
                param_idx += 1

            if updates:
                updates.append("updated_at = NOW()")
                updates.append("expires_at = NOW() + INTERVAL '24 hours'")

                query = f"""
                    UPDATE sessions
                    SET {', '.join(updates)}
                    WHERE telegram_id = $1
                """
                await conn.execute(query, *params)

                # Invalidate Redis cache (will be refreshed on next access)
                cache = await get_redis_cache()
                if cache and cache.is_connected():
                    cache_key = SessionManager._get_cache_key(telegram_id)
                    await cache.delete(cache_key)
                    logger.debug(f"🗑️ Invalidated cache: session:{telegram_id}")

    @staticmethod
    async def delete_session(telegram_id: int) -> None:
        """Delete session (from both Redis + Supabase)"""
        # Delete from Supabase
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM sessions WHERE telegram_id = $1",
                telegram_id
            )

        # Delete from Redis
        cache = await get_redis_cache()
        if cache and cache.is_connected():
            cache_key = SessionManager._get_cache_key(telegram_id)
            await cache.delete(cache_key)
            logger.debug(f"🗑️ Deleted session: session:{telegram_id}")

    @staticmethod
    async def cleanup_expired_sessions() -> int:
        """
        Remove expired sessions from Supabase
        Redis TTL handles cache expiration automatically

        Returns:
            Number of deleted sessions
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            result = await conn.fetch("""
                DELETE FROM sessions
                WHERE expires_at < NOW()
                RETURNING id
            """)
            deleted_count = len(result)

            if deleted_count > 0:
                logger.info(f"🧹 Cleaned up {deleted_count} expired sessions from Supabase")

            return deleted_count

    @staticmethod
    async def set_session_field(telegram_id: int, field: str, value: Any) -> None:
        """Set a specific field in session data"""
        current_session = await SessionManager.get_session(telegram_id)
        data = current_session.get("data", {})
        data[field] = value
        await SessionManager.update_session(telegram_id, data=data)

    @staticmethod
    async def get_session_field(telegram_id: int, field: str, default: Any = None) -> Any:
        """Get a specific field from session data"""
        current_session = await SessionManager.get_session(telegram_id)
        return current_session.get("data", {}).get(field, default)

    @staticmethod
    async def get_cache_stats() -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with Redis stats or error
        """
        cache = await get_redis_cache()
        if not cache or not cache.is_connected():
            return {
                "enabled": False,
                "message": "Redis cache disabled or disconnected"
            }

        stats = await cache.get_stats()
        stats["enabled"] = True
        return stats
