#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from infrastructure_api import get_infrastructure_summary

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def update_all_districts_infrastructure():
    """
    Обновляет инфраструктуру для ВСЕХ районов с координатами
    """
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logging.error("❌ DATABASE_URL не найден")
        return False
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Получаем ВСЕ районы с координатами, у которых нет инфраструктуры или расстояния
        districts_query = text("""
            SELECT id, name, slug, latitude, longitude 
            FROM districts 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            AND (infrastructure_data IS NULL OR distance_to_center IS NULL)
            ORDER BY name
        """)
        
        districts = session.execute(districts_query).fetchall()
        total_districts = len(districts)
        
        logging.info(f"🏘️ Найдено {total_districts} районов для обновления инфраструктуры")
        
        success_count = 0
        error_count = 0
        
        for i, district in enumerate(districts, 1):
            district_id, name, slug, lat, lng = district
            
            logging.info(f"📍 [{i}/{total_districts}] Обрабатываю район: {name}")
            
            try:
                # Получаем инфраструктуру
                infrastructure = get_infrastructure_summary(float(lat), float(lng))
                
                # Обновляем запись в базе данных
                update_query = text("""
                    UPDATE districts 
                    SET 
                        distance_to_center = :distance,
                        infrastructure_data = :infrastructure_json,
                        updated_at = NOW()
                    WHERE id = :district_id
                """)
                
                session.execute(update_query, {
                    'distance': infrastructure['distance_to_center'],
                    'infrastructure_json': json.dumps(infrastructure, ensure_ascii=False),
                    'district_id': district_id
                })
                
                session.commit()
                success_count += 1
                
                logging.info(f"  ✅ {name}: {infrastructure['distance_to_center']} км от центра")
                logging.info(f"     🏥 Медицина: {infrastructure['medical_count']}, 🎓 Образование: {infrastructure['education_count']}")
                
                # Пауза для API
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"  ❌ Ошибка для района {name}: {e}")
                error_count += 1
                session.rollback()
                continue
        
        session.close()
        
        logging.info(f"\\n📈 Обновление завершено!")
        logging.info(f"   ✅ Успешно: {success_count}")
        logging.info(f"   ❌ Ошибки: {error_count}")
        
        return success_count > 0
        
    except Exception as e:
        logging.error(f"❌ Общая ошибка: {e}")
        return False

def main():
    """Основная функция"""
    logging.info("🚀 Запуск автоматического обновления инфраструктуры районов")
    success = update_all_districts_infrastructure()
    
    if success:
        logging.info("✅ Обновление инфраструктуры завершено успешно")
        exit(0)
    else:
        logging.error("❌ Ошибка в процессе обновления")
        exit(1)

if __name__ == "__main__":
    main()