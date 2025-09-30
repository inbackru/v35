import json
import os
import re
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

class SmartSearch:
    def __init__(self):
        self.synonyms = {
            'студия': ['студия', 'однушка', '1 комната', '1-комнатная'],
            '1 комната': ['студия', 'однушка', '1 комната', '1-комнатная'],
            '2 комнаты': ['двушка', '2 комнаты', '2-комнатная', 'двухкомнатная'],
            '3 комнаты': ['трешка', '3 комнаты', '3-комнатная', 'трехкомнатная'],
            '4 комнаты': ['четырешка', '4 комнаты', '4-комнатная', 'четырехкомнатная'],
            'центр': ['центр', 'центральный', 'цум', 'красная площадь'],
            'недорого': ['недорого', 'дешево', 'бюджет', 'эконом'],
            'дорого': ['дорого', 'премиум', 'элитный', 'люкс'],
            'метро': ['метро', 'станция метро', 'рядом с метро'],
            'парк': ['парк', 'у парка', 'рядом с парком', 'зеленая зона'],
            'школа': ['школа', 'рядом со школой', 'образование'],
            'новый': ['новый', 'новостройка', 'свежий ремонт'],
            'большой': ['большой', 'просторный', 'много места'],
            'маленький': ['маленький', 'компактный', 'уютный']
        }
        
        self.districts_ru = {
            'центр': ['Центральный', 'Западный'],
            'прикубанский': ['Прикубанский'],
            'карасунский': ['Карасунский'], 
            'фмр': ['ФМР', 'Фестивальный'],
            'юмр': ['ЮМР', 'Юбилейный'],
            'гидростроителей': ['Гидростроителей'],
            'комсомольский': ['Комсомольский'],
            'автопарк': ['Автопарк']
        }

    def analyze_search_query(self, query):
        """Анализирует поисковый запрос с помощью OpenAI для извлечения критериев"""
        if not openai_client:
            print("OpenAI client not available, using fallback analysis")
            return self.fallback_analysis(query)
            
        try:
            prompt = f"""
            Проанализируй запрос о поиске квартиры в Краснодаре и извлеки критерии поиска.
            
            Запрос: "{query}"
            
            Верни JSON с критериями:
            {{
                "rooms": ["1", "2", "3", "4", "студия"] или [],
                "district": "название района" или "",
                "price_range": ["min", "max"] или [],
                "features": ["новостройка", "парковка", "балкон"] или [],
                "keywords": ["ключевые", "слова"] или [],
                "semantic_search": true/false
            }}
            
            Районы Краснодара: Центральный, Западный, Прикубанский, Карасунский, ФМР, ЮМР, Гидростроителей, Комсомольский, Автопарк
            
            Примеры:
            "двушка в центре недорого" -> {{"rooms": ["2"], "district": "Центральный", "price_range": [], "keywords": ["недорого"]}}
            "квартира у парка" -> {{"rooms": [], "district": "", "features": ["парк"], "semantic_search": true}}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            print(f"DEBUG: OpenAI analysis result: {result}")
            return result
            
        except Exception as e:
            print(f"ERROR: OpenAI analysis failed: {e}")
            # Проверяем, если это ошибка квоты API
            if "quota" in str(e).lower() or "429" in str(e):
                print("OpenAI quota exceeded, using intelligent fallback")
            return self.fallback_analysis(query)

    def fallback_analysis(self, query):
        """Умный резервный анализ без OpenAI"""
        query_lower = query.lower()
        result = {
            "rooms": [],
            "district": "",
            "price_range": [],
            "features": [],
            "keywords": [],
            "semantic_search": False
        }
        
        # Улучшенный поиск количества комнат
        room_patterns = {
            'студия': ['студ', 'studio'],
            '1': ['1-к', '1к', '1 к', 'однок', 'одноком', '1 комн', '1комн', '1-комнатная', '1-комн', 'однокомнатная'],
            '2': ['2-к', '2к', '2 к', 'двух', 'двушка', '2 комн', '2комн', '2-комнатная', '2-комн', 'двухкомнатная'],
            '3': ['3-к', '3к', '3 к', 'трех', 'трешка', '3 комн', '3комн', '3-комнатная', '3-комн', 'трехкомнатная'],
            '4': ['4-к', '4к', '4 к', 'четырех', '4 комн', '4комн']
        }
        
        for room_num, patterns in room_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                if room_num == 'студия':
                    result["rooms"] = ["0"]  # Студия = 0 комнат в системе
                else:
                    result["rooms"] = [room_num]
                break
        
        # Улучшенный поиск районов
        district_patterns = {
            'Центральный': ['центр', 'центральн', 'центр города'],
            'Западный': ['запад', 'западн'],
            'Карасунский': ['карасун', 'карасунск'],
            'Прикубанский': ['прикубан', 'прикубанск'],
            'ФМР': ['фмр', 'фестивальн'],
            'ЮМР': ['юмр', 'юбилейн'],
            'Гидростроителей': ['гидро', 'гидростроит']
        }
        
        for district_name, patterns in district_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                result["district"] = district_name
                break
        
        # Поиск цены
        price_patterns = {
            'недорого': ['недорог', 'дешев', 'бюджет', 'эконом'],
            'дорого': ['дорог', 'премиум', 'элитн', 'люкс']
        }
        
        for price_type, patterns in price_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                result["keywords"].append(price_type)
                break
        
        # Типы недвижимости (важно для "дом")
        property_type_patterns = {
            'дом': ['дом', 'дома', 'частн', 'коттедж'],
            'таунхаус': ['таунхаус', 'таун'],
            'пентхаус': ['пентхаус', 'мансард'],
            'апартаменты': ['апартамент'],
            'студия': ['студ'],
            'квартира': ['квартир']
        }
        
        for prop_type, patterns in property_type_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                result["keywords"].append(prop_type)
                break
        
        # Класс недвижимости (ВАЖНО: только точные совпадения классов)
        property_class_patterns = {
            'эконом': ['эконом', 'бюджет'],
            'комфорт': ['комфорт'],
            'бизнес': ['бизнес'],
            'премиум': ['премиум'],
            'элит': ['элит', 'люкс', 'vip']
        }
        
        # Ищем точные совпадения класса недвижимости
        for class_type, patterns in property_class_patterns.items():
            for pattern in patterns:
                if pattern == query_lower:  # Только точное совпадение
                    result["keywords"].append(class_type)
                    return result  # Возвращаем сразу для класса недвижимости
        
        # Материал стен
        wall_material_patterns = {
            'монолит': ['монолит'],
            'кирпич': ['кирпич'],
            'панель': ['панель'],
            'газобетон': ['газобетон']
        }
        
        for material, patterns in wall_material_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                result["keywords"].append(material)
                break
        
        # Особенности
        feature_patterns = {
            'парк': ['парк', 'зелен', 'сквер'],
            'метро': ['метро', 'станц'],
            'новостройка': ['новый', 'новостр', 'современ'],
            'парковка': ['парков', 'гараж'],
            'балкон': ['балкон', 'лоджи']
        }
        
        for feature_name, patterns in feature_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                result["features"].append(feature_name)
        
        # Fallback analysis completed
        return result

    def semantic_property_search(self, properties, query, criteria):
        """Семантический поиск по свойствам"""
        if not criteria.get("semantic_search") and not criteria.get("features"):
            return properties
            
        if not openai_client:
            print("OpenAI client not available, skipping semantic search")
            return properties
            
        try:
            # Подготавливаем данные о квартирах для анализа
            properties_text = []
            for prop in properties:
                prop_text = f"ID: {prop['id']}, {prop['title']}, {prop['location']}, "
                prop_text += f"{prop.get('description', '')}, район {prop['district']}, "
                prop_text += f"{prop.get('nearby', '')}, {prop.get('complex_name', '')}"
                properties_text.append(prop_text)
            
            # Запрос к OpenAI для семантического поиска
            prompt = f"""
            Найди наиболее подходящие квартиры для запроса: "{query}"
            
            Критерии поиска: {criteria}
            
            Доступные квартиры:
            {chr(10).join(properties_text[:20])}  # Ограничиваем для токенов
            
            Верни JSON со списком ID квартир, отсортированных по релевантности:
            {{"relevant_ids": [1, 5, 12, ...]}}
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            relevant_ids = result.get("relevant_ids", [])
            
            # Сортируем квартиры по релевантности
            if relevant_ids:
                sorted_properties = []
                for prop_id in relevant_ids:
                    for prop in properties:
                        if prop['id'] == prop_id:
                            sorted_properties.append(prop)
                            break
                
                # Добавляем остальные квартиры в конец
                for prop in properties:
                    if prop not in sorted_properties:
                        sorted_properties.append(prop)
                        
                return sorted_properties
                
        except Exception as e:
            print(f"ERROR: Semantic search failed: {e}")
            
        return properties

    def generate_search_suggestions(self, query):
        """Генерирует умные подсказки для автокомплита"""
        if not openai_client:
            print("OpenAI client not available, using fallback suggestions")
            return self.fallback_suggestions(query)
            
        try:
            prompt = f"""
            Пользователь ищет квартиру в Краснодаре. Текущий ввод: "{query}"
            
            Предложи 5 релевантных вариантов завершения запроса.
            
            Верни JSON:
            {{"suggestions": ["вариант 1", "вариант 2", ...]}}
            
            Учитывай:
            - Районы: Центральный, Западный, Прикубанский, Карасунский, ФМР, ЮМР
            - Типы: студия, 1-комнатная, 2-комнатная, 3-комнатная
            - Особенности: рядом с метро, у парка, новостройка, с парковкой
            """
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("suggestions", [])
            
        except Exception as e:
            print(f"ERROR: Suggestions generation failed: {e}")
            return self.fallback_suggestions(query)

    def fallback_suggestions(self, query):
        """Умные резервные подсказки без OpenAI"""
        suggestions = []
        query_lower = query.lower()
        
        if not query_lower:
            return [
                "1-комнатная квартира", 
                "2-комнатная в центре", 
                "квартира у парка",
                "новостройка с парковкой",
                "студия недорого"
            ]
        
        # Умные подсказки на основе введенного текста
        if any(char.isdigit() for char in query_lower):
            # Если есть цифры, предлагаем варианты с комнатами
            if "1" in query_lower:
                suggestions.extend([
                    "1-комнатная квартира",
                    "1-комнатная в центре",
                    "1-комнатная новостройка"
                ])
            elif "2" in query_lower:
                suggestions.extend([
                    "2-комнатная квартира", 
                    "2-комнатная в центре",
                    "2-комнатная с балконом"
                ])
            elif "3" in query_lower:
                suggestions.extend([
                    "3-комнатная квартира",
                    "3-комнатная просторная",
                    "3-комнатная семейная"
                ])
        
        # Районы Краснодара
        districts = {
            "центр": ["Центральный район", "квартира в центре", "центр города"],
            "запад": ["Западный район", "квартира на западе", "Западный округ"],
            "карасун": ["Карасунский район", "квартира в Карасунском", "Карасунский округ"],
            "прикубан": ["Прикубанский округ", "квартира в Прикубанском", "Прикубанский район"],
            "гидро": ["район Гидростроителей", "Гидростроителей", "квартира у ГЭС"]
        }
        
        for district_key, district_suggestions in districts.items():
            if district_key in query_lower:
                suggestions.extend(district_suggestions[:2])
        
        # Особенности недвижимости  
        features = {
            "парк": ["квартира у парка", "рядом с парком", "зеленая зона"],
            "метро": ["рядом с метро", "у станции метро", "транспортная доступность"],
            "новый": ["новостройка", "новый дом", "современный ЖК"],
            "недорог": ["недорогая квартира", "бюджетная квартира", "доступное жилье"],
            "семь": ["семейная квартира", "для семьи", "просторная квартира"],
            "студ": ["студия", "квартира-студия", "однокомнатная студия"]
        }
        
        for feature_key, feature_suggestions in features.items():
            if feature_key in query_lower:
                suggestions.extend(feature_suggestions[:2])
        
        # Если ничего не найдено, предлагаем популярные варианты
        if not suggestions:
            suggestions = [
                f"{query} в центре",
                f"{query} недорого", 
                f"{query} новостройка",
                f"{query} с парковкой",
                f"{query} рядом с парком"
            ]
        
        # Ограничиваем количество подсказок
        return suggestions[:5]

# Создаем глобальный экземпляр
smart_search = SmartSearch()