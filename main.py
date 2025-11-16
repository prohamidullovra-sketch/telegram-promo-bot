import logging
from telegram.ext import Application, MessageHandler, filters
from handlers.dice_handler import DiceHandler
from utils.helpers import setup_logging
from config import settings

setup_logging()
logger = logging.getLogger(__name__)

def main():
    try:
        if not settings.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не настроен")
        
        application = Application.builder().token(settings.BOT_TOKEN).build()
        dice_handler = DiceHandler()
        
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, dice_handler.handle_message)
        )
        
        logger.info("Bot started")
        print("Бот запущен! Ctrl+C для остановки")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start: {e}")
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()
