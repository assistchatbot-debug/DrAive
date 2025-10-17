# Deployment Guide

Руководство по развертыванию DrAivBot в production.

## 🎯 Требования

### Минимальные требования

- **CPU**: 1 vCPU
- **RAM**: 512 MB
- **Disk**: 2 GB
- **OS**: Ubuntu 20.04+ / Debian 11+
- **Python**: 3.11+
- **Network**: Stable internet connection

### Рекомендуемые требования

- **CPU**: 2 vCPU
- **RAM**: 2 GB
- **Disk**: 10 GB (SSD)
- **OS**: Ubuntu 22.04 LTS
- **Python**: 3.11+

---

## 🚀 Варианты развертывания

### Option 1: Systemd Service (Recommended)

Лучший вариант для VPS/Dedicated серверов.

#### 1. Подготовка сервера

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Установить git
sudo apt install git -y

# Создать пользователя для бота
sudo useradd -m -s /bin/bash draivbot
sudo su - draivbot
```

#### 2. Клонировать репозиторий

```bash
cd ~
git clone <repository-url> draivbot
cd draivbot
```

#### 3. Создать виртуальное окружение

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Настроить .env

```bash
nano .env
```

```env
TELEGRAM_BOT_TOKEN=your_token_here
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=your_anon_key_here
```

#### 5. Тестовый запуск

```bash
python bot.py
# Проверьте что бот запускается
# Ctrl+C для остановки
```

#### 6. Создать systemd service

```bash
exit  # Выйти из пользователя draivbot
sudo nano /etc/systemd/system/draivbot.service
```

```ini
[Unit]
Description=DrAivBot - AI Strategy Advisor
After=network.target

[Service]
Type=simple
User=draivbot
WorkingDirectory=/home/draivbot/draivbot
Environment="PATH=/home/draivbot/draivbot/venv/bin"
ExecStart=/home/draivbot/draivbot/venv/bin/python bot.py
Restart=always
RestartSec=10

# Logging
StandardOutput=append:/var/log/draivbot/bot.log
StandardError=append:/var/log/draivbot/error.log

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

#### 7. Создать директорию для логов

```bash
sudo mkdir -p /var/log/draivbot
sudo chown draivbot:draivbot /var/log/draivbot
```

#### 8. Запустить сервис

```bash
# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить автозапуск
sudo systemctl enable draivbot

# Запустить бота
sudo systemctl start draivbot

# Проверить статус
sudo systemctl status draivbot

# Просмотр логов
sudo tail -f /var/log/draivbot/bot.log
```

#### 9. Управление сервисом

```bash
# Остановить
sudo systemctl stop draivbot

# Перезапустить
sudo systemctl restart draivbot

# Просмотр статуса
sudo systemctl status draivbot

# Просмотр логов
journalctl -u draivbot -f
```

---

### Option 2: Docker (Advanced)

Контейнеризация для изоляции и портативности.

#### 1. Создать Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directories
RUN mkdir -p bot/data/reports bot/data/responses

# Set environment
ENV PYTHONUNBUFFERED=1

# Run bot
CMD ["python", "bot.py"]
```

#### 2. Создать docker-compose.yml

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: draivbot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./bot/data:/app/bot/data
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### 3. Собрать и запустить

```bash
# Собрать образ
docker-compose build

# Запустить контейнер
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановить
docker-compose down

# Перезапустить
docker-compose restart
```

---

### Option 3: Screen/Tmux (Quick & Dirty)

⚠️ Не рекомендуется для production!

```bash
# Установить screen
sudo apt install screen -y

# Создать сессию
screen -S draivbot

# Запустить бота
cd ~/draivbot
source venv/bin/activate
python bot.py

# Отключиться: Ctrl+A, затем D
# Подключиться обратно: screen -r draivbot
```

---

## 🔧 Post-Deployment

### 1. Мониторинг

#### Systemd

```bash
# Логи в реальном времени
sudo journalctl -u draivbot -f

# Последние 100 строк
sudo journalctl -u draivbot -n 100

# Ошибки
sudo journalctl -u draivbot -p err
```

#### Docker

```bash
# Логи контейнера
docker logs -f draivbot

# Статистика ресурсов
docker stats draivbot
```

### 2. Backup

```bash
# Создать backup скрипт
sudo nano /usr/local/bin/draivbot-backup.sh
```

```bash
#!/bin/bash

BACKUP_DIR="/backups/draivbot"
DATE=$(date +%Y%m%d_%H%M%S)

# Создать директорию для backup
mkdir -p $BACKUP_DIR

# Backup данных
tar -czf $BACKUP_DIR/data_$DATE.tar.gz \
    /home/draivbot/draivbot/bot/data

# Backup .env
cp /home/draivbot/draivbot/.env \
   $BACKUP_DIR/env_$DATE.bak

# Удалить старые backup (старше 7 дней)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Сделать исполняемым
sudo chmod +x /usr/local/bin/draivbot-backup.sh

# Добавить в cron (ежедневно в 3:00)
sudo crontab -e
```

```cron
0 3 * * * /usr/local/bin/draivbot-backup.sh >> /var/log/draivbot/backup.log 2>&1
```

### 3. Обновления

```bash
# Перейти в директорию бота
cd /home/draivbot/draivbot

# Остановить бота
sudo systemctl stop draivbot

# Создать backup
/usr/local/bin/draivbot-backup.sh

# Получить обновления
git pull origin main

# Обновить зависимости
source venv/bin/activate
pip install -r requirements.txt

# Запустить бота
sudo systemctl start draivbot

# Проверить статус
sudo systemctl status draivbot
```

### 4. Настройка Firewall

```bash
# Установить UFW
sudo apt install ufw -y

# Разрешить SSH
sudo ufw allow 22/tcp

# Включить firewall
sudo ufw enable

# Проверить статус
sudo ufw status
```

---

## 🔒 Security Hardening

### 1. Ограничение прав

```bash
# Права на файлы
chmod 700 /home/draivbot/draivbot
chmod 600 /home/draivbot/draivbot/.env

# Владелец
chown -R draivbot:draivbot /home/draivbot/draivbot
```

### 2. Fail2ban (защита от brute-force)

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Automatic Security Updates

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 📊 Monitoring & Alerts

### 1. Health Check Script

```bash
#!/bin/bash
# /usr/local/bin/draivbot-healthcheck.sh

SERVICE_NAME="draivbot"

if systemctl is-active --quiet $SERVICE_NAME; then
    echo "✅ DrAivBot is running"
    exit 0
else
    echo "❌ DrAivBot is down!"
    # Restart service
    systemctl restart $SERVICE_NAME

    # Send alert (опционально)
    # curl -X POST https://hooks.slack.com/... \
    #   -d '{"text": "DrAivBot is down and restarted"}'

    exit 1
fi
```

### 2. Cron для health check

```cron
*/5 * * * * /usr/local/bin/draivbot-healthcheck.sh >> /var/log/draivbot/health.log 2>&1
```

---

## 🌐 Reverse Proxy (опционально)

Если планируется веб-интерфейс.

### Nginx

```nginx
server {
    listen 80;
    server_name bot.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🐛 Troubleshooting

### Бот не запускается

```bash
# Проверить логи
sudo journalctl -u draivbot -n 50

# Проверить .env файл
cat .env

# Проверить права
ls -la /home/draivbot/draivbot

# Проверить процесс
ps aux | grep bot.py
```

### Высокое использование памяти

```bash
# Проверить использование
ps aux --sort=-%mem | head -n 10

# Добавить swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### База данных недоступна

```bash
# Проверить connection string
python -c "from bot.config import SUPABASE_URL; print(SUPABASE_URL)"

# Проверить сетевое соединение
ping supabase.co

# Проверить через psql
psql "postgresql://..."
```

---

## 📈 Performance Tuning

### Python Optimization

```bash
# Установить PyPy (опционально, для ускорения)
sudo apt install pypy3 pypy3-venv -y

# Использовать PyPy вместо CPython
pypy3 -m venv venv_pypy
source venv_pypy/bin/activate
pip install -r requirements.txt
```

### Database Connection Pool

Уже настроено в `bot/core/database.py`:
```python
pool_size=10
max_overflow=20
pool_recycle=300
```

---

## 📞 Support

При проблемах с развертыванием:

1. Проверьте логи: `sudo journalctl -u draivbot -n 100`
2. Проверьте статус: `sudo systemctl status draivbot`
3. Проверьте конфигурацию: `cat .env`
4. Создайте issue в репозитории

---

## ✅ Checklist

Перед переходом в production:

- [ ] `.env` файл настроен корректно
- [ ] База данных создана и доступна
- [ ] Systemd service работает
- [ ] Логи пишутся корректно
- [ ] Backup настроен
- [ ] Health check работает
- [ ] Firewall настроен
- [ ] Security updates включены
- [ ] Мониторинг настроен
- [ ] Бот отвечает в Telegram

---

**Готово к production!** 🚀

После развертывания протестируйте все основные функции бота.
