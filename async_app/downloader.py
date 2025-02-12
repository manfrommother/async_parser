import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

async def find_file_links(session, date):
    """
    Находит ссылки на файлы для конкретной даты.
    
    Args:
        session (aiohttp.ClientSession): Сессия для HTTP-запросов
        date (datetime): Дата для поиска файлов
    
    Returns:
        list: Список найденных ссылок на файлы
    """
    # Форматируем дату для URL
    date_str = date.strftime("%Y%m%d")
    url = f"https://spimex.com/markets/oil_products/trades/results/"
    
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.text()
        soup = BeautifulSoup(content, "html.parser")
        
        # Ищем все ссылки с нужной датой
        links = []
        for link in soup.find_all("a", class_="accordeon-inner__item-title", href=True):
            if date_str in link["href"]:
                links.append("https://spimex.com" + link["href"])
        
        return links

async def download_file(session, url):
    """
    Скачивает содержимое файла по URL.
    
    Args:
        session (aiohttp.ClientSession): Сессия для HTTP-запросов
        url (str): URL файла
    
    Returns:
        tuple: (дата файла, содержимое файла)
    """
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        
        # Извлекаем дату из URL
        date_match = re.search(r'(\d{8})', url)
        if date_match:
            date_str = date_match.group(1)
            file_date = datetime.strptime(date_str, "%Y%m%d")
        else:
            file_date = None
            
        return file_date, content

async def download_files_for_period(days=7):
    """
    Скачивает файлы за указанный период дней.
    
    Args:
        days (int): Количество дней для скачивания (по умолчанию 7)
    
    Returns:
        list: Список кортежей (дата, содержимое файла)
    """
    async with aiohttp.ClientSession() as session:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Создаем список дат для скачивания
        dates = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Пропускаем выходные
                dates.append(current_date)
            current_date += timedelta(days=1)

        # Получаем ссылки на файлы для всех дат
        all_links = []
        for date in dates:
            links = await find_file_links(session, date)
            all_links.extend(links)

        # Скачиваем все файлы параллельно
        tasks = [download_file(session, link) for link in all_links]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Фильтруем успешные результаты
        valid_results = [(date, content) for date, content in results 
                        if isinstance(content, bytes) and date is not None]
        
        return valid_results