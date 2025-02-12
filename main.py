import asyncio
import time
from datetime import datetime

# Импорт модулей асинхронной версии
from async_app.downloader import download_files_for_period as async_download_files
from async_app.parser import parse_data as async_parse_data
from async_app.db_loader import load_data as async_load_data
from async_app.database import init_db as async_init_db, engine as async_engine

# Импорт модулей синхронной версии
from sync_app.downloader import download_files_for_period as sync_download_files
from sync_app.parser import parse_data as sync_parse_data
from sync_app.db_loader import load_data as sync_load_data
from sync_app.database import init_db as sync_init_db, engine as sync_engine

def format_time(seconds):
    """Форматирует время в удобочитаемый вид"""
    return f"{seconds:.3f}"

async def run_async_version(days=7):
    """
    Запускает асинхронную версию приложения.
    """
    print(f"\n=== Асинхронная версия (период: {days} дней) ===")
    timings = {}
    total_records = 0
    
    # Отключаем echo для движка базы данных
    async_engine.echo = False
    
    # Инициализация БД
    print("1. Инициализация базы данных...")
    start = time.perf_counter()
    await async_init_db()
    timings['db_init'] = time.perf_counter() - start

    # Скачивание данных
    print("2. Скачивание данных с сайта...")
    start = time.perf_counter()
    files = await async_download_files(days)
    timings['download'] = time.perf_counter() - start
    print(f"   Найдено файлов: {len(files)}")

    # Парсинг данных
    print("3. Парсинг данных...")
    start = time.perf_counter()
    all_data = []
    for date, content in files:
        data = async_parse_data(content)
        total_records += len(data)
        all_data.extend(data)
    timings['parse'] = time.perf_counter() - start

    # Загрузка в БД
    print("4. Загрузка данных в базу...")
    start = time.perf_counter()
    await async_load_data(all_data)
    timings['db_load'] = time.perf_counter() - start

    total_time = sum(timings.values())
    
    print(f"\nРезультаты асинхронной версии:")
    print(f"├── Инициализация БД: {format_time(timings['db_init'])} сек")
    print(f"├── Скачивание файлов: {format_time(timings['download'])} сек")
    print(f"├── Парсинг данных: {format_time(timings['parse'])} сек")
    print(f"├── Загрузка в БД: {format_time(timings['db_load'])} сек")
    print(f"├── Обработано файлов: {len(files)}")
    print(f"└── Всего записей: {total_records}")
    return total_time, len(files), total_records

def run_sync_version(days=7):
    """
    Запускает синхронную версию приложения.
    """
    print(f"\n=== Синхронная версия (период: {days} дней) ===")
    timings = {}
    total_records = 0
    
    # Отключаем echo для движка базы данных
    sync_engine.echo = False
    
    # Инициализация БД
    print("1. Инициализация базы данных...")
    start = time.perf_counter()
    sync_init_db()
    timings['db_init'] = time.perf_counter() - start

    # Скачивание данных
    print("2. Скачивание данных с сайта...")
    start = time.perf_counter()
    files = sync_download_files(days)
    timings['download'] = time.perf_counter() - start
    print(f"   Найдено файлов: {len(files)}")

    # Парсинг данных
    print("3. Парсинг данных...")
    start = time.perf_counter()
    all_data = []
    for date, content in files:
        data = sync_parse_data(content)
        total_records += len(data)
        all_data.extend(data)
    timings['parse'] = time.perf_counter() - start

    # Загрузка в БД
    print("4. Загрузка данных в базу...")
    start = time.perf_counter()
    sync_load_data(all_data)
    timings['db_load'] = time.perf_counter() - start

    total_time = sum(timings.values())
    
    print(f"\nРезультаты синхронной версии:")
    print(f"├── Инициализация БД: {format_time(timings['db_init'])} сек")
    print(f"├── Скачивание файлов: {format_time(timings['download'])} сек")
    print(f"├── Парсинг данных: {format_time(timings['parse'])} сек")
    print(f"├── Загрузка в БД: {format_time(timings['db_load'])} сек")
    print(f"├── Обработано файлов: {len(files)}")
    print(f"└── Всего записей: {total_records}")
    return total_time, len(files), total_records

def main(days=7):
    """
    Основная функция: запускает обе версии и выводит сравнительный анализ производительности.
    """
    print("=" * 60)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")
    print(f"Дата и время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Период анализа: {days} дней")
    print("=" * 60)

    # Запуск обеих версий
    async_time, async_files, async_records = asyncio.run(run_async_version(days))
    sync_time, sync_files, sync_records = run_sync_version(days)

    # Подробное сравнение
    print("\n=== Итоговое сравнение ===")
    print(f"{'Метрика':25} {'Асинхронная':15} {'Синхронная':15}")
    print("-" * 60)
    print(f"{'Общее время (сек)':25} {format_time(async_time):15} {format_time(sync_time):15}")
    print(f"{'Обработано файлов':25} {async_files:15} {sync_files:15}")
    print(f"{'Всего записей':25} {async_records:15} {sync_records:15}")
    
    # Анализ производительности
    diff = abs(async_time - sync_time)
    faster = "асинхронная" if async_time < sync_time else "синхронная"
    percent = (diff / max(async_time, sync_time)) * 100

    print("\nВЫВОДЫ:")
    print(f"1. {faster.capitalize()} версия быстрее на {format_time(diff)} сек ({percent:.1f}%)")
    
    # Анализ эффективности для разного количества файлов
    if async_files > 1:
        async_per_file = async_time / async_files
        sync_per_file = sync_time / sync_files
        print(f"2. Среднее время на файл:")
        print(f"   - Асинхронная версия: {format_time(async_per_file)} сек")
        print(f"   - Синхронная версия:  {format_time(sync_per_file)} сек")
    
    # Рекомендации
    print("\nРЕКОМЕНДАЦИИ:")
    if async_time < sync_time:
        print("• Для обработки нескольких файлов рекомендуется использовать асинхронную версию")
        print("• Асинхронная версия особенно эффективна при большом количестве файлов")
    else:
        print("• Для текущего набора данных синхронная версия показывает лучшую производительность")
        print("• Рекомендуется провести дополнительное тестирование с большим количеством файлов")
    
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Сравнение производительности синхронной и асинхронной версий парсера')
    parser.add_argument('--days', type=int, default=7,
                      help='Количество дней для анализа (по умолчанию: 7)')
    
    args = parser.parse_args()
    main(args.days)