import re
import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from services.dice_service import DiceService

logger = logging.getLogger(__name__)

class DiceHandler:
    def __init__(self):
        self.dice_service = DiceService()
        self.pattern = re.compile(r'^([A-Z0-9]{5})\s+(\d)$', re.IGNORECASE)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            message = update.message or update.channel_post
            if not message or not message.text:
                return
            
            text = message.text.strip()
            match = self.pattern.search(text)
            
            if not match:
                return
            
            promocode_name = match.group(1).upper()
            user_choice = int(match.group(2))
            
            user_info = ""
            if message.from_user:
                user_info = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
            
            logger.info(f"Game request: promocode={promocode_name}, choice={user_choice}, user={user_info}")
            
            success, result_message = await self.dice_service.process_game(
                user_choice, promocode_name, user_info, update, context
            )
            
            await message.reply_text(result_message)
            
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
    
    async def maintenance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда для тех. работ (только для админов)"""
        try:
            # ТВОЙ ID ТЕПЕРЬ ЗДЕСЬ ↓
            ADMIN_IDS = [1275508553]  # Innovator @Putinbrothe
            
            if update.effective_user.id not in ADMIN_IDS:
                await update.message.reply_text("❌ Доступ запрещен")
                return
            
            if context.args and context.args[0].lower() in ['on', 'вкл']:
                self.dice_service.set_maintenance(True)
                await update.message.reply_text("🔧 Технические работы ВКЛЮЧЕНЫ")
            elif context.args and context.args[0].lower() in ['off', 'выкл']:
                self.dice_service.set_maintenance(False)
                await update.message.reply_text("✅ Технические работы ВЫКЛЮЧЕНЫ")
            else:
                status = "ВКЛЮЧЕН" if self.dice_service.is_maintenance() else "ВЫКЛЮЧЕН"
                await update.message.reply_text(f"🔧 Режим тех. работ: {status}\nИспользуй: /maintenance on/off")
                
        except Exception as e:
            logger.error(f"Error in maintenance command: {e}")
            await update.message.reply_text("❌ Ошибка команды")

def setup_dice_handlers(application):
    dice_handler = DiceHandler()
    application.add_handler(CommandHandler("maintenance", dice_handler.maintenance_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dice_handler.handle_message))
    return dice_handler
