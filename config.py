import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

#База данных
DATABASE_URL = os.getenv('DATABASE_URL')
SYNC_DATABASE_URL = os.getenv('SYNC_DATABASE_URL')

#Url и пути
SPIMEX_URL = os.getenv('DATABASE_URL')
DOWNLOAD_PATH = Path(os.getenv('DOWNLOAD_PATH', './downloads'))

#Создаем директорию для загрузок, если она не существует 
DOWNLOAD_PATH.mkdir(exist_ok=True)

