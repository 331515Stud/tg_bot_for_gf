FROM python:3.11-slim

# Установка зависимостей ОС, включая Tesseract, OpenCV и дополнительные библиотеки
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

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска бота
CMD ["python", "app/telegram_bot.py"]
