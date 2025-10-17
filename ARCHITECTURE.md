# DrAivBot Architecture

Enterprise-level modular architecture for scalable SaaS platform.

## 🏗️ Design Principles

### 1. **Modularity**
Each module is independent and can be developed/deployed separately.

### 2. **Scalability**
- Database sessions (not in-memory)
- Connection pooling
- Async operations
- Ready for horizontal scaling

### 3. **Maintainability**
- Clear separation of concerns
- Centralized utilities
- Type hints throughout
- Comprehensive logging

### 4. **Security**
- RLS (Row Level Security) on all tables
- Company data isolation
- Session expiration
- No hardcoded secrets

---

## 📦 Project Structure

```
project/
├── bot.py                      # Main entry point
├── requirements.txt            # Dependencies
├── .env                        # Environment variables (not in repo)
├── README.md                   # User documentation
├── CHANGELOG.md                # Version history
├── ARCHITECTURE.md             # This file
│
├── bot/                        # Main bot package
│   ├── config.py              # Configuration management
│   │
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── database.py        # Database operations (Supabase)
│   │   ├── session.py         # Session management (persistent)
│   │   └── notifications.py   # User notifications
│   │
│   ├── modules/               # Feature modules (independent)
│   │   ├── __init__.py
│   │   │
│   │   ├── company/           # Company management
│   │   │   ├── __init__.py    # Router registration
│   │   │   ├── handlers.py    # Callback/message handlers
│   │   │   └── orgchart.py    # 7x21 organizational structure
│   │   │
│   │   ├── analysis/          # Business analysis (7x21 questionnaire)
│   │   │   ├── __init__.py
│   │   │   ├── handlers.py
│   │   │   ├── questionnaire.py
│   │   │   └── ai_core.py     # OpenAI integration
│   │   │
│   │   ├── planner/           # Task scheduler & calendar
│   │   │   ├── __init__.py
│   │   │   ├── handlers.py
│   │   │   ├── calendar.py
│   │   │   └── events.py
│   │   │
│   │   ├── admin_scale/       # Goal management (Admin Scale)
│   │   ├── communications/    # Communications module
│   │   ├── zrs/               # Work documents (ZRS)
│   │   └── training/          # Knowledge base
│   │
│   ├── utils/                 # Shared utilities
│   │   ├── __init__.py
│   │   ├── keyboards.py       # Reusable keyboard layouts
│   │   └── texts.py           # i18n text resources
│   │
│   └── data/                  # Generated data
│       ├── reports/           # Excel reports
│       └── responses/         # User responses (JSON)
```

---

## 🔄 Request Flow

### User Interaction Flow

```
User → Telegram → Bot
                   ↓
            Message Handler
                   ↓
         Session Manager (load session)
                   ↓
          Router (dispatch to module)
                   ↓
         Module Handler
                   ↓
    Database Operations (if needed)
                   ↓
         Update Session
                   ↓
    Send Response to User
```

### Example: Company Registration

```
1. User clicks "🚀 Начать работу"
   ↓
2. Callback: "create_company"
   ↓
3. company/handlers.py → start_company_registration()
   ↓
4. SessionManager.update_session(state="COMPANY_REGISTRATION")
   ↓
5. Ask user for company name
   ↓
6. User sends company name
   ↓
7. bot.py → handle_message() → process_company_name()
   ↓
8. database.create_company()
   ↓
9. database.create_user()
   ↓
10. orgchart.create_company_positions() (21 positions)
    ↓
11. SessionManager.update_session(state="MENU")
    ↓
12. Send success message + main menu
```

---

## 🗄️ Database Schema

### Tables Overview

| Table | Purpose | RLS | Cascade |
|-------|---------|-----|---------|
| `companies` | Company registry | ✅ | - |
| `users` | User accounts | ✅ | ON DELETE company |
| `positions` | 21-position orgchart | ✅ | ON DELETE company |
| `invitation_links` | Employee invitations | ✅ | ON DELETE company |
| `sessions` | Bot sessions (persistent) | ✅ | ON DELETE user |
| `events` | Calendar events | ✅ | ON DELETE user/company |

### Key Relationships

```
companies (1) ──────── (N) users
                          │
                          └─── (N) positions
                          │
                          └─── (N) events
                          │
                          └─── (1) sessions

positions (N) ──────── (1) users (assigned_user_id)

invitation_links (N) ── (1) companies
                    └── (1) positions
                    └── (1) users (created_by)
```

### Session Storage

```json
{
  "telegram_id": 123456789,
  "user_id": "uuid",
  "company_id": "uuid",
  "state": "MENU",
  "data": {
    "lang": "ru",
    "event_creation": {...},
    "analysis_progress": {...}
  },
  "expires_at": "2025-10-18T12:00:00Z"
}
```

**Benefits:**
- Survives bot restarts
- No memory limit
- Automatic cleanup (24h)
- Queryable for analytics

---

## 🔌 Module System

### Creating a New Module

#### 1. Create Module Structure

```bash
mkdir bot/modules/my_module
touch bot/modules/my_module/__init__.py
touch bot/modules/my_module/handlers.py
```

#### 2. Define Router (`__init__.py`)

```python
from aiogram import Router

router = Router(name="my_module")

from . import handlers
```

#### 3. Create Handlers (`handlers.py`)

```python
from aiogram import types, F
from bot.modules.my_module import router
from bot.core.session import SessionManager
from bot.core.database import get_user_by_telegram_id

@router.callback_query(F.data == "my_action")
async def handle_my_action(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    session = await SessionManager.get_session(telegram_id)

    # Your logic here

    await callback.answer()
```

#### 4. Register in Main Bot (`bot.py`)

```python
from bot.modules.my_module import router as my_module_router

dp.include_router(my_module_router)
```

### Module Independence

**Each module should:**
- Have its own router
- Manage its own state
- Not depend on other modules
- Use only core utilities

**Example Module Structure:**

```python
# bot/modules/planner/__init__.py
from aiogram import Router
router = Router(name="planner")
from . import handlers

# bot/modules/planner/handlers.py
from bot.modules.planner import router

@router.callback_query(F.data == "planner_day")
async def show_day_view(callback):
    # Planner-specific logic
    pass
```

---

## 🔧 Core Components

### 1. Database (`core/database.py`)

**Responsibilities:**
- Database connection management
- CRUD operations
- Query helpers

**Key Functions:**
```python
async def get_user_by_telegram_id(telegram_id: int)
async def create_company(name: str)
async def get_company_positions(company_id: str)
async def create_event(user_id, company_id, title, ...)
```

**Connection Pooling:**
```python
engine = create_async_engine(
    DATABASE_URL_ASYNC,
    pool_size=10,          # 10 persistent connections
    max_overflow=20,       # 20 overflow connections
    pool_timeout=30,       # 30 sec timeout
    pool_recycle=300       # Recycle every 5 min
)
```

### 2. Session Manager (`core/session.py`)

**Responsibilities:**
- Load/save sessions from Supabase
- Automatic expiration (24h)
- State management

**Key Methods:**
```python
async def get_session(telegram_id: int)
async def update_session(telegram_id, state=None, data=None, ...)
async def delete_session(telegram_id: int)
async def cleanup_expired_sessions()
```

**Usage Example:**
```python
# Get session
session = await SessionManager.get_session(telegram_id)
lang = session.get("data", {}).get("lang", "ru")

# Update session
await SessionManager.update_session(
    telegram_id,
    state="ANALYSIS",
    data={"lang": "ru", "question_index": 5}
)
```

### 3. Notifications (`core/notifications.py`)

**Responsibilities:**
- Send notifications to users
- Task progress updates
- Error alerts

**Usage Example:**
```python
notifications = NotificationManager(bot)

await notifications.notify_task_progress(
    telegram_id=123456,
    task_name="Анализ бизнес-идеи",
    status="✅",
    details="Отчет готов!"
)
```

---

## 🌐 Internationalization (i18n)

### Text Management

All texts stored in `bot/utils/texts.py`:

