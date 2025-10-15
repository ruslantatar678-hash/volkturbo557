# 📈 Forex Telegram Bot (Docker + Render Ready)

## 🚀 Deploy to Render
1. Создай новый приватный репозиторий на GitHub и загрузи сюда файлы из этого архива.
2. На [Render.com](https://render.com) создай новый **Web Service**.
3. Подключи репозиторий и выбери:
   - **Environment:** Docker
   - Render сам найдёт `Dockerfile`
4. Добавь переменные окружения в разделе *Environment Variables*:
   ```
   TELEGRAM_BOT_TOKEN=твой_токен_бота
   ALPHAVANTAGE_API_KEY=твой_API_ключ
   FX_BASE=EUR
   FX_QUOTE=USD
   ```
5. Нажми **Deploy** — бот запустится и будет ждать команду /start в Telegram.

## ⚙️ Local Run
```bash
docker build -t forexbot .
docker run --env-file .env forexbot
```

