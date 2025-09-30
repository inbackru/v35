#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import logging
import threading
import schedule
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import subprocess

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('background_processor.log')
    ]
)

class BackgroundProcessor:
    """Фоновый процессор для автоматического обновления данных"""
    
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.running = False
        
    def check_database_connection(self):
        """Проверка соединения с базой данных"""
        try:
            engine = create_engine(self.database_url)
            Session = sessionmaker(bind=engine)
            session = Session()
            session.execute(text("SELECT 1"))
            session.close()
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка подключения к БД: {e}")
            return False
    
    def get_statistics(self):
        """Получение текущей статистики обработки"""
        try:
            engine = create_engine(self.database_url)
            Session = sessionmaker(bind=engine)
            session = Session()
            
            # Статистика районов
            districts_stats = session.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN infrastructure_data IS NOT NULL THEN 1 END) as with_infra,
                    COUNT(CASE WHEN distance_to_center IS NOT NULL THEN 1 END) as with_distance
                FROM districts
            """)).fetchone()
            
            # Статистика улиц
            streets_stats = session.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN latitude IS NOT NULL THEN 1 END) as with_coords
                FROM streets
            """)).fetchone()
            
            session.close()
            
            return {
                'districts': {
                    'total': districts_stats[0],
                    'with_infrastructure': districts_stats[1],
                    'with_distance': districts_stats[2],
                    'infra_percent': round(100.0 * districts_stats[1] / districts_stats[0], 1) if districts_stats[0] > 0 else 0,
                    'distance_percent': round(100.0 * districts_stats[2] / districts_stats[0], 1) if districts_stats[0] > 0 else 0
                },
                'streets': {
                    'total': streets_stats[0],
                    'with_coordinates': streets_stats[1],
                    'percent_complete': round(100.0 * streets_stats[1] / streets_stats[0], 1) if streets_stats[0] > 0 else 0,
                    'remaining': streets_stats[0] - streets_stats[1]
                }
            }
            
        except Exception as e:
            logging.error(f"❌ Ошибка получения статистики: {e}")
            return None
    
    def process_districts_infrastructure(self):
        """Обработка инфраструктуры районов"""
        logging.info("🏘️ Запуск обновления инфраструктуры районов")
        
        try:
            result = subprocess.run(
                [sys.executable, 'auto_infrastructure_update.py'],
                capture_output=True,
                text=True,
                timeout=1800  # 30 минут
            )
            
            if result.returncode == 0:
                logging.info("✅ Обновление инфраструктуры районов завершено")
                return True
            else:
                logging.error(f"❌ Ошибка обновления инфраструктуры: {result.stderr}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Ошибка запуска процесса инфраструктуры: {e}")
            return False
    
    def process_streets_coordinates(self):
        """Обработка координат улиц"""
        logging.info("🛣️ Запуск обработки координат улиц")
        
        try:
            result = subprocess.run(
                [sys.executable, 'auto_streets_coordinates.py'],
                capture_output=True,
                text=True,
                timeout=600  # 10 минут
            )
            
            if result.returncode == 0:
                logging.info("✅ Обработка координат улиц завершена")
                return True
            else:
                logging.warning(f"⚠️ Процесс координат завершился: {result.stderr}")
                return True  # Это нормально, может не быть данных для обработки
                
        except Exception as e:
            logging.error(f"❌ Ошибка запуска процесса координат: {e}")
            return False
    
    def scheduled_infrastructure_update(self):
        """Плановое обновление инфраструктуры (раз в 6 часов)"""
        if not self.running:
            return
            
        stats = self.get_statistics()
        if stats and stats['districts']['infra_percent'] < 100:
            logging.info("⏰ Плановое обновление инфраструктуры районов")
            self.process_districts_infrastructure()
    
    def scheduled_streets_update(self):
        """Плановое обновление координат улиц (каждые 15 минут)"""
        if not self.running:
            return
            
        stats = self.get_statistics()
        if stats and stats['streets']['percent_complete'] < 100:
            logging.info("⏰ Плановая обработка координат улиц")
            self.process_streets_coordinates()
    
    def print_status(self):
        """Вывод текущего статуса"""
        stats = self.get_statistics()
        if stats:
            logging.info("📊 Текущий статус:")
            logging.info(f"   🏘️ Районы: {stats['districts']['with_infrastructure']}/{stats['districts']['total']} ({stats['districts']['infra_percent']}%) с инфраструктурой")
            logging.info(f"   🛣️ Улицы: {stats['streets']['with_coordinates']}/{stats['streets']['total']} ({stats['streets']['percent_complete']}%) с координатами")
            logging.info(f"   📍 Осталось улиц: {stats['streets']['remaining']}")
    
    def start(self):
        """Запуск фонового процессора"""
        if not self.check_database_connection():
            logging.error("❌ Не удается подключиться к базе данных")
            return False
        
        self.running = True
        
        # Настройка расписания
        schedule.every(15).minutes.do(self.scheduled_streets_update)  # Улицы каждые 15 минут
        schedule.every(6).hours.do(self.scheduled_infrastructure_update)  # Инфраструктура каждые 6 часов
        schedule.every(1).hours.do(self.print_status)  # Статус каждый час
        
        logging.info("🚀 Фоновый процессор запущен")
        self.print_status()
        
        # Немедленный запуск обработки
        self.scheduled_infrastructure_update()
        self.scheduled_streets_update()
        
        # Основной цикл
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Проверяем расписание каждую минуту
                
        except KeyboardInterrupt:
            logging.info("⏹️ Получен сигнал остановки")
        finally:
            self.running = False
            logging.info("🛑 Фоновый процессор остановлен")
    
    def stop(self):
        """Остановка фонового процессора"""
        self.running = False

def main():
    """Основная функция"""
    processor = BackgroundProcessor()
    processor.start()

if __name__ == "__main__":
    main()