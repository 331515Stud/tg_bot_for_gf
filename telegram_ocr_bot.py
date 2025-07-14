import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import io

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# OCR.Space API endpoint
OCR_API_URL = "https://api.ocr.space/parse/image"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Я бот, который распознаёт текст на изображениях. '
        'Отправь мне картинку, и я верну тебе текст с неё!'
    )

# Обработчик для получения изображений
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем файл изображения
    photo = update.message.photo[-1]  # Берем изображение с самым высоким разрешением
    photo_file = await photo.get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    # Подготовка данных для отправки в OCR.Space
    files = {'file': ('image.jpg', photo_bytes, 'image/jpeg')}
    payload = {
        'language': 'rus',  # Поддержка русского языка, можно изменить на 'eng' или другой
        'isOverlayRequired': False,
        'filetype': 'JPG',
        'detectOrientation': True,
        'scale': True,
        # 'apikey': 'YOUR_OCR_SPACE_API_KEY'  # Раскомментируйте и добавьте API-ключ, если есть
    }

    # Отправляем запрос к OCR.Space API
    try:
        response = requests.post(OCR_API_URL, files=files, data=payload)
        response.raise_for_status()
        result = response.json()

        # Проверяем результат
        if result.get('IsErroredOnProcessing', True):
            error_message = result.get('ErrorMessage', ['Неизвестная ошибка'])
            logger.error(f"Ошибка OCR.Space: {error_message}")
            await update.message.reply_text('Произошла ошибка при обработке изображения.')
            return

        # Извлекаем текст
        parsed_text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')
        if parsed_text.strip():
            await update.message.reply_text(f'Распознанный текст:\n\n{parsed_text}')
        else:
            await update.message.reply_text('Не удалось распознать текст на изображении.')

    except Exception as e:
        logger.error(f"Ошибка при распознавании текста: {e}")
        await update.message.reply_text('Произошла ошибка при обработке изображения.')

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text('Произошла ошибка. Попробуйте снова.')

def main() -> None:
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    application = Application.builder().token('YOUR_BOT_TOKEN').build()

    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_error_handler(error_handler)

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()