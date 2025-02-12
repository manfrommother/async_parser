import io
from typing import List, Dict
from datetime import datetime
import pandas as pd

def parse_data(file_content) -> List[Dict]:
    """
    Парсит данные из содержимого Excel‑файла.
    
    Если file_content является байтами (Excel‑файл), то:
      1. Сначала считывается весь лист без заголовка для поиска строки с датой торгов.
      2. Затем считывается таблица, начиная с нужной строки (например, с индексом 6).
      3. Удаляются столбцы с именами, содержащими "Unnamed".
      4. Переименовываются столбцы согласно заданному маппингу:
           "Объем\nДоговоров\nв единицах\nизмерения"  -> "volume"
           "Цена (за единицу измерения), руб."       -> "price"
           "Код\nИнструмента"                         -> "instrument_code"
           "Наименование\nИнструмента"                -> "instrument_name"
           "Базис\nпоставки"                          -> "basis"
           "Обьем\nДоговоров,\nруб."                  -> "value_contracts"
           "Изменение рыночной\nцены к цене\nпредыдуего дня" -> "price_change"
           "Цена в Заявках (за единицу\nизмерения)"   -> "price_in_quotes"
           "Количество\nДоговоров,\nшт."              -> "contracts_count"
      5. Если дата торгов была найдена, она добавляется ко всем записям в столбец 'trade_date'.
    
    Если file_content является строкой, предполагается, что это CSV‑данные (не используется для данного задания).
    
    Args:
        file_content (bytes или str): Содержимое файла.
        
    Returns:
        List[Dict]: Список словарей с данными торгов.
    """
    if isinstance(file_content, bytes):
        # Создаем объект ExcelFile из бинарных данных
        excel_file = pd.ExcelFile(io.BytesIO(file_content))
        # Предполагаем, что данные находятся на первом листе
        sheet_name = excel_file.sheet_names[0]
        
        # Считываем весь лист без заголовка для поиска метаданных (например, даты торгов)
        df_full = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        
        trade_date = None
        # Ищем в каждой ячейке строку, содержащую "Дата торгов:"
        for _, row in df_full.iterrows():
            for cell in row:
                if isinstance(cell, str) and "Дата торгов:" in cell:
                    parts = cell.split("Дата торгов:")
                    if len(parts) > 1:
                        date_str = parts[1].strip()
                        try:
                            # Разбираем дату в формате ДД.ММ.ГГГГ
                            trade_date = datetime.strptime(date_str, "%d.%m.%Y")
                        except Exception as e:
                            print(f"Ошибка при разборе даты: {e}")
                    break
            if trade_date is not None:
                break

        # Задаем номер строки, в которой находятся заголовки таблицы (0-indexed)
        header_row = 6  
        
        # Считываем таблицу с заголовками, начиная с header_row
        df_table = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row)
        
        # Удаляем столбцы, имена которых содержат "Unnamed"
        df_table = df_table.loc[:, ~df_table.columns.str.contains('Unnamed')]
        
        # Если дата торгов была найдена, добавляем ее как новый столбец
        if trade_date is not None:
            df_table['trade_date'] = trade_date
        else:
            print("Дата торгов не найдена в метаданных Excel-файла.")
        
        # Маппинг заголовков для переименования столбцов:
        rename_mapping = {
            "Код\nИнструмента": "instrument_code",
            "Наименование\nИнструмента": "instrument_name",
            "Базис\nпоставки": "basis",
            "Объем\nДоговоров\nв единицах\nизмерения": "volume",
            "Обьем\nДоговоров,\nруб.": "value_contracts",
            "Изменение рыночной\nцены к цене\nпредыдуего дня": "price_change",
            "Цена (за единицу измерения), руб.": "price",
            "Цена в Заявках (за единицу\nизмерения)": "price_in_quotes",
            "Количество\nДоговоров,\nшт.": "contracts_count"
        }
        df_table.rename(columns=rename_mapping, inplace=True)
        
        # Выведем список столбцов для отладки
        print("Столбцы после переименования:", df_table.columns.tolist())
        
        # Проверка наличия столбцов 'volume' и 'price' и приведение их к числовому типу
        if "volume" in df_table.columns:
            df_table["volume"] = pd.to_numeric(df_table["volume"], errors='coerce')
        else:
            print("Warning: Столбец 'volume' не найден. Текущие столбцы:", df_table.columns.tolist())
        
        if "price" in df_table.columns:
            df_table["price"] = pd.to_numeric(df_table["price"], errors='coerce')
        else:
            print("Warning: Столбец 'price' не найден. Текущие столбцы:", df_table.columns.tolist())
        
        return df_table.to_dict(orient="records")
    
    elif isinstance(file_content, str):
        print("Ожидался Excel-файл, но получена строка. Проверьте источник данных.")
        return []
    
    else:
        raise TypeError("Неподдерживаемый тип file_content. Ожидается bytes или str.")



