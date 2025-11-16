import os
import json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', '@manager_protaxi')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
SHEET_NAME = os.getenv('SHEET_NAME', 'promocodes')
CREDENTIALS_FILE = 'credentials/service_account.json'

WIN_MESSAGE = "Вы выиграли! для активации промокода обратитесь к @manager_protaxi"
LOSE_MESSAGE = "К сожалению, вы не угадали. попробуйте еще раз!"
