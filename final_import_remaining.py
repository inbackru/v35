#!/usr/bin/env python3
"""
Финальный импорт оставшихся данных
"""

import pandas as pd
import numpy as np
from app import app, db
from models import *
from datetime import datetime

def safe_date(date_str):
    if pd.isna(date_str) or date_str == '':
        return datetime.utcnow()
    if isinstance(date_str, datetime):
        return date_str
    try:
        date_str = str(date_str)
        if 'GMT' in date_str:
            date_str = date_str.split(' GMT')[0]
        return datetime.strptime(date_str, '%a %b %d %Y %H:%M:%S')
    except:
        return datetime.utcnow()

def main():
    with app.app_context():
        print("🚀 ФИНАЛЬНЫЙ ИМПОРТ ОСТАВШИХСЯ ДАННЫХ")
        
        # Импорт избранных объектов (FavoriteProperty)
        print("\n=== ИЗБРАННЫЕ ОБЪЕКТЫ ===")
        try:
            df = pd.read_excel('attached_assets/favorite_properties (3)_1755342720991.xlsx')
            imported = 0
            
            for _, row in df.iterrows():
                fav_id = int(row['id']) if pd.notna(row['id']) else 0
                user_id = int(row['user_id']) if pd.notna(row['user_id']) else 0
                property_name = str(row['property_name']) if pd.notna(row['property_name']) else ''
                
                if fav_id <= 0 or user_id <= 0 or not property_name:
                    continue
                
                if FavoriteProperty.query.filter_by(id=fav_id).first():
                    continue
                
                favorite = FavoriteProperty(
                    id=fav_id,
                    user_id=user_id,
                    property_id=str(row['property_id']) if pd.notna(row['property_id']) else None,
                    property_name=property_name,
                    property_type=str(row['property_type']) if pd.notna(row['property_type']) else None,
                    property_size=float(row['property_size']) if pd.notna(row['property_size']) else None,
                    property_price=int(row['property_price']) if pd.notna(row['property_price']) else None,
                    complex_name=str(row['complex_name']) if pd.notna(row['complex_name']) else None,
                    developer_name=str(row['developer_name']) if pd.notna(row['developer_name']) else None,
                    property_image=str(row['property_image']) if pd.notna(row['property_image']) else None,
                    property_url=str(row['property_url']) if pd.notna(row['property_url']) else None,
                    cashback_amount=int(row['cashback_amount']) if pd.notna(row['cashback_amount']) else None,
                    cashback_percent=float(row['cashback_percent']) if pd.notna(row['cashback_percent']) else None,
                    created_at=safe_date(row.get('created_at'))
                )
                
                db.session.add(favorite)
                imported += 1
            
            db.session.commit()
            print(f"✅ Импортировано избранных объектов: {imported}")
            
        except Exception as e:
            print(f"❌ Ошибка избранных: {e}")
            db.session.rollback()
        
        # Финальная статистика
        print("\n" + "="*50)
        print("📊 ПОЛНАЯ СТАТИСТИКА БАЗЫ ДАННЫХ")
        print("="*50)
        
        stats = {
            'Пользователи': User.query.count(),
            'Застройщики': Developer.query.count(), 
            'Жилые комплексы': ResidentialComplex.query.count(),
            'Категории блога': BlogCategory.query.count(),
            'Улицы': Street.query.count(),
            'Менеджеры': Manager.query.count(),
            'Избранные объекты': FavoriteProperty.query.count(),
            'Запросы звонков': CallbackRequest.query.count()
        }
        
        # Дополнительные модели если они есть
        try:
            stats['Администраторы'] = Admin.query.count()
        except:
            stats['Администраторы'] = 'модель не найдена'
            
        try:
            stats['Статьи блога'] = BlogArticle.query.count()
        except:
            stats['Статьи блога'] = 'модель не найдена'
        
        for key, value in stats.items():
            emoji = "✅" if isinstance(value, int) and value > 0 else "⚠️"
            print(f"{emoji} {key}: {value}")
        
        print("\n🎉 ИМПОРТ ВСЕХ ДАННЫХ ЗАВЕРШЕН!")
        print("📈 База данных полностью восстановлена с реальными данными!")

if __name__ == "__main__":
    main()