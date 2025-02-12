import io
from typing import List, Dict
from datetime import datetime
import pandas as pd

def parse_data(file_content: bytes) -> List[Dict]:
    """
    Парсит данные из содержимого Excel-файла.
    
    Args:
        file_content (bytes): Содержимое Excel-файла.
        
    Returns:
        List[Dict]: Список словарей с данными торгов.
    """
    if isinstance(file_content, bytes):
        # Создаем объект ExcelFile из бинарных данных
        excel_file = pd.ExcelFile(io.BytesIO(file_content))
        # Предполагаем, что данные находятся на первом листе
        sheet_name = excel_file.sheet_names[0]
        
        # Считываем весь лист без заголовка для поиска метаданных
        df_full = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        
        trade_date = None
        # Ищем строку с датой торгов
        for _, row in df_full.iterrows():
            for cell in row:
                if isinstance(cell, str) and "Дата торгов:" in cell:
                    parts = cell.split("Дата торгов:")
                    if len(parts) > 1:
                        date_str = parts[1].strip()
                        try:
                            trade_date = datetime.strptime(date_str, "%d.%m.%Y")
                        except Exception as e:
                            print(f"Ошибка при разборе даты: {e}")
                    break
            if trade_date is not None:
                break

        # Считываем таблицу с заголовками
        header_row = 6
        df_table = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row)
        
        # Удаляем столбцы без имени
        df_table = df_table.loc[:, ~df_table.columns.str.contains('Unnamed')]
        
        # Добавляем дату торгов
        if trade_date is not None:
            df_table['trade_date'] = trade_date
        
        # Маппинг заголовков
        rename_mapping = {
            "Объем\nДоговоров\nв единицах\nизмерения": "volume",
            "Цена (за единицу измерения), руб.": "price"
        }
        df_table.rename(columns=rename_mapping, inplace=True)
        
        # Приводим числовые столбцы к правильному типу
        if "volume" in df_table.columns:
            df_table["volume"] = pd.to_numeric(df_table["volume"], errors='coerce')
        
        if "price" in df_table.columns:
            df_table["price"] = pd.to_numeric(df_table["price"], errors='coerce')
        
        return df_table.to_dict(orient="records")
    
    else:
        raise TypeError("Неподдерживаемый тип file_content. Ожидается bytes.")