# DrAivBot - AI Strategy Advisor

Enterprise-level SaaS platform for corporate business management with AI assistance.

## 🎯 Overview

DrAivBot is a Telegram-based AI assistant designed for enterprise business management, implementing the 7x21 organizational methodology. It helps companies:

- ✅ Analyze business ideas with AI (GPT-4o-mini)
- ✅ Build financial models and business plans
- ✅ Manage organizational structure (21 positions across 7 departments)
- ✅ Schedule tasks and events
- ✅ Automate routine operations
- ✅ Scale to millions of corporate users

## 🏗️ Architecture

### Modular Design

```
project/
├── bot.py                  # Main entry point with routing
├── requirements.txt        # Python dependencies
├── bot/
│   ├── config.py          # Configuration management
│   ├── core/              # Core functionality
│   │   ├── database.py    # Database operations (Supabase)
│   │   ├── session.py     # Session management (persistent)
│   │   └── notifications.py  # User notifications
│   ├── modules/           # Feature modules (independent)
│   │   ├── company/       # Company registration & orgchart
│   │   ├── analysis/      # Business analysis (7x21)
│   │   ├── planner/       # Task scheduler
│   │   ├── admin_scale/   # Goal management
│   │   ├── communications/# Internal/external comms
│   │   ├── zrs/           # Work documents
│   │   └── training/      # Knowledge base
│   ├── utils/             # Shared utilities
│   │   ├── keyboards.py   # Common keyboards
│   │   └── texts.py       # i18n texts (RU/EN)
│   └── data/              # Generated files
│       ├── reports/       # Excel reports
│       └── responses/     # User responses
```

### Technology Stack

- **Framework**: aiogram 3.4+ (Telegram Bot API)
- **Database**: Supabase (PostgreSQL)
- **AI**: OpenAI GPT-4o-mini
- **Session Storage**: Supabase (persistent, survives restarts)
- **Language**: Python 3.11+
- **Architecture**: Modular, event-driven

## 🚀 Features

### MVP (Current)

1. **Company Registration** ✅
   - Create company with 21-position structure
   - Founder automatically assigned to all positions
   - Invitation system for employees

2. **Business Analysis** (in development)
   - 7x21 methodology questionnaire
   - AI-powered market analysis
   - Financial modeling (CAPEX, OPEX, ROI)
   - Excel report generation

3. **Task Planner** (in development)
   - Calendar integration
   - Event scheduling
   - Timezone support
   - Reminders

### Roadmap

- Admin Scale (Goal Management)
- Communications Module
- Work Documents (ZRS)
- Training & Knowledge Base
- API for web interface integration

## 📦 Installation

### Prerequisites

- Python 3.11+
- Supabase account
- Telegram Bot Token
- OpenAI API Key

### Setup

1. **Clone repository**
```bash
git clone <repository-url>
cd project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**

Create `.env` file:
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token

# OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini

# Supabase
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=your_anon_key
```

4. **Run migrations**

Database schema is automatically created via Supabase MCP tools.

5. **Start bot**
```bash
python bot.py
```

## 📊 Database Schema

### Tables

- **companies** - Company registry
- **users** - User accounts (linked to Telegram)
- **positions** - 21-position organizational structure
- **sessions** - Persistent bot sessions
- **events** - Calendar events and tasks
- **invitation_links** - Employee invitation system

### Key Features

- **Row Level Security (RLS)** enabled on all tables
- **Auto-expiring sessions** (24 hours)
- **Cascade deletes** for data integrity
- **Indexes** for performance optimization

## 🔧 Configuration

### Session Management

```python
SESSION_TIMEOUT_HOURS = 24  # Sessions expire after 24 hours
```

Sessions are stored in Supabase, surviving bot restarts.

### Language Support

Currently supports:
- 🇷🇺 Russian
- 🇬🇧 English

Add new languages in `bot/utils/texts.py`

## 🎨 Development

### Adding a New Module

1. Create module directory:
```bash
mkdir bot/modules/my_module
```

2. Create `__init__.py`:
```python
from aiogram import Router
router = Router(name="my_module")
from . import handlers
```

3. Create `handlers.py`:
```python
from aiogram import types, F
from bot.modules.my_module import router

@router.callback_query(F.data == "my_action")
async def my_handler(callback: types.CallbackQuery):
    # Your logic here
    pass
```

4. Register router in `bot.py`:
```python
from bot.modules.my_module import router as my_module_router
dp.include_router(my_module_router)
```

### Code Style

- **Modularity**: Each module is independent
- **Clean imports**: Use absolute imports
- **Type hints**: Use where possible
- **Async/await**: All I/O operations are async
- **Error handling**: Use try/except with logging

## 🔒 Security

- **RLS enabled** on all tables
- **Service role** used for bot operations
- **Company isolation** at database level
- **No hardcoded secrets** (use .env)
- **Session expiration** for inactive users

## 📈 Scalability

### Current Capacity

- **Database**: Supabase PostgreSQL (10GB free tier)
- **Sessions**: In-database storage (no memory limit)
- **Concurrent users**: ~100k+ (with proper indexing)

### Future Optimizations

- **Redis cache** for active sessions
- **Connection pooling** (already implemented)
- **Horizontal scaling** via load balancer
- **CDN** for static assets

## 🐛 Troubleshooting

### Common Issues

**Bot doesn't start**
- Check `TELEGRAM_BOT_TOKEN` in `.env`
- Verify Supabase connection

**Sessions not persisting**
- Check database migrations applied
- Verify RLS policies

**AI analysis fails**
- Check `OPENAI_API_KEY` validity
- Verify model name (gpt-4o-mini)

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📄 License

Proprietary - All Rights Reserved

## 👥 Team

- **Architect**: DrAiv Team
- **AI Integration**: OpenAI GPT-4o-mini
- **Infrastructure**: Supabase

## 🤝 Contributing

This is a private enterprise project. For access, contact the team.

---

**Version**: 2.0.0 (Modular Architecture)
**Last Updated**: 2025-10-17
