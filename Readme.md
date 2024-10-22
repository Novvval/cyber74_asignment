### Mvideo monitoring service

Приложение для отслеживания продуктов на сайте mvideo.ru

Состоит из API, сервиса мониторинга и телеграм бота

Технологии: FastApi, SqlAlchemy, Postgres, Celery, Redis, Aiogram 

### Запуск

1. Создать бота в телеграме при помощи BotFather или использовать существующий токен бота 
2. Создать файл .env по примеру .env.example (там не хватает только токена телеграм бота):

```
# postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_PORT=5432

# monitoring
BROWSER_BIN=/usr/bin/google-chrome-stable
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
MONITORING_URL=http://monitoring:8001

# api
API_URL=http://api:8000

# telegram
BOT_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXX
```
3. Запустить проект командой `docker-compose up`
4. API доступен по http://127.0.0.1:8000, Мониторинг по http://127.0.0.1:8001