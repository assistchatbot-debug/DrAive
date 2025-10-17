"""
Database operations for DrAivBot
Uses Supabase PostgreSQL with asyncpg directly (no SQLAlchemy ORM)
"""
import asyncpg
import os
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

from bot.config import SUPABASE_URL

logger = logging.getLogger(__name__)

# Extract project ID from Supabase URL
match = re.search(r'https://([^.]+)\.supabase\.co', SUPABASE_URL)
if not match:
    raise ValueError("Invalid SUPABASE_URL format")

project_id = match.group(1)

# Get database password from environment
# This should be set in production environment
db_password = os.getenv("SUPABASE_DB_PASSWORD", "postgres")

# Async PostgreSQL connection string for Supabase
DATABASE_URL = f"postgresql://postgres.{project_id}:{db_password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# Connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    """Get or create connection pool"""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=5,
            max_size=20,
            command_timeout=30,
            server_settings={
                'application_name': 'drAivBot'
            }
        )
        logger.info("✅ Database connection pool created")
    return _pool


async def close_pool():
    """Close connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


async def get_user_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
    """Get user by Telegram ID"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id, telegram_id, username, full_name, company_id, language, timezone
            FROM users
            WHERE telegram_id = $1
        """, telegram_id)

        if row:
            return {
                "id": str(row['id']),
                "telegram_id": row['telegram_id'],
                "username": row['username'],
                "full_name": row['full_name'],
                "company_id": str(row['company_id']) if row['company_id'] else None,
                "language": row['language'],
                "timezone": row['timezone']
            }
        return None


async def create_user(
    telegram_id: int,
    username: Optional[str] = None,
    full_name: Optional[str] = None,
    company_id: Optional[str] = None,
    language: str = "ru"
) -> Dict[str, Any]:
    """Create a new user"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO users (telegram_id, username, full_name, company_id, language)
            VALUES ($1, $2, $3, $4::uuid, $5)
            RETURNING id, telegram_id, username, full_name, company_id, language, timezone
        """, telegram_id, username, full_name, company_id, language)

        return {
            "id": str(row['id']),
            "telegram_id": row['telegram_id'],
            "username": row['username'],
            "full_name": row['full_name'],
            "company_id": str(row['company_id']) if row['company_id'] else None,
            "language": row['language'],
            "timezone": row['timezone']
        }


async def get_company_by_id(company_id: str) -> Optional[Dict[str, Any]]:
    """Get company by ID"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id, name, created_at
            FROM companies
            WHERE id = $1::uuid
        """, company_id)

        if row:
            return {
                "id": str(row['id']),
                "name": row['name'],
                "created_at": row['created_at']
            }
        return None


async def create_company(name: str) -> Dict[str, Any]:
    """Create a new company"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO companies (name)
            VALUES ($1)
            RETURNING id, name, created_at
        """, name)

        return {
            "id": str(row['id']),
            "name": row['name'],
            "created_at": row['created_at']
        }


async def get_company_positions(company_id: str) -> List[Dict[str, Any]]:
    """Get all positions for a company"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, company_id, position_number, position_name,
                   department_number, division_number, assigned_user_id,
                   is_founder, is_ceo
            FROM positions
            WHERE company_id = $1::uuid
            ORDER BY position_number
        """, company_id)

        positions = []
        for row in rows:
            positions.append({
                "id": str(row['id']),
                "company_id": str(row['company_id']),
                "position_number": row['position_number'],
                "position_name": row['position_name'],
                "department_number": row['department_number'],
                "division_number": row['division_number'],
                "assigned_user_id": str(row['assigned_user_id']) if row['assigned_user_id'] else None,
                "is_founder": row['is_founder'],
                "is_ceo": row['is_ceo']
            })
        return positions


async def create_position(
    company_id: str,
    position_number: int,
    position_name: str,
    department_number: int,
    division_number: int,
    assigned_user_id: Optional[str] = None,
    is_founder: bool = False,
    is_ceo: bool = False
) -> Dict[str, Any]:
    """Create a new position"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        position_id = await conn.fetchval("""
            INSERT INTO positions (
                company_id, position_number, position_name,
                department_number, division_number, assigned_user_id,
                is_founder, is_ceo
            )
            VALUES (
                $1::uuid, $2, $3, $4, $5, $6::uuid, $7, $8
            )
            RETURNING id
        """, company_id, position_number, position_name, department_number,
            division_number, assigned_user_id, is_founder, is_ceo)

        return {"id": str(position_id)}


async def get_events_for_user(
    user_id: str,
    start_date: datetime,
    end_date: datetime
) -> List[Dict[str, Any]]:
    """Get events for user in date range"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, title, description, event_type, event_date,
                   duration_minutes, reminder_minutes
            FROM events
            WHERE user_id = $1::uuid
              AND event_date >= $2
              AND event_date < $3
            ORDER BY event_date
        """, user_id, start_date, end_date)

        events = []
        for row in rows:
            events.append({
                "id": str(row['id']),
                "title": row['title'],
                "description": row['description'],
                "event_type": row['event_type'],
                "event_date": row['event_date'],
                "duration_minutes": row['duration_minutes'],
                "reminder_minutes": row['reminder_minutes']
            })
        return events


async def create_event(
    user_id: str,
    company_id: str,
    title: str,
    event_type: str,
    event_date: datetime,
    description: Optional[str] = None,
    duration_minutes: int = 60,
    reminder_minutes: Optional[int] = None
) -> Dict[str, Any]:
    """Create a new event"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        event_id = await conn.fetchval("""
            INSERT INTO events (
                user_id, company_id, title, description, event_type,
                event_date, duration_minutes, reminder_minutes
            )
            VALUES (
                $1::uuid, $2::uuid, $3, $4, $5, $6, $7, $8
            )
            RETURNING id
        """, user_id, company_id, title, description, event_type,
            event_date, duration_minutes, reminder_minutes)

        return {"id": str(event_id)}
