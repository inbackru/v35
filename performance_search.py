"""
Супер-оптимизированный поиск недвижимости
Команда чемпионов по производительности
"""
import re
import time
from typing import List, Dict, Any, Optional
from sqlalchemy import text, and_, or_
from app import db

class SuperSmartSearch:
    """Самый быстрый и умный поиск недвижимости в мире"""
    
    def __init__(self):
        # Синонимы и сокращения для улучшения поиска
        self.synonyms = {
            'студия': ['студ', 'st', 'studio', '0к', '0 комн'],
            '1-комнатная': ['1к', '1 комн', '1комн', 'однушка', 'однокомнатная'],
            '2-комнатная': ['2к', '2 комн', '2комн', 'двушка', 'двухкомнатная'],
            '3-комнатная': ['3к', '3 комн', '3комн', 'трешка', 'трехкомнатная'],
            '4-комнатная': ['4к', '4 комн', '4комн', 'четырехкомнатная'],
            
            # Районы
            'центральный': ['центр', 'downtown', 'central'],
            'хостинский': ['хоста', 'khosta'],
            'кудепста': ['кудепста м-н', 'кудепстинский'],
            'адлер': ['адлер м-н', 'adler'],
            
            # Застройщики
            'неометрия': ['неометр', 'geometria', 'geo'],
            'ава': ['ava group'],
            
            # Типы объектов
            'квартира': ['кв', 'apt', 'apartment', 'flat'],
            'новостройка': ['новострой', 'новая', 'новый дом'],
        }
        
        # Стоп-слова
        self.stop_words = {'в', 'на', 'с', 'по', 'от', 'до', 'для', 'или', 'и', 'а', 'но'}
        
        # Кэш для ускорения
        self.cache = {}
    
    def normalize_query(self, query: str) -> str:
        """Нормализация поискового запроса"""
        query = query.lower().strip()
        
        # Убираем специальные символы
        query = re.sub(r'[^\w\s\-]', ' ', query)
        
        # Убираем лишние пробелы
        query = ' '.join(query.split())
        
        return query
    
    def extract_search_criteria(self, query: str) -> Dict[str, Any]:
        """Извлекает критерии поиска из запроса"""
        normalized = self.normalize_query(query)
        criteria = {
            'rooms': [],
            'districts': [],
            'complexes': [],
            'developers': [],
            'price_min': None,
            'price_max': None,
            'area_min': None,
            'area_max': None,
            'keywords': [],
            'streets': []
        }
        
        words = normalized.split()
        
        for word in words:
            if word in self.stop_words:
                continue
                
            # Поиск количества комнат
            if word in ['студия', 'студ', 'studio']:
                criteria['rooms'].append(0)
            elif re.match(r'^(\d)[к-]?комн?$', word):
                match = re.match(r'^(\d)', word)
                if match:
                    rooms = int(match.group(1))
                    criteria['rooms'].append(rooms)
            
            # Поиск цены
            price_match = re.search(r'(\d+)(?:млн|мил|m)', word)
            if price_match:
                price = int(price_match.group(1)) * 1000000
                if not criteria['price_min']:
                    criteria['price_min'] = price
                else:
                    criteria['price_max'] = price
            
            # Поиск площади
            area_match = re.search(r'(\d+)(?:м|кв)', word)
            if area_match:
                area = int(area_match.group(1))
                if not criteria['area_min']:
                    criteria['area_min'] = area
                else:
                    criteria['area_max'] = area
            
            # Добавляем в ключевые слова
            criteria['keywords'].append(word)
        
        return criteria
    
    def build_optimized_query(self, criteria: Dict[str, Any]) -> tuple:
        """Строит оптимизированный SQL запрос"""
        
        base_query = """
        SELECT DISTINCT
            p.inner_id as id,
            p.object_rooms as rooms,
            p.object_area as area,
            p.price,
            p.complex_name,
            p.developer_name,
            p.parsed_district as district,
            p.complex_sales_address as address,
            p.address_position_lat as lat,
            p.address_position_lon as lon,
            p.photos,
            p.url
        FROM excel_properties p
        WHERE 1=1
        """
        
        conditions = []
        params = {}
        
        # Фильтр по комнатам
        if criteria['rooms']:
            conditions.append("p.object_rooms = ANY(:rooms)")
            params['rooms'] = criteria['rooms']
        
        # Фильтр по цене
        if criteria['price_min']:
            conditions.append("p.price >= :price_min")
            params['price_min'] = criteria['price_min']
        if criteria['price_max']:
            conditions.append("p.price <= :price_max")
            params['price_max'] = criteria['price_max']
        
        # Фильтр по площади
        if criteria['area_min']:
            conditions.append("p.object_area >= :area_min")
            params['area_min'] = criteria['area_min']
        if criteria['area_max']:
            conditions.append("p.object_area <= :area_max")
            params['area_max'] = criteria['area_max']
        
        # Текстовый поиск с использованием индексов
        text_conditions = []
        for i, keyword in enumerate(criteria['keywords'][:5]):  # Ограничиваем до 5 слов
            param_name = f'keyword_{i}'
            text_conditions.append(f"""
                (LOWER(p.complex_name) LIKE :%{param_name}% OR
                 LOWER(p.developer_name) LIKE :%{param_name}% OR
                 LOWER(p.parsed_district) LIKE :%{param_name}% OR
                 LOWER(p.complex_sales_address) LIKE :%{param_name}%)
            """)
            params[param_name] = f'%{keyword}%'
        
        if text_conditions:
            conditions.append(f"({' OR '.join(text_conditions)})")
        
        # Добавляем условия к запросу
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
        
        # Сортировка по релевантности
        base_query += """
        ORDER BY 
            CASE WHEN LOWER(p.complex_name) LIKE :main_query THEN 1 ELSE 2 END,
            p.price ASC
        LIMIT 50
        """
        params['main_query'] = f"%{' '.join(criteria['keywords'][:3])}%"
        
        return base_query, params
    
    def search_suggestions(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """Быстрые подсказки для автодополнения"""
        if len(query) < 2:
            return []
        
        # ❌ ОТКЛЮЧАЕМ КЭШ для отладки типов квартир 
        # cache_key = f"suggestions_{query.lower()}_{limit}"
        # if cache_key in self.cache:
        #     cached_data, timestamp = self.cache[cache_key]
        #     if time.time() - timestamp < 30:
        #         return cached_data
        
        suggestions = []
        query_lower = f'%{query.lower()}%'
        
        try:
            # 🏠 ПРИОРИТЕТ 1: ТИПЫ КВАРТИР - восстанавливаем пропавшие подсказки!
            query_clean = query.lower().strip()
# print(f"🔍 DEBUG: Searching for '{query_clean}'")
            
            # ✅ УЛУЧШЕННАЯ ЛОГИКА: Студии (object_rooms = 0) 
            studio_keywords = ['студ', 'studio', '0к', '0 к', '0-к', 'студий']
            if any(word in query_clean for word in studio_keywords) or query_clean == '0':
                count = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE object_rooms = 0")).scalar()
                if count > 0:
                    suggestions.append({
                        'text': 'Студии',
                        'subtitle': f'{count} квартир доступно',
                        'type': 'rooms',
                        'icon': 'fas fa-home',
                        'url': '/properties?rooms=0',
                        'priority': 1  # ✅ ПРИОРИТЕТ 1 - самый важный
                    })
            
            # ✅ МАКСИМАЛЬНО ГИБКИЙ ПОИСК: 1-комнатные (object_rooms = 1)
            one_room_keywords = ['1к', '1 к', '1-к', '1-ком', '1 ком', 'одн', 'однок', 'однокомн', 
                                'однокомнатн', 'однокомнатная', 'однокомнатные', 'однушк', 'однушка', 'одноком']
            if any(word in query_clean for word in one_room_keywords) or query_clean == '1':
                count = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE object_rooms = 1")).scalar()
                if count > 0:
                    suggestions.append({
                        'text': '1-комнатные квартиры',
                        'subtitle': f'{count} квартир доступно',
                        'type': 'rooms',
                        'icon': 'fas fa-home',
                        'url': '/properties?rooms=1',
                        'priority': 1  # ✅ ПРИОРИТЕТ 1 - самый важный
                    })
                    
            # ✅ МАКСИМАЛЬНО ГИБКИЙ ПОИСК: 2-комнатные (object_rooms = 2)  
            two_room_keywords = ['2к', '2 к', '2-к', '2-ком', '2 ком', 'двух', 'двухк', 'двухком',
                                'двухкомнатн', 'двухкомнатная', 'двухкомнатные', 'двушк', 'двушка', 'двуком', 'двухком']
            if any(word in query_clean for word in two_room_keywords) or query_clean == '2':
                count = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE object_rooms = 2")).scalar()
                if count > 0:
                    suggestions.append({
                        'text': '2-комнатные квартиры',
                        'subtitle': f'{count} квартир доступно',
                        'type': 'rooms',
                        'icon': 'fas fa-home',
                        'url': '/properties?rooms=2',
                        'priority': 1  # ✅ ПРИОРИТЕТ 1 - самый важный
                    })
                    
            # ✅ МАКСИМАЛЬНО ГИБКИЙ ПОИСК: 3-комнатные (object_rooms = 3)
            three_room_keywords = ['3к', '3 к', '3-к', '3-ком', '3 ком', 'трех', 'трёх', 'трехк', 'трёхк',
                                  'трехкомнатн', 'трехкомнатная', 'трехкомнатные', 'трёхкомнатн', 'трёхкомнатная', 'трёхкомнатные', 'трешк', 'трешка', 'трёшка', 'триком']
            if any(word in query_clean for word in three_room_keywords) or query_clean == '3':
                count = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE object_rooms = 3")).scalar()
                if count > 0:
                    suggestions.append({
                        'text': '3-комнатные квартиры',
                        'subtitle': f'{count} квартир доступно',
                        'type': 'rooms',
                        'icon': 'fas fa-home',
                        'url': '/properties?rooms=3',
                        'priority': 1  # ✅ ПРИОРИТЕТ 1 - самый важный
                    })
                    
            # ✅ УЛУЧШЕННАЯ ЛОГИКА: 4-комнатные (object_rooms = 4)
            four_room_keywords = ['4к', '4 к', '4-к', '4-ком', '4 ком', 'четыр', 'четырех', 'четырёх',
                                 'четырехкомнатн', 'четырехкомнатная', 'четырехкомнатные', 'четырёхкомнатн', 'четырёхкомнатная', 'четырёхкомнатные']
            if any(word in query_clean for word in four_room_keywords) or query_clean == '4':
                count = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE object_rooms = 4")).scalar()
                if count > 0:
                    suggestions.append({
                        'text': '4-комнатные квартиры',
                        'subtitle': f'{count} квартир доступно', 
                        'type': 'rooms',
                        'icon': 'fas fa-home',
                        'url': '/properties?rooms=4',
                        'priority': 1  # ✅ ПРИОРИТЕТ 1 - самый важный
                    })
            
            # Общий поиск по "комн" если ничего конкретного не нашли
            if ('комн' in query_clean or 'комнат' in query_clean) and not any(suggestions):
                for room_num in [1, 2, 3, 4]:
                    count = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE object_rooms = :rooms"), {'rooms': room_num}).scalar()
                    if count > 0:
                        suggestions.append({
                            'text': f'{room_num}-комнатные квартиры',
                            'subtitle': f'{count} квартир доступно',
                            'type': 'rooms',
                            'icon': 'fas fa-home',
                            'url': f'/properties?rooms={room_num}'
                        })
            
            # ЖК (приоритет 2)  
            complexes = db.session.execute(text("""
                SELECT DISTINCT complex_name, COUNT(*) as count
                FROM excel_properties 
                WHERE LOWER(complex_name) LIKE :query
                AND complex_name IS NOT NULL 
                GROUP BY complex_name
                ORDER BY count DESC, complex_name
                LIMIT 50
            """), {'query': query_lower}).fetchall()
            
            for row in complexes:
                suggestions.append({
                    'type': 'complex',
                    'title': row[0],
                    'subtitle': f'{row[1]} квартир',
                    'icon': 'building',
                    'url': f'/properties?residential_complex={row[0]}',
                    'priority': 3
                })
            
            # Улицы (приоритет 2)
            streets = db.session.execute(text("""
                SELECT DISTINCT 
                    CASE 
                        WHEN complex_sales_address LIKE '%улица%' THEN
                            TRIM(SUBSTRING(complex_sales_address FROM '([^,]*улица[^,]*)'))
                        ELSE complex_sales_address
                    END as street_name,
                    COUNT(*) as count
                FROM excel_properties 
                WHERE LOWER(complex_sales_address) LIKE :query
                AND complex_sales_address IS NOT NULL 
                AND complex_sales_address LIKE '%улица%'
                GROUP BY street_name
                ORDER BY count DESC
                LIMIT 20
            """), {'query': query_lower}).fetchall()
            
            for row in streets:
                suggestions.append({
                    'type': 'street',
                    'title': row[0],
                    'subtitle': f'{row[1]} объектов',
                    'icon': 'road',
                    'url': f'/properties?search={row[0]}',
                    'priority': 4
                })
            
            # Города (приоритет 1 - самый важный!)
            cities = db.session.execute(text("""
                SELECT DISTINCT 
                    CASE 
                        WHEN complex_sales_address LIKE '%Сочи%' THEN 'Сочи'
                        WHEN complex_sales_address LIKE '%Краснодар%' THEN 'Краснодар'
                        WHEN complex_sales_address LIKE '%Анапа%' THEN 'Анапа'
                        WHEN complex_sales_address LIKE '%Новороссийск%' THEN 'Новороссийск'
                        WHEN complex_sales_address LIKE '%Геленджик%' THEN 'Геленджик'
                        ELSE NULL
                    END as city,
                    COUNT(*) as count
                FROM excel_properties 
                WHERE complex_sales_address IS NOT NULL
                AND LOWER(
                    CASE 
                        WHEN complex_sales_address LIKE '%Сочи%' THEN 'Сочи'
                        WHEN complex_sales_address LIKE '%Краснодар%' THEN 'Краснодар'
                        WHEN complex_sales_address LIKE '%Анапа%' THEN 'Анапа'
                        WHEN complex_sales_address LIKE '%Новороссийск%' THEN 'Новороссийск'
                        WHEN complex_sales_address LIKE '%Геленджик%' THEN 'Геленджик'
                        ELSE ''
                    END
                ) LIKE :query
                GROUP BY 
                    CASE 
                        WHEN complex_sales_address LIKE '%Сочи%' THEN 'Сочи'
                        WHEN complex_sales_address LIKE '%Краснодар%' THEN 'Краснодар'
                        WHEN complex_sales_address LIKE '%Анапа%' THEN 'Анапа'
                        WHEN complex_sales_address LIKE '%Новороссийск%' THEN 'Новороссийск'
                        WHEN complex_sales_address LIKE '%Геленджик%' THEN 'Геленджик'
                        ELSE NULL
                    END
                HAVING 
                    CASE 
                        WHEN complex_sales_address LIKE '%Сочи%' THEN 'Сочи'
                        WHEN complex_sales_address LIKE '%Краснодар%' THEN 'Краснодар'
                        WHEN complex_sales_address LIKE '%Анапа%' THEN 'Анапа'
                        WHEN complex_sales_address LIKE '%Новороссийск%' THEN 'Новороссийск'
                        WHEN complex_sales_address LIKE '%Геленджик%' THEN 'Геленджик'
                        ELSE NULL
                    END IS NOT NULL
                ORDER BY count DESC
                LIMIT 20
            """), {'query': query_lower}).fetchall()
            
            for row in cities:
                suggestions.append({
                    'type': 'city',
                    'title': row[0],
                    'subtitle': f'{row[1]} предложений',
                    'icon': 'map-marker-alt',
                    'url': f'/properties?search={row[0]}',
                    'priority': 1
                })

            # Районы (приоритет 2)
            districts = db.session.execute(text("""
                SELECT DISTINCT parsed_district, COUNT(*) as count
                FROM excel_properties 
                WHERE LOWER(parsed_district) LIKE :query
                AND parsed_district IS NOT NULL 
                GROUP BY parsed_district
                ORDER BY count DESC
                LIMIT 15
            """), {'query': query_lower}).fetchall()
            
            for row in districts:
                suggestions.append({
                    'type': 'district',
                    'title': row[0],
                    'subtitle': f'{row[1]} предложений',
                    'icon': 'map-pin',
                    'url': f'/properties?district={row[0]}',
                    'priority': 2
                })
            
            # Застройщики (приоритет 5)
            developers = db.session.execute(text("""
                SELECT DISTINCT developer_name, COUNT(*) as count
                FROM excel_properties 
                WHERE LOWER(developer_name) LIKE :query
                AND developer_name IS NOT NULL 
                GROUP BY developer_name
                ORDER BY count DESC
                LIMIT 15
            """), {'query': query_lower}).fetchall()
            
            for row in developers:
                suggestions.append({
                    'type': 'developer',
                    'title': row[0],
                    'subtitle': f'{row[1]} объектов',
                    'icon': 'user-tie',
                    'url': f'/properties?developer={row[0]}',
                    'priority': 4
                })
            
            # Типы квартир - ТОЛЬКО если явно ищут квартиры
            query_has_room_keywords = any(word in query.lower() for word in ['студ', 'комн', 'квартир'])
            if query_has_room_keywords:
                room_suggestions = []
                if 'студ' in query.lower():
                    room_suggestions.append({'rooms': 0, 'name': 'Студии'})
                
                # Ищем конкретные цифры только если есть контекст квартир
                if 'комн' in query.lower() or 'квартир' in query.lower():
                    for i in range(1, 5):
                        if str(i) in query or f'{i}к' in query or f'{i} комн' in query:
                            room_suggestions.append({'rooms': i, 'name': f'{i}-комнатные'})
                
                for room_type in room_suggestions[:2]:
                    result = db.session.execute(text("""
                        SELECT COUNT(*) FROM excel_properties WHERE object_rooms = :rooms
                    """), {'rooms': room_type['rooms']}).fetchone()
                    count = result[0] if result else 0
                    
                    suggestions.append({
                        'type': 'rooms',
                        'title': room_type['name'],
                        'subtitle': f'{count} предложений',
                        'icon': 'home',
                        'url': f'/properties?rooms={room_type["rooms"]}',
                        'priority': 5
                    })
            
            # Сортируем по приоритету и показываем больше результатов
            suggestions = sorted(suggestions, key=lambda x: x['priority'])[:min(limit, 100)]
            
            # ✅ ИСПРАВЛЕНО: Убираем priority из результата (если есть)
            for suggestion in suggestions:
                if 'priority' in suggestion:
                    suggestion.pop('priority', None)
            
            # ❌ КЭШИРОВАНИЕ ПОЛНОСТЬЮ ОТКЛЮЧЕНО для отладки типов квартир
            # self.cache[cache_key] = (suggestions, time.time())
            
            return suggestions
            
        except Exception as e:
            print(f"Search suggestions error: {e}")
            return []
    
    def search_properties(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """Основной поиск недвижимости"""
        if len(query) < 2:
            return {'results': [], 'total': 0, 'criteria': {}}
        
        criteria = self.extract_search_criteria(query)
        sql_query, params = self.build_optimized_query(criteria)
        
        try:
            results = db.session.execute(text(sql_query), params).fetchall()
            
            properties = []
            for row in results:
                properties.append({
                    'id': row[0],
                    'rooms': row[1] or 0,
                    'area': row[2] or 0,
                    'price': row[3] or 0,
                    'complex_name': row[4] or '',
                    'developer_name': row[5] or '',
                    'district': row[6] or '',
                    'address': row[7] or '',
                    'lat': row[8],
                    'lon': row[9],
                    'photos': row[10] or 0,
                    'url': row[11] or f'/object/{row[0]}'
                })
            
            return {
                'results': properties,
                'total': len(properties),
                'criteria': criteria,
                'query': query
            }
            
        except Exception as e:
            print(f"Search properties error: {e}")
            return {'results': [], 'total': 0, 'criteria': criteria}

# Создаем глобальный экземпляр
super_search = SuperSmartSearch()