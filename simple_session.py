"""
Simple In-Memory Session Manager (Fallback)
Uses dictionary for session storage when database is unavailable
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# In-memory session storage
_sessions: Dict[int, Dict[str, Any]] = {}

SESSION_TIMEOUT_HOURS = 24


class SimpleSessionManager:
    """Simple session manager using in-memory storage"""

    @staticmethod
    async def get_session(telegram_id: int) -> Dict[str, Any]:
        """Get or create session"""
        if telegram_id not in _sessions:
            _sessions[telegram_id] = {
                "telegram_id": telegram_id,
                "user_id": None,
                "company_id": None,
                "state": "MENU",
                "data": {},
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=SESSION_TIMEOUT_HOURS)
            }
            logger.debug(f"✅ Created new session for {telegram_id}")

        # Check expiration
        session = _sessions[telegram_id]
        if session["expires_at"] < datetime.utcnow():
            # Renew expired session
            session["expires_at"] = datetime.utcnow() + timedelta(hours=SESSION_TIMEOUT_HOURS)
            logger.debug(f"🔄 Renewed expired session for {telegram_id}")

        return session

    @staticmethod
    async def update_session(
        telegram_id: int,
        state: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        company_id: Optional[str] = None
    ) -> None:
        """Update session"""
        session = await SimpleSessionManager.get_session(telegram_id)

        if state is not None:
            session["state"] = state
        if data is not None:
            session["data"] = data
        if user_id is not None:
            session["user_id"] = user_id
        if company_id is not None:
            session["company_id"] = company_id

        session["expires_at"] = datetime.utcnow() + timedelta(hours=SESSION_TIMEOUT_HOURS)
        logger.debug(f"✏️ Updated session for {telegram_id}")

    @staticmethod
    async def delete_session(telegram_id: int) -> None:
        """Delete session"""
        if telegram_id in _sessions:
            del _sessions[telegram_id]
            logger.debug(f"🗑️ Deleted session for {telegram_id}")

    @staticmethod
    async def cleanup_expired_sessions() -> int:
        """Remove expired sessions"""
        now = datetime.utcnow()
        expired = [tid for tid, sess in _sessions.items() if sess["expires_at"] < now]

        for tid in expired:
            del _sessions[tid]

        if expired:
            logger.info(f"🧹 Cleaned up {len(expired)} expired sessions")

        return len(expired)

    @staticmethod
    async def create_session(telegram_id: int, **kwargs) -> Dict[str, Any]:
        """Create new session"""
        session = {
            "telegram_id": telegram_id,
            "user_id": kwargs.get("user_id"),
            "company_id": kwargs.get("company_id"),
            "state": kwargs.get("state", "MENU"),
            "data": kwargs.get("data", {}),
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=SESSION_TIMEOUT_HOURS)
        }
        _sessions[telegram_id] = session
        logger.debug(f"✅ Created session for {telegram_id}")
        return session
