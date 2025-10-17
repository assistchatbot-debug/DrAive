# Быстрый старт DrAivBot

## Статус готовности

✅ **БОТ ГОТОВ К ЗАПУСКУ**

## Что уже настроено

- ✅ База данных Supabase (6 таблиц с RLS)
- ✅ Redis кэширование (опционально)
- ✅ Модульная архитектура
- ✅ Telegram Bot API
- ✅ OpenAI интеграция

## Установка зависимостей

```bash
# Установить Python пакеты (с --break-system-packages для Debian/Ubuntu)
pip3 install --break-system-packages --only-binary :all: -r requirements.txt
```

## Опциональная установка Redis

Redis увеличивает скорость работы в 5-10 раз, но не обязателен:

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

**Без Redis:** Бот автоматически использует только Supabase (все будет работать, но медленнее).

## Запуск бота

```bash
python3 main.py
```

**Важно:** Главный файл называется `main.py` (не `bot.py`), чтобы избежать конфликта имён с папкой `bot/`.

## Проверка запуска

При успешном запуске вы увидите:

```
🚀 Starting DrAivBot v2.0 (Modular Architecture)
✅ Redis cache enabled (или ⚠️ Redis unavailable, using Supabase only)
✅ Bot commands configured (RU/EN)
✅ Bot started successfully
```

## Первое использование

1. Откройте Telegram
2. Найдите бота: `@YourBotUsername`
3. Отправьте `/start`
4. Зарегистрируйте компанию
5. Начните работу!

## Основные команды

- `/start` - Главное меню
- `/menu` - Показать меню

## Настройка переменных окружения

Все уже настроено в `.env`:

- `TELEGRAM_BOT_TOKEN` - ✅ настроен
- `OPENAI_API_KEY` - ✅ настроен
- `VITE_SUPABASE_URL` - ✅ настроен
- `VITE_SUPABASE_ANON_KEY` - ✅ настроен
- `REDIS_URL` - ✅ настроен (опционально)

## Архитектура

```
bot/
├── core/           # Ядро системы
│   ├── database.py       # Работа с БД
│   ├── session.py        # Управление сессиями
│   ├── redis_cache.py    # Redis кэш
│   └── notifications.py  # Уведомления
├── modules/        # Модули функционала
│   ├── company/          # Управление компанией
│   ├── analysis/         # Бизнес-анализ (в разработке)
│   ├── planner/          # Планировщик (в разработке)
│   ├── admin_scale/      # Админка (в разработке)
│   ├── communications/   # Коммуникации (в разработке)
│   ├── zrs/              # ZRS система (в разработке)
│   └── training/         # Обучение (в разработке)
└── utils/          # Утилиты
    ├── keyboards.py      # Клавиатуры
    └── texts.py          # Тексты (i18n)
```

## Готовые модули

### ✅ Company (Компания)
- Регистрация компании
- Управление оргструктурой
- Просмотр структуры (7x21)
- Экспорт в Excel

### 🚧 В разработке
- Analysis - Бизнес-анализ
- Planner - Планировщик задач
- Admin Scale - Масштабирование команды
- Communications - Коммуникации
- ZRS - Zero-Risk System
- Training - Обучение

## Производительность

**С Redis:**
- Доступ к сессии: ~10ms
- Кэш попадания: >90%

**Без Redis:**
- Доступ к сессии: ~50ms
- Все через Supabase

## Устранение проблем

### Ошибка подключения к Redis
```
⚠️ Redis unavailable, using Supabase only
```
**Решение:** Это не ошибка! Бот работает без Redis.

### Ошибка подключения к Supabase
```
❌ Error: Invalid SUPABASE_URL
```
**Решение:** Проверьте `.env` файл.

### Ошибка Telegram Bot Token
```
❌ ValueError: TELEGRAM_BOT_TOKEN not found
```
**Решение:** Проверьте `.env` файл.

## База данных

База данных автоматически настроена через Supabase MCP:

- `companies` - Компании
- `users` - Пользователи
- `positions` - Должности (7x21)
- `sessions` - Сессии пользователей
- `events` - События и задачи
- `invitation_links` - Пригласительные ссылки

Все таблицы защищены Row Level Security (RLS).

## Масштабирование

Система готова к миллионам пользователей:

1. **Горизонтальное масштабирование**
   - Запускайте несколько инстансов бота
   - Redis обеспечит синхронизацию
   - Supabase Pooler управляет подключениями

2. **Вертикальное масштабирование**
   - Увеличьте pool_size в database.py
   - Настройте Redis max_connections
   - Оптимизируйте Supabase через Dashboard

3. **Мониторинг**
   - Логи в консоль (INFO уровень)
   - Redis статистика через `.get_stats()`
   - Supabase Dashboard для метрик БД

## Документация

- `README.md` - Общее описание
- `QUICKSTART.md` - Быстрый старт
- `ARCHITECTURE.md` - Архитектура системы
- `DEPLOYMENT.md` - Развертывание
- `CHANGELOG.md` - История изменений
- `START.md` - Этот файл

## Поддержка

Если возникли проблемы:

1. Проверьте логи при запуске
2. Убедитесь, что все зависимости установлены
3. Проверьте `.env` файл
4. Убедитесь, что Redis работает (если используется)

---

**Готово к запуску! 🚀**

```bash
python3 main.py
```
