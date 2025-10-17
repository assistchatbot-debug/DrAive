# Changelog

All notable changes to DrAivBot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2025-10-17

### 🚀 Redis Cache Integration - Performance Upgrade

**Hybrid Session Storage: Redis + Supabase**

### ✨ New Features

**Redis Cache Layer**
- ✅ Hybrid session storage: Redis (hot) + Supabase (cold)
- ✅ 5-10x faster session access (~10ms vs ~50ms)
- ✅ Automatic TTL (24 hours)
- ✅ Graceful fallback if Redis unavailable
- ✅ Connection pooling (50 connections)
- ✅ Cache-aside pattern with auto-refresh

**Performance**
- Redis HIT: ~10ms
- Redis MISS → Supabase: ~50ms
- Cache invalidation on updates
- Background TTL expiration

**New Files**
- `bot/core/redis_cache.py` - Redis connection manager (300+ lines)
- Updated `bot/core/session.py` - Hybrid session manager

**Dependencies**
```txt
redis==5.0.1
hiredis==2.3.2
```

**Configuration**
```env
REDIS_URL=redis://localhost:6379/0
ENABLE_REDIS_CACHE=true
```

### 🔧 Usage

```bash
# Install Redis
sudo apt install redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:alpine

# Bot will auto-detect and use Redis
```

**Without Redis**: Bot works normally, using only Supabase.

---

## [2.0.0] - 2025-10-17

### 🎯 Major Refactoring - Modular Architecture

This is a complete rewrite of DrAivBot with enterprise-grade architecture for scalability and maintainability.

### ✨ New Architecture

**Modular Structure**
- Created independent modules: `company`, `analysis`, `planner`, `admin_scale`, `communications`, `zrs`, `training`
- Each module has its own router and handlers
- Clean separation of concerns
- Easy to add new features without touching existing code

**Core Infrastructure**
- `bot/core/database.py` - Centralized database operations with Supabase
- `bot/core/session.py` - Persistent session management (no more in-memory loss)
- `bot/core/notifications.py` - Unified notification system
- `bot/utils/keyboards.py` - Reusable keyboard layouts
- `bot/utils/texts.py` - Multilingual text resources (i18n)

**Database Schema**
- All tables created via Supabase migration
- RLS (Row Level Security) enabled on all tables
- Automatic session cleanup (24h expiration)
- Optimized indexes for performance

### 🚀 Features

**Session Management**
- ✅ Persistent sessions in Supabase (survives bot restarts)
- ✅ Automatic expiration after 24 hours
- ✅ JSON data storage for flexible state
- ✅ Background cleanup task

**Company Module**
- ✅ Company registration flow
- ✅ Automatic creation of 21-position organizational structure
- ✅ Founder assigned to all positions initially
- ✅ Orgchart display
- 🔄 Invitation system (in progress)

**Multilingual Support**
- ✅ Russian and English
- ✅ Auto-detect user language from Telegram
- ✅ Manual language switcher in settings
- ✅ Centralized text management

**Bot Commands**
- `/start` - Start bot / Main menu
- `/menu` - Show main menu

### 🔧 Technical Improvements

**Database**
- PostgreSQL via Supabase
- Async SQLAlchemy
- Connection pooling (10 connections + 20 overflow)
- Auto-reconnect on connection loss

**Code Quality**
- Type hints throughout
- Proper error handling
- Logging system
- Clean async/await patterns

**Scalability**
- Modular design allows horizontal scaling
- Database sessions instead of in-memory (no memory limit)
- Ready for Redis cache integration
- Background task system

### 📦 Dependencies

```txt
python-dotenv==1.0.0
aiogram==3.4.1
aiohttp==3.9.3
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1
openai==1.12.0
openpyxl==3.1.2
python-dateutil==2.8.2
pytz==2024.1
```

### 🗄️ Database Tables

1. **companies** - Company registry
2. **users** - User accounts (Telegram linked)
3. **positions** - 21-position organizational structure (7x21 methodology)
4. **invitation_links** - Employee invitation system
5. **sessions** - Persistent bot sessions
6. **events** - Calendar events and tasks

### 🔒 Security

- RLS enabled on all tables
- Service role for bot operations
- Company data isolation
- Automatic session expiration
- No hardcoded credentials

### 🐛 Bug Fixes

- Fixed session loss on bot restart (now persistent in DB)
- Fixed memory leaks from in-memory sessions
- Fixed race conditions in state management

### 🔄 Migration Notes

**Breaking Changes**
- Complete rewrite - not backward compatible with v1.x
- New database schema required
- Sessions need to be recreated

**Migration Steps**
1. Deploy new database schema
2. Update environment variables
3. Install new dependencies
4. Deploy bot code

---

## [1.7.0] - 2025-10-14

### 🎯 Major UX Update - Main Menu + Multilingual Support

**New Features**
- Main Menu System with 7 interactive sections
- Multilingual Support (RU/EN)
- Auto-detect user language
- Manual language switcher

---

## [1.6.0] - 2025-10-13

### 🎯 Major Changes - Compact Table Structure

- COMPACT TABULAR organizational structure
- 4 rows × 27 columns representation
- 45% code reduction in ai_core.py

---

## [1.5.2] - 2025-10-13

### Horizontal Format
- 10 columns instead of 8
- Combined unit numbering (7.19, 1.1, etc.)

---

## [1.5.1] - 2025-10-13

### 8-Column Organizational Structure
- Implemented 8-column structure
- Full 7x21 methodology
- 36 rows total (7 departments × 21 units)

---

## [1.4.4] - 2025-10-12

### Initial Release

**Features**
- AI-powered business analysis using OpenAI
- 7x21 methodology questionnaire (66 questions)
- Multi-currency financial data extraction
- Automated Excel report generation
- SWOT analysis and recommendations
- Telegram bot interface
- Two modes: full survey and test autofill

**Tech Stack**
- Python 3.11
- aiogram 3.x
- OpenAI API (gpt-4o-mini)
- openpyxl

---

## Version Numbering

- **Major** (X.0.0) - Breaking changes, architecture changes
- **Minor** (0.X.0) - New features, backward compatible
- **Patch** (0.0.X) - Bug fixes, minor improvements
