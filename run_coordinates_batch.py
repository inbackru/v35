#!/usr/bin/env python3
"""
Скрипт для запуска пакетной обработки координат
Можно запускать несколько раз - продолжит с места остановки
"""

from advanced_coordinates_processor import AdvancedCoordinatesProcessor
from app import app
import sys

def main():
    """Главная функция"""
    
    # Параметры командной строки  
    batch_size = 100  # по умолчанию для большого лимита
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            print("❌ Неверный размер пакета. Используйте число.")
            return
    
    print(f"📦 Размер пакета: {batch_size}")
    
    with app.app_context():
        processor = AdvancedCoordinatesProcessor()
        processor.batch_size = batch_size
        
        # Показываем текущую статистику
        stats = processor.get_stats()
        print(f"""
📊 Статистика перед обработкой:
🏘️ Районы: {stats['districts']['with_coords']}/{stats['districts']['total']} (осталось: {stats['districts']['remaining']})
🛣️ Улицы: {stats['streets']['with_coords']}/{stats['streets']['total']} (осталось: {stats['streets']['remaining']})
🌐 API запросы сегодня: {stats['api_usage']['daily_requests']}/{stats['api_usage']['daily_limit']}
        """)
        
        if stats['districts']['remaining'] == 0 and stats['streets']['remaining'] == 0:
            print("🎉 Все координаты уже получены!")
            return
            
        if not processor.check_daily_limit():
            print("⚠️ Дневной лимит API запросов исчерпан")
            return
        
        # Запускаем обработку
        processor.run_incremental_processing()

if __name__ == "__main__":
    main()