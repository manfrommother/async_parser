import requests
from pathlib import Path
from datetime import datetime
from ..config import SPIMEX_URL, DOWNLOAD_PATH

class SyncDownloader:
    """Класс для синхронной загрузки с сайта SPIMEX"""
    
    def __init__(self):
        self.base_url = SPIMEX_URL
        self.download_path = DOWNLOAD_PATH

    def download_file(self, url: str, filename: str) -> Path:
        """
        Скачивает один файл синхронно.
        
        Args:
            url: URL до файла для скачивания
            filename: Название скаченного файла
            
        Returns:
            Путь до скаченного файла
        """
        filepath = self.download_path / filename
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return filepath
        raise Exception(f"Failed to download {url}, status: {response.status_code}")

    def download_files(self, dates: list[datetime]) -> list[Path]:
        """
        Скачивание множества файлов синхронно
        
        Args:
            dates: Список дат для скачивания
            
        Returns:
            Список путей скаченных файлов
        """
        downloaded_files = []
        for date in dates:
            filename = f"spimex_{date.strftime('%Y%m%d')}.xlsx"
            url = f"{self.base_url}/{filename}"
            filepath = self.download_file(url, filename)
            downloaded_files.append(filepath)
        return downloaded_files