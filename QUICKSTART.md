# Quick Start Guide

Быстрый запуск DrAivBot за 5 минут.

## 📋 Предварительные требования

- Python 3.11+
- Telegram Bot Token (от [@BotFather](https://t.me/botfather))
- Supabase аккаунт (бесплатно на [supabase.com](https://supabase.com))
- OpenAI API Key (опционально для AI-анализа)

## 🚀 Установка

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd project
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить окружение

Создайте файл `.env` в корне проекта:

```env
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenAI (опционально)
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini

# Supabase
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=your_anon_key_here
```

### 5. Проверить БД

База данных уже создана через Supabase MCP. Проверить можно через Supabase Studio:
- Открыть [Supabase Dashboard](https://app.supabase.com)
- Перейти в Table Editor
- Убедиться что есть таблицы: `companies`, `users`, `positions`, `sessions`, `events`

### 6. Запустить бота

```bash
python bot.py
```

Вы должны увидеть:
```
🚀 Starting DrAivBot v2.0 (Modular Architecture)
✅ Bot commands configured (RU/EN)
✅ Bot started successfully
```

## ✅ Проверка работы

1. **Найдите бота в Telegram**
   - Откройте Telegram
   - Найдите бота по username (из @BotFather)

2. **Отправьте `/start`**
   - Должно появиться приветственное сообщение
   - Кнопки: "🚀 Начать работу" и "📩 У меня есть приглашение"

3. **Создайте компанию**
   - Нажмите "🚀 Начать работу"
   - Введите название компании
   - Бот создаст компанию с 21 позицией оргсхемы

4. **Проверьте главное меню**
   - Должны отобразиться 8 разделов:
     - 💡 Анализ бизнес-идеи
     - 📅 Планировщик
     - 🎯 Управление целями
     - 👥 Организационная структура
     - 💬 Коммуникации
     - 📋 Рабочие документы
     - 📚 База знаний
     - ⚙️ Настройки

## 🔧 Настройка

### Изменить язык

1. Нажмите "⚙️ Настройки / Settings"
2. Выберите язык (🇷🇺 Русский или 🇬🇧 English)

### Проверить сессии

Сессии хранятся в таблице `sessions` в Supabase:

```sql
SELECT * FROM sessions WHERE telegram_id = YOUR_TELEGRAM_ID;
```

### Просмотр логов

Бот пишет логи в консоль:
```bash
# Запустить с подробными логами
python bot.py 2>&1 | tee bot.log
```

## 🐛 Устранение неполадок

### Бот не запускается

**Проблема**: `ValueError: TELEGRAM_BOT_TOKEN not found`
- **Решение**: Проверьте `.env` файл, убедитесь что токен правильный

**Проблема**: `Error connecting to Supabase`
- **Решение**: Проверьте `VITE_SUPABASE_URL` и `VITE_SUPABASE_SUPABASE_ANON_KEY`

### Бот не отвечает

**Проблема**: Бот онлайн, но не отвечает на `/start`
- **Решение**:
  1. Остановите бота (Ctrl+C)
  2. Проверьте логи на ошибки
  3. Перезапустите: `python bot.py`

### Ошибки БД

**Проблема**: `relation "users" does not exist`
- **Решение**: Миграция не применена. Проверьте Supabase Dashboard → SQL Editor

## 📊 Проверка структуры БД

Подключитесь к Supabase и выполните:

```sql
-- Проверить таблицы
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Проверить количество компаний
SELECT COUNT(*) FROM companies;

-- Проверить сессии
SELECT COUNT(*) FROM sessions WHERE expires_at > NOW();
```

## 🎯 Следующие шаги

1. **Создать первую компанию** через бота
2. **Изучить код модулей** в `bot/modules/`
3. **Добавить новый модуль** (см. [ARCHITECTURE.md](ARCHITECTURE.md))
4. **Настроить OpenAI** для AI-анализа
5. **Развернуть на сервере** (Docker или systemd)

## 📚 Полезные ссылки

- [README.md](README.md) - Подробная документация
- [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура проекта
- [CHANGELOG.md](CHANGELOG.md) - История изменений
- [Supabase Docs](https://supabase.com/docs)
- [aiogram Docs](https://docs.aiogram.dev/)

## 💡 Полезные команды

```bash
# Активировать виртуальное окружение
source venv/bin/activate

# Установить новую зависимость
pip install package_name
pip freeze > requirements.txt

# Проверить код
python -m pylint bot/

# Запустить с debug логами
python bot.py --debug

# Остановить бота
# Нажмите Ctrl+C
```

## 🆘 Поддержка

Если возникли проблемы:
1. Проверьте логи бота
2. Проверьте Supabase Dashboard
3. Прочитайте [ARCHITECTURE.md](ARCHITECTURE.md)
4. Создайте issue в репозитории

---

**Готово!** 🎉 Бот запущен и готов к работе.

Следующий шаг: изучите модуль `company` чтобы понять как устроена архитектура.
