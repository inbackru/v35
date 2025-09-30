"""
ПОЛНЫЙ импорт ВСЕХ 82 столбцов из Excel
"""
import pandas as pd
import os
import sys
from sqlalchemy import text
from datetime import datetime
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db

def safe_value(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    return str(value).strip()

def safe_int(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    try:
        return int(float(value))
    except:
        return None

def safe_bigint(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    try:
        return int(float(value))
    except:
        return None

def safe_float(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    try:
        return float(value)
    except:
        return None

def safe_bool(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    if str(value).lower() in ['true', '1', 'yes', 'да']:
        return True
    elif str(value).lower() in ['false', '0', 'no', 'нет']:
        return False
    return None

def safe_datetime(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    try:
        if isinstance(value, str):
            return value  # Пусть PostgreSQL сам парсит
        return str(value)
    except:
        return None

def import_all_82_columns():
    """Импорт ВСЕХ 82 столбцов"""
    file_path = 'attached_assets/excel_properties_1756658927673.xlsx'
    
    try:
        df = pd.read_excel(file_path)
        print(f"Excel файл: {len(df)} квартир, {len(df.columns)} столбцов")
        
        # Полная очистка
        db.session.execute(text("TRUNCATE TABLE excel_properties RESTART IDENTITY CASCADE"))
        db.session.commit()
        print("Таблица очищена")
        
        imported = 0
        with_photos = 0
        
        for idx, row in df.iterrows():
            try:
                inner_id = safe_bigint(row.get('inner_id'))
                if not inner_id:
                    continue
                
                # ВСЕ 82 ПОЛЯ из Excel - полное соответствие
                data = {
                    'inner_id': inner_id,
                    'url': safe_value(row.get('url')),
                    'photos': safe_value(row.get('photos')),  # Фотографии!
                    'address_id': safe_int(row.get('address_id')),
                    'address_guid': safe_value(row.get('address_guid')),
                    'address_kind': safe_value(row.get('address_kind')),
                    'address_name': safe_value(row.get('address_name')),
                    'address_subways': safe_value(row.get('address_subways')),
                    'address_locality_id': safe_int(row.get('address_locality_id')),
                    'address_locality_kind': safe_value(row.get('address_locality_kind')),
                    'address_locality_name': safe_value(row.get('address_locality_name')),
                    'address_locality_subkind': safe_value(row.get('address_locality_subkind')),
                    'address_locality_display_name': safe_value(row.get('address_locality_display_name')),
                    'address_position_lat': safe_float(row.get('address_position_lat')),
                    'address_position_lon': safe_float(row.get('address_position_lon')),
                    'address_display_name': safe_value(row.get('address_display_name')),
                    'address_short_display_name': safe_value(row.get('address_short_display_name')),
                    'complex_id': safe_bigint(row.get('complex_id')),
                    'complex_name': safe_value(row.get('complex_name')),
                    'complex_phone': safe_value(row.get('complex_phone')),
                    'complex_building_id': safe_int(row.get('complex_building_id')),
                    'complex_building_name': safe_value(row.get('complex_building_name')),
                    'complex_building_released': safe_bool(row.get('complex_building_released')),
                    'complex_building_is_unsafe': safe_bool(row.get('complex_building_is_unsafe')),
                    'complex_building_accreditation': safe_bool(row.get('complex_building_accreditation')),
                    'complex_building_end_build_year': safe_int(row.get('complex_building_end_build_year')),
                    'complex_building_complex_product': safe_bool(row.get('complex_building_complex_product')),
                    'complex_building_end_build_quarter': safe_int(row.get('complex_building_end_build_quarter')),
                    'complex_building_has_green_mortgage': safe_bool(row.get('complex_building_has_green_mortgage')),
                    'complex_min_rate': safe_int(row.get('complex_min_rate')),
                    'complex_sales_phone': safe_value(row.get('complex_sales_phone')),
                    'complex_sales_address': safe_value(row.get('complex_sales_address')),
                    'complex_object_class_id': safe_int(row.get('complex_object_class_id')),
                    'complex_object_class_display_name': safe_value(row.get('complex_object_class_display_name')),
                    'complex_has_big_check': safe_bool(row.get('complex_has_big_check')),
                    'complex_end_build_year': safe_int(row.get('complex_end_build_year')),
                    'complex_financing_sber': safe_bool(row.get('complex_financing_sber')),
                    'complex_telephony_b_number': safe_bigint(row.get('complex_telephony_b_number')),
                    'complex_telephony_r_number': safe_bigint(row.get('complex_telephony_r_number')),
                    'complex_with_renovation': safe_bool(row.get('complex_with_renovation')),
                    'complex_first_build_year': safe_int(row.get('complex_first_build_year')),
                    'complex_start_build_year': safe_int(row.get('complex_start_build_year')),
                    'complex_end_build_quarter': safe_int(row.get('complex_end_build_quarter')),
                    'complex_has_accreditation': safe_bool(row.get('complex_has_accreditation')),
                    'complex_has_approve_flats': safe_bool(row.get('complex_has_approve_flats')),
                    'complex_mortgage_tranches': safe_bool(row.get('complex_mortgage_tranches')),
                    'complex_has_green_mortgage': safe_bool(row.get('complex_has_green_mortgage')),
                    'complex_phone_substitution': safe_bigint(row.get('complex_phone_substitution')),
                    'complex_show_contact_block': safe_bool(row.get('complex_show_contact_block')),
                    'complex_first_build_quarter': safe_int(row.get('complex_first_build_quarter')),
                    'complex_start_build_quarter': safe_int(row.get('complex_start_build_quarter')),
                    'complex_has_mortgage_subsidy': safe_bool(row.get('complex_has_mortgage_subsidy')),
                    'complex_has_government_program': safe_bool(row.get('complex_has_government_program')),
                    'min_rate': safe_int(row.get('min_rate')),
                    'trade_in': safe_bool(row.get('trade_in')),
                    'deal_type': safe_value(row.get('deal_type')),
                    'developer_id': safe_bigint(row.get('developer_id')),
                    'developer_name': safe_value(row.get('developer_name')),
                    'region_id': safe_int(row.get('region_id')),
                    'city_id': safe_int(row.get('city_id')),
                    'parsed_region': safe_value(row.get('parsed_region')),
                    'parsed_city': safe_value(row.get('parsed_city')),
                    'parsed_district': safe_value(row.get('parsed_district')),
                    'developer_site': safe_value(row.get('developer_site')),
                    'developer_holding_id': safe_int(row.get('developer_holding_id')),
                    'is_auction': safe_bool(row.get('is_auction')),
                    'price': safe_int(row.get('price')),
                    'max_price': safe_int(row.get('max_price')),
                    'min_price': safe_int(row.get('min_price')),
                    'square_price': safe_int(row.get('square_price')),
                    'mortgage_price': safe_int(row.get('mortgage_price')),
                    'renovation_type': safe_value(row.get('renovation_type')),
                    'renovation_display_name': safe_value(row.get('renovation_display_name')),
                    'description': safe_value(row.get('description')),
                    'object_area': safe_float(row.get('object_area')),
                    'object_rooms': safe_int(row.get('object_rooms')),
                    'object_max_floor': safe_int(row.get('object_max_floor')),
                    'object_min_floor': safe_int(row.get('object_min_floor')),
                    'object_is_apartment': safe_bool(row.get('object_is_apartment')),
                    'published_dt': safe_datetime(row.get('published_dt')),
                    'chat_available': safe_bool(row.get('chat_available')),
                    'placement_type': safe_value(row.get('placement_type'))
                }
                
                # Фильтрация None значений
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if 'photos' in clean_data and clean_data['photos']:
                    with_photos += 1
                
                if clean_data and 'inner_id' in clean_data:
                    columns = ', '.join(clean_data.keys())
                    placeholders = ', '.join([f':{k}' for k in clean_data.keys()])
                    
                    sql = f"INSERT INTO excel_properties ({columns}) VALUES ({placeholders})"
                    db.session.execute(text(sql), clean_data)
                    db.session.commit()
                    
                    imported += 1
                    
                    if imported % 50 == 0:
                        print(f"Импортировано {imported} квартир (с фото: {with_photos})...")
                        
            except Exception as e:
                db.session.rollback()
                if imported < 5:
                    print(f"Ошибка {idx}: {str(e)[:100]}...")
                continue
                
        print(f"\n🎉 ПОЛНЫЙ ИМПОРТ ВСЕХ 82 СТОЛБЦОВ ЗАВЕРШЕН!")
        print(f"✅ Импортировано: {imported} квартир")
        print(f"📸 С фотографиями: {with_photos} квартир")
        
        # Финальная проверка
        result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties"))
        total = result.scalar()
        
        result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE photos IS NOT NULL AND photos != ''"))
        photos_in_db = result.scalar()
        
        print(f"🏠 В базе итого: {total} квартир")
        print(f"📷 С фотографиями в базе: {photos_in_db}")
        
        # Показать примеры с фотографиями
        result = db.session.execute(text("""
            SELECT inner_id, complex_name, developer_name, photos, object_area, object_rooms, price
            FROM excel_properties 
            WHERE photos IS NOT NULL AND photos != ''
            ORDER BY inner_id
            LIMIT 3
        """))
        
        print(f"\n📋 Примеры полных данных:")
        for row in result:
            photos_count = len(json.loads(row[3])) if row[3] and row[3].startswith('[') else 0
            print(f"ID: {row[0]}")
            print(f"  ЖК: {row[1]}")
            print(f"  Застройщик: {row[2]}")
            print(f"  Площадь: {row[4]} м²")
            print(f"  Комнат: {row[5]}")
            print(f"  Цена: {row[6]:,} руб")
            print(f"  Фото: {photos_count} штук")
            print("")
        
        return imported
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        db.session.rollback()
        return 0

# ЗАПУСК ПОЛНОГО ИМПОРТА
with app.app_context():
    import_all_82_columns()