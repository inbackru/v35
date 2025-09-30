#!/usr/bin/env python3
"""
Демонстрация автоматического создания новых объектов из Excel
Система автоматически создает:
1. Новых застройщиков (если их нет в базе)
2. Новые ЖК (если их нет в базе)
3. Новые квартиры (добавляет в таблицу excel_properties)
"""

import pandas as pd
import json
from flask import Flask
from app import app, db
from sqlalchemy import text
import os

def show_current_state():
    """Показывает текущее состояние базы данных"""
    
    with app.app_context():
        print("📊 ТЕКУЩЕЕ СОСТОЯНИЕ БАЗЫ ДАННЫХ:")
        print("=" * 50)
        
        # Застройщики
        developers_count = db.session.execute(text("SELECT COUNT(*) FROM developers")).scalar()
        print(f"🏗️ Застройщики: {developers_count}")
        
        # ЖК
        complexes_count = db.session.execute(text("SELECT COUNT(*) FROM residential_complexes")).scalar()  
        print(f"🏢 Жилые комплексы: {complexes_count}")
        
        # Квартиры в Excel таблице
        properties_count = db.session.execute(text("SELECT COUNT(*) FROM excel_properties")).scalar()
        print(f"🏠 Квартиры в excel_properties: {properties_count}")
        
        print("\n📋 ПОСЛЕДНИЕ ЗАСТРОЙЩИКИ:")
        developers = db.session.execute(text("SELECT name FROM developers ORDER BY id DESC LIMIT 5")).fetchall()
        for dev in developers:
            print(f"   • {dev[0]}")
            
        print("\n🏢 ПОСЛЕДНИЕ ЖК:")
        complexes = db.session.execute(text("SELECT name FROM residential_complexes ORDER BY id DESC LIMIT 5")).fetchall()
        for comp in complexes:
            print(f"   • {comp[0]}")

def analyze_excel_file(filename):
    """Анализирует Excel файл и показывает что будет создано"""
    
    print(f"\n🔍 АНАЛИЗ ФАЙЛА: {filename}")
    print("=" * 50)
    
    try:
        df = pd.read_excel(filename)
        print(f"📊 Записей в файле: {len(df)}")
        print(f"📋 Колонок: {len(df.columns)}")
        
        # Анализируем застройщиков
        unique_developers = df['developer_name'].dropna().unique()
        print(f"\n🏗️ Уникальных застройщиков: {len(unique_developers)}")
        for dev in unique_developers[:10]:  # Показываем первые 10
            print(f"   • {dev}")
        if len(unique_developers) > 10:
            print(f"   ... и ещё {len(unique_developers) - 10}")
            
        # Анализируем ЖК
        unique_complexes = df['complex_name'].dropna().unique()
        print(f"\n🏢 Уникальных ЖК: {len(unique_complexes)}")
        for comp in unique_complexes[:10]:  # Показываем первые 10
            print(f"   • {comp}")
        if len(unique_complexes) > 10:
            print(f"   ... и ещё {len(unique_complexes) - 10}")
            
        # Проверяем фотографии
        photos_count = df['photos'].notna().sum()
        print(f"\n📷 Записей с фотографиями: {photos_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка анализа файла: {e}")
        return False

def import_to_excel_table_only(filename):
    """Импортирует данные только в таблицу excel_properties"""
    
    print(f"\n⚡ БЫСТРЫЙ ИМПОРТ В excel_properties")
    print("=" * 50)
    
    with app.app_context():
        try:
            df = pd.read_excel(filename)
            
            # Очищаем таблицу
            db.session.execute(text("DELETE FROM excel_properties"))
            print("🧹 Очищена таблица excel_properties")
            
            # Импортируем все данные
            imported = 0
            
            for index, row in df.iterrows():
                try:
                    # Подготавливаем данные
                    data = {}
                    for col in df.columns:
                        value = row[col]
                        if pd.isna(value):
                            data[col] = None
                        elif col == 'photos' and isinstance(value, str):
                            try:
                                data[col] = json.loads(value)
                            except:
                                data[col] = [value] if value else []
                        else:
                            data[col] = value
                    
                    # Добавляем уникальный ID если нет
                    if 'inner_id' not in data or not data['inner_id']:
                        data['inner_id'] = f"new_prop_{imported + 1}"
                    
                    # Создаем SQL запрос
                    columns = ', '.join([f'"{k}"' for k in data.keys()])
                    placeholders = ', '.join([f':{k}' for k in data.keys()])
                    
                    query = f'INSERT INTO excel_properties ({columns}) VALUES ({placeholders})'
                    db.session.execute(text(query), data)
                    
                    imported += 1
                    
                    if imported % 100 == 0:
                        print(f"   📦 Импортировано: {imported} квартир...")
                        
                except Exception as e:
                    print(f"   ❌ Ошибка строки {index}: {e}")
                    continue
            
            db.session.commit()
            print(f"✅ Успешно импортировано: {imported} квартир")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка импорта: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🎯 ДЕМО: АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ОБЪЕКТОВ ИЗ EXCEL")
    print("=" * 60)
    
    # Показываем текущее состояние
    show_current_state()
    
    # Анализируем новый файл
    filename = "attached_assets/Сочи_1756384471034.xlsx"
    if os.path.exists(filename):
        if analyze_excel_file(filename):
            # Импортируем данные
            success = import_to_excel_table_only(filename)
            
            if success:
                print(f"\n🎉 ИМПОРТ ЗАВЕРШЕН!")
                print("=" * 30)
                print("📈 Новое состояние:")
                show_current_state()
                
                print(f"\n💡 КАК РАБОТАЕТ АВТОМАТИЧЕСКОЕ СОЗДАНИЕ:")
                print("=" * 50)
                print("1. 🏗️ Система проверяет застройщиков в excel_properties")
                print("2. 🔄 Автоматически создает новых если их нет в базе developers")
                print("3. 🏢 Аналогично создает новые ЖК в residential_complexes")
                print("4. 🏠 Все квартиры сохраняются в excel_properties с полными данными")
                print("5. 🔗 Связи между объектами создаются автоматически по названиям")
                print("6. 📸 Фотографии извлекаются из JSON и отображаются на сайте")
                print("\n🎯 РЕЗУЛЬТАТ: Все новые данные автоматически появляются на сайте!")
            
    else:
        print(f"❌ Файл {filename} не найден!")