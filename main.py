import logging
from telegram.ext import Application, MessageHandler, filters
from handlers.dice_handler import setup_dice_handlers
from utils.helpers import setup_logging
from config import settings

setup_logging()
logger = logging.getLogger(__name__)

def main():
    try:
        if not settings.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не настроен")
        
        application = Application.builder().token(settings.BOT_TOKEN).build()
        setup_dice_handlers(application)
        
        logger.info("Bot started")
        print("Бот запущен! Ctrl+C для остановки")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start: {e}")
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()
