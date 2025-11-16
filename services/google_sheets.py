import gspread
import logging
from google.oauth2.service_account import Credentials
from config.settings import CREDENTIALS_FILE, GOOGLE_SHEETS_ID, SHEET_NAME
from datetime import datetime

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        self.client = None
        self.sheet = None
        self.connect()
    
    def connect(self):
        try:
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open_by_key(GOOGLE_SHEETS_ID).worksheet(SHEET_NAME)
            logger.info("Connected to Google Sheets")
        except Exception as e:
            logger.error(f"Error connecting to Google Sheets: {e}")
            raise
    
    def check_promocode_available(self, promocode_name):
        """Проверяем существует ли промокод и доступен ли он"""
        try:
            records = self.sheet.get_all_records()
            for record in records:
                if (record.get('promocode', '').lower() == promocode_name.lower() and 
                    record.get('used', '').upper() == 'FALSE'):
                    return True
            return False
        except Exception as e:
            logger.error(f"Error checking promocode: {e}")
            return False
    
    def record_game_attempt(self, promocode_name, user_info, user_choice, dice_result):
        """Записываем данные о попытке игры для всех игроков"""
        try:
            print(f"📝 Записываем попытку игры: {promocode_name}, пользователь: {user_info}")
            print(f"🎲 Результат: выбор={user_choice}, выпало={dice_result}")
            
            records = self.sheet.get_all_records()
            
            for i, record in enumerate(records, start=2):
                current_promo = record.get('promocode', '')
                
                if current_promo.lower() == promocode_name.lower():
                    # ОБНОВЛЯЕМ ДАННЫЕ ДЛЯ ВСЕХ ИГРОКОВ - used=TRUE для всех!
                    self.sheet.update_cell(i, 2, 'TRUE')  # used -> TRUE для ВСЕХ
                    self.sheet.update_cell(i, 3, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # data_used
                    self.sheet.update_cell(i, 4, f"{user_info} (выбор:{user_choice}, результат:{dice_result})")  # user_info + данные игры
                    
                    print(f"✅ Данные записаны для промокода {promocode_name} (used=TRUE)")
                    return True
            
            print("❌ Промокод не найден для записи данных")
            return False
            
        except Exception as e:
            print(f"💥 Ошибка при записи данных игры: {e}")
            return False
