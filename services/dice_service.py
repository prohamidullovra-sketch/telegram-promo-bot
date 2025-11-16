import random
import logging
import asyncio
from services.google_sheets import GoogleSheetsService

logger = logging.getLogger(__name__)

class DiceService:
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.maintenance_mode = False  # Режим тех. работ
    
    def roll_dice(self):
        return random.randint(1, 6)
    
    def set_maintenance(self, status: bool):
        """Включить/выключить тех. работы"""
        self.maintenance_mode = status
        logger.info(f"Maintenance mode: {status}")
    
    def is_maintenance(self):
        return self.maintenance_mode
    
    async def process_game(self, user_choice, promocode_name, user_info="", update=None, context=None):
        try:
            # Проверка тех. работ
            if self.is_maintenance():
                return False, "🔧 Идут технические работы. Попробуйте позже!"
            
            if not 1 <= user_choice <= 6:
                return False, "Неверное число. Выберите от 1 до 6"
            
            # Проверяем существует ли такой промокод и доступен ли он
            promocode_available = self.sheets_service.check_promocode_available(promocode_name)
            
            if not promocode_available:
                return False, f"Промокод '{promocode_name}' не найден или уже использован"
            
            # АНИМАЦИЯ БРОСКА КУБИКА TELEGRAM
            dice_result = self.roll_dice()
            if update and context:
                message = update.message or update.channel_post
                if message:
                    dice_message = await message.reply_dice(emoji="🎲")
                    await asyncio.sleep(4)
                    dice_result = dice_message.dice.value
            
            logger.info(f"Dice roll: {dice_result}, User choice: {user_choice}, Promocode: {promocode_name}")
            
            # ЗАПИСЫВАЕМ ДАННЫЕ ДЛЯ ВСЕХ ИГРОКОВ
            success = self.sheets_service.record_game_attempt(promocode_name, user_info, user_choice, dice_result)
            
            if not success:
                return False, "Ошибка записи данных в таблицу"
            
            # Проверка выигрыша с НОВЫМИ ТЕКСТАМИ
            if user_choice == dice_result:
                return True, f"✅ Ура! Вам выпало число {dice_result}!\nВы выиграли промо-период без комиссии нашего таксопарка на 24 часа!\nДля активации обратитесь к @manager_protaxi"
            else:
                return False, f"❌ Эх, почти!\nВыпало число {dice_result}. Совершите еще 10 поездок — и новая попытка ваша!"
                
        except Exception as e:
            logger.error(f"Error processing game: {e}")
            return False, "Произошла ошибка. Попробуйте позже."
