import aiohttp
import asyncio
from pathlib import Path
from datetime import datetime
from ..config import SPIMEX_URL, DOWNLOAD_PATH


class AsyncDownloader:
    '''класс для асинхронной загрузки файлов с SPIMEX'''

    def __init__(self):
        self.base_url = SPIMEX_URL
        self.download_path = DOWNLOAD_PATH

    async def download_file(self, session: aiohttp.ClientSession, url: str, filename: str) -> Path:
        '''Скачивает файл асинхронно
            Args:
                session: aiohttp сессия
                url: URL для скачивания
                filename: название файла дл сохранения
                
            Returns:
                Путь до скаченного файла
        '''
        filepath = self.download_path / filename
        async with session.get(url) as response:
            if response.status == 200:
                with open(filepath, 'wb') as f:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                return filepath
            raise Exception(f'Загрузка провалена {url}, произошла ошибка: {response.status}')

    async def download_files(self, dates: list[datetime]) -> list[Path]:
        '''
        Скачивает неопределенное кол-во файлов асинхронно
        
        Args:
            dates: список с датами для загрузки
        
        Returns:
            Список путей до скачанных файлов
        '''
        async with aiohttp.ClientSession() as session:
            tasks = []
            for date in dates:
                filename = f'spimex_{date.strftime('%Y%m%d')}.xlsx'
                url = f'{self.base_url}/{filename}'
                tasks.append(self.download_file(session, url, filename))

            return await asyncio.gather(*tasks)

