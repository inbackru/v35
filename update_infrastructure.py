#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from infrastructure_api import get_infrastructure_summary

def update_infrastructure_data():
    """
    Обновляет данные об инфраструктуре для районов и улиц с координатами
    """
    
    # Подключение к базе данных
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Ошибка: DATABASE_URL не найден в переменных окружения")
        return False
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("🏘️ Обновление инфраструктуры районов...")
        
        # Получаем районы с координатами
        districts_query = text("""
            SELECT id, name, slug, latitude, longitude 
            FROM districts 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            LIMIT 10
        """)
        
        districts = session.execute(districts_query).fetchall()
        
        for district in districts:
            district_id, name, slug, lat, lng = district
            
            print(f"📍 Обрабатываю район: {name}")
            
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
            
            print(f"  ✅ {name}: {infrastructure['distance_to_center']} км от центра")
            print(f"     Медицина: {infrastructure['medical_count']}, Образование: {infrastructure['education_count']}")
        
        print("\\n🛣️ Обновление инфраструктуры улиц...")
        
        # Получаем улицы с координатами (ограничиваем для тестирования)
        streets_query = text("""
            SELECT id, name, latitude, longitude 
            FROM streets 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            LIMIT 10
        """)
        
        streets = session.execute(streets_query).fetchall()
        
        for street in streets:
            street_id, name, lat, lng = street
            
            print(f"📍 Обрабатываю улицу: {name}")
            
            # Получаем инфраструктуру
            infrastructure = get_infrastructure_summary(float(lat), float(lng))
            
            # Обновляем запись в базе данных
            update_query = text("""
                UPDATE streets 
                SET 
                    distance_to_center = :distance,
                    infrastructure_data = :infrastructure_json,
                    updated_at = NOW()
                WHERE id = :street_id
            """)
            
            session.execute(update_query, {
                'distance': infrastructure['distance_to_center'],
                'infrastructure_json': json.dumps(infrastructure, ensure_ascii=False),
                'street_id': street_id
            })
            
            print(f"  ✅ {name}: {infrastructure['distance_to_center']} км от центра")
        
        # Подтверждаем изменения
        session.commit()
        session.close()
        
        print("\\n🎉 Обновление инфраструктуры завершено!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления инфраструктуры: {e}")
        return False

if __name__ == "__main__":
    success = update_infrastructure_data()
    if not success:
        sys.exit(1)