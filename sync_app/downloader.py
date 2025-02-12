import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def find_file_links(date):
    """
    Находит ссылки на файлы для конкретной даты.
    
    Args:
        date (datetime): Дата для поиска файлов
    
    Returns:
        list: Список найденных ссылок на файлы
    """
    date_str = date.strftime("%Y%m%d")
    url = f"https://spimex.com/markets/oil_products/trades/results/"
    
    response = requests.get(url)
    response.raise_for_status()
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    
    links = []
    for link in soup.find_all("a", class_="accordeon-inner__item-title", href=True):
        if date_str in link["href"]:
            links.append("https://spimex.com" + link["href"])
    
    return links

def download_file(url):
    """
    Скачивает содержимое файла по URL.
    
    Args:
        url (str): URL файла
    
    Returns:
        tuple: (дата файла, содержимое файла)
    """
    response = requests.get(url)
    response.raise_for_status()
    content = response.content
    
    # Извлекаем дату из URL
    date_match = re.search(r'(\d{8})', url)
    if date_match:
        date_str = date_match.group(1)
        file_date = datetime.strptime(date_str, "%Y%m%d")
    else:
        file_date = None
        
    return file_date, content

def download_files_for_period(days=7):
    """
    Скачивает файлы за указанный период дней.
    
    Args:
        days (int): Количество дней для скачивания (по умолчанию 7)
    
    Returns:
        list: Список кортежей (дата, содержимое файла)
    """
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
        links = find_file_links(date)
        all_links.extend(links)

    # Скачиваем все файлы
    results = []
    for link in all_links:
        try:
            result = download_file(link)
            if isinstance(result[1], bytes) and result[0] is not None:
                results.append(result)
        except Exception as e:
            print(f"Error downloading {link}: {e}")
    
    return results