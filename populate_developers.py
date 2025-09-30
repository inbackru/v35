#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных застройщиками с полной информацией
"""

import json
import random
from app import app, db
from models import Developer

# Данные партнеров-застройщиков
DEVELOPERS_DATA = [
    {
        'name': 'ГК ССК',
        'full_name': 'ООО "Группа Компаний ССК"',
        'description': 'Крупнейшая строительная компания Юга России, специализирующаяся на жилищном строительстве. Основана в 1994 году, за время работы построено более 2,5 миллионов квадратных метров жилья.',
        'phone': '+7 (861) 992-99-55',
        'website': 'ssk-group.ru',
        'address': 'г. Краснодар, ул. Мира, 45',
        'established_year': 1994,
        'inn': '2312345678',
        'experience_years': 30
    },
    {
        'name': 'DOGMA',
        'full_name': 'ООО "ДОГМА"',
        'description': 'Современная строительная компания, специализирующаяся на комфортном жилье с уникальной архитектурой. Известна инновационными решениями в области жилищного строительства.',
        'phone': '+7 (861) 205-77-99',
        'website': 'dogma-krd.ru',
        'address': 'г. Краснодар, ул. Красная, 122',
        'established_year': 2008,
        'inn': '2312345679',
        'experience_years': 16
    },
    {
        'name': 'ТОЧНО',
        'full_name': 'ООО "ТОЧНО"',
        'description': 'Застройщик премиального сегмента, создающий жилые комплексы с высоким уровнем комфорта. Особое внимание уделяется качеству строительства и архитектурным решениям.',
        'phone': '+7 (861) 201-05-55',
        'website': 'tochno-krd.ru',
        'address': 'г. Краснодар, пр. Чекистов, 25',
        'established_year': 2012,
        'inn': '2312345680',
        'experience_years': 12
    },
    {
        'name': 'AVA GROUP',
        'full_name': 'ООО "АВА ГРУПП"',
        'description': 'Динамично развивающаяся строительная компания, специализирующаяся на малоэтажном и среднеэтажном строительстве. Отличается индивидуальным подходом к каждому проекту.',
        'phone': '+7 (861) 298-44-33',
        'website': 'avagroup.ru',
        'address': 'г. Краснодар, ул. Северная, 326',
        'established_year': 2015,
        'inn': '2312345681',
        'experience_years': 9
    },
    {
        'name': 'ЮГСТРОЙИНВЕСТ',
        'full_name': 'ООО "ЮГСТРОЙИНВЕСТ"',
        'description': 'Крупный застройщик Краснодарского края с опытом работы более 15 лет. Специализируется на строительстве жилых комплексов комфорт-класса с развитой инфраструктурой.',
        'phone': '+7 (861) 992-11-22',
        'website': 'yugstroyinvest.ru',
        'address': 'г. Краснодар, ул. Тургенева, 158',
        'established_year': 2009,
        'inn': '2312345682',
        'experience_years': 15
    },
    {
        'name': 'НЕОМЕТРИЯ',
        'full_name': 'ООО "НЕОМЕТРИЯ"',
        'description': 'Инновационная строительная компания, создающая современные жилые пространства с использованием новейших технологий. Лидер в области «умного дома».',
        'phone': '+7 (861) 203-55-77',
        'website': 'neometriya.ru',
        'address': 'г. Краснодар, ул. Ставропольская, 149',
        'established_year': 2016,
        'inn': '2312345683',
        'experience_years': 8
    },
    {
        'name': 'ВКБ-НОВОСТРОЙКИ',
        'full_name': 'ООО "ВКБ-НОВОСТРОЙКИ"',
        'description': 'Строительная компания, специализирующаяся на создании доступного и комфортного жилья. Активно использует современные строительные технологии для оптимизации стоимости.',
        'phone': '+7 (861) 255-88-99',
        'website': 'vkb-novostroyki.ru',
        'address': 'г. Краснодар, ул. Дзержинского, 100',
        'established_year': 2013,
        'inn': '2312345684',
        'experience_years': 11
    },
    {
        'name': 'МЕТРИКС',
        'full_name': 'ООО "МЕТРИКС"',
        'description': 'Современный застройщик, сочетающий классические архитектурные решения с инновационными подходами. Известен качественным исполнением и соблюдением сроков.',
        'phone': '+7 (861) 274-33-44',
        'website': 'metriks.ru',
        'address': 'г. Краснодар, ул. Российская, 267',
        'established_year': 2014,
        'inn': '2312345685',
        'experience_years': 10
    }
]

# Дополнительные застройщики
MORE_DEVELOPERS = [
    'АЛЬФАСТРОЙИНВЕСТ', 'ГИНСИТИ', 'СЕМЬЯ', 'ЕВРОПЕЯ', 'ГАРАНТИЯ',
    'ЕКАТЕРИНОДАРИНВЕСТ-СТРОЙ', 'РОМЕКС ДЕВЕЛОПМЕНТ', 'ДАРСТРОЙ', 'БАУИНВЕСТ'
]

def create_slug(name):
    """Создает slug из названия"""
    return name.lower().replace(' ', '-').replace('гк', '').replace('оoo', '').replace('оао', '').strip('-')

def generate_company_details(name, index):
    """Генерирует детали компании"""
    base_inn = 2312000000 + (index * 100)
    base_kpp = 231200000 + (index * 10)
    base_ogrn = 1002300000000 + (index * 1000)
    
    return {
        'inn': str(base_inn + random.randint(10, 99)),
        'kpp': str(base_kpp + random.randint(1, 9)),
        'ogrn': str(base_ogrn + random.randint(100, 999)),
        'legal_address': f'г. Краснодар, ул. {random.choice(["Красная", "Северная", "Калинина", "Гагарина", "Мира"])}, {random.randint(50, 300)}',
        'bank_name': 'ПАО СБЕРБАНК',
        'bank_bik': '040349602',
        'bank_account': f'4070281{random.randint(10000000000, 99999999999)}'
    }

def generate_coordinates():
    """Генерирует случайные координаты в Краснодаре"""
    # Примерные границы Краснодара
    lat_min, lat_max = 45.0, 45.1
    lon_min, lon_max = 38.9, 39.1
    
    return {
        'latitude': round(random.uniform(lat_min, lat_max), 6),
        'longitude': round(random.uniform(lon_min, lon_max), 6)
    }

def generate_infrastructure():
    """Генерирует список инфраструктуры"""
    all_infrastructure = [
        'Детский сад', 'Школа', 'Спортивные площадки', 'Парковка',
        'Торговые центры', 'Благоустроенная территория', 'Охрана',
        'Детские площадки', 'Фитнес-центр', 'Медицинский центр'
    ]
    return json.dumps(random.sample(all_infrastructure, random.randint(4, 7)), ensure_ascii=False)

def generate_features():
    """Генерирует список особенностей застройщика"""
    all_features = [
        'Собственное производство материалов',
        'Соблюдение сроков сдачи',
        'Контроль качества на всех этапах',
        'Гибкие условия покупки',
        'Ипотечные программы',
        'Система умный дом',
        'Энергоэффективные решения',
        'Экологичные материалы'
    ]
    return json.dumps(random.sample(all_features, random.randint(3, 6)), ensure_ascii=False)

def populate_developers():
    """Заполняет базу данных застройщиками"""
    
    with app.app_context():
        print("Создание таблиц...")
        db.create_all()
        
        print("Очистка существующих данных...")
        Developer.query.delete()
        
        # Добавляем основных застройщиков с детальной информацией
        for i, dev_data in enumerate(DEVELOPERS_DATA):
            coordinates = generate_coordinates()
            company_details = generate_company_details(dev_data['name'], i)
            
            developer = Developer(
                name=dev_data['name'],
                slug=create_slug(dev_data['name']),
                full_name=dev_data['full_name'],
                description=dev_data['description'],
                phone=dev_data['phone'],
                website=dev_data['website'],
                address=dev_data['address'],
                established_year=dev_data['established_year'],
                experience_years=dev_data['experience_years'],
                
                # Координаты
                latitude=coordinates['latitude'],
                longitude=coordinates['longitude'],
                
                # Статистика
                total_complexes=random.randint(3, 12),
                total_properties=random.randint(150, 1500),
                properties_sold=random.randint(500, 5000),
                rating=round(random.uniform(4.3, 4.9), 1),
                
                # Финансы
                min_price=random.randint(4500000, 8000000),
                max_cashback_percent=round(random.uniform(5.0, 10.0), 1),
                
                # Реквизиты
                inn=company_details['inn'],
                kpp=company_details['kpp'],
                ogrn=company_details['ogrn'],
                legal_address=company_details['legal_address'],
                bank_name=company_details['bank_name'],
                bank_bik=company_details['bank_bik'],
                bank_account=company_details['bank_account'],
                
                # Особенности
                features=generate_features(),
                infrastructure=generate_infrastructure(),
                
                is_active=True,
                is_partner=True
            )
            
            db.session.add(developer)
            print(f"Добавлен застройщик: {dev_data['name']}")
        
        # Добавляем остальных застройщиков с базовой информацией
        for i, name in enumerate(MORE_DEVELOPERS, len(DEVELOPERS_DATA)):
            coordinates = generate_coordinates()
            company_details = generate_company_details(name, i)
            
            developer = Developer(
                name=name,
                slug=create_slug(name),
                full_name=f'ООО "{name}"',
                description=f'{name} - надежный застройщик Краснодарского края с многолетним опытом строительства качественного жилья комфорт-класса.',
                phone=f'+7 (861) {random.randint(200, 299)}-{random.randint(10, 99)}-{random.randint(10, 99)}',
                website=f'{name.lower().replace(" ", "").replace("-", "")}.ru',
                address=f'г. Краснодар, ул. {random.choice(["Красная", "Северная", "Калинина", "Гагарина"])}, {random.randint(50, 300)}',
                established_year=random.randint(2005, 2018),
                experience_years=random.randint(6, 19),
                
                # Координаты
                latitude=coordinates['latitude'],
                longitude=coordinates['longitude'],
                
                # Статистика
                total_complexes=random.randint(2, 8),
                total_properties=random.randint(80, 800),
                properties_sold=random.randint(200, 2000),
                rating=round(random.uniform(4.2, 4.8), 1),
                
                # Финансы
                min_price=random.randint(4000000, 7500000),
                max_cashback_percent=round(random.uniform(3.0, 9.0), 1),
                
                # Реквизиты
                inn=company_details['inn'],
                kpp=company_details['kpp'],
                ogrn=company_details['ogrn'],
                legal_address=company_details['legal_address'],
                bank_name=company_details['bank_name'],
                bank_bik=company_details['bank_bik'],
                bank_account=company_details['bank_account'],
                
                # Особенности
                features=generate_features(),
                infrastructure=generate_infrastructure(),
                
                is_active=True,
                is_partner=True
            )
            
            db.session.add(developer)
            print(f"Добавлен застройщик: {name}")
        
        db.session.commit()
        
        total_count = Developer.query.count()
        print(f"\n✅ Успешно добавлено {total_count} застройщиков в базу данных!")

if __name__ == '__main__':
    populate_developers()