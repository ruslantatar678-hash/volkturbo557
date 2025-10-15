FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Позволяет Render передавать свои переменные окружения внутрь контейнера
ARG TELEGRAM_BOT_TOKEN
ARG ALPHAVANTAGE_API_KEY
ARG FX_BASE
ARG FX_QUOTE

ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ENV ALPHAVANTAGE_API_KEY=${ALPHAVANTAGE_API_KEY}
ENV FX_BASE=${FX_BASE}
ENV FX_QUOTE=${FX_QUOTE}

CMD ["python", "bot.py"]
