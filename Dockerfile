FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Эта строка гарантирует передачу переменных окружения
ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]