```python
TEXTS = {
    "ru": {
        "welcome": "👋 Добро пожаловать!",
        "menu_title": "📋 Что будем делать?",
        ...
    },
    "en": {
        "welcome": "👋 Welcome!",
        "menu_title": "📋 What would you like to do?",
        ...
    }
}

def get_text(lang: str, key: str) -> str:
    return TEXTS.get(lang, TEXTS["ru"]).get(key, key)
```

### Usage in Handlers

```python
from bot.utils.texts import get_text

session = await SessionManager.get_session(telegram_id)
lang = session.get("data", {}).get("lang", "ru")

await message.answer(get_text(lang, "welcome"))
```

### Adding New Language

1. Add to `TEXTS` dict in `texts.py`
2. Add language button in `keyboards.py`
3. Add callback handler for `lang_XX`

---

## 🚀 Scalability Strategy

### Current Capacity

- **Users**: ~100k concurrent
- **Database**: 10GB free tier (Supabase)
- **Sessions**: No memory limit (stored in DB)
- **API Rate Limits**: Telegram (30 msg/sec)

### Scaling Path

#### Phase 1: Vertical Scaling (Current)
- Connection pooling ✅
- Database indexes ✅
- Async operations ✅

#### Phase 2: Caching Layer
```python
# Redis for hot sessions
import aioredis

redis = await aioredis.create_redis_pool('redis://localhost')

# Cache active sessions in Redis
# Fallback to Supabase for cold sessions
```

#### Phase 3: Horizontal Scaling
```
Load Balancer
    ├── Bot Instance 1
    ├── Bot Instance 2
    └── Bot Instance 3
         ↓
    Supabase (shared)
    Redis (shared)
```

#### Phase 4: Microservices
```
API Gateway
    ├── Bot Service
    ├── Analysis Service (OpenAI)
    ├── Notification Service
    └── Scheduler Service
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
Never commit `.env` file:
```gitignore
.env
*.env
```

### 2. RLS Policies
All tables have RLS enabled:
```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role has full access"
  ON users FOR ALL
  USING (true) WITH CHECK (true);
```

### 3. Session Expiration
Auto-cleanup expired sessions:
```python
async def cleanup_sessions():
    while True:
        await SessionManager.cleanup_expired_sessions()
        await asyncio.sleep(3600)  # Every hour
```

### 4. Input Validation
Always validate user input:
```python
company_name = message.text.strip()
if len(company_name) < 3:
    await message.answer("❌ Name too short")
    return
```

---

## 📊 Monitoring & Logging

### Logging Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("✅ Bot started")
logger.error(f"❌ Error: {e}")
```

### Key Metrics to Track

- Active users per hour
- Session count
- Database query time
- OpenAI API latency
- Error rate
- Message throughput

---

## 🧪 Testing Strategy

### Unit Tests (Future)

```python
# tests/test_database.py
import pytest
from bot.core.database import create_company

@pytest.mark.asyncio
async def test_create_company():
    company = await create_company("Test Corp")
    assert company["name"] == "Test Corp"
    assert company["id"] is not None
```

### Integration Tests

Test full user flows:
1. Company registration
2. Employee invitation
3. Business analysis
4. Event scheduling

---

## 🔄 Deployment

### Development
```bash
python bot.py
```

### Production

**Option 1: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

**Option 2: Systemd Service**
```ini
[Unit]
Description=DrAivBot
After=network.target

[Service]
Type=simple
User=bot
WorkingDirectory=/opt/draivbot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📝 Version Control

### Git Workflow

```bash
main          # Production
  ↓
develop       # Staging
  ↓
feature/*     # Feature branches
```

### Commit Messages

```
feat: Add planner module
fix: Session not persisting
refactor: Move keyboards to utils
docs: Update architecture docs
```

---

## 🛠️ Development Tools

- **IDE**: VSCode / PyCharm
- **Linting**: pylint, black
- **Type Checking**: mypy
- **Testing**: pytest
- **Database**: Supabase Studio

---

**Last Updated**: 2025-10-17
**Version**: 2.0.0
