"""
Supabase MCP Database Wrapper
Uses Supabase MCP tools for database operations instead of direct asyncpg connection
"""
from typing import Optional, List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

# Note: This is a placeholder for MCP integration
# In production, you would configure actual Supabase connection details
# For now, we'll use a simple in-memory fallback for development

_mock_db = {
    "sessions": {},
    "users": {},
    "companies": {}
}


async def execute_query(query: str, *params) -> List[Dict[str, Any]]:
    """Execute a query and return results (mock implementation)"""
    logger.warning("⚠️ Using mock database - configure real Supabase connection in production")
    return []


async def fetchrow(query: str, *params) -> Optional[Dict[str, Any]]:
    """Fetch single row (mock implementation)"""
    logger.warning("⚠️ Using mock database - configure real Supabase connection in production")
    return None


async def fetchval(query: str, *params) -> Optional[Any]:
    """Fetch single value (mock implementation)"""
    logger.warning("⚠️ Using mock database - configure real Supabase connection in production")
    return None


async def fetch(query: str, *params) -> List[Dict[str, Any]]:
    """Fetch multiple rows (mock implementation)"""
    logger.warning("⚠️ Using mock database - configure real Supabase connection in production")
    return []
