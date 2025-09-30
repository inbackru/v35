#!/usr/bin/env python3
"""
АВТОМАТИЧЕСКИЙ ИМПОРТ ДАННЫХ ИЗ ПАРСЕРА
Для использования с системой автоматического парсинга недвижимости
"""

import pandas as pd
import sys
import os
from datetime import datetime
from app import app, db
from models import Developer, ResidentialComplex, Building, Property
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_from_excel(excel_file_path):
    """
    Автоматический импорт данных из Excel файла парсера
    """
    if not os.path.exists(excel_file_path):
        logger.error(f"Файл {excel_file_path} не найден")
        return False
    
    try:
        # Импортируем с помощью существующего скрипта
        from import_parser_data import import_hierarchy_from_parser
        
        with app.app_context():
            stats = import_hierarchy_from_parser(excel_file_path)
            logger.info(f"Импорт завершен: {stats}")
            return True
            
    except Exception as e:
        logger.error(f"Ошибка импорта: {e}")
        return False

def import_from_api_data(data_dict):
    """
    Импорт данных напрямую из API/JSON парсера
    """
    logger.info(f"Получены данные для импорта: {len(data_dict)} записей")
    
    # Здесь можно добавить логику для прямого импорта из API
    # Пока используем временный файл Excel
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python auto_parser_import.py <путь_к_файлу.xlsx>")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    success = import_from_excel(excel_file)
    
    if success:
        print("✅ Автоматический импорт завершен успешно")
        sys.exit(0)
    else:
        print("❌ Ошибка автоматического импорта")
        sys.exit(1)
