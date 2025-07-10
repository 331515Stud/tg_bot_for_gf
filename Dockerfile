FROM python:3.11-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    libopencv-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip
RUN pip install --upgrade pip

# Рабочая директория
WORKDIR /app

# Копирование файлов
COPY . .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Открытие порта (для веб-хука)
EXPOSE 10000

# Запуск бота
CMD ["python", "app/telegram_bot.py"]
