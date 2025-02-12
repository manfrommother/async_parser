# SPIMEX Data Parser

Проект для асинхронного и синхронного парсинга данных с сайта биржи СПИМЕКС (https://spimex.com).

## Описание

Приложение скачивает файлы с результатами торгов с сайта СПИМЕКС, парсит их и загружает данные в базу данных PostgreSQL. Реализованы две версии: асинхронная (используя aiohttp и асинхронный SQLAlchemy) и синхронная (используя requests и стандартный SQLAlchemy) для сравнения производительности.

### Основные возможности:
- Асинхронное и синхронное скачивание файлов
- Парсинг Excel-файлов с данными торгов
- Загрузка данных в PostgreSQL
- Поддержка выбора периода анализа (по умолчанию 7 дней)
- Сравнительный анализ производительности двух версий

## Требования

- Python 3.8+
- PostgreSQL 12+

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/spimex-parser.git
cd spimex-parser
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# или
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте базу данных в PostgreSQL:
```sql
CREATE DATABASE spimex;
```

5. Настройте подключение к базе данных:
   - Откройте файлы `async_app/database.py` и `sync_app/database.py`
   - Измените параметры подключения (DATABASE_URL) в соответствии с вашими настройками

## Использование

### Базовый запуск
```bash
python main.py
```

### Запуск с указанием периода анализа
```bash
python main.py --days 14  # Анализ за 14 дней
```

## Структура проекта

```
spimex-parser/
├── async_app/
│   ├── __init__.py
│   ├── database.py      # Асинхронное подключение к БД
│   ├── downloader.py    # Асинхронное скачивание файлов
│   ├── parser.py        # Парсинг данных
│   ├── models.py        # ORM модели
│   └── db_loader.py     # Загрузка данных в БД
├── sync_app/
│   ├── __init__.py
│   ├── database.py      # Синхронное подключение к БД
│   ├── downloader.py    # Синхронное скачивание файлов
│   ├── parser.py        # Парсинг данных
│   ├── models.py        # ORM модели
│   └── db_loader.py     # Загрузка данных в БД
├── main.py              # Основной скрипт
├── requirements.txt     # Зависимости проекта
└── README.md           # Документация
```

## Особенности реализации

- Асинхронная версия использует aiohttp для параллельного скачивания файлов
- Обе версии используют pandas для парсинга Excel-файлов
- SQLAlchemy используется как ORM для работы с базой данных
- Учитываются выходные дни (файлы не скачиваются за субботу и воскресенье)
- Реализована обработка ошибок при скачивании и парсинге

## Зависимости

Основные библиотеки:
- aiohttp
- sqlalchemy
- asyncpg
- pandas
- requests
- beautifulsoup4
- psycopg2-binary
- openpyxl
