"""
Configuration module for DrAivBot
Loads environment variables and provides centralized configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Supabase Configuration
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("VITE_SUPABASE_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY not found in environment variables")

# Database Configuration (async connection string)
DATABASE_URL = f"postgresql+asyncpg://postgres.lilkhrrocptlthoxfmen:{os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# Redis Configuration (optional - graceful fallback to Supabase only)
REDIS_URL = os.getenv("REDIS_URL")  # Format: redis://host:port/db or redis://password@host:port/db
ENABLE_REDIS_CACHE = os.getenv("ENABLE_REDIS_CACHE", "true").lower() == "true"

# Directories
REPORTS_DIR = "bot/data/reports"
RESPONSES_DIR = "bot/data/responses"

# Bot Settings
SESSION_TIMEOUT_HOURS = 24  # Sessions expire after 24 hours
MAX_SESSION_DATA_SIZE = 10 * 1024  # 10KB max session data
DEFAULT_LANGUAGE = "ru"
DEFAULT_TIMEZONE = "UTC"

# Feature Flags
ENABLE_DEMO_MODE = True  # Allow test mode without OpenAI
ENABLE_AUTO_CLEANUP = True  # Auto-cleanup expired sessions
