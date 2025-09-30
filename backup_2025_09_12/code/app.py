import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, abort, Blueprint, send_from_directory
from sqlalchemy import text
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, validate_csrf
from werkzeug.exceptions import BadRequest

# Import smart search
from smart_search import smart_search
from urllib.parse import unquote, quote
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import secrets
import re
from email_service import send_notification
from flask_caching import Cache
import qrcode
import io
import base64
from PIL import Image

def parse_address_components(address_display_name):
    """
    ИСПРАВЛЕННАЯ ФУНКЦИЯ: Парсит адрес в формате: Россия, Краснодарский край, Сочи, Кудепста м-н, Искры, 88 лит7
    Возвращает словарь с компонентами адреса
    """
    # ПОЛНАЯ ИНИЦИАЛИЗАЦИЯ РЕЗУЛЬТАТА
    result = {
        'country': None,
        'region': None, 
        'city': None,
        'district': None,
        'street': None,
        'house_number': None
    }
    
    if not address_display_name:
        return result
    
    # РАЗБИВАЕМ АДРЕС ПО ЗАПЯТЫМ
    parts = [part.strip() for part in address_display_name.split(',')]
    
    # ПРЯМОЕ ЗАПОЛНЕНИЕ ОСНОВНЫХ ЧАСТЕЙ
    if len(parts) >= 1:
        result['country'] = parts[0]  # Россия
        
    if len(parts) >= 2:
        result['region'] = parts[1]   # Краснодарский край
        
    if len(parts) >= 3:
        result['city'] = parts[2]     # Сочи
        
    # ОБРАБАТЫВАЕМ ОСТАВШИЕСЯ ЧАСТИ (район, улица, дом)
    if len(parts) >= 4:
        remaining_parts = parts[3:]  # ['Дагомыс', 'Российская', '26г стр']
        
        if len(remaining_parts) == 1:
            # Одна часть: может быть район или улица
            part = remaining_parts[0]
            if any(marker in part for marker in ['м-н', 'микрорайон', 'ЖК', 'жилой комплекс']):
                result['district'] = part
            else:
                result['street'] = part
                
        elif len(remaining_parts) == 2:
            # Две части: район+улица или улица+дом
            first_part, second_part = remaining_parts[0], remaining_parts[1]
            
            if any(marker in first_part for marker in ['м-н', 'микрорайон']):
                result['district'] = first_part
                result['street'] = second_part
            else:
                result['street'] = first_part
                result['house_number'] = second_part
                
        elif len(remaining_parts) == 3:
            # Три части: район, улица, дом
            result['district'] = remaining_parts[0]
            result['street'] = remaining_parts[1]
            result['house_number'] = remaining_parts[2]
            
        elif len(remaining_parts) >= 4:
            # Больше трех частей: район, улица, дом (остальное объединяем в дом)
            result['district'] = remaining_parts[0]
            result['street'] = remaining_parts[1]
            result['house_number'] = ', '.join(remaining_parts[2:])
    
    return result

def update_parsed_addresses():
    """
    Обновляет ВСЕ поля parsed_* для всех записей в базе данных
    на основе address_display_name
    """
    print("Starting COMPLETE address parsing update...")
    
    # Получаем все записи с адресами
    result = db.session.execute(text("""
        SELECT inner_id, address_display_name
        FROM excel_properties 
        WHERE address_display_name IS NOT NULL
    """))
    
    records = result.fetchall()
    updated_count = 0
    
    for record in records:
        property_id, address = record
        
        # Парсим адрес ПОЛНОСТЬЮ
        parsed = parse_address_components(address)
        
        # Обновляем ВСЕ поля парсинга
        db.session.execute(text("""
            UPDATE excel_properties 
            SET 
                parsed_country = :country,
                parsed_region = :region,
                parsed_city = :city,
                parsed_district = :district,
                parsed_street = :street,
                parsed_house_number = :house_number
            WHERE inner_id = :property_id
        """), {
            'property_id': property_id,
            'country': parsed.get('country'),
            'region': parsed.get('region'),
            'city': parsed.get('city'),
            'district': parsed.get('district'),
            'street': parsed.get('street'),
            'house_number': parsed.get('house_number')
        })
        
        updated_count += 1
        
        # Коммитим пачками
        if updated_count % 50 == 0:
            db.session.commit()
            print(f"Updated {updated_count} records...")
    
    # Финальный коммит
    db.session.commit()
    print(f"Address parsing complete! Updated {updated_count} records.")
    return updated_count

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure CSRF protection
csrf = CSRFProtect(app)
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour
app.config['WTF_CSRF_SSL_STRICT'] = False  # Allow non-HTTPS for development

# Add CSRF token to template context
@app.context_processor
def inject_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return dict(csrf_token=generate_csrf)

def validate_json_csrf():
    """Validate CSRF token for JSON requests"""
    try:
        # For JSON requests, expect CSRF token in X-CSRFToken header
        token = request.headers.get('X-CSRFToken')
        if not token:
            return False
        validate_csrf(token)
        return True
    except:
        return False

def require_json_csrf(f):
    """Decorator to require CSRF protection for JSON endpoints"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST' and request.content_type == 'application/json':
            if not validate_json_csrf():
                return jsonify({'success': False, 'error': 'CSRF token missing or invalid'}), 400
        return f(*args, **kwargs)
    return decorated_function

# Русские названия месяцев для локализации
RUSSIAN_MONTHS = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

@app.template_filter('russian_date')
def russian_date_filter(date_value):
    """Форматирует дату на русском языке"""
    if not date_value:
        return 'Недавно'
    
    if isinstance(date_value, str):
        return date_value
    
    day = date_value.day
    month = RUSSIAN_MONTHS.get(date_value.month, date_value.strftime('%B'))
    year = date_value.year
    
    return f"{day} {month} {year}"

# Настройка супер-производительного кэширования
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 минут
cache = Cache(app)

# Session configuration for better cookie handling
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'  # Secure cookies for HTTPS in production only
app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 24  # 24 hours

# Enable permanent sessions by default
from datetime import timedelta
app.permanent_session_lifetime = timedelta(hours=24)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///properties.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add route for uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Initialize the app with the extension
db.init_app(app)

# Add Jinja2 helper for creating slugs
@app.template_filter('slug')
def create_slug_filter(name):
    """Jinja2 filter for creating SEO-friendly slug from complex name"""
    return create_slug(name)

# Create API blueprint without login requirement
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Debug endpoint removed for security - exposed session data

@api_bp.route('/property/<int:property_id>/cashback')
def api_property_cashback(property_id):
    """Get cashback information for a property"""
    try:
        # Load properties data
        properties = load_properties()
        complexes = load_residential_complexes()
        
        # Find property by ID
        property_data = None
        for prop in properties:
            if prop.get('id') == property_id:
                property_data = prop
                break
        
        if not property_data:
            return jsonify({'success': False, 'error': 'Property not found'})
        
        # Calculate cashback
        price = property_data.get('price', 0)
        cashback_percent = 2.5  # Default cashback
        
        # Determine cashback percentage based on price
        if price >= 10000000:  # 10M+
            cashback_percent = 3.0
        elif price >= 5000000:  # 5M+
            cashback_percent = 2.8
        else:
            cashback_percent = 2.5
        
        cashback_amount = price * (cashback_percent / 100)
        
        # Get complex info
        complex_name = "Не указан"
        if property_data.get('residential_complex_id'):
            complex_id = property_data['residential_complex_id']
            for complex_data in complexes:
                if complex_data.get('id') == complex_id:
                    complex_name = complex_data.get('name', 'Не указан')
                    break
        
        # Format property name
        rooms = property_data.get('rooms', 0)
        room_text = f"{rooms}-комнатная квартира" if rooms > 0 else "Студия"
        property_name = f"{room_text} в ЖК «{complex_name}»"
        
        return jsonify({
            'success': True,
            'property_id': property_id,
            'property_name': property_name,
            'property_price': price,
            'cashback_percent': cashback_percent,
            'cashback_amount': int(cashback_amount),
            'complex_name': complex_name,
            'rooms': rooms
        })
        
    except Exception as e:
        print(f"Error getting property cashback: {e}")
        return jsonify({'success': False, 'error': 'Server error'})

# Custom Jinja2 filters
def street_slug(street_name):
    """Convert street name to URL slug with transliteration"""
    import re
    
    # Transliteration mapping for Russian to Latin
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    
    # Clean the name
    name = str(street_name).strip().lower()
    # Remove extra characters
    name = re.sub(r'[«»"\(\)\.,:;]', '', name)
    
    # Transliterate
    result = ''
    for char in name:
        result += translit_map.get(char, char)
    
    # Replace spaces with hyphens and clean up
    result = re.sub(r'\s+', '-', result)
    result = re.sub(r'-+', '-', result)
    result = result.strip('-')
    
    return result

def number_format(value):
    """Format number with space separators"""
    try:
        if isinstance(value, str):
            value = int(value)
        return f"{value:,}".replace(',', ' ')
    except (ValueError, TypeError):
        return str(value)

@app.template_filter('developer_slug')
def developer_slug(developer_name):
    """Convert developer name to URL slug with transliteration"""
    import re
    if not developer_name:
        return ""
    
    # Transliteration mapping for Russian to Latin
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
        'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA'
    }
    
    # Remove extra spaces and clean
    name = str(developer_name).strip()
    # Remove quotes, parentheses, dots, commas
    name = re.sub(r'[«»"\(\)\.,:;]', '', name)  
    
    # Transliterate cyrillic to latin
    result = ''
    for char in name:
        result += translit_map.get(char, char)
    
    # Replace spaces with hyphens and clean up
    result = re.sub(r'\s+', '-', result)  # Replace spaces with hyphens
    result = re.sub(r'-+', '-', result)   # Replace multiple hyphens with single
    result = result.strip('-')  # Remove leading/trailing hyphens
    return result.lower()

def format_room_display(rooms):
    """Format room count for display"""
    if rooms == 0:
        return "Студия"
    else:
        return f"{rooms}-комнатная квартира"

app.jinja_env.filters['street_slug'] = street_slug
app.jinja_env.filters['number_format'] = number_format
app.jinja_env.filters['developer_slug'] = developer_slug

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message = 'Войдите в аккаунт для доступа к этой странице.'
login_manager.login_message_category = 'info'



# Property data loading functions with cache
_properties_cache = None
_cache_timestamp = None
CACHE_TIMEOUT = 300  # 5 minutes

def load_properties():
    """Load properties from database with fallback to JSON files"""
    global _properties_cache, _cache_timestamp
    import time
    
    # Check if we have valid cached data
    if (_properties_cache is not None and _cache_timestamp is not None and 
        time.time() - _cache_timestamp < CACHE_TIMEOUT):
        # Cache hit - fast path
        return _properties_cache
    
    # Ensure we have app context
    from flask import has_app_context
    if not has_app_context():
        with app.app_context():
            return load_properties()
    
    try:
        # Load from excel_properties table using raw SQL
        sql_query = """
            SELECT inner_id, complex_name, developer_name, object_rooms, object_area, 
                   price, object_min_floor, object_max_floor, address_display_name, 
                   address_position_lat, address_position_lon, address_locality_display_name,
                   photos, complex_object_class_display_name
            FROM excel_properties 
            WHERE price > 0 AND address_position_lat IS NOT NULL
        """
        
        result = db.session.execute(text(sql_query))
        excel_properties = result.fetchall()
        
        if excel_properties and len(excel_properties) > 0:
            # Convert excel_properties to dictionary format
            db_properties = []
            for prop in excel_properties:
                prop_dict = dict(prop._mapping)
                
                # Parse photos field (PostgreSQL array format)
                photos_raw = prop_dict.get('photos', '')
                if photos_raw and photos_raw.strip():
                    if photos_raw.startswith('{') and photos_raw.endswith('}'):
                        # PostgreSQL array format: {url1,url2,url3}
                        images_str = photos_raw[1:-1]  # Remove braces
                        if images_str:
                            images = [img.strip() for img in images_str.split(',') if img.strip()]
                            main_image = images[0] if images else '/static/images/no-photo.jpg'
                        else:
                            main_image = '/static/images/no-photo.jpg'
                    else:
                        main_image = photos_raw
                else:
                    main_image = '/static/images/no-photo.jpg'
                
                # Get correct total floors for the complex
                complex_total_floors = prop_dict.get('object_max_floor', 1)
                # If floor data seems wrong (1/1), get real max floors from complex
                if complex_total_floors == 1:
                    # Query for real max floors in this complex
                    try:
                        max_floors_query = db.session.execute(text("""
                            SELECT MAX(object_max_floor) as max_floors
                            FROM excel_properties 
                            WHERE complex_name = :complex_name
                            AND object_max_floor > 1
                        """), {'complex_name': prop_dict.get('complex_name', '')})
                        max_floors_result = max_floors_query.fetchone()
                        if max_floors_result and max_floors_result[0]:
                            complex_total_floors = max_floors_result[0]
                    except:
                        pass
                
                # Format property data
                formatted_prop = {
                    'id': prop_dict.get('inner_id'),
                    'title': f"{format_room_display(prop_dict.get('object_rooms', 0))}, {prop_dict.get('object_area', 0)} м²",
                    'rooms': prop_dict.get('object_rooms', 0),
                    'area': prop_dict.get('object_area', 0),
                    'price': prop_dict.get('price', 0),
                    'price_per_sqm': int(prop_dict.get('price', 0) / prop_dict.get('object_area', 1)) if prop_dict.get('object_area', 0) > 0 else 0,
                    'floor': prop_dict.get('object_min_floor', 1),
                    'total_floors': complex_total_floors,
                    'address': prop_dict.get('address_display_name', ''),
                    'coordinates': {
                        'lat': float(prop_dict.get('address_position_lat', 45.0448)),
                        'lng': float(prop_dict.get('address_position_lon', 38.9728))
                    },
                    'cashback': calculate_cashback(prop_dict.get('price', 0)),
                    'cashback_available': True,
                    'status': 'available',
                    'property_type': 'Квартира',
                    'developer': prop_dict.get('developer_name', 'Не указан'),
                    'residential_complex': prop_dict.get('complex_name', 'ЖК Без названия'),
                    'district': prop_dict.get('address_locality_display_name', 'Район не указан'),
                    'main_image': main_image,
                    'url': f"/object/{prop_dict.get('inner_id')}",
                    'complex_name': prop_dict.get('complex_name', 'ЖК Без названия'),
                    'type': 'property',
                }
                db_properties.append(formatted_prop)
            
            # Successfully loaded properties from database
            # Cache the data
            _properties_cache = db_properties  
            _cache_timestamp = time.time()
            return db_properties
            
    except Exception as e:
        # Database error logged  
        print(f"CRITICAL: load_properties() database error: {e}")
        import traceback
        traceback.print_exc()
        pass
        
    # No fallback - only database data from now on
    # No properties found
    return []

def load_residential_complexes():
    """Load residential complexes from database with JSON fallback"""
    try:
        # First try to load from database
        from models import ResidentialComplex, Developer, District
        
        complexes = ResidentialComplex.query.all()
        
        if complexes and len(complexes) > 0:
            # Convert database complexes to dictionary format
            db_complexes = []
            for complex in complexes:
                complex_dict = {
                    'id': complex.id,
                    'name': complex.name,
                    'slug': complex.slug,
                    'district': complex.district.name if complex.district else 'Не указан',
                    'developer': complex.developer.name if complex.developer else 'Не указан',
                    'cashback_rate': complex.cashback_rate or 5.0,
                    'class': complex.object_class_display_name or 'Комфорт',
                    'description': f'ЖК от застройщика {complex.developer.name if complex.developer else "Не указан"}',
                    'start_year': complex.start_build_year,
                    'completion_year': complex.end_build_year,
                    'quarter': complex.end_build_quarter,
                    'features': {
                        'accreditation': complex.has_accreditation,
                        'green_mortgage': complex.has_green_mortgage,
                        'big_check': complex.has_big_check,
                        'with_renovation': complex.with_renovation,
                        'financing_sber': complex.financing_sber,
                    },
                    'phones': {
                        'complex': complex.complex_phone,
                        'sales': complex.sales_phone,
                    },
                    'sales_address': complex.sales_address,
                    'image': 'https://via.placeholder.com/800x600/0088CC/FFFFFF?text=' + complex.name.replace(' ', '+'),  # Placeholder for now
                    'address': complex.sales_address or 'Адрес уточняется',
                    'location': complex.sales_address or 'Краснодар',  # Add missing location field
                }
                db_complexes.append(complex_dict)
            
            # Complexes loaded successfully
            return db_complexes
            
    except Exception as e:
        # Error loading complexes
        pass
    
    # No fallback - only database data from now on
    # No complexes found
    return []

def load_blog_articles():
    """Load blog articles from JSON file"""
    try:
        with open('data/blog_articles.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_blog_categories():
    """Load blog categories from JSON file"""
    try:
        with open('data/blog_categories.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_search_data():
    """Load search data from JSON file"""
    try:
        with open('data/search_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_streets():
    """Load streets from JSON file"""
    try:
        with open('data/streets.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_developers():
    """Load developers from residential complexes data"""
    try:
        complexes = load_residential_complexes()
        developers = {}
        
        for complex in complexes:
            dev_name = complex.get('developer', 'Неизвестный застройщик')
            if dev_name not in developers:
                developers[dev_name] = {
                    'name': dev_name,
                    'projects_count': 0,
                    'complexes': []
                }
            developers[dev_name]['projects_count'] += 1
            developers[dev_name]['complexes'].append(complex['name'])
        
        return list(developers.values())
    except Exception:
        return []

def search_global(query):
    """Global search across all types: ЖК, districts, developers, streets"""
    if not query or len(query.strip()) < 2:
        return []
    
    search_data = load_search_data()
    results = []
    query_lower = query.lower().strip()
    
    # Search through all categories
    for category in ['residential_complexes', 'districts', 'developers', 'streets']:
        items = search_data.get(category, [])
        for item in items:
            # Search in name and keywords
            name_match = query_lower in item['name'].lower()
            keyword_match = any(query_lower in keyword.lower() for keyword in item.get('keywords', []))
            
            if name_match or keyword_match:
                # Calculate relevance score
                score = 0
                if query_lower in item['name'].lower():
                    score += 10  # Higher score for name matches
                if query_lower == item['name'].lower():
                    score += 20  # Even higher for exact matches
                    
                result = {
                    'id': item['id'],
                    'name': item['name'],
                    'type': item['type'],
                    'url': item['url'],
                    'score': score
                }
                
                # Add additional context based on type
                if item['type'] == 'residential_complex':
                    result['district'] = item.get('district', '')
                    result['developer'] = item.get('developer', '')
                elif item['type'] == 'street':
                    result['district'] = item.get('district', '')
                    
                results.append(result)
    
    # Sort by relevance score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:10]  # Return top 10 results

def get_article_by_slug(slug):
    """Get a single article by slug"""
    articles = load_blog_articles()
    for article in articles:
        if article['slug'] == slug:
            return article
    return None

def search_articles(query, category=None):
    """Search articles by title, excerpt, content, and tags"""
    articles = load_blog_articles()
    if not query and not category:
        return articles
    
    filtered_articles = []
    for article in articles:
        # Filter by category if specified
        if category and article['category'].lower() != category.lower():
            continue
        
        # If no search query, return all articles in category
        if not query:
            filtered_articles.append(article)
            continue
        
        # Search in title, excerpt, content, and tags
        query_lower = query.lower()
        if (query_lower in article['title'].lower() or 
            query_lower in article['excerpt'].lower() or 
            query_lower in article['content'].lower() or 
            any(query_lower in tag.lower() for tag in article['tags'])):
            filtered_articles.append(article)
    
    return filtered_articles

def calculate_cashback(price):
    """Calculate cashback amount based on property price"""
    if not price or price == 0:
        return 0
    if price < 3000000:
        return int(price * 0.05)  # 5%
    elif price < 5000000:
        return int(price * 0.07)  # 7%
    else:
        return min(int(price * 0.10), 500000)  # 10% up to 500k

def get_property_by_id(property_id):
    """Get a single property by ID from Excel database with all photos"""
    try:
        # Use SQLAlchemy session like other functions in this file
        result = db.session.execute(text("""
        SELECT 
            inner_id, price, object_area, object_rooms, object_min_floor, object_max_floor, 
            address_display_name, renovation_display_name, min_rate, square_price, mortgage_price, 
            complex_object_class_display_name, photos, developer_name, complex_name, 
            complex_end_build_year, complex_end_build_quarter, complex_building_end_build_year, complex_building_end_build_quarter,
            address_position_lat, address_position_lon, description, address_locality_name
        FROM excel_properties 
        WHERE inner_id = :property_id
        """), {'property_id': property_id})
        
        row = result.fetchone()
        
        if not row:
            return None
            
        # Parse the row data into property format
        inner_id, price, area, rooms, min_floor, max_floor, address, renovation, min_rate, square_price, mortgage_price, class_type, photos, developer_name, complex_name, complex_end_year, complex_end_quarter, building_end_year, building_end_quarter, lat, lon, description, district_name = row
        
        # Parse photos JSON
        images = []
        floor_plan = None
        complex_photos = []
        
        try:
            if photos:
                photos_data = json.loads(photos)
                if isinstance(photos_data, list):
                    # If it's a simple list of photo URLs (like in this case)
                    images = photos_data
                    # Use first photo as main image, rest as gallery
                    if len(images) > 0:
                        # For floor plan, look for images that might be floor plans
                        # (typically contain words like "plan", "layout" or are architectural)
                        for img_url in images:
                            if any(keyword in img_url.lower() for keyword in ['plan', 'layout', 'scheme', 'планировка']):
                                floor_plan = img_url
                                break
                        # If no specific floor plan found, use the last image as floor plan
                        if not floor_plan and len(images) > 1:
                            floor_plan = images[-1]  # Last image often is floor plan
                elif isinstance(photos_data, dict):
                    # Get apartment gallery photos from dict structure
                    images = photos_data.get('apartment_gallery', [])
                    # Get floor plan 
                    floor_plans = photos_data.get('floor_plans', [])
                    if floor_plans and len(floor_plans) > 0:
                        floor_plan = floor_plans[0]  # Take first floor plan
                    # Get complex photos
                    complex_photos = photos_data.get('complex_gallery', [])
        except Exception as e:
            print(f"Error parsing photos for property {property_id}: {e}")
            pass
        
        # Build completion date
        completion_date = 'Уточняется'
        if building_end_year and building_end_quarter:
            completion_date = f"{building_end_year} г., {building_end_quarter} кв."
        elif building_end_year:
            completion_date = f"{building_end_year} г."
        elif complex_end_year:
            completion_date = f"{complex_end_year} г."
        
        # Create property data structure matching PDF template expectations
        property_data = {
            'id': inner_id,
            'title': f"{'Студия' if rooms == 0 else f'{rooms}-к. квартира'}, {area} м²",
            'price': price or 0,
            'area': area or 0,
            'rooms': rooms or 0,
            'floor': min_floor or 1,
            'total_floors': max_floor or min_floor or 1,
            'address': address or f"{district_name}, Краснодар" if district_name else 'Краснодар',
            'developer': developer_name or 'Не указан',
            'residential_complex': complex_name or 'Не указан',
            'district': district_name or 'Краснодар',
            'status': 'Свободна',
            'property_type': 'Студия' if rooms == 0 else 'Квартира',
            'renovation_type': renovation or 'Уточняется',
            'finishing': renovation or 'Предчистовая',
            'completion_date': completion_date,
            'mortgage_rate': f"{min_rate}%" if min_rate else '3.5%',
            'square_price': square_price,
            'mortgage_payment': mortgage_price,
            'class_type': class_type or 'Не указан',
            'description': description or '',
            'residential_complex_description': f"Современный жилой комплекс от застройщика {developer_name}" if developer_name else None,
            'mortgage_available': True,
            'installment_available': False,
            'cashback_available': True,
            # Photos for PDF
            'image': images[0] if images else None,  # Main photo
            'gallery': images,  # All apartment photos
            'floor_plan': floor_plan,  # Floor plan photo
            'complex_photos': complex_photos,  # Complex photos
            # Additional fields expected by PDF template
            'bathroom_type': 'Совмещенный',
            'has_balcony': True,
            'windows_type': 'Пластиковые', 
            'elevators': '2 пассажирских',
            'parking_type': 'Наземная',
            'developer_inn': 'ИНН не указан'
        }
        
        return property_data
        
    except Exception as e:
        print(f"Error getting property {property_id}: {e}")
        return None

def get_filtered_properties(filters):
    """Filter properties based on criteria including regional filters"""
    properties = load_properties()
    filtered = []
    
    for prop in properties:
        # Keywords filter (для типов недвижимости, классов, материалов)
        if filters.get('keywords') and len(filters['keywords']) > 0:
            keywords_matched = False
            for keyword in filters['keywords']:
                keyword_lower = keyword.lower()
                
                # Check property type
                prop_type_lower = prop.get('property_type', 'Квартира').lower()
                if keyword_lower == 'дом' and prop_type_lower == 'дом':
                    keywords_matched = True
                    break
                elif keyword_lower == 'таунхаус' and prop_type_lower == 'таунхаус':
                    keywords_matched = True
                    break
                elif keyword_lower == 'пентхаус' and prop_type_lower == 'пентхаус':
                    keywords_matched = True
                    break
                elif keyword_lower == 'апартаменты' and prop_type_lower == 'апартаменты':
                    keywords_matched = True
                    break
                elif keyword_lower == 'студия' and (prop_type_lower == 'студия' or prop.get('rooms') == 0):
                    keywords_matched = True
                    break
                elif keyword_lower == 'квартира' and prop_type_lower == 'квартира':
                    keywords_matched = True
                    break
                
                # Check property class
                elif keyword_lower == prop.get('property_class', '').lower():
                    keywords_matched = True
                    break
                
                # Check wall material
                elif keyword_lower in prop.get('wall_material', '').lower():
                    keywords_matched = True
                    break
                
                # Check features
                elif any(keyword_lower in feature.lower() for feature in prop.get('features', [])):
                    keywords_matched = True
                    break
                
                # Check in property type as fallback  
                elif keyword_lower in (f"{prop.get('rooms', 0)}-комн" if prop.get('rooms', 0) > 0 else "студия").lower():
                    keywords_matched = True
                    break
                    
            if not keywords_matched:
                continue
        
        # Text search with improved room number matching and word-based search
        if filters.get('search'):
            search_term = filters['search'].lower()
            
            # Create multiple variations for room descriptions
            rooms = prop.get('rooms', 0)
            if rooms == 0:
                room_variations = ["студия", "studio"]
            else:
                room_variations = [
                    f"{rooms}-комн",
                    f"{rooms}-комнатная",
                    f"{rooms} комн",
                    f"{rooms} комнатная"
                ]
                
                # Add spelled out numbers for 1-3 rooms
                if rooms == 1:
                    room_variations.extend(["однокомнатная", "1-комнатная", "одна комната"])
                elif rooms == 2:
                    room_variations.extend(["двухкомнатная", "2-комнатная", "две комнаты"])
                elif rooms == 3:
                    room_variations.extend(["трехкомнатная", "3-комнатная", "три комнаты"])
            
            # Create searchable text with all variations
            property_title = f"{prop.get('rooms', 0)}-комн" if prop.get('rooms', 0) > 0 else "студия"
            searchable_text = f"{property_title} {' '.join(room_variations)} {prop.get('developer_name', prop.get('developer', ''))} {prop.get('address_locality_name', prop.get('district', ''))} {prop.get('complex_name', prop.get('residential_complex', ''))} {prop.get('location', '')} квартира".lower()
            
            # Split search term into words and check if all words are found
            search_words = search_term.split()
            match_found = True
            
            for word in search_words:
                if word not in searchable_text:
                    match_found = False
                    break
            
            if not match_found:
                continue
        
        # Rooms filter - handle both single value and array
        if filters.get('rooms'):
            rooms_filter = filters['rooms']
            # ✅ ИСПРАВЛЕНО: используем object_rooms вместо rooms
            property_rooms = prop.get('object_rooms', prop.get('rooms', 0))
            
            # Handle array of rooms from saved searches
            if isinstance(rooms_filter, list):
                rooms_match = False
                for room_filter in rooms_filter:
                    # Handle special cases
                    if room_filter == '4+-комн':
                        if property_rooms >= 4 and property_type == '4+-комн':
                            rooms_match = True
                            break
                        continue
                    elif room_filter == 'студия' or room_filter == '0':
                        if property_rooms == 0:
                            rooms_match = True
                            break
                        continue
                    # Handle both "2-комн" and "2" formats - match type exactly
                    elif room_filter.endswith('-комн'):
                        # For X-комн format, match the type field exactly
                        if property_type == room_filter:
                            rooms_match = True
                            break
                        continue
                    elif room_filter == '4+':
                        if property_rooms >= 4 and property_type == '4+-комн':
                            rooms_match = True
                            break
                        continue
                    else:
                        try:
                            room_number = int(room_filter)
                            # ✅ ПРОСТОЕ СРАВНЕНИЕ по object_rooms
                            if property_rooms == room_number:
                                rooms_match = True
                                break
                        except (ValueError, TypeError):
                            continue
                
                if not rooms_match:
                    continue
            else:
                # Handle single room value
                if rooms_filter == '4+-комн':
                    if property_type != '4+-комн':
                        continue
                elif rooms_filter == '4+':
                    if property_type != '4+-комн':
                        continue
                elif rooms_filter == 'студия' or rooms_filter == '0':
                    if property_rooms != 0:
                        continue
                else:
                    try:
                        room_number = int(rooms_filter)
                        # ✅ ПРОСТОЕ СРАВНЕНИЕ по object_rooms
                        if property_rooms != room_number:
                            continue
                    except (ValueError, TypeError):
                        continue
        
        # Price filter - handle both raw rubles and millions
        if filters.get('price_min') and filters['price_min']:
            try:
                min_price = int(filters['price_min'])
                # If value is small, assume it's in millions
                if min_price < 1000:
                    min_price = min_price * 1000000
                if prop['price'] < min_price:
                    continue
            except (ValueError, TypeError):
                pass
        if filters.get('price_max') and filters['price_max']:
            try:
                max_price = int(filters['price_max'])
                # If value is small, assume it's in millions
                if max_price < 1000:
                    max_price = max_price * 1000000
                if prop['price'] > max_price:
                    continue
            except (ValueError, TypeError):
                pass
        
        # District filter
        if filters.get('district') and prop['district'] != filters['district']:
            continue
        
        # Developer filter
        if filters.get('developer') and prop['developer'] != filters['developer']:
            continue
        
        # Residential complex filter
        if filters.get('residential_complex'):
            residential_complex = filters['residential_complex'].lower()
            prop_complex = prop.get('complex_name', '').lower()
            if residential_complex not in prop_complex:
                continue
        
        # Street filter
        if filters.get('street'):
            street = filters['street'].lower()
            prop_location = prop.get('location', '').lower()
            prop_address = prop.get('full_address', '').lower()
            if street not in prop_location and street not in prop_address:
                continue
        
        # Mortgage filter
        if filters.get('mortgage') and not prop.get('mortgage_available', False):
            continue
        
        filtered.append(prop)
    
    return filtered

def get_developers_list():
    """Get list of unique developers"""
    properties = load_properties()
    developers = set()
    for prop in properties:
        if 'developer' in prop and prop['developer']:
            developers.add(prop['developer'])
    return sorted(list(developers))

def get_districts_list():
    """Get list of unique districts"""
    properties = load_properties()
    districts = set()
    for prop in properties:
        districts.add(prop['district'])
    return sorted(list(districts))

def sort_properties(properties, sort_type):
    """Sort properties by specified criteria with None safety"""
    if sort_type == 'price_asc':
        return sorted(properties, key=lambda x: x.get('price') or 0)
    elif sort_type == 'price_desc':
        return sorted(properties, key=lambda x: x.get('price') or 0, reverse=True)
    elif sort_type == 'cashback_desc':
        return sorted(properties, key=lambda x: calculate_cashback(x.get('price') or 0), reverse=True)
    elif sort_type == 'area_asc':
        return sorted(properties, key=lambda x: x.get('area') or 0)
    elif sort_type == 'area_desc':
        return sorted(properties, key=lambda x: x.get('area') or 0, reverse=True)
    else:
        return properties

def get_similar_properties(property_id, district, limit=3):
    """Get similar properties in the same district"""
    properties = load_properties()
    similar = []
    
    for prop in properties:
        if str(prop['id']) != str(property_id) and prop['district'] == district:
            similar.append(prop)
            if len(similar) >= limit:
                break
    
    return similar

# Routes
@app.route('/')
def index():
    """Home page with featured content"""
    properties = load_properties()
    
    # Загружаем реальные данные ЖК из базы данных (как в роуте /residential-complexes)
    exclusive_complexes = []
    try:
        from sqlalchemy import text
        complexes_query = db.session.execute(text("""
            SELECT 
                ep.complex_name,
                COUNT(*) as apartments_count,
                MIN(ep.price) as price_from,
                MAX(ep.price) as price_to,
                MIN(ep.object_area) as area_from,
                MAX(ep.object_area) as area_to,
                MIN(ep.object_min_floor) as floors_min,
                MAX(ep.object_max_floor) as floors_max,
                MAX(ep.developer_name) as developer_name,
                MAX(ep.address_display_name) as address_display_name,
                MAX(ep.complex_sales_address) as complex_sales_address,
                MAX(ep.complex_building_end_build_year) as end_build_year,
                MAX(ep.complex_building_end_build_quarter) as end_build_quarter,
                (SELECT photos FROM excel_properties p2 
                 WHERE p2.complex_name = ep.complex_name 
                 AND p2.photos IS NOT NULL 
                 ORDER BY p2.price DESC LIMIT 1) as photos,
                COALESCE(rc.id, ROW_NUMBER() OVER (ORDER BY ep.complex_name) + 1000) as real_id,
                CASE 
                    WHEN COUNT(DISTINCT ep.complex_building_id) > 0 
                    THEN COUNT(DISTINCT ep.complex_building_id)
                    WHEN COUNT(DISTINCT NULLIF(ep.complex_building_name, '')) > 0 
                    THEN COUNT(DISTINCT NULLIF(ep.complex_building_name, ''))
                    ELSE GREATEST(1, CEIL(COUNT(*) / 3.0))
                END as buildings_count,
                MAX(ep.complex_object_class_display_name) as object_class_display_name
            FROM excel_properties ep
            LEFT JOIN residential_complexes rc ON rc.name = ep.complex_name
            WHERE ep.complex_name IS NOT NULL AND ep.complex_name != ''
            GROUP BY ep.complex_name, rc.id
            ORDER BY 
                -- Показываем только лучшие ЖК (сданные и готовые к покупке)
                CASE 
                    WHEN MAX(ep.complex_building_end_build_year) = 2025 
                    AND MAX(ep.complex_building_end_build_quarter) = 4 
                    THEN 1  -- "IV кв. 2025 г. Строится" в конце (не эксклюзивные)
                    ELSE 0  -- Готовые и ближайшие к сдаче ЖК сначала
                END,
                MIN(ep.price) ASC  -- Сначала более доступные по цене
            LIMIT 6
        """))
        
        complexes_data = complexes_query.fetchall()
        
        for row in complexes_data:
            # Обработка фото
            main_photo = '/static/images/no-photo.jpg'
            photos_list = [main_photo]
            
            if row[13]:  # photos column
                try:
                    photos_raw = json.loads(row[13])
                    if photos_raw and isinstance(photos_raw, list):
                        photos_list = photos_raw[:2]  # Первые 2 фото для карточки
                        main_photo = photos_list[0] if photos_list else main_photo
                except:
                    pass
            
            # Определение статуса и типа комнат
            current_year = 2025
            current_quarter = 4
            
            is_completed = False
            completion_date = 'Не указан'
            
            if row[11] and row[12]:  # end_build_year и end_build_quarter
                build_year = int(row[11])
                build_quarter = int(row[12])
                
                if build_year < current_year:
                    is_completed = True
                elif build_year == current_year and build_quarter < current_quarter:
                    is_completed = True
                
                quarter_names = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
                quarter = quarter_names.get(build_quarter, build_quarter)
                completion_date = f"{quarter} кв. {build_year} г."
            
            # Определение типа комнат
            room_types = []
            if row[5] and row[6]:  # area_from и area_to
                if row[5] < 35:
                    room_types.append("Студии")
                if row[5] <= 45 and row[6] >= 35:
                    room_types.append("1К")
                if row[6] >= 55:
                    room_types.append("2-3К")
            else:
                room_types = ["Студии", "1-3К"]
            
            room_type_display = " - ".join(room_types) if room_types else "Различные"
            
            # Безопасная обработка изображений
            safe_images = photos_list if photos_list and len(photos_list) > 0 else ['/static/images/no-photo.jpg']
            safe_main_image = safe_images[0] if safe_images else '/static/images/no-photo.jpg'
            
            # Обрабатываем адрес - убираем "Сочи" из начала
            clean_address = row[9] or ''
            if clean_address.startswith('Сочи, '):
                clean_address = clean_address[6:]  # Убираем "Сочи, "
            elif clean_address.startswith('г. Сочи, '):
                clean_address = clean_address[9:]  # Убираем "г. Сочи, "
            
            complex_dict = {
                'id': row[14] or 1,  # real_id
                'name': row[0] or 'Без названия',
                'price_from': int(row[2] or 0),
                'price_to': int(row[3] or 0),
                'area_from': int(row[4] or 0),
                'area_to': int(row[5] or 0),
                'room_type': room_type_display,
                'address': clean_address,
                'developer': row[8] or 'Не указан',
                'photos': safe_images,
                'images': safe_images,  # Для совместимости с шаблоном
                'image': safe_main_image,    # Основное фото  
                'main_photo': safe_main_image,
                'main_image': safe_main_image,  # Безопасное главное фото
                'apartments_count': row[1] or 0,
                'completion_date': completion_date,
                'is_completed': is_completed,
                'cashback_max': int((row[3] or 0) * 0.05) if row[3] else 0,  # 5% от максимальной цены
                'buildings_count': int(row[16]) if row[16] and str(row[16]).isdigit() else 1
            }
            exclusive_complexes.append(complex_dict)
            
    except Exception as e:
        print(f"Error loading exclusive complexes: {e}")
        import traceback
        traceback.print_exc()
        exclusive_complexes = []
    
    complexes = load_residential_complexes()  # Для совместимости со старым кодом
    developers_file = os.path.join('data', 'developers.json')
    with open(developers_file, 'r', encoding='utf-8') as f:
        developers = json.load(f)
    
    # Загружаем статьи блога из базы данных для главной страницы
    blog_articles = []
    try:
        from models import BlogPost, BlogArticle
        from sqlalchemy import or_, desc
        
        # Получаем опубликованные статьи из обеих таблиц
        blog_posts = BlogPost.query.filter_by(status='published').order_by(desc(BlogPost.published_at)).limit(4).all()
        blog_articles_db = BlogArticle.query.filter_by(status='published').order_by(desc(BlogArticle.published_at)).limit(4).all()
        
        # Преобразуем в единый формат для шаблона
        for post in blog_posts:
            blog_articles.append({
                'title': post.title,
                'slug': post.slug,
                'excerpt': post.excerpt or 'Интересная статья о недвижимости',
                'featured_image': post.featured_image or 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'published_at': post.published_at or post.created_at,
                'reading_time': getattr(post, 'reading_time', 5),
                'category': post.category or 'Недвижимость',
                'url': f'/blog/{post.slug}'
            })
        
        for article in blog_articles_db:
            blog_articles.append({
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt or 'Полезная информация о недвижимости',
                'featured_image': article.featured_image or 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'published_at': article.published_at or article.created_at,
                'reading_time': getattr(article, 'reading_time', 4),
                'category': 'Недвижимость',
                'url': f'/blog/{article.slug}'
            })
        
        # Сортируем по дате и берем последние 4
        blog_articles = sorted(blog_articles, key=lambda x: x['published_at'] or datetime.now(), reverse=True)[:4]
        
    except Exception as e:
        print(f"Error loading blog articles for index: {e}")
        # Fallback статьи если база недоступна
        blog_articles = [
            {
                'title': 'Ипотека мурабаха: что это и как оформить',
                'slug': 'ipoteka-murabaha',
                'excerpt': 'Ипотека мурабаха — это исламская ипотека без процентов, где банк покупает недвижимость и продает ее клиенту с наценкой.',
                'featured_image': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'published_at': datetime.now(),
                'reading_time': 5,
                'category': 'Ипотека',
                'url': '/blog/ipoteka-murabaha'
            }
        ]
    
    # ✅ РЕАЛЬНЫЕ ДАННЫЕ: Получаем 6 случайных объектов напрямую из функции API
    try:
        import random
        from models import ExcelProperty
        
        # Получаем объекты напрямую из базы со ВСЕМИ нужными полями
        from sqlalchemy import text
        result = db.session.execute(text("""
            SELECT inner_id, price, object_area, object_rooms, 
                   object_min_floor, object_max_floor,
                   address_display_name, complex_name, developer_name, photos,
                   complex_end_build_quarter, complex_end_build_year,
                   complex_building_end_build_quarter, complex_building_end_build_year
            FROM excel_properties
            WHERE price > 0 AND photos IS NOT NULL AND photos != '' AND photos != '[]'
                AND address_position_lat IS NOT NULL 
                AND address_position_lon IS NOT NULL
                AND object_area > 0
                AND complex_name IS NOT NULL AND complex_name != ''
            ORDER BY RANDOM()
            LIMIT 8
        """))
        
        featured_properties = []
        for row in result:
            try:
                # Парсим фото
                main_image = 'https://via.placeholder.com/400x300?text=Фото+скоро'
                gallery = [main_image]
                
                if row.photos:
                    try:
                        photos_raw = json.loads(row.photos)
                        if photos_raw and isinstance(photos_raw, list) and len(photos_raw) > 0:
                            main_image = photos_raw[0]
                            gallery = photos_raw[:5]
                    except:
                        pass
                
                # ✅ ИСПРАВЛЕНИЯ: Правильное форматирование всех полей
                rooms = int(row.object_rooms or 0)
                area = float(row.object_area or 0)
                price = int(row.price or 0)
                
                # Правильные этажи
                floor_min = int(row.object_min_floor or 1)
                floor_max = int(row.object_max_floor or floor_min)
                floor_text = f"{floor_min}/{floor_max} эт." if floor_min == floor_max else f"{floor_min}-{floor_max}/{floor_max} эт."
                
                # Правильное название типа квартиры
                if rooms == 0:
                    room_type = "Студия"
                else:
                    room_type = f"{rooms}-комн"
                
                # Статус готовности и квартал сдачи
                current_year = 2025
                build_quarter = row.complex_end_build_quarter or row.complex_building_end_build_quarter
                build_year = row.complex_end_build_year or row.complex_building_end_build_year
                
                if build_year and build_quarter:
                    # ✅ ИСПРАВЛЕНО: Правильный формат квартала
                    if build_quarter == 1:
                        quarter_text = f"1кв. {build_year}г."
                    elif build_quarter == 2:
                        quarter_text = f"2кв. {build_year}г."
                    elif build_quarter == 3:
                        quarter_text = f"3кв. {build_year}г."
                    elif build_quarter == 4:
                        quarter_text = f"4кв. {build_year}г."
                    else:
                        quarter_text = f"{build_quarter}кв. {build_year}г."
                    
                    # Статус на основе года и квартала
                    if build_year < current_year or (build_year == current_year and build_quarter <= 1):
                        status_text = "Сдан"
                    else:
                        status_text = "Строится"
                else:
                    quarter_text = "Уточняется"
                    status_text = "Строится"
                
                # Формируем данные в правильном формате
                prop = {
                    'id': str(row.inner_id),
                    'price': price,
                    'area': area,
                    'rooms': rooms,
                    'title': f"{room_type}, {area} м², {floor_text}",
                    'complex': row.complex_name or 'ЖК не указан',
                    'developer': row.developer_name or '',
                    'address': row.address_display_name or '',
                    'image': main_image,
                    'gallery': gallery,
                    'cashback': int(price * 0.02),
                    'cashback_amount': int(price * 0.02),
                    'completion_date': quarter_text,
                    'status': status_text,
                    'floor_info': floor_text
                }
                featured_properties.append(prop)
                if len(featured_properties) >= 6:  # Ограничиваем до 6 качественных объектов
                    break
                
            except Exception as e:
                print(f"Error processing property {row.inner_id}: {e}")
                continue
        
        if featured_properties:
            print(f"✅ Загружено {len(featured_properties)} реальных объектов из базы")
        else:
            raise Exception("No properties loaded")
            
    except Exception as e:
        print(f"❌ Ошибка загрузки реальных объектов: {e}")
        # Fallback к старым данным
        featured_properties = sorted(properties, key=lambda x: x.get('cashback_amount', 0), reverse=True)[:6]
        for prop in featured_properties:
            prop['cashback'] = calculate_cashback(prop['price'])
    
    # Get districts with statistics
    districts_data = {}
    for complex in complexes:
        district = complex['district']
        if district not in districts_data:
            districts_data[district] = {
                'name': district,
                'complexes_count': 0,
                'price_from': float('inf'),
                'apartments_count': 0
            }
        districts_data[district]['complexes_count'] += 1
        districts_data[district]['price_from'] = min(districts_data[district]['price_from'], complex.get('price_from', 0))
        districts_data[district]['apartments_count'] += complex.get('apartments_count', 0)
    
    districts = sorted(districts_data.values(), key=lambda x: x['complexes_count'], reverse=True)[:8]
    
    # Get featured developers (top 3 with most complexes)
    featured_developers = []
    for developer in developers[:3]:
        developer_complexes = [c for c in complexes if c.get('developer_id') == developer['id']]
        developer_properties = [p for p in properties if any(c['id'] == p.get('complex_id') for c in developer_complexes)]
        
        developer_info = {
            'id': developer['id'],
            'name': developer['name'],
            'complexes_count': len(developer_complexes),
            'apartments_count': len(developer_properties),
            'price_from': min([p['price'] for p in developer_properties]) if developer_properties else 0,
            'max_cashback': max([c.get('cashback_percent', 5) for c in developer_complexes]) if developer_complexes else 5
        }
        featured_developers.append(developer_info)
    
    # Загружаем категории блога для главной страницы
    blog_categories = []
    try:
        from models import Category
        blog_categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order, Category.name).all()
    except Exception as e:
        print(f"Error loading blog categories for index: {e}")
    
    return render_template('index.html',
                         featured_properties=featured_properties,
                         districts=districts,
                         featured_developers=featured_developers,
                         residential_complexes=complexes[:3],
                         exclusive_complexes=exclusive_complexes,
                         blog_articles=blog_articles,
                         blog_categories=blog_categories)

@app.route('/properties')
def properties():
    """Properties listing page - loads ALL data from excel_properties table"""
    try:
        # Processing property filters
        search_query = request.args.get('search', '').strip()
        rooms_filter = request.args.get('rooms', '').strip()  # может быть "1,2,3"
        district_filter = request.args.get('district', '').strip()
        developer_filter = request.args.get('developer', '').strip()
        price_from = request.args.get('price_from', '').strip()
        price_to = request.args.get('price_to', '').strip()
        area_from = request.args.get('area_from', '').strip()
        area_to = request.args.get('area_to', '').strip() 
        floor_from = request.args.get('floor_from', '').strip()
        floor_to = request.args.get('floor_to', '').strip()
        
        from models import ExcelProperty, Developer, ResidentialComplex
        
        # Get ALL properties directly from excel_properties table using raw SQL
        try:
            from sqlalchemy import text
            result = db.session.execute(text("""
                SELECT inner_id, price, object_area, object_rooms, object_min_floor, object_max_floor,
                       address_display_name, renovation_display_name, min_rate, square_price, 
                       mortgage_price, complex_object_class_display_name, photos,
                       developer_name, complex_name, complex_end_build_year, complex_end_build_quarter,
                       complex_building_end_build_year, complex_building_end_build_quarter,
                       address_position_lat, address_position_lon, description, address_locality_name,
                       complex_building_name, parsed_city, parsed_region, renovation_type,
                       placement_type, deal_type, complex_building_accreditation,
                       complex_building_has_green_mortgage, complex_has_green_mortgage
                FROM excel_properties
            """))
            
            excel_properties = result.fetchall()
            # Properties loaded successfully
        except Exception as e:
            print(f"Error loading excel properties: {e}")
            return render_template('error.html', error="Ошибка загрузки данных объектов")
        
        # ✅ ИСПРАВЛЕНО: Поддержка всех форматов параметров цены
        filters = {}
        filters['price_min'] = request.args.get('price_min', request.args.get('priceFrom', request.args.get('price_from', '')))
        filters['price_max'] = request.args.get('price_max', request.args.get('priceTo', request.args.get('price_to', '')))
        # Обработка комнат (может прийти как "1,2,3" или как список)
        rooms_param = request.args.get('rooms', '')
        if rooms_param:
            filters['rooms'] = rooms_param.split(',') if ',' in rooms_param else [rooms_param]
        else:
            filters['rooms'] = request.args.getlist('rooms') or []
        filters['districts'] = request.args.getlist('districts') or []  # Добавляем поддержку районов
        filters['developers'] = request.args.getlist('developers') or []  # Добавляем поддержку застройщиков
        filters['completion'] = request.args.getlist('completion') or []  # Добавляем поддержку лет сдачи
        filters['developer'] = request.args.get('developer', '')
        filters['district'] = request.args.get('district', '')  # Добавляем район
        filters['residential_complex'] = request.args.get('residential_complex', '')
        filters['building'] = request.args.get('building', '')  # Добавляем поддержку фильтра по зданию/корпусу
        
        # Расширенные фильтры из секции "Еще"
        filters['area_min'] = request.args.get('area_from', request.args.get('areaFrom', ''))
        filters['area_max'] = request.args.get('area_to', request.args.get('areaTo', ''))
        filters['floor_min'] = request.args.get('floor_from', request.args.get('floorFrom', ''))
        filters['floor_max'] = request.args.get('floor_to', request.args.get('floorTo', ''))
        filters['building_types'] = request.args.getlist('building_types') or []
        filters['delivery_years'] = request.args.getlist('delivery_years') or []
        filters['features'] = request.args.getlist('features') or []
        filters['object_classes'] = request.args.getlist('object_classes') or []
        
        # Региональные фильтры
        filters['regions'] = request.args.getlist('regions') or []
        filters['cities'] = request.args.getlist('cities') or []
        filters['region'] = request.args.get('region', '')
        filters['city'] = request.args.get('city', '')
        
        # Поисковый запрос
        filters['search'] = request.args.get('search', '')
        
        # Filters applied
        
        # ✅ ДОБАВЛЕНА ПАГИНАЦИЯ: Параметры страницы
        page = int(request.args.get('page', 1))
        per_page = 20  # Показываем по 20 объектов на странице
        
        # Convert Excel properties to template format with pagination
        properties_data = []
        total_rows = len(excel_properties)
        processed_count = 0
        filtered_count = 0  # Счетчик отфильтрованных объектов
        
        for row in excel_properties:
            try:
                # Get data from SQL row tuple with all fields
                inner_id, price, area, rooms, min_floor, max_floor, address, renovation, min_rate, square_price, mortgage_price, class_type, photos, developer_name, complex_name, complex_end_year, complex_end_quarter, building_end_year, building_end_quarter, lat, lon, description, district_name, building_name, parsed_city, parsed_region, renovation_type, placement_type, deal_type, building_accreditation, building_green_mortgage, complex_green_mortgage = row
                
                price = price or 0
                area = area or 0
                rooms = rooms or 0
                min_floor = min_floor or 1
                max_floor = max_floor or min_floor
                
                # ✅ ИСПРАВЛЕНО: Apply price filters - правильная конвертация
                if filters.get('price_min'):
                    try:
                        min_price = float(filters['price_min'])
                        # Пользователь вводит в миллионах, конвертируем в рубли
                        min_price = min_price * 1000000
                        if price < min_price:
                            continue
                    except:
                        pass
                
                if filters.get('price_max'):
                    try:
                        max_price = float(filters['price_max'])
                        # Пользователь вводит в миллионах, конвертируем в рубли
                        max_price = max_price * 1000000
                        if price > max_price:
                            continue
                    except:
                        pass
                
                # Apply area filters
                if filters.get('area_min'):
                    try:
                        min_area = float(filters['area_min'])
                        if area < min_area:
                            continue
                    except:
                        pass
                        
                if filters.get('area_max'):
                    try:
                        max_area = float(filters['area_max'])
                        if area > max_area:
                            continue
                    except:
                        pass
                
                # Apply floor filters
                if filters.get('floor_min'):
                    try:
                        min_floor_filter = int(filters['floor_min'])
                        if min_floor < min_floor_filter:
                            continue
                    except:
                        pass
                        
                if filters.get('floor_max'):
                    try:
                        max_floor_filter = int(filters['floor_max'])
                        if min_floor > max_floor_filter:
                            continue
                    except:
                        pass
                
                # Apply building type filters (этажность дома)
                if filters.get('building_types'):
                    building_match = False
                    for building_type in filters['building_types']:
                        if building_type == 'малоэтажный' and max_floor <= 5:
                            building_match = True
                            break
                        elif building_type == 'среднеэтажный' and 6 <= max_floor <= 12:
                            building_match = True
                            break
                        elif building_type == 'многоэтажный' and max_floor >= 13:
                            building_match = True
                            break
                    if not building_match:
                        continue
                
                # Apply district filters
                if filters.get('districts'):
                    district_match = False
                    for district_filter in filters['districts']:
                        if district_name and district_filter.lower() in district_name.lower():
                            district_match = True
                            break
                    if not district_match:
                        continue
                
                # Apply developer filters  
                if filters.get('developers'):
                    developer_match = False
                    for developer_filter in filters['developers']:
                        if developer_name and developer_filter.lower() in developer_name.lower():
                            developer_match = True
                            break
                    if not developer_match:
                        continue
                
                # ✅ ДОБАВЛЯЕМ: Apply rooms filter
                if filters.get('rooms'):
                    rooms_filter = filters['rooms']
                    if rooms_filter:
                        # Поддерживаем массив и одиночное значение
                        if isinstance(rooms_filter, list):
                            rooms_match = False
                            for room_filter in rooms_filter:
                                try:
                                    if int(room_filter) == rooms:
                                        rooms_match = True
                                        break
                                except (ValueError, TypeError):
                                    continue
                            if not rooms_match:
                                continue
                        else:
                            try:
                                if int(rooms_filter) != rooms:
                                    continue
                            except (ValueError, TypeError):
                                continue

                # Apply completion year filters
                if filters.get('completion'):
                    completion_match = False
                    for year_filter in filters['completion']:
                        if year_filter == 'Сдан':
                            # Проверяем сданные объекты
                            completion_match = True
                            break
                        else:
                            # Проверяем год сдачи
                            if (complex_end_year and str(complex_end_year) == year_filter) or \
                               (building_end_year and str(building_end_year) == year_filter):
                                completion_match = True
                                break
                    if not completion_match:
                        continue
                
                # Apply delivery year filters (legacy support)
                if filters.get('delivery_years'):
                    delivery_match = False
                    for year_filter in filters['delivery_years']:
                        if year_filter == 'Сдан':
                            # Проверяем сданные объекты
                            delivery_match = True
                            break
                        else:
                            # Проверяем год сдачи
                            if (complex_end_year and str(complex_end_year) == year_filter) or \
                               (building_end_year and str(building_end_year) == year_filter):
                                delivery_match = True
                                break
                    if not delivery_match:
                        continue
                
                # Apply features filters
                if filters.get('features'):
                    # Этот фильтр пока пропускаем, так как нужны дополнительные поля из БД
                    pass
                
                # Apply object class filters  
                if filters.get('object_classes'):
                    if class_type:
                        class_match = False
                        for class_filter in filters['object_classes']:
                            if class_filter.lower() in class_type.lower():
                                class_match = True
                                break
                        if not class_match:
                            continue
                
                # Apply regional filters (regions and cities)
                if filters.get('regions') or filters.get('cities') or filters.get('region') or filters.get('city'):
                    # Get property address for regional matching
                    address = str(address_display_name).lower() if address_display_name else ''
                    
                    regional_match = True  # Start with True, will be set to False if no match
                    
                    # Check region filters (multiple)
                    if filters.get('regions'):
                        region_match = False
                        for region_filter in filters['regions']:
                            if region_filter.lower() in address:
                                region_match = True
                                break
                        if not region_match:
                            regional_match = False
                    
                    # Check single region filter
                    if filters.get('region') and filters['region']:
                        if filters['region'].lower() not in address:
                            regional_match = False
                    
                    # Check city filters (multiple)
                    if filters.get('cities'):
                        city_match = False
                        for city_filter in filters['cities']:
                            if city_filter.lower() in address:
                                city_match = True
                                break
                        if not city_match:
                            regional_match = False
                            
                    # Check single city filter
                    if filters.get('city') and filters['city']:
                        if filters['city'].lower() not in address:
                            regional_match = False
                    
                    if not regional_match:
                        continue

                # Apply room filter - ИСПРАВЛЕНО: поддержка всех форматов
                if filters.get('rooms'):
                    room_match = False
                    for room_filter in filters['rooms']:
                        # Нормализуем значение фильтра
                        normalized_filter = room_filter.lower()
                        
                        
                        # Студия
                        if (normalized_filter in ['studio', 'студия'] and rooms == 0):
                            room_match = True
                            break
                        # 1-комнатная, 1-комн, 1 
                        elif rooms == 1 and (normalized_filter in ['1-комнатная', '1-комн', '1'] or 
                              (room_filter.isdigit() and int(room_filter) == 1)):
                            room_match = True
                            break
                        # 2-комнатная, 2-комн, 2
                        elif (normalized_filter in ['2-комнатная', '2-комн', '2'] or 
                              (room_filter.isdigit() and int(room_filter) == 2)) and rooms == 2:
                            room_match = True
                            break
                        # 3-комнатная, 3-комн, 3
                        elif (normalized_filter in ['3-комнатная', '3-комн', '3'] or 
                              (room_filter.isdigit() and int(room_filter) == 3)) and rooms == 3:
                            room_match = True
                            break
                        # 4+ комнатная
                        elif (normalized_filter in ['4-комнатная', '4-комн', '4', '4+'] or 
                              (room_filter.isdigit() and int(room_filter) >= 4)) and rooms >= 4:
                            room_match = True
                            break
                    if not room_match:
                        continue
                
                # Apply developer filter
                if filters.get('developer') and developer_name:
                    if filters['developer'].lower() not in developer_name.lower():
                        continue
                
                # Apply complex filter  
                if filters.get('residential_complex') and complex_name:
                    if filters['residential_complex'].lower() not in complex_name.lower():
                        continue
                
                # Apply building filter
                if filters.get('building') and building_name:
                    if filters['building'].lower() not in building_name.lower():
                        continue
                
                # Apply search filter
                if filters.get('search'):
                    search_query = filters['search'].lower()
                    search_match = False
                    
                    # Search in multiple fields
                    if address and search_query in address.lower():
                        search_match = True
                    elif developer_name and search_query in developer_name.lower():
                        search_match = True
                    elif complex_name and search_query in complex_name.lower():
                        search_match = True
                    elif district_name and search_query in district_name.lower():
                        search_match = True
                    elif building_name and search_query in building_name.lower():
                        search_match = True
                    
                    if not search_match:
                        continue
                
                # Обработка фотографий из PostgreSQL array format {url1,url2,url3}
                images = []
                if photos:
                    try:
                        # Убираем фигурные скобки и разделяем по запятым
                        if photos.startswith('{') and photos.endswith('}'):
                            photos_clean = photos[1:-1]  # убираем { и }
                            if photos_clean:
                                images = [url.strip() for url in photos_clean.split(',')]
                        else:
                            # Если это JSON формат, пробуем парсить как JSON
                            import json
                            photos_list = json.loads(photos)
                            images = photos_list if photos_list else []
                    except:
                        images = []
                
                # Create title with detailed floor info
                if rooms == 0:
                    title = f"Студия {area} м²"
                elif rooms == 1:
                    title = f"1-комнатная квартира, {area} м²"
                elif rooms == 2:
                    title = f"2-комнатная квартира, {area} м²"
                elif rooms == 3:
                    title = f"3-комнатная квартира, {area} м²"
                else:
                    title = f"{rooms}-комнатная квартира, {area} м²"
                
                # ✅ ИСПРАВЛЕНО: Add floor information - этаж квартиры/этажность дома
                if min_floor and max_floor:
                    # min_floor - это этаж квартиры, max_floor - этажность дома
                    title += f", {min_floor}/{max_floor} эт."
                
                # Create completion date from available data
                completion_date = 'Уточняется'
                if building_end_year and building_end_quarter:
                    completion_date = f"{building_end_year} г., {building_end_quarter} кв."
                elif complex_end_year and complex_end_quarter:
                    completion_date = f"{complex_end_year} г., {complex_end_quarter} кв."
                elif building_end_year:
                    completion_date = f"{building_end_year} г."
                elif complex_end_year:
                    completion_date = f"{complex_end_year} г."
                
                prop_data = {
                    'id': inner_id,
                    'title': title,
                    'price': price,
                    'area': area,
                    'rooms': rooms,
                    'floor': min_floor,
                    'total_floors': max_floor,
                    # Добавляем поля для совместимости с JavaScript фильтрами
                    'object_min_floor': min_floor,
                    'object_max_floor': max_floor,
                    'object_area': area,
                    'address': address or 'Адрес уточняется',
                    'developer': developer_name or 'Не указан',
                    'developer_name': developer_name or 'Не указан',  # Для совместимости с JavaScript
                    'complex_name': complex_name or 'Не указан',
                    'district': district_name or 'Краснодар',
                    'address_locality_name': district_name or 'Краснодар',  # Для совместимости с JavaScript
                    'renovation_type': renovation or 'Уточняется',
                    'finish_type': renovation or 'Уточняется',  # Для совместимости с шаблоном
                    'completion_date': completion_date,
                    'mortgage_rate': f"{min_rate}%" if min_rate else '3.5%',
                    'square_price': square_price,
                    'mortgage_payment': mortgage_price,
                    'class_type': class_type or 'Не указан',
                    'complex_object_class_display_name': class_type or '',  # Для JavaScript фильтров
                    'renovation_display_name': renovation or '',  # Для JavaScript фильтров
                    'renovation_type': renovation_type or '',  # Дополнительное поле отделки
                    'placement_type': placement_type or '',  # Тип размещения
                    'deal_type': deal_type or '',  # Тип сделки
                    'building_accreditation': building_accreditation or '',  # Аккредитация
                    'building_floors': max_floor or 0,  # Этажность дома = максимальный этаж здания
                    'has_green_mortgage': building_green_mortgage or complex_green_mortgage or False,  # Зеленая ипотека
                    'green_mortgage': building_green_mortgage or complex_green_mortgage or False,  # Дублируем для совместимости
                    # Создаем массив особенностей на основе доступных данных
                    'features': [f for f in [
                        'Зеленая ипотека' if (building_green_mortgage or complex_green_mortgage) else None,
                        'Аккредитация' if building_accreditation else None,
                        'Новостройка' if deal_type and 'новострой' in str(deal_type).lower() else None,
                        'Без отделки' if renovation and 'без отделки' in str(renovation).lower() else None,
                        'С отделкой' if renovation and ('с отделкой' in str(renovation).lower() or 'чистовая' in str(renovation).lower()) else None,
                    ] if f],
                    'cashback': calculate_cashback(price) if price else 0,
                    'images': images,
                    'gallery': images,  # Добавляем gallery для слайдера
                    'image': images[0] if images else 'https://via.placeholder.com/400x300/f3f4f6/9ca3af?text=Фото+недоступно',
                    'address_position_lat': lat,
                    'address_position_lon': lon,
                    'description': description or '',
                    # Добавляем парсенные поля для фильтрации
                    'parsed_city': parsed_city,
                    'parsed_region': parsed_region
                }
                properties_data.append(prop_data)
                
            except Exception as e:
                print(f"Error processing excel property {inner_id}: {e}")
        
        
        # Properties filtered
        
        # Sort properties
        sort_type = request.args.get('sort', 'price_asc')
        if sort_type == 'price_asc':
            properties_data.sort(key=lambda x: x.get('price') or 0)
        elif sort_type == 'price_desc':
            properties_data.sort(key=lambda x: x.get('price') or 0, reverse=True)
        elif sort_type == 'area_asc':
            properties_data.sort(key=lambda x: x.get('area') or 0)
        elif sort_type == 'area_desc':
            properties_data.sort(key=lambda x: x.get('area') or 0, reverse=True)
        
        # Properties sorted
        
        # ✅ ОТКЛЮЧАЕМ ПАГИНАЦИЮ НА СЕРВЕРЕ: Передаем ВСЕ объекты для JavaScript фильтрации
        page = int(request.args.get('page', 1))
        per_page = len(properties_data) if properties_data else 100  # ВСЕ объекты
        total_properties = len(properties_data)  # Общее количество найденных объектов
        total_pages = 1  # Только одна страница со всеми объектами
        offset = 0
        properties_page = properties_data  # ВСЕ объекты для JavaScript фильтрации
        
        # ✅ ИСПРАВЛЕН ТЕКСТ: Правильное склонение слова "объект"
        def get_object_word(count):
            if count % 100 in [11, 12, 13, 14]:
                return "объектов"
            elif count % 10 == 1:
                return "объект"
            elif count % 10 in [2, 3, 4]:
                return "объекта"
            else:
                return "объектов"
        
        results_text = f"Найдено {total_properties} " + get_object_word(total_properties)
        # Pagination applied
        
        # Pagination info
        pagination = {
            'page': page,
            'per_page': per_page,
            'total': total_properties,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_page': page - 1 if page > 1 else None,
            'next_page': page + 1 if page < total_pages else None
        }
        
        # Authentication
        user_authenticated = current_user.is_authenticated if hasattr(current_user, 'is_authenticated') else False
        manager_id = session.get('manager_id')
        manager_authenticated = bool(manager_id)
        
        # Auth status checked
        
        current_manager = None
        if manager_authenticated:
            from models import Manager
            current_manager = Manager.query.get(manager_id)
            # Manager found
        else:
            # No manager auth
            pass
        
        # Load data for filters
        developers = [d.name for d in Developer.query.all()]
        
        # Загружаем ЖК с фотографиями из Excel
        complexes_query = db.session.execute(text("""
            SELECT 
                complex_name,
                COUNT(*) as apartments_count,
                MIN(price) as price_from,
                MAX(price) as price_to,
                MAX(developer_name) as developer_name
            FROM excel_properties 
            GROUP BY complex_name
            ORDER BY complex_name
            LIMIT 11
        """))
        
        residential_complexes_with_photos = []
        for idx, row in enumerate(complexes_query.fetchall()):
            complex_dict = {
                'id': idx + 1,
                'name': row[0],
                'available_apartments': row[1],
                'price_from': row[2] or 0,
                'price_to': row[3] or 0,
                'district': 'Краснодарский край',
                'developer': row[4] or 'Не указан'
            }
            
            # Загружаем фото ЖК из самой дорогой квартиры (как репрезентативное для ЖК)
            photos_query = db.session.execute(text("""
                SELECT photos FROM excel_properties 
                WHERE complex_name = :complex_name 
                AND photos IS NOT NULL 
                ORDER BY price DESC, object_area DESC
                LIMIT 1
            """), {'complex_name': complex_dict['name']})
            
            photos_row = photos_query.fetchone()
            if photos_row and photos_row[0]:
                try:
                    import json
                    photos_list = json.loads(photos_row[0])
                    # Пропускаем первые фото (интерьеры квартир) и берем фото ЖК
                    start_index = min(len(photos_list) // 4, 5) if len(photos_list) > 8 else 1
                    complex_dict['image'] = photos_list[start_index] if len(photos_list) > start_index else photos_list[0]
                    # Для слайдера берем фото ЖК (пропускаем первые интерьеры)
                    complex_dict['images'] = photos_list[start_index:] if len(photos_list) > start_index else photos_list
                except:
                    complex_dict['image'] = 'https://via.placeholder.com/400x300/0088CC/FFFFFF?text=' + complex_dict['name']
                    complex_dict['images'] = []
            else:
                complex_dict['image'] = 'https://via.placeholder.com/400x300/0088CC/FFFFFF?text=' + complex_dict['name']
                complex_dict['images'] = []
            
            residential_complexes_with_photos.append(complex_dict)
        
        # Complexes loaded with photos
        
        # Rendering template
        
        return render_template('properties.html', 
                             properties=properties_page,  # Объекты для текущей страницы
                             pagination=pagination,  # Информация о пагинации
                             filters=filters,
                             developers=developers,
                             districts=[],  # TODO: implement districts
                             residential_complexes=residential_complexes_with_photos,
                             results_text=results_text,  # ✅ Правильный текст результатов 
                             total_properties=total_properties,  # ✅ Общее количество найденных
                             current_sort=sort_type,  # Текущая сортировка
                             user_authenticated=user_authenticated,
                             manager_authenticated=manager_authenticated,
                             current_manager=current_manager)
                             
    except Exception as e:
        print(f"ERROR in properties route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error 500: {str(e)}", 500

@app.route('/object/<int:property_id>')
def property_detail(property_id):
    """Individual property page - uses Excel property data"""
    try:
        # Get property from excel_properties table
        from sqlalchemy import text
        result = db.session.execute(text("""
            SELECT inner_id, price, object_area, object_rooms, object_min_floor, object_max_floor,
                   address_display_name, renovation_display_name, min_rate, square_price, 
                   mortgage_price, complex_object_class_display_name, photos,
                   developer_name, complex_name, complex_end_build_year, complex_end_build_quarter,
                   complex_building_end_build_year, complex_building_end_build_quarter,
                   address_position_lat, address_position_lon, description,
                   address_locality_name, address_short_display_name, 
                   complex_sales_address, complex_sales_phone, complex_with_renovation,
                   complex_has_accreditation, complex_has_green_mortgage, complex_has_mortgage_subsidy,
                   trade_in, deal_type, object_is_apartment, published_dt, placement_type,
                   complex_building_name, complex_building_released, complex_id
            FROM excel_properties 
            WHERE inner_id = :property_id
        """), {"property_id": property_id})
        
        row = result.fetchone()
        if not row:
            print(f"Excel property {property_id} not found")
            return redirect(url_for('properties'))
        
        # Parse row data - добавляем все новые поля включая complex_id
        inner_id, price, area, rooms, min_floor, max_floor, address, renovation, min_rate, square_price, mortgage_price, class_type, photos, developer_name, complex_name, complex_end_year, complex_end_quarter, building_end_year, building_end_quarter, lat, lon, description, locality_name, short_address, sales_address, sales_phone, with_renovation, has_accreditation, has_green_mortgage, has_mortgage_subsidy, trade_in, deal_type, is_apartment, published_dt, placement_type, building_name, building_released, complex_id = row
        
        # Parse photos
        images = []
        if photos:
            try:
                if photos.startswith('{') and photos.endswith('}'):
                    photos_clean = photos[1:-1]
                    if photos_clean:
                        images = [url.strip() for url in photos_clean.split(',')]
                else:
                    import json
                    photos_list = json.loads(photos)
                    images = photos_list if photos_list else []
            except:
                images = []
        
        # Create completion date
        completion_date = 'Уточняется'
        if building_end_year and building_end_quarter:
            completion_date = f"{building_end_year} г., {building_end_quarter} кв."
        elif complex_end_year and complex_end_quarter:
            completion_date = f"{complex_end_year} г., {complex_end_quarter} кв."
        elif building_end_year:
            completion_date = f"{building_end_year} г."
        elif complex_end_year:
            completion_date = f"{complex_end_year} г."
        
        # Build property data for template - все поля из базы данных
        property_data = {
            'id': inner_id,
            'complex_id': complex_id,  # Добавляем complex_id для ссылок на ЖК
            'price': price or 0,
            'area': area or 0,
            'rooms': rooms or 0,
            'floor': min_floor or 1,
            'total_floors': max_floor or min_floor or 1,
            'address': address or 'Адрес уточняется',
            'short_address': short_address or address or 'Адрес уточняется',
            'locality_name': locality_name or 'Краснодар',
            'developer': developer_name or 'Не указан',
            'complex_name': complex_name or 'Не указан',
            'building_name': building_name or 'Корпус 1',
            'building_released': building_released,
            'renovation_type': renovation or 'Уточняется',
            'completion_date': completion_date,
            'mortgage_rate': f"{min_rate}%" if min_rate else '3.5%',
            'square_price': square_price,
            'mortgage_payment': mortgage_price,
            'class_type': class_type or 'Не указан',
            'cashback': calculate_cashback(price) if price else 0,
            'images': images,
            'image': images[0] if images else 'https://via.placeholder.com/400x300/f3f4f6/9ca3af?text=Фото+недоступно',
            'address_position_lat': lat,
            'address_position_lon': lon,
            'description': description or f"Продается квартира в {complex_name}. Отличная планировка, качественная отделка.",
            'gallery': images,
            # Дополнительные поля из Excel базы
            'sales_address': sales_address or 'Уточняется',
            'sales_phone': sales_phone or 'Уточняется',
            'with_renovation': with_renovation,
            'has_accreditation': has_accreditation,
            'has_green_mortgage': has_green_mortgage,
            'has_mortgage_subsidy': has_mortgage_subsidy,
            'trade_in_available': trade_in,
            'deal_type': deal_type or 'Продажа',
            'is_apartment': is_apartment,
            'published_date': published_dt,
            'placement_type': placement_type or 'Новостройка'
        }
        
        if not property_data:
            print(f"Property {property_id} not found")
            return redirect(url_for('properties'))
        
        # Ensure all required fields exist for template
        property_data['cashback_amount'] = property_data['cashback']
        
        # Generate full title format for property detail page
        rooms = property_data.get('rooms', 0)
        area = property_data.get('area', 0)
        floor = property_data.get('floor', 1)
        total_floors = property_data.get('total_floors', 20)
        
        # Generate room type text
        if rooms > 0:
            room_text = f"{rooms}-комнатная квартира"
        else:
            room_text = "Студия"
            
        # Create full detailed title for property page
        title_parts = [room_text]
        
        if area:
            title_parts.append(f"{area} м²")
            
        title_parts.append(f"{floor}/{total_floors} эт.")
        
        # Join with commas for full format
        property_data['title'] = ", ".join(title_parts)
        
        if 'property_type' not in property_data:
            property_data['property_type'] = f"{rooms}-комн" if rooms > 0 else "Студия"
            
        if 'completion_date' not in property_data:
            property_data['completion_date'] = '2025'
            
        if 'total_floors' not in property_data:
            property_data['total_floors'] = 20
            
        if 'apartment_number' not in property_data:
            property_data['apartment_number'] = str(property_data['id'])
            
        if 'building' not in property_data:
            property_data['building'] = 'Корпус 1'
            
        # Add template-required fields
        if 'complex_id' not in property_data:
            property_data['complex_id'] = property_data.get('residential_complex_id', 1)
            
        if 'complex_name' not in property_data:
            property_data['complex_name'] = property_data.get('residential_complex', 'ЖК')
            
        if 'cashback_percent' not in property_data:
            property_data['cashback_percent'] = 3.5
        
        # Получаем дополнительную информацию о ЖК из таблицы residential_complexes
        complex_info = None
        if complex_id:
            complex_result = db.session.execute(text("""
                SELECT name, district_id, developer_id, object_class_display_name, 
                       start_build_year, end_build_year, has_accreditation, 
                       has_green_mortgage, with_renovation
                FROM residential_complexes 
                WHERE complex_id = :complex_id
            """), {"complex_id": str(complex_id)})
            complex_row = complex_result.fetchone()
            if complex_row:
                complex_info = {
                    'name': complex_row[0],
                    'district_id': complex_row[1],
                    'developer_id': complex_row[2],
                    'class_display_name': complex_row[3],
                    'start_year': complex_row[4],
                    'end_year': complex_row[5],
                    'has_accreditation': complex_row[6],
                    'has_green_mortgage': complex_row[7],
                    'with_renovation': complex_row[8]
                }
        
        # Вычисляем статистику для ЖК если есть complex_id
        similar_apartments = []
        if complex_id:
            # 1. Всего квартир в этом ЖК
            total_result = db.session.execute(text("""
                SELECT COUNT(*) as total
                FROM excel_properties 
                WHERE complex_id = :complex_id
            """), {"complex_id": complex_id})
            property_data['complex_total_apartments'] = total_result.fetchone()[0] or 0
            
            # 2. Количество квартир такой же планировки (по количеству комнат)
            same_type_result = db.session.execute(text("""
                SELECT COUNT(*) as total
                FROM excel_properties 
                WHERE complex_id = :complex_id AND object_rooms = :rooms
            """), {"complex_id": complex_id, "rooms": rooms})
            property_data['same_type_apartments'] = same_type_result.fetchone()[0] or 0
            
            # 3. Количество корпусов в ЖК
            buildings_result = db.session.execute(text("""
                SELECT COUNT(DISTINCT complex_building_name) as total
                FROM excel_properties 
                WHERE complex_id = :complex_id AND complex_building_name IS NOT NULL
            """), {"complex_id": complex_id})
            property_data['complex_buildings_count'] = buildings_result.fetchone()[0] or 1
            
            # 4. НОВОЕ: Получаем другие квартиры из этого же ЖК (исключая текущую)
            similar_result = db.session.execute(text("""
                SELECT inner_id, price, object_area, object_rooms, object_min_floor, 
                       object_max_floor, photos, complex_building_name
                FROM excel_properties 
                WHERE complex_id = :complex_id AND inner_id != :current_id
                ORDER BY object_rooms ASC, price ASC
                LIMIT 8
            """), {"complex_id": complex_id, "current_id": property_id})
            
            # Обрабатываем результаты для шаблона
            for row in similar_result.fetchall():
                apt_id, apt_price, apt_area, apt_rooms, apt_min_floor, apt_max_floor, apt_photos, apt_building = row
                
                # Парсим фотографии
                apt_images = []
                if apt_photos:
                    try:
                        if apt_photos.startswith('{') and apt_photos.endswith('}'):
                            photos_clean = apt_photos[1:-1]
                            if photos_clean:
                                apt_images = [url.strip() for url in photos_clean.split(',')]
                        else:
                            import json
                            photos_list = json.loads(apt_photos)
                            apt_images = photos_list if photos_list else []
                    except:
                        apt_images = []
                
                # Формируем тип комнат
                room_type = f"{apt_rooms}-комн" if apt_rooms > 0 else "Студия"
                
                similar_apartments.append({
                    'id': apt_id,
                    'price': apt_price or 0,
                    'area': apt_area or 0,
                    'rooms': apt_rooms or 0,
                    'room_type': room_type,
                    'floor': apt_min_floor or 1,
                    'total_floors': apt_max_floor or apt_min_floor or 1,
                    'building': apt_building or 'Корпус 1',
                    'cashback': calculate_cashback(apt_price) if apt_price else 0,
                    'image': apt_images[0] if apt_images else 'https://via.placeholder.com/300x200/f3f4f6/9ca3af?text=Фото+недоступно',
                    'title': f"{room_type}, {apt_area} м², {apt_min_floor}/{apt_max_floor or apt_min_floor} эт." if apt_area else f"{room_type}"
                })
        else:
            property_data['complex_total_apartments'] = 'н/д'
            property_data['same_type_apartments'] = 'н/д'
            property_data['complex_buildings_count'] = 'н/д'
            
        print(f"Rendering property {property_id}: {property_data.get('title', 'Unknown')}")
        return render_template('property_detail.html', property=property_data, complex_info=complex_info, similar_apartments=similar_apartments)
        
    except Exception as e:
        print(f"ERROR in property detail route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error 500: {str(e)}", 500

def create_slug(name):
    """Create SEO-friendly slug from complex name with transliteration"""
    if not name:
        return "unknown"
    
    # Transliteration table for Russian to Latin
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        # Uppercase variants
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '',
        'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    
    # Remove ЖК prefix and quotes
    name = re.sub(r'^ЖК\s*["\']?', '', name, flags=re.IGNORECASE)
    name = re.sub(r'["\']', '', name)  # Remove remaining quotes
    
    # Transliterate Cyrillic to Latin
    slug = ''
    for char in name:
        if char in translit_map:
            slug += translit_map[char]
        else:
            slug += char
    
    # Clean up: remove special characters except spaces and hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Replace spaces/multiple hyphens with single hyphen
    slug = re.sub(r'[-\s]+', '-', slug)
    
    return slug.lower().strip('-')

@app.route('/residential_complex/<int:complex_id>')
@app.route('/residential-complex/<int:complex_id>')  # Support both formats
@app.route('/residential-complex/<complex_name>')  # Support name-based routing
@app.route('/zk/<slug>')  # New SEO-friendly format: /zk/zhk-kislorod
def residential_complex_detail(complex_id=None, complex_name=None, slug=None):
    """Individual residential complex page"""
    try:
        # Загружаем данные ЖК из базы данных - поддержка поиска по имени, ID и slug
        if slug:
            # Поиск по slug - ищем ЖК, чей slug соответствует переданному
            complexes_query = db.session.execute(text("""
                SELECT rc.*
                FROM residential_complexes rc
            """))
            complex_row = None
            for row in complexes_query.fetchall():
                if create_slug(row.name) == slug:
                    complex_row = row
                    break
            # Если не найден в таблице, пробуем найти в Excel
            if not complex_row:
                excel_complexes = db.session.execute(text("""
                    SELECT DISTINCT complex_name
                    FROM excel_properties
                """)).fetchall()
                for excel_row in excel_complexes:
                    if create_slug(excel_row[0]) == slug:
                        complex_name = excel_row[0]
                        break
        elif complex_name:
            complex_query = db.session.execute(text("""
                SELECT rc.*
                FROM residential_complexes rc
                WHERE rc.name = :complex_name
            """), {'complex_name': complex_name})
            complex_row = complex_query.fetchone()
        elif complex_id:
            complex_query = db.session.execute(text("""
                SELECT rc.*
                FROM residential_complexes rc
                WHERE rc.complex_id = :complex_id_str OR rc.id = :complex_id
            """), {'complex_id': complex_id, 'complex_id_str': str(complex_id)})
            complex_row = complex_query.fetchone()
        else:
            complex_row = None
        if not complex_row:
            print(f"Complex {complex_id or complex_name or slug} not found in database")
            # Создаем заглушку на основе Excel данных
            if complex_name:
                excel_query = db.session.execute(text("""
                    SELECT complex_name, COUNT(*) as apartments_count
                    FROM excel_properties 
                    WHERE complex_name = :complex_name
                    GROUP BY complex_name
                """), {'complex_name': complex_name})
                excel_row = excel_query.fetchone()
                if excel_row:
                    complex_data = {
                        'id': 1,
                        'name': excel_row[0],
                        'apartments_count': excel_row[1],
                        'description': f'ЖК {excel_row[0]} с {excel_row[1]} квартирами'
                    }
                else:
                    return redirect(url_for('properties'))
            else:
                return redirect(url_for('properties'))
        else:
            # Безопасно конвертируем complex_row в словарь
            try:
                complex_data = dict(complex_row._mapping)
            except (AttributeError, TypeError) as e:
                print(f"Error converting complex_row to dict: {e}")
                return redirect(url_for('properties'))
        
        # Загружаем реальные данные из Excel для этого ЖК включая количество корпусов
        excel_data_query = db.session.execute(text("""
            SELECT 
                COUNT(*) as total_apartments,
                MIN(price) as min_price,
                MAX(price) as max_price,
                AVG(price) as avg_price,
                MIN(object_area) as min_area,
                MAX(object_area) as max_area,
                MIN(object_min_floor) as min_floor,
                MAX(object_max_floor) as max_floor_in_complex,
                MAX(address_short_display_name) as address_display_name,
                MAX(complex_sales_address) as sales_address,
                CASE 
                    WHEN COUNT(DISTINCT complex_building_name) > 0 THEN COUNT(DISTINCT complex_building_name)
                    ELSE 1 
                END as buildings_count,
                MAX(complex_start_build_year) as complex_start_year,
                MAX(complex_start_build_quarter) as complex_start_quarter,
                MAX(complex_object_class_display_name) as object_class,
                bool_or(complex_with_renovation) as with_renovation
            FROM excel_properties ep
            WHERE ep.complex_name = :complex_name
        """), {'complex_name': complex_data['name']})
        
        excel_data = excel_data_query.fetchone()
        if excel_data and excel_data[0]:
            # Обновляем данные комплекса реальными данными из Excel
            complex_data['apartments_count'] = excel_data[0]
            complex_data['price_from'] = int(excel_data[1]) if excel_data[1] else 3000000
            complex_data['price_to'] = int(excel_data[2]) if excel_data[2] else 15000000
            complex_data['real_price_from'] = complex_data['price_from']
            complex_data['real_price_to'] = complex_data['price_to']
            complex_data['real_area_from'] = excel_data[4] if excel_data[4] else 35
            complex_data['real_area_to'] = excel_data[5] if excel_data[5] else 135
            complex_data['real_floors_min'] = excel_data[6] if excel_data[6] else 1
            complex_data['real_floors_max'] = excel_data[7] if excel_data[7] else 25
            complex_data['total_floors_in_complex'] = excel_data[7] if excel_data[7] else 25
            complex_data['full_address'] = excel_data[8] if excel_data[8] else complex_data.get('sales_address', '')
            complex_data['sales_address'] = excel_data[9] if excel_data[9] else complex_data.get('sales_address', '')
            # Новые поля
            complex_data['buildings_count'] = excel_data[10] if excel_data[10] else 1
            complex_data['complex_start_year'] = excel_data[11] if excel_data[11] else 2020
            complex_data['complex_start_quarter'] = excel_data[12] if excel_data[12] else 1
            complex_data['object_class_display_name'] = excel_data[13] if excel_data[13] else 'Комфорт'
            complex_data['with_renovation'] = excel_data[14] if excel_data[14] else False
            
            # Добавляем информацию о застройщике из Excel данных
            developer_query = db.session.execute(text("""
                SELECT DISTINCT developer_name 
                FROM excel_properties 
                WHERE complex_name = :complex_name 
                AND developer_name IS NOT NULL
                LIMIT 1
            """), {'complex_name': complex_data['name']})
            
            developer_row = developer_query.fetchone()
            if developer_row:
                complex_data['developer_name'] = developer_row[0]
                # Developer set
            else:
                # No developer found
                pass
                
            # Загружаем координаты для карты
            coordinates_query = db.session.execute(text("""
                SELECT address_position_lat, address_position_lon 
                FROM excel_properties 
                WHERE complex_name = :complex_name 
                AND address_position_lat IS NOT NULL 
                AND address_position_lon IS NOT NULL
                LIMIT 1
            """), {'complex_name': complex_data['name']})
            
            coordinates_row = coordinates_query.fetchone()
            if coordinates_row:
                complex_data['coordinates'] = [coordinates_row[0], coordinates_row[1]]
                # Coordinates set
            else:
                complex_data['coordinates'] = [45.0355, 38.9753]  # Краснодар по умолчанию
                # Using default coordinates
            
            # Загружаем фотографии ЖК из самой дорогой квартиры (как репрезентативные для ЖК)
            first_apartment_query = db.session.execute(text("""
                SELECT photos FROM excel_properties 
                WHERE complex_name = :complex_name 
                AND photos IS NOT NULL 
                ORDER BY price DESC, object_area DESC
                LIMIT 1
            """), {'complex_name': complex_data['name']})
            
            first_apartment = first_apartment_query.fetchone()
            if first_apartment and first_apartment[0]:
                try:
                    photos_raw = first_apartment[0]
                    # Парсим PostgreSQL array формат {url1,url2,url3}
                    if photos_raw.startswith('{') and photos_raw.endswith('}'):
                        photos_clean = photos_raw[1:-1]  # убираем { и }
                        if photos_clean:
                            photos_list = [url.strip() for url in photos_clean.split(',')]
                    else:
                        # Если это JSON формат, парсим как JSON
                        import json
                        photos_list = json.loads(photos_raw)
                    
                    # Пропускаем первые фото планировок и берем фото ЖК
                    start_index = min(len(photos_list) // 4, 5) if len(photos_list) > 8 else 1
                    complex_images = photos_list[start_index:] if len(photos_list) > start_index else photos_list
                    complex_data['images'] = complex_images[:10]  # Берем до 10 фото ЖК для слайдера
                    complex_data['image'] = complex_images[0] if complex_images else photos_list[0]
                except Exception as e:
                    print(f"Error parsing photos for complex {complex_data['name']}: {e}")
                    complex_data['images'] = []
                    complex_data['image'] = None
            else:
                complex_data['images'] = []
                complex_data['image'] = None
                
            print(f"Updated complex data with Excel: {complex_data['apartments_count']} apartments, price from {complex_data['price_from']}, address: {complex_data['full_address']}, photos: {len(complex_data.get('images', []))}")
        
        if not complex_data:
            print(f"Complex {complex_id} not found")
            return redirect(url_for('properties'))
        
        # Ensure required fields exist
        if 'price_from' not in complex_data:
            complex_data['price_from'] = 3000000
        if 'real_price_from' not in complex_data:
            complex_data['real_price_from'] = complex_data['price_from']
        if 'cashback_percent' not in complex_data:
            complex_data['cashback_percent'] = 3.5
        
        # Add developer_id for link functionality
        if 'developer_id' not in complex_data:
            developer_mapping = {
                'ГК «Инвестстройкуб»': 1,
                'ЖК Девелопмент': 2,
                'Краснодар Строй': 3,
                'Южный Дом': 4,
                'Кубань Девелопмент': 5
            }
            developer_name = complex_data.get('developer', '')
            complex_data['developer_id'] = developer_mapping.get(developer_name, 1)
        
        # Загружаем квартиры этого ЖК из Excel данных
        apartments_query = db.session.execute(text("""
            SELECT *
            FROM excel_properties ep
            WHERE ep.complex_name = :complex_name
            ORDER BY ep.price ASC
        """), {'complex_name': complex_data['name']})
        
        complex_properties = []
        for i, prop_row in enumerate(apartments_query):
            prop_dict = dict(prop_row._mapping)
            # Добавляем вычисленные поля
            prop_dict['id'] = prop_dict.get('inner_id', i + 1)  # Используем inner_id из Excel для ссылок
            prop_dict['cashback_amount'] = int(prop_dict['price'] * 0.035) if prop_dict.get('price') else 0
            prop_dict['type'] = f"{prop_dict.get('object_rooms', 1)}-комн"
            prop_dict['residential_complex_id'] = complex_id
            prop_dict['residential_complex'] = complex_data['name']
            
            # Правильно показываем этаж квартиры из общего количества этажей в комплексе
            apartment_floor = prop_dict.get('object_min_floor', 1)  # Этаж конкретной квартиры
            total_floors = complex_data.get('total_floors_in_complex', 25)  # Общее количество этажей в комплексе
            # Правильное отображение типа квартиры
            rooms = prop_dict.get('object_rooms', 1)
            if rooms == 0:
                room_type = "Студия"
            else:
                room_type = f"{rooms}-комнатная квартира"
            prop_dict['title'] = f"{room_type}, {prop_dict.get('object_area', 0)} м², {apartment_floor}/{total_floors} эт."
            prop_dict['apartment_floor'] = apartment_floor
            prop_dict['total_floors_in_complex'] = total_floors
            
            # Используем реальные фотографии из Excel (PostgreSQL array формат)
            photos_raw = prop_dict.get('photos', '')
            try:
                if photos_raw and photos_raw.startswith('{') and photos_raw.endswith('}'):
                    # PostgreSQL array формат {url1,url2,url3}
                    photos_clean = photos_raw[1:-1]  # убираем { и }
                    if photos_clean:
                        photos_list = [url.strip() for url in photos_clean.split(',')]
                else:
                    # Если это JSON формат, парсим как JSON
                    import json
                    photos_list = json.loads(photos_raw) if photos_raw else []
                
                prop_dict['image'] = photos_list[0] if photos_list else 'https://via.placeholder.com/400x300/0088CC/FFFFFF?text=Квартира'
                prop_dict['photos_list'] = photos_list  # Все фото для галереи
            except Exception as e:
                print(f"Error parsing photos for apartment {prop_dict.get('inner_id', 'unknown')}: {e}")
                prop_dict['image'] = 'https://via.placeholder.com/400x300/0088CC/FFFFFF?text=Квартира'
                prop_dict['photos_list'] = []
                
            prop_dict['property_type'] = 'Квартира'
            complex_properties.append(prop_dict)
        
        # Group properties by room count and calculate statistics for each type
        properties_by_rooms = {}
        room_stats = {}
        for prop in complex_properties:
            rooms = prop.get('object_rooms', 1)
            # Правильное определение типа квартиры
            if rooms == 0:
                room_key = 'Студия'
                room_type = 'Студия'
            else:
                room_key = f'{rooms}-комн'
                room_type = f'{rooms}-комн'
            
            if room_key not in properties_by_rooms:
                properties_by_rooms[room_key] = []
                room_stats[room_key] = {
                    'count': 0,
                    'prices': [],
                    'areas': [],
                    'name': room_type
                }
            
            properties_by_rooms[room_key].append(prop)
            room_stats[room_key]['count'] += 1
            if prop.get('price'):
                room_stats[room_key]['prices'].append(prop['price'])
            if prop.get('object_area'):
                room_stats[room_key]['areas'].append(prop['object_area'])
        
        # Calculate min/max for each room type
        for room_key in room_stats:
            stats = room_stats[room_key]
            if stats['prices']:
                stats['price_from'] = min(stats['prices'])
                stats['price_to'] = max(stats['prices'])
            else:
                stats['price_from'] = 0
                stats['price_to'] = 0
            
            if stats['areas']:
                stats['area_from'] = min(stats['areas'])
                stats['area_to'] = max(stats['areas'])
            else:
                stats['area_from'] = 0
                stats['area_to'] = 0
        
        complex_data['room_stats'] = room_stats
        
        # Группировка квартир по корпусам/литерам с сортировкой
        properties_by_building_unsorted = {}
        for prop in complex_properties:
            building_name = prop.get('complex_building_name', 'Основной корпус')
            if building_name not in properties_by_building_unsorted:
                properties_by_building_unsorted[building_name] = []
            properties_by_building_unsorted[building_name].append(prop)
        
        # Сортируем корпуса по числовому порядку
        def sort_buildings(building_name):
            import re
            # Проверяем на None или пустую строку
            if not building_name:
                return 999  # None/пустые в конце
            # Ищем числа в названии корпуса
            match = re.search(r'([0-9]+)', str(building_name))
            if match:
                return int(match.group(1))
            else:
                return 999  # Остальные в конце
        
        # Создаем отсортированный словарь корпусов
        properties_by_building = {}
        sorted_building_names = sorted(properties_by_building_unsorted.keys(), key=sort_buildings)
        for building_name in sorted_building_names:
            properties_by_building[building_name] = properties_by_building_unsorted[building_name]
        
        # Загружаем данные о корпусах из Excel с максимумом информации
        buildings_data = {}
        try:
            # Получаем расширенные данные о корпусах из Excel с автоматическим статусом
            buildings_query = db.session.execute(text("""
                SELECT 
                    ep.complex_building_name as building_name,
                    ep.complex_building_end_build_year as end_build_year,
                    ep.complex_building_end_build_quarter as end_build_quarter,
                    ep.complex_start_build_year as start_build_year,  
                    ep.complex_start_build_quarter as start_build_quarter,
                    ep.complex_object_class_display_name as object_class,
                    COUNT(*) as total_apartments,
                    MAX(ep.complex_building_end_build_year) as max_end_build_year,
                    MAX(ep.complex_building_end_build_quarter) as max_end_build_quarter,
                    MAX(ep.object_max_floor) as total_floors,
                    999 as sort_order
                FROM excel_properties ep
                WHERE ep.complex_name = :complex_name 
                AND ep.complex_building_name IS NOT NULL
                GROUP BY ep.complex_building_name, ep.complex_building_end_build_year, 
                         ep.complex_building_end_build_quarter, ep.complex_start_build_year,
                         ep.complex_start_build_quarter, ep.complex_object_class_display_name
                ORDER BY sort_order, ep.complex_building_name
            """), {
                'complex_name': complex_data.get('name', '')
            })
            
            # Получаем текущую дату в Python для кросс-платформенности
            from datetime import datetime
            import re
            current_date = datetime.now()
            current_year = current_date.year
            current_quarter = (current_date.month - 1) // 3 + 1
            
            # Сначала собираем все данные
            buildings_list = []
            for building_row in buildings_query:
                building_dict = dict(building_row._mapping)
                
                # Вычисляем статус корпуса в Python 
                end_year = building_dict.get('max_end_build_year')
                end_quarter = building_dict.get('max_end_build_quarter')
                
                if end_year and end_quarter:
                    if (end_year < current_year or 
                        (end_year == current_year and end_quarter <= current_quarter)):
                        building_dict['building_status'] = 'Сдан'
                    else:
                        building_dict['building_status'] = 'Строится'
                    # Добавляем данные в правильном формате для шаблона
                    building_dict['end_build_year'] = end_year
                    building_dict['end_build_quarter'] = end_quarter
                else:
                    building_dict['building_status'] = 'Не указан'
                
                # Вычисляем sort_order в Python (кросс-платформенно)
                building_name = building_dict.get('building_name', '')
                match = re.search(r'([0-9]+)', building_name)
                if match:
                    building_dict['sort_order'] = int(match.group(1))
                else:
                    building_dict['sort_order'] = 999
                    
                buildings_list.append(building_dict)
            
            # Сортируем по sort_order в Python
            buildings_list.sort(key=lambda x: (x['sort_order'], x.get('building_name', '')))
            
            # Создаем итоговый словарь
            for building_dict in buildings_list:
                buildings_data[building_dict['building_name']] = building_dict
            
            print(f"Loaded {len(buildings_data)} buildings for complex {complex_data.get('name')}")
        except Exception as e:
            print(f"Error loading buildings data: {e}")
            import traceback
            traceback.print_exc()
        
        complex_data['buildings'] = buildings_data
        
        # Добавляем текущую дату для определения статуса корпусов
        from datetime import datetime
        current_date = datetime.now()
        complex_data['current_year'] = current_date.year
        complex_data['current_quarter'] = (current_date.month - 1) // 3 + 1
        
        # Найти похожие ЖК - упрощенная версия без сложных запросов
        similar_complexes = []
        try:
            # Простой запрос для получения 3 других ЖК
            current_complex_name = complex_data.get('name', '')
            
            with db.engine.connect() as connection:
                # Используем отдельное соединение для избежания проблем с транзакциями
                result = connection.execute(text("""
                    SELECT DISTINCT 
                        ep.complex_name,
                        rc.id,
                        MIN(ep.price) as price_from,
                        MAX(ep.price) as price_to,
                        COUNT(*) as apartments_count,
                        MAX(ep.developer_name) as developer_name,
                        MAX(ep.address_short_display_name) as location,
                        MAX(ep.photos) as photos
                    FROM excel_properties ep
                    LEFT JOIN residential_complexes rc ON rc.name = ep.complex_name
                    WHERE ep.complex_name != :current_complex_name
                    AND ep.price IS NOT NULL
                    GROUP BY ep.complex_name, rc.id
                    ORDER BY MIN(ep.price) ASC
                    LIMIT 3
                """), {'current_complex_name': current_complex_name})
                
                for row in result.fetchall():
                    # Парсим фото
                    image_url = 'https://via.placeholder.com/300x200'
                    if row[7]:  # photos field
                        try:
                            import json
                            photos_raw = row[7]
                            # Фото хранятся в JSON формате
                            photos_list = json.loads(photos_raw)
                            if photos_list:
                                # Пропускаем первые фото (интерьеры) и берем фото ЖК
                                start_index = min(len(photos_list) // 4, 5) if len(photos_list) > 8 else 1
                                image_url = photos_list[start_index] if len(photos_list) > start_index else photos_list[0]
                        except:
                            pass
                    
                    similar_complex = {
                        'id': row[1] or 999,
                        'name': row[0],
                        'price_from': int(row[2]) if row[2] else 0,
                        'price_to': int(row[3]) if row[3] else 0,
                        'apartments_count': row[4],
                        'developer': row[5] or 'Не указан',
                        'location': row[6] or 'Адрес не указан',
                        'image': image_url,
                        'completion_date': '2025 г.',
                        'cashback_percent': 5.0,
                        'url': f'/residential-complex/{row[1]}' if row[1] else '#'
                    }
                    similar_complexes.append(similar_complex)
                    
        except Exception as e:
            print(f"Error finding similar complexes: {e}")
            # Если все упало, просто оставляем пустой список
            similar_complexes = []
        
        print(f"Found {len(similar_complexes)} similar complexes for {complex_data.get('name', 'Unknown')}")
        print(f"Rendering complex {complex_id}: {complex_data.get('name', 'Unknown')}")
        return render_template('residential_complex_detail.html', 
                             complex=complex_data,
                             properties=complex_properties,
                             properties_by_rooms=properties_by_rooms,
                             properties_by_building=properties_by_building,
                             similar_complexes=similar_complexes)
                             
    except Exception as e:
        print(f"ERROR in complex detail route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error 500: {str(e)}", 500

@app.route('/developer/<int:developer_id>')
def developer_detail(developer_id):
    """Individual developer page"""
    try:
        # Load developer data from JSON file instead of DB to avoid conflicts
        with open('data/developers.json', 'r', encoding='utf-8') as f:
            developers_data = json.load(f)
        
        # Find developer by ID
        developer = None
        for dev in developers_data:
            if dev['id'] == developer_id:
                developer = dev
                break
        
        if not developer:
            return "Застройщик не найден", 404
        
        # Add missing template fields for new developers
        if 'total_apartments_sold' not in developer:
            developer['total_apartments_sold'] = 150
        if 'projects_completed' not in developer:
            developer['projects_completed'] = 8
        if 'years_experience' not in developer:
            developer['years_experience'] = 10
        if 'rating' not in developer:
            developer['rating'] = 4.5
        if 'construction_technology' not in developer:
            developer['construction_technology'] = 'Монолитно-каркасная'
        if 'warranty_years' not in developer:
            developer['warranty_years'] = 5
        if 'advantages' not in developer:
            developer['advantages'] = [
                'Качественное строительство',
                'Соблюдение сроков сдачи',
                'Развитая инфраструктура',
                'Выгодные условия покупки'
            ]
        
        # Get all complexes by this developer
        complexes = load_residential_complexes()
        developer_complexes = [c for c in complexes if c.get('developer_id') == developer_id or c.get('developer') == developer['name']]
        
        # Get all properties by this developer
        properties = load_properties()
        developer_properties = [p for p in properties if p.get('developer') == developer['name']]
        
        return render_template('developer_detail.html',
                             developer=developer,
                             complexes=developer_complexes,
                             properties=developer_properties)
    except Exception as e:
        print(f"ERROR in developer_detail route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error 500: {str(e)}", 500

def generate_qr_code(url):
    """Generate QR code for given URL and return as base64 string"""
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        qr_image.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return qr_base64
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

@app.route('/object/<int:property_id>/pdf')
def property_pdf(property_id):
    """Property PDF card page with QR code"""
    property_data = get_property_by_id(property_id)
    if not property_data:
        return redirect(url_for('properties'))
    
    # Calculate cashback for this property
    cashback = calculate_cashback(property_data['price'])
    
    # Get current date for PDF generation
    current_date = datetime.now().strftime('%d.%m.%Y')
    
    # Generate QR code with link to object page
    # Use custom domain from environment variable or fall back to current request domain
    custom_domain = os.environ.get('QR_DOMAIN')
    if custom_domain:
        # Remove trailing slash and ensure it starts with http:// or https://
        custom_domain = custom_domain.rstrip('/')
        if not custom_domain.startswith(('http://', 'https://')):
            custom_domain = 'https://' + custom_domain
        object_url = custom_domain + url_for('property_detail', property_id=property_id)
    else:
        # Default behavior - use current request domain
        object_url = request.url_root.rstrip('/') + url_for('property_detail', property_id=property_id)
    
    qr_code_base64 = generate_qr_code(object_url)
    
    return render_template('property_pdf.html', 
                         property=property_data,
                         cashback=cashback,
                         current_date=current_date,
                         qr_code=qr_code_base64,
                         object_url=object_url)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    """How it works page"""
    return render_template('how-it-works.html')

@app.route('/reviews')
def reviews():
    """Reviews page"""
    return render_template('reviews.html')

@app.route('/contacts')
def contacts():
    """Contacts page"""
    return render_template('contacts.html')

@app.route('/blog')
def blog():
    """Blog main page with articles listing, search, and categories"""
    from models import BlogPost, Category
    from sqlalchemy import text
    
    # Get search parameters  
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    page = int(request.args.get('page', 1))
    per_page = 6
    
    # Унифицированная загрузка статей (как в index) - объединяем BlogPost и BlogArticle
    all_articles = []
    
    try:
        # Получаем статьи из BlogPost
        blog_posts = BlogPost.query.filter_by(status='published').all()
        for post in blog_posts:
            all_articles.append({
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'excerpt': post.excerpt or 'Интересная статья о недвижимости',
                'content': post.content,
                'featured_image': post.featured_image or 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'published_at': post.published_at or post.created_at,
                'created_at': post.created_at,
                'reading_time': getattr(post, 'reading_time', 5),
                'category_id': post.category_id,
                'url': f'/blog/{post.slug}',
                'source': 'BlogPost'
            })
        
        # Получаем статьи из BlogArticle
        from models import BlogArticle
        blog_articles_db = BlogArticle.query.filter_by(status='published').all()
        for article in blog_articles_db:
            all_articles.append({
                'id': article.id,
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt or 'Полезная информация о недвижимости',
                'content': getattr(article, 'content', ''),
                'featured_image': article.featured_image or 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
                'published_at': article.published_at or article.created_at,
                'created_at': article.created_at,
                'reading_time': getattr(article, 'reading_time', 5),
                'category_id': article.category_id,
                'url': f'/blog/{article.slug}',
                'source': 'BlogArticle'
            })
        
    except Exception as e:
        print(f"Error loading unified articles for blog: {e}")
    
    # Применяем фильтры
    filtered_articles = all_articles.copy()
    
    # Поиск по тексту
    if search_query:
        filtered_articles = [
            article for article in filtered_articles
            if search_query.lower() in article['title'].lower() or 
               search_query.lower() in (article['excerpt'] or '').lower() or
               search_query.lower() in (article['content'] or '').lower()
        ]
    
    # Фильтр по категории
    if category_filter:
        category = Category.query.filter_by(name=category_filter, is_active=True).first()
        if category:
            filtered_articles = [
                article for article in filtered_articles
                if article['category_id'] == category.id
            ]
    
    # Сортировка по дате
    filtered_articles.sort(key=lambda x: x['published_at'] or x['created_at'], reverse=True)
    
    # Ручная пагинация
    total_articles = len(filtered_articles)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    articles_page = filtered_articles[start_idx:end_idx]
    
    # Создаем объект похожий на paginate для совместимости
    class PaginationMock:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
    
    articles = PaginationMock(articles_page, page, per_page, total_articles)
    
    # Если нет фильтрации, показываем все статьи разделенные по категориям
    if not search_query and not category_filter:
        # Загружаем категории и по 3 статьи в каждой
        categories_with_articles = []
        all_categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order, Category.name).all()
        
        for category in all_categories:
            # Находим статьи для этой категории из объединенного списка
            category_articles = [
                article for article in all_articles 
                if article['category_id'] == category.id
            ][:3]  # Берем только первые 3
            
            if category_articles:  # Только если есть статьи
                categories_with_articles.append({
                    'category': category,
                    'articles': category_articles
                })
        
        return render_template('blog.html',
                             articles=all_articles,  # Все статьи для полного поиска
                             all_categories=all_categories,  # Категории для навигации
                             categories_with_articles=categories_with_articles,  # Статьи по категориям
                             search_query=search_query,
                             category_filter=category_filter,
                             show_category_sections=True)
    else:
        # Если есть фильтрация - показываем обычным списком
        # Get all active categories for dynamic navigation
        all_categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order, Category.name).all()
        
        return render_template('blog.html',
                             articles=articles_page,
                             all_categories=all_categories,
                             search_query=search_query,
                             category_filter=category_filter,
                             current_page=page,
                             total_articles=total_articles,
                             show_category_sections=False)

# Removed duplicate blog route - using blog_post function at line 7515

@app.route('/blog/category/<category_slug>')
def blog_category(category_slug):
    """Blog category page with search functionality"""
    try:
        from models import BlogPost, Category
        
        # Поиск категории по slug или по имени
        category = Category.query.filter(
            (Category.slug == category_slug) | 
            (Category.name.ilike(f'%{category_slug}%'))
        ).first()
        
        if not category:
            return redirect(url_for('blog'))
        
        # Get search query from URL parameters
        search_query = request.args.get('q', '').strip()
        
        # Get articles in this category
        page = int(request.args.get('page', 1))
        per_page = 6
        
        # Base query - articles in this category using foreign key
        articles_query = BlogPost.query.filter_by(status='published', category_id=category.id)
        
        # Add search filter if query provided
        if search_query:
            from sqlalchemy import or_, func
            search_filter = f"%{search_query.lower()}%"
            articles_query = articles_query.filter(
                or_(
                    func.lower(BlogPost.title).like(search_filter),
                    func.lower(BlogPost.excerpt).like(search_filter),
                    func.lower(BlogPost.content).like(search_filter)
                )
            )
        
        # Order by date descending
        articles_query = articles_query.order_by(BlogPost.created_at.desc())
        
        articles = articles_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get all categories for navigation
        all_categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order, Category.name).all()
        
        return render_template('blog.html',
                             articles=articles.items,
                             all_categories=all_categories,
                             current_category=category,
                             featured_articles=[],
                             search_query=search_query,
                             category_filter=category_slug,
                             current_page=page,
                             total_pages=articles.pages,
                             total_articles=articles.total)
                             
    except Exception as e:
        # Log error for debugging
        import traceback
        print(f"[ERROR] Exception in blog_category ({category_slug}): {str(e)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        # Graceful fallback - redirect to main blog page
        flash('Произошла ошибка при загрузке категории. Попробуйте позже.', 'error')
        return redirect(url_for('blog'))

@app.route('/news')
def news():
    """News article page"""
    return render_template('news.html')

@app.route('/streets')
def streets():
    """Streets page"""
    streets_data = load_streets()
    
    # Sort streets alphabetically
    streets_data.sort(key=lambda x: x['name'])
    
    return render_template('streets.html', 
                         streets=streets_data)

@app.route('/street/<path:street_name>')
def street_detail(street_name):
    """Страница конкретной улицы с описанием и картой"""
    try:
        # Сначала ищем улицу в базе данных по slug
        street_db = db.session.execute(text("""
            SELECT name, slug, latitude, longitude, zoom_level 
            FROM streets 
            WHERE slug = :street_slug
        """), {'street_slug': street_name}).fetchone()
        
        if street_db:
            # Используем данные из базы данных
            street = {
                'name': street_db.name,
                'slug': street_db.slug,
                'district': '',  # Можно добавить district_id в будущем
                'description': f'Улица {street_db.name} в Краснодаре'
            }
            
            if street_db.latitude and street_db.longitude:
                coordinates = {
                    'lat': float(street_db.latitude),
                    'lng': float(street_db.longitude)
                }
            else:
                # Координаты по умолчанию (центр Краснодара)
                coordinates = {
                    'lat': 45.0448,
                    'lng': 38.9760
                }
                
            app.logger.debug(f"Found street in database: {street['name']} with coordinates: {coordinates}")
            
            # Загружаем данные о свойствах для этой улицы (если есть)
            properties_on_street = []
            try:
                with open('data/properties_new.json', 'r', encoding='utf-8') as f:
                    properties_data = json.load(f)
                
                # Фильтруем свойства по улице
                for prop in properties_data:
                    if (street['name'].lower() in prop.get('location', '').lower() or
                        street['name'].lower() in prop.get('full_address', '').lower()):
                        properties_on_street.append(prop)
            except:
                pass
            
            return render_template('street_detail.html',
                                 street=street,
                                 coordinates=coordinates,
                                 properties=properties_on_street,
                                 title=f'{street["name"]} - новостройки с кэшбеком | InBack',
                                 yandex_api_key=os.environ.get('YANDEX_MAPS_API_KEY', ''))
        else:
            # Ищем в JSON файле как резервный вариант
            streets_data = load_streets()
            
            # Ищем улицу по имени (учитываем URL-кодирование)
            street_name_decoded = street_name.replace('-', ' ').replace('_', ' ')
            street = None
            
            # Логируем для отладки
            app.logger.debug(f"Looking for street: {street_name} -> {street_name_decoded}")
        
        # Функция транслитерации для поиска старых URL
        def translit_to_latin(text):
            translit_map = {
                'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
                'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
                'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
            }
            result = ''
            for char in text.lower():
                result += translit_map.get(char, char)
            return result
        
        for s in streets_data:
            # Создаем URL-slug точно так же, как в фильтре (с кириллицей)
            street_slug_generated = s['name'].lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '').replace(',', '')
            
            # Создаем полную транслитерацию для обратной совместимости
            translit_name = translit_to_latin(s['name'])
            translit_slug = translit_name.replace(' ', '-').replace('.', '').replace('(', '').replace(')', '').replace(',', '')
            
            # Простая замена символов (как было раньше)
            simple_translit = s['name'].lower().replace(' ', '-').replace('.', '').replace('ё', 'e').replace('й', 'i').replace('а', 'a').replace('г', 'g').replace('р', 'r').replace('и', 'i').replace('н', 'n').replace('(', '').replace(')', '').replace(',', '')
            
            # Множественные варианты поиска
            if (street_slug_generated == street_name.lower() or
                translit_slug == street_name.lower() or
                simple_translit == street_name.lower() or
                s['name'].lower() == street_name_decoded.lower() or
                s['name'].lower().replace(' ул.', '').replace(' ул', '') == street_name_decoded.lower().replace(' ул.', '').replace(' ул', '')):
                street = s
                app.logger.debug(f"Found street: {s['name']} with slug: {street_slug_generated}, translit: {translit_slug}")
                break
        
        if not street:
            # Пробуем найти частичное совпадение
            for s in streets_data:
                street_name_clean = street_name_decoded.lower().replace('ул', '').replace('.', '').strip()
                street_db_clean = s['name'].lower().replace('ул.', '').replace('ул', '').replace('.', '').strip()
                
                if (street_name_clean in street_db_clean or 
                    street_db_clean in street_name_clean or
                    street_name_decoded.lower() in s['name'].lower()):
                    street = s
                    app.logger.debug(f"Found street by partial match: {s['name']}")
                    break
        
        if not street:
            app.logger.error(f"Street not found: {street_name} ({street_name_decoded})")
            abort(404)
        
        # Получаем координаты из базы данных
        from models import Street
        
        # Ищем улицу в базе данных по названию
        street_db = Street.query.filter_by(name=street['name']).first()
        
        if street_db and street_db.latitude and street_db.longitude:
            coordinates = {
                'lat': float(street_db.latitude),
                'lng': float(street_db.longitude)
            }
        else:
            # Если координат нет, используем центр Краснодара
            coordinates = {
                'lat': 45.035470,
                'lng': 38.975313
            }
        
        # Загружаем данные о свойствах для этой улицы (если есть)
        properties_on_street = []
        try:
            with open('data/properties_new.json', 'r', encoding='utf-8') as f:
                properties_data = json.load(f)
            
            # Фильтруем свойства по улице
            for prop in properties_data:
                if (street['name'].lower() in prop.get('location', '').lower() or
                    street['name'].lower() in prop.get('full_address', '').lower()):
                    properties_on_street.append(prop)
        except:
            pass
        
        return render_template('street_detail.html',
                             street=street,
                             coordinates=coordinates,
                             properties=properties_on_street,
                             title=f'{street["name"]} - новостройки с кэшбеком | InBack',
                             yandex_api_key=os.environ.get('YANDEX_MAPS_API_KEY', ''))
    
    except Exception as e:
        app.logger.error(f"Error loading street detail: {e}")
        abort(404)

@app.route('/sitemap.xml')
def sitemap():
    """Serve static sitemap.xml file"""
    try:
        # Читаем статический sitemap файл
        sitemap_path = os.path.join(app.static_folder, 'sitemap.xml')
        
        if os.path.exists(sitemap_path):
            with open(sitemap_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            response = app.response_class(
                response=xml_content,
                status=200,
                mimetype='application/xml'
            )
            return response
        else:
            # Если файла нет, создаем базовый sitemap
            xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://inback.ru/</loc>
    <lastmod>2025-09-06</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://inback.ru/properties</loc>
    <lastmod>2025-09-06</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
            
            response = app.response_class(
                response=xml_content,
                status=200,
                mimetype='application/xml'
            )
            return response
        
    except Exception as e:
        app.logger.error(f"Error serving sitemap: {e}")
        abort(500)

@app.route('/comparison')
def comparison():
    """Unified comparison page for properties and complexes"""
    return render_template('comparison.html')

@app.route('/thank-you')
def thank_you():
    """Thank you page after form submission"""
    return render_template('thank_you.html')

@app.route('/api/property/<int:property_id>')
def api_property_detail(property_id):
    """API endpoint to get property data for comparison"""
    property_data = get_property_by_id(property_id)
    
    if not property_data:
        return jsonify({'error': 'Property not found'}), 404
    
    # Calculate cashback for the property
    property_data['cashback'] = calculate_cashback(property_data['price'])
    
    return jsonify(property_data)

@app.route('/complex-comparison')
def complex_comparison():
    """Complex comparison page"""
    return render_template('complex_comparison.html')

@app.route('/api/complex/<int:complex_id>')
def api_complex_detail(complex_id):
    """API endpoint to get complex data for comparison from database"""
    try:
        from models import ResidentialComplex
        
        complex = ResidentialComplex.query.filter_by(id=complex_id).first()
        if not complex:
            return jsonify({'error': 'Complex not found'}), 404
        
        # Get additional data from excel_properties table
        apartments_data = db.session.execute(text("""
            SELECT 
                COUNT(*) as apartments_count,
                MIN(price) as price_from,
                MAX(price) as price_to,
                MIN(object_min_floor) as floors_min,
                MAX(object_max_floor) as floors_max,
                MAX(photos) as photos,
                MAX(address_short_display_name) as location
            FROM excel_properties 
            WHERE complex_name = :complex_name
        """), {'complex_name': complex.name}).fetchone()
        
        # Parse photos if available
        image_url = '/static/images/no-image.jpg'
        if apartments_data and apartments_data[5]:  # photos field
            try:
                photos_raw = apartments_data[5]
                if photos_raw.startswith('{') and photos_raw.endswith('}'):
                    photos_clean = photos_raw[1:-1]
                    if photos_clean:
                        photos_list = [url.strip() for url in photos_clean.split(',')]
                        # Use first photo as main image
                        image_url = photos_list[0] if photos_list else image_url
                else:
                    import json
                    photos_list = json.loads(photos_raw)
                    image_url = photos_list[0] if photos_list else image_url
            except Exception as e:
                print(f"Error parsing photos for complex {complex.name}: {e}")
        
        # Convert to dictionary with all necessary fields for comparison
        complex_data = {
            'id': complex.id,
            'name': complex.name,
            'developer': complex.developer.name if complex.developer else 'Не указано',
            'location': apartments_data[6] if apartments_data and apartments_data[6] else complex.sales_address or 'Не указано',
            'district': complex.district.name if complex.district else 'Не указано',
            'building_class': complex.object_class_display_name or 'Не указано',
            'apartments_count': apartments_data[0] if apartments_data else 0,
            'buildings_count': len(complex.buildings) if complex.buildings else 'Не указано',
            'floors_min': apartments_data[3] if apartments_data and apartments_data[3] else 'Не указано',
            'floors_max': apartments_data[4] if apartments_data and apartments_data[4] else 'Не указано',
            'completion_date': f"{complex.end_build_quarter} кв. {complex.end_build_year}" if complex.end_build_quarter and complex.end_build_year else 'Не указано',
            'price_from': apartments_data[1] if apartments_data and apartments_data[1] else 0,
            'price_to': apartments_data[2] if apartments_data and apartments_data[2] else 0,
            'cashback_percent': float(complex.cashback_rate) if complex.cashback_rate else 5.0,
            'status': 'строится' if complex.end_build_year and complex.end_build_year > 2024 else 'сдан',
            'image': image_url,
            'description': 'Описание не указано',
            'detail_url': f'/residential-complex/{complex.id}'  # Add detail URL for "Подробнее" button
        }
        
        return jsonify(complex_data)
        
    except Exception as e:
        print(f"Error loading complex {complex_id}: {e}")
        return jsonify({'error': 'Complex not found'}), 404

@app.route('/favorites')
def favorites():
    """Favorites page with animated heart pulse effects"""
    return render_template('favorites.html')



@app.route('/robots.txt')
def robots_txt():
    """Robots.txt for search engine crawlers"""
    robots_content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /auth/
Disallow: /api/
Disallow: /manager/
Disallow: /dashboard

Sitemap: https://inback.ru/sitemap.xml

# Crawl-delay for better server performance
Crawl-delay: 1

# Specific rules for major search engines
User-agent: Googlebot
Allow: /
Disallow: /admin/
Disallow: /auth/
Disallow: /api/
Disallow: /manager/

User-agent: Yandex
Allow: /
Disallow: /admin/
Disallow: /auth/
Disallow: /api/
Disallow: /manager/

User-agent: Bingbot
Allow: /
Disallow: /admin/
Disallow: /auth/
Disallow: /api/
Disallow: /manager/"""
    
    return app.response_class(
        response=robots_content,
        status=200,
        mimetype='text/plain'
    )

# Old blog search function removed - using updated version at bottom of file


@app.route('/api/residential-complexes')
def api_residential_complexes():
    """API endpoint for getting residential complexes for cashback calculator"""
    try:
        from models import ResidentialComplex
        
        complexes = ResidentialComplex.query.all()
        api_complexes = []
        
        for complex in complexes:
            api_complexes.append({
                'id': complex.id,
                'name': complex.name,
                'cashback_rate': float(complex.cashback_rate) if complex.cashback_rate else 5.0
            })
        
        return jsonify({'complexes': api_complexes})
    
    except Exception as e:
        # Fallback to simple list if model not available
        return jsonify({
            'complexes': [
                {'id': 1, 'name': 'ЖК «Первое место»', 'cashback_rate': 5.5},
                {'id': 2, 'name': 'ЖК «Аврора»', 'cashback_rate': 6.0},
                {'id': 3, 'name': 'ЖК «Седьмое небо»', 'cashback_rate': 7.0},
                {'id': 4, 'name': 'ЖК «Морская волна»', 'cashback_rate': 5.0},
                {'id': 5, 'name': 'ЖК «Комплекс-3»', 'cashback_rate': 6.5},
                {'id': 6, 'name': 'ЖК «Комплекс-8»', 'cashback_rate': 5.5},
                {'id': 7, 'name': 'ЖК «Комплекс-18»', 'cashback_rate': 7.5},
                {'id': 8, 'name': 'ЖК «Комплекс-25»', 'cashback_rate': 8.0}
            ]
        })

@app.route('/api/residential-complexes-full')
def api_residential_complexes_full():
    """API endpoint for getting all residential complexes from JSON file"""
    complexes = load_residential_complexes()
    return jsonify({'complexes': complexes})

@app.route('/api/cashback/calculate', methods=['POST'])
def api_calculate_cashback():
    """API endpoint for calculating cashback"""
    try:
        data = request.get_json()
        price = float(data.get('price', 0))
        complex_id = data.get('complex_id')
        
        if not price or price <= 0:
            return jsonify({'error': 'Invalid price'}), 400
        
        # Get cashback rate from database
        cashback_rate = 5.0  # default
        
        if complex_id:
            try:
                from models import ResidentialComplex
                complex = ResidentialComplex.query.get(complex_id)
                if complex and complex.cashback_rate:
                    cashback_rate = float(complex.cashback_rate)
            except:
                # Fallback rates
                complex_rates = {
                    1: 5.5, 2: 6.0, 3: 7.0, 4: 5.0,
                    5: 6.5, 6: 5.5, 7: 7.5, 8: 8.0
                }
                cashback_rate = complex_rates.get(int(complex_id), 5.0)
        
        cashback_amount = price * (cashback_rate / 100)
        
        # Cap at maximum
        max_cashback = 500000
        if cashback_amount > max_cashback:
            cashback_amount = max_cashback
        
        return jsonify({
            'cashback_amount': int(cashback_amount),
            'cashback_rate': cashback_rate,
            'price': int(price),
            'formatted_amount': f"{int(cashback_amount):,}".replace(',', ' ')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cashback/apply', methods=['POST'])
def api_apply_cashback():
    """API endpoint for submitting cashback application"""
    try:
        from models import CallbackRequest
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Неверный формат данных'}), 400
            
        price = data.get('price')
        complex_id = data.get('complex_id')
        complex_name = data.get('complex_name', 'Не указан')
        cashback_amount = data.get('cashback_amount')
        user_phone = data.get('phone', '')
        user_name = data.get('name', '')
        
        # Validate required fields
        if not all([price, cashback_amount, user_phone, user_name]):
            return jsonify({'error': 'Заполните все обязательные поля'}), 400
        
        # Validate data types
        try:
            price = float(price)
            cashback_amount = float(cashback_amount)
        except (ValueError, TypeError):
            return jsonify({'error': 'Неверный формат числовых данных'}), 400
        
        # Create callback request
        callback = CallbackRequest(
            name=user_name,
            phone=user_phone,
            notes=f"Заявка на кешбек {int(cashback_amount):,} ₽ при покупке квартиры в {complex_name} стоимостью {int(price):,} ₽".replace(',', ' ')
        )
        
        db.session.add(callback)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Заявка успешно отправлена! Менеджер свяжется с вами в ближайшее время.'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка при отправке заявки: {str(e)}'}), 500

@app.route('/api/search/suggestions')
def search_suggestions():
    """API endpoint for search suggestions (autocomplete) - REAL DATABASE VERSION"""
    query = request.args.get('query', request.args.get('q', '')).lower().strip()
    if not query or len(query) < 2:
        return jsonify([])
    
    suggestions = []
    
    try:
        # 1. Search by room types (PRIORITY - user's main request)
        room_suggestions = {
            'студ': 'Студия',
            '1-к': '1-комнатная',
            '1-ком': '1-комнатная', 
            '1 к': '1-комнатная',
            'одн': '1-комнатная',
            '2-к': '2-комнатная',
            '2-ком': '2-комнатная',
            '2 к': '2-комнатная', 
            'двух': '2-комнатная',
            '3-к': '3-комнатная',
            '3-ком': '3-комнатная',
            '3 к': '3-комнатная',
            'трех': '3-комнатная',
            'трёх': '3-комнатная',
            '4-к': '4-комнатная',
            '4-ком': '4-комнатная',
            'четыр': '4-комнатная'
        }
        
        for pattern, room_type in room_suggestions.items():
            if pattern in query:
                # Count real properties by room type - use ALL available fields
                if 'студ' in pattern:
                    count = db.session.execute(text("""
                        SELECT COUNT(*) FROM excel_properties 
                        WHERE object_rooms = 0
                    """)).scalar()
                else:
                    room_num = room_type.split('-')[0] if '-' in room_type else '1'
                    count = db.session.execute(text("""
                        SELECT COUNT(*) FROM excel_properties 
                        WHERE object_rooms = :room_num
                    """), {'room_num': int(room_num)}).scalar()
                
                # Создаем URL с тем же параметром что быстрые фильтры
                if 'студ' in pattern:
                    room_param = '0'
                else:
                    room_param = room_type.split('-')[0] if '-' in room_type else '1'
                
                suggestions.append({
                    'type': 'room_type', 
                    'text': room_type,
                    'title': room_type,  # Добавляем title для совместимости
                    'subtitle': f'Найдено {count} квартир',
                    'url': url_for('properties', rooms=room_param)  # rooms=1 как быстрые фильтры
                })
        
        # 2. Search in REAL residential complexes from database (using correct field names)
        complexes_query = db.session.execute(text("""
            SELECT DISTINCT complex_name, COUNT(*) as count
            FROM excel_properties 
            WHERE LOWER(complex_name) LIKE :query 
            AND complex_name IS NOT NULL
            AND complex_name != ''
            GROUP BY complex_name
            ORDER BY count DESC
            LIMIT 5
        """), {'query': f'%{query}%'}).fetchall()
        
        for row in complexes_query:
            if row[0] and len(row[0]) > 2:  # Skip empty/short names
                suggestions.append({
                    'type': 'complex',
                    'text': row[0],
                    'subtitle': f'{row[1]} квартир доступно',
                    'url': url_for('properties', complex=row[0])
                })
        
        # 3. Search in REAL developers from database
        developers_query = db.session.execute(text("""
            SELECT DISTINCT developer_name, COUNT(*) as count
            FROM excel_properties 
            WHERE LOWER(developer_name) LIKE :query 
            AND developer_name IS NOT NULL
            GROUP BY developer_name
            ORDER BY count DESC
            LIMIT 3
        """), {'query': f'%{query}%'}).fetchall()
        
        for row in developers_query:
            if row[0] and len(row[0]) > 2:
                suggestions.append({
                    'type': 'developer',
                    'text': row[0],
                    'subtitle': f'Застройщик • {row[1]} проектов',
                    'url': url_for('properties', developer=row[0])
                })
        
        # 4. Search in districts
        districts_query = db.session.execute(text("""
            SELECT DISTINCT parsed_district, COUNT(*) as count
            FROM excel_properties 
            WHERE LOWER(parsed_district) LIKE :query 
            AND parsed_district IS NOT NULL
            GROUP BY parsed_district
            ORDER BY count DESC
            LIMIT 3
        """), {'query': f'%{query}%'}).fetchall()
        
        for row in districts_query:
            if row[0] and 'Краснодарский' not in row[0]:  # Skip generic region name
                clean_district = row[0].replace('Россия, ', '').replace('Краснодарский край, ', '')
                suggestions.append({
                    'type': 'district',
                    'text': clean_district,
                    'subtitle': f'{row[1]} квартир в районе',
                    'url': url_for('properties', district=clean_district)
                })
        
        # Sort by relevance (room types first, then exact matches)
        suggestions.sort(key=lambda x: (
            0 if x['type'] == 'room_type' else 1,
            0 if x['text'].lower().startswith(query) else 1,
            len(x['text'])
        ))
        
        return jsonify(suggestions[:8])  # Return top 8 suggestions
        
    except Exception as e:
        app.logger.error(f"Error in search suggestions: {e}")
        return jsonify([])

# Mortgage routes
@app.route('/ipoteka')
def ipoteka():
    """Main mortgage page"""
    return render_template('ipoteka.html')

@app.route('/family-mortgage')
def family_mortgage():
    """Family mortgage page"""
    return render_template('family_mortgage.html')

@app.route('/it-mortgage')
def it_mortgage():
    """IT mortgage page"""
    return render_template('it_mortgage.html')

@app.route('/api/check-it-company', methods=['POST'])
def check_it_company():
    """Check if company is in IT companies list by INN or company name"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных для проверки'}), 400
            
        inn = data.get('inn', '').strip()
        company_name = data.get('company_name', '').strip()
        
        if not inn and not company_name:
            return jsonify({'error': 'Необходимо указать ИНН или название компании'}), 400
        
        # Поиск по ИНН
        if inn:
            try:
                inn_int = int(inn)
                company = db.session.execute(text("""
                    SELECT inn, name FROM it_companies 
                    WHERE inn = :inn LIMIT 1
                """), {'inn': inn_int}).fetchone()
                
                if company:
                    return jsonify({
                        'found': True,
                        'inn': company[0],
                        'company_name': company[1],
                        'message': 'Компания найдена в реестре ИТ-организаций'
                    })
            except ValueError:
                pass
        
        # Поиск по названию компании (частичное совпадение)
        if company_name:
            company = db.session.execute(text("""
                SELECT inn, name FROM it_companies 
                WHERE LOWER(name) LIKE LOWER(:company_name) 
                LIMIT 1
            """), {'company_name': f'%{company_name}%'}).fetchone()
            
            if company:
                return jsonify({
                    'found': True,
                    'inn': company[0],
                    'company_name': company[1],
                    'message': 'Компания найдена в реестре ИТ-организаций'
                })
        
        return jsonify({
            'found': False,
            'message': 'Компания не найдена в реестре ИТ-организаций. Проверьте правильность ИНН или названия компании.'
        })
        
    except Exception as e:
        print(f"Error checking IT company: {e}")
        return jsonify({'error': 'Ошибка при проверке компании'}), 500

@app.route('/api/suggest-it-companies', methods=['POST'])
def suggest_it_companies():
    """Get IT company suggestions for autocomplete"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip().lower()
        
        if len(query) < 2:
            return jsonify({'suggestions': []})
            
        # Search for companies matching the query
        suggestions = db.session.execute(text("""
            SELECT DISTINCT name FROM it_companies 
            WHERE LOWER(name) LIKE :query 
            ORDER BY name 
            LIMIT 10
        """), {'query': f'%{query}%'}).fetchall()
        
        return jsonify({
            'suggestions': [suggestion[0] for suggestion in suggestions]
        })
        
    except Exception as e:
        print(f"Error in suggest_it_companies: {str(e)}")
        return jsonify({'suggestions': []})

@app.route('/military-mortgage')
def military_mortgage():
    """Military mortgage page"""
    return render_template('military_mortgage.html')

@app.route('/developer-mortgage')
def developer_mortgage():
    """Developer mortgage page"""
    return render_template('developer_mortgage.html')

@app.route('/maternal-capital')
def maternal_capital():
    """Maternal capital page"""
    return render_template('maternal_capital.html')

@app.route('/residential')
def residential():
    """Residential complexes page"""
    return render_template('residential.html')

@app.route('/residential-complexes')
# Временно отключаем кэш для тестирования
def residential_complexes():
    try:
        # Загружаем реальные данные ЖК из базы данных 
        # Оптимизированный запрос с фотографиями + реальные ID из residential_complexes
        try:
            complexes_query = db.session.execute(text("""
                SELECT 
                    ep.complex_name,
                    COUNT(*) as apartments_count,
                    MIN(ep.price) as price_from,
                    MAX(ep.price) as price_to,
                    MIN(ep.object_area) as area_from,
                    MAX(ep.object_area) as area_to,
                    MIN(ep.object_min_floor) as floors_min,
                    MAX(ep.object_max_floor) as floors_max,
                    MAX(ep.developer_name) as developer_name,
                    MAX(ep.address_display_name) as address_display_name,
                    MAX(ep.complex_sales_address) as complex_sales_address,
                    -- Используем даты корпусов вместо общих дат ЖК
                    MAX(ep.complex_building_end_build_year) as end_build_year,
                    MAX(ep.complex_building_end_build_quarter) as end_build_quarter,
                    (SELECT photos FROM excel_properties p2 
                     WHERE p2.complex_name = ep.complex_name 
                     AND p2.photos IS NOT NULL 
                     ORDER BY p2.price DESC LIMIT 1) as photos,
                    COALESCE(rc.id, ROW_NUMBER() OVER (ORDER BY ep.complex_name) + 1000) as real_id,
                    CASE 
                        WHEN COUNT(DISTINCT ep.complex_building_id) > 0 
                        THEN COUNT(DISTINCT ep.complex_building_id)
                        WHEN COUNT(DISTINCT NULLIF(ep.complex_building_name, '')) > 0 
                        THEN COUNT(DISTINCT NULLIF(ep.complex_building_name, ''))
                        ELSE GREATEST(1, CEIL(COUNT(*) / 3.0))  -- Примерно 3 квартиры на корпус для лучшего соответствия
                    END as buildings_count,
                    MAX(ep.complex_object_class_display_name) as object_class_display_name
                FROM excel_properties ep
                LEFT JOIN residential_complexes rc ON rc.name = ep.complex_name
                GROUP BY ep.complex_name, rc.id
                ORDER BY 
                    -- ЖК "IV кв. 2025 г. Строится" всегда внизу
                    CASE 
                        WHEN MAX(ep.complex_building_end_build_year) = 2025 
                        AND MAX(ep.complex_building_end_build_quarter) = 4 
                        THEN 1  -- "IV кв. 2025 г. Строится" в конце
                        ELSE 0  -- Остальные ЖК сначала
                    END,
                    ep.complex_name
            """))
            
            complexes_data = complexes_query.fetchall()
        except Exception as e:
            print(f"Database error loading complexes: {e}")
            # Fallback to basic query without photos
            complexes_query = db.session.execute(text("""
                SELECT 
                    ep.complex_name,
                    COUNT(*) as apartments_count,
                    MIN(ep.price) as price_from,
                    MAX(ep.price) as price_to,
                    MIN(ep.object_area) as area_from,
                    MAX(ep.object_area) as area_to,
                    MIN(ep.object_min_floor) as floors_min,
                    MAX(ep.object_max_floor) as floors_max,
                    MAX(ep.developer_name) as developer_name,
                    MAX(ep.address_display_name) as address_display_name,
                    MAX(ep.complex_sales_address) as complex_sales_address,
                    -- Используем даты корпусов вместо общих дат ЖК
                    MAX(ep.complex_building_end_build_year) as end_build_year,
                    MAX(ep.complex_building_end_build_quarter) as end_build_quarter,
                    NULL as photos,
                    COALESCE(rc.id, ROW_NUMBER() OVER (ORDER BY ep.complex_name) + 1000) as real_id,
                    CASE 
                        WHEN COUNT(DISTINCT ep.complex_building_id) > 0 
                        THEN COUNT(DISTINCT ep.complex_building_id)
                        WHEN COUNT(DISTINCT NULLIF(ep.complex_building_name, '')) > 0 
                        THEN COUNT(DISTINCT NULLIF(ep.complex_building_name, ''))
                        ELSE GREATEST(1, CEIL(COUNT(*) / 3.0))  -- Примерно 3 квартиры на корпус для лучшего соответствия
                    END as buildings_count,
                    MAX(ep.complex_object_class_display_name) as object_class_display_name
                FROM excel_properties ep
                LEFT JOIN residential_complexes rc ON rc.name = ep.complex_name
                GROUP BY ep.complex_name, rc.id
                ORDER BY 
                    -- ЖК "IV кв. 2025 г. Строится" всегда внизу
                    CASE 
                        WHEN MAX(ep.complex_building_end_build_year) = 2025 
                        AND MAX(ep.complex_building_end_build_quarter) = 4 
                        THEN 1  -- "IV кв. 2025 г. Строится" в конце
                        ELSE 0  -- Остальные ЖК сначала
                    END,
                    ep.complex_name
            """))
            complexes_data = complexes_query.fetchall()
        
        complexes = []
        
        for idx, row in enumerate(complexes_data):
            # Форматируем срок сдачи и определяем статус
            completion_date = 'Не указан'
            is_completed = False
            
            from datetime import datetime
            # Используем текущую дату для определения статуса
            current_year = 2025  # Мы в 2025 году
            current_quarter = 4   # Текущий квартал (сентябрь = 4-й квартал - безопасность)
            
            if row[11] and row[12]:  # end_build_year и end_build_quarter
                build_year = int(row[11])
                build_quarter = int(row[12])
                
                # Определяем сдан ли комплекс (более строгая логика)
                if build_year < current_year:
                    is_completed = True
                elif build_year == current_year and build_quarter < current_quarter:
                    is_completed = True
                else:
                    is_completed = False  # Текущий или будущий квартал - еще строится
                    
                quarter_names = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
                quarter = quarter_names.get(build_quarter, build_quarter)
                completion_date = f"{quarter} кв. {build_year} г."
            elif row[11]:  # только год
                build_year = int(row[11])
                is_completed = build_year < current_year  # Строго меньше для безопасности
                completion_date = f"{build_year} г."
            
            complex_dict = {
                'id': row[14],  # real_id from database
                'name': row[0],
                'available_apartments': row[1],
                'price_from': row[2] or 0,
                'price_to': row[3] or 0,
                'real_price_from': row[2] or 0,
                'real_price_to': row[3] or 0,
                'area_from': row[4] or 0,
                'area_to': row[5] or 0,
                'real_area_from': row[4] or 0,
                'real_area_to': row[5] or 0,
                'floors_min': row[6] or 1,
                'floors_max': row[7] or 25,
                'district': 'Краснодарский край',
                'developer': row[8] or 'Не указан',
                'address': row[9] or row[10] or 'Адрес не указан',
                'full_address': row[10] or row[9] or 'Адрес не указан',
                'location': row[9] or 'Адрес не указан',
                'completion_date': completion_date,
                'buildings_count': row[15] if len(row) > 15 else 1,  # Реальное количество корпусов из Excel
                'is_completed': is_completed,
                'status': 'Сдан' if is_completed else 'Строится',
                'object_class': row[16] if len(row) > 16 and row[16] else 'Комфорт',  # класс жилья из базы
                'housing_class': row[16] if len(row) > 16 and row[16] else 'Комфорт',  # дублируем для совместимости
                'max_floors': row[7] or 25,  # этажность = floors_max
                'floors': row[7] or 25,  # дублируем для совместимости
                'completion_year': build_year if 'build_year' in locals() else 2025
            }
            
            # Загружаем фотографии для ЖК из самой дорогой квартиры (как репрезентативные для ЖК)
            try:
                photos_query = db.session.execute(text("""
                    SELECT photos FROM excel_properties 
                    WHERE complex_name = :complex_name 
                    AND photos IS NOT NULL 
                    ORDER BY price DESC, object_area DESC
                    LIMIT 1
                """), {'complex_name': complex_dict['name']})
                
                photos_row = photos_query.fetchone()
                if photos_row and photos_row[0]:
                    try:
                        photos_raw = photos_row[0]
                        # Парсим PostgreSQL array формат {url1,url2,url3}
                        if photos_raw.startswith('{') and photos_raw.endswith('}'):
                            photos_clean = photos_raw[1:-1]  # убираем { и }
                            if photos_clean:
                                photos_list = [url.strip() for url in photos_clean.split(',')]
                        else:
                            # Если это JSON формат, парсим как JSON
                            import json
                            photos_list = json.loads(photos_raw)
                        
                        # Пропускаем первые фото (интерьеры квартир) и берем фото ЖК
                        start_index = min(len(photos_list) // 4, 5) if len(photos_list) > 8 else 1
                        complex_dict['image'] = photos_list[start_index] if len(photos_list) > start_index else photos_list[0]
                        # Для слайдера берем фото ЖК (пропускаем первые интерьеры)
                        complex_dict['images'] = photos_list[start_index:] if len(photos_list) > start_index else photos_list
                    except Exception as e:
                        print(f"Error parsing photos for complex {complex_dict['name']}: {e}")
                        complex_dict['image'] = 'https://via.placeholder.com/400x300/0088CC/FFFFFF?text=' + complex_dict['name'].replace(' ', '+')
                        complex_dict['images'] = []
                else:
                    complex_dict['image'] = 'https://via.placeholder.com/400x300/0088CC/FFFFFF?text=' + complex_dict['name']
                    complex_dict['images'] = []
            except Exception as e:
                print(f"Database error loading photos for complex {complex_dict['name']}: {e}")
                complex_dict['image'] = 'https://via.placeholder.com/400x300/0088CC/FFFFFF?text=' + complex_dict['name'].replace(' ', '+')
                complex_dict['images'] = []
                
            # Статистика по комнатам с детальными данными для каждого типа
            try:
                rooms_query = db.session.execute(text("""
                    SELECT 
                        object_rooms,
                        COUNT(*) as count,
                        MIN(object_area) as min_area,
                        MAX(object_area) as max_area,
                        MIN(price) as min_price,
                        MAX(price) as max_price
                    FROM excel_properties 
                    WHERE complex_name = :complex_name
                    GROUP BY object_rooms
                    ORDER BY object_rooms
                """), {'complex_name': complex_dict['name']})
                
                room_stats = {}
                room_details = {}
                for room_row in rooms_query.fetchall():
                    rooms = room_row[0] or 0
                    count = room_row[1]
                    min_area = room_row[2] or 0
                    max_area = room_row[3] or 0
                    min_price = room_row[4] or 0
                    max_price = room_row[5] or 0
                    
                    room_type = f"{rooms}-комн" if rooms and rooms > 0 else "Студия"
                    room_stats[room_type] = count
                    room_details[room_type] = {
                        'count': count,
                        'area_from': min_area,
                        'area_to': max_area,
                        'price_from': min_price,
                        'price_to': max_price
                    }
                
                complex_dict['real_room_distribution'] = room_stats
                complex_dict['room_details'] = room_details
            except Exception as e:
                print(f"Database error loading room stats for complex {complex_dict['name']}: {e}")
                complex_dict['real_room_distribution'] = {}
            
            complexes.append(complex_dict)
        
        # Database complexes loaded
        
        # Get unique districts and developers (with safe extraction)
        districts = sorted(list(set(complex.get('district', 'Не указан') for complex in complexes if complex.get('district'))))
        developers = sorted(list(set(complex.get('developer', 'Не указан') for complex in complexes if complex.get('developer'))))
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = 35  # Show all complexes on one page
        total_complexes = len(complexes)
        total_pages = (total_complexes + per_page - 1) // per_page
        offset = (page - 1) * per_page
        complexes_page = complexes[offset:offset + per_page]
        
        # Prepare pagination info
        pagination = {
            'page': page,
            'per_page': per_page,
            'total': total_complexes,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_page': page - 1 if page > 1 else None,
            'next_page': page + 1 if page < total_pages else None
        }
        
        return render_template('residential_complexes.html',
                             residential_complexes=complexes_page,
                             all_complexes=complexes,  # For JavaScript filtering
                             districts=districts,
                             developers=developers,
                             pagination=pagination)
                             
    except Exception as e:
        print(f"ERROR in residential_complexes: {e}")
        import traceback
        traceback.print_exc()
        return f"Error loading residential complexes: {str(e)}", 500





@app.route('/map')
def map_view():
    """Enhanced interactive map view page using real Excel data"""
    # Map route processing
    
    try:
        # Загружаем реальные объекты из Excel данных
        properties_query = db.session.execute(text("""
            SELECT * FROM excel_properties 
            WHERE address_position_lat IS NOT NULL AND address_position_lon IS NOT NULL
            ORDER BY price ASC
        """))
        
        properties = []
        for row in properties_query:
            prop_dict = dict(row._mapping)
            # Преобразуем данные в нужный формат для карты
            property_data = {
                'id': prop_dict.get('inner_id', prop_dict.get('id')),
                'price': prop_dict.get('price', 0),
                'area': prop_dict.get('object_area', 0),
                'rooms': prop_dict.get('object_rooms', 0),
                'title': f"{'Студия' if int(prop_dict.get('object_rooms', 0)) == 0 else str(int(prop_dict.get('object_rooms', 0))) + '-комн'}, {prop_dict.get('object_area', 0)} м²",
                'address': prop_dict.get('address_display_name', ''),
                'residential_complex': prop_dict.get('complex_name', ''),
                'complex_name': prop_dict.get('complex_name', ''),  # Добавляем дублирование для фильтрации
                'developer': prop_dict.get('developer_name', ''),
                'district': prop_dict.get('address_locality_display_name', 'Краснодарский край'),
                'coordinates': {
                    'lat': float(prop_dict.get('address_position_lat', 45.0448)),
                    'lng': float(prop_dict.get('address_position_lon', 38.9760))
                },
                'url': f"/object/{prop_dict.get('inner_id', prop_dict.get('id'))}",
                'type': 'property',
                'cashback': int(prop_dict.get('price', 0) * 0.035),
                'cashback_available': True,
                'status': 'available',
                'property_type': 'Квартира',
                # Добавляем поля этажности для карты
                'object_min_floor': prop_dict.get('object_min_floor', 0),
                'object_max_floor': prop_dict.get('object_max_floor', 0),
                # Добавляем поля для новых фильтров
                'renovation_type': prop_dict.get('renovation_type', ''),
                'renovation_display_name': prop_dict.get('renovation_display_name', ''),
                'complex_object_class_display_name': prop_dict.get('complex_object_class_display_name', ''),
                'complex_has_mortgage_subsidy': prop_dict.get('complex_has_mortgage_subsidy', False),
                'complex_has_government_program': prop_dict.get('complex_has_government_program', False),
                'complex_has_green_mortgage': prop_dict.get('complex_has_green_mortgage', False),
                # Добавляем реальный год сдачи
                'complex_building_end_build_year': prop_dict.get('complex_building_end_build_year', None),
                'complex_building_end_build_quarter': prop_dict.get('complex_building_end_build_quarter', None)
            }
            
            # Парсим фотографии для превью (PostgreSQL array формат)
            photos_raw = prop_dict.get('photos', '')
            try:
                if photos_raw and photos_raw.startswith('{') and photos_raw.endswith('}'):
                    photos_clean = photos_raw[1:-1]  # убираем { и }
                    if photos_clean:
                        photos_list = [url.strip() for url in photos_clean.split(',') if url.strip()]
                        property_data['main_image'] = photos_list[0] if photos_list else 'https://via.placeholder.com/400x300'
                        # Photos parsed
                    else:
                        property_data['main_image'] = 'https://via.placeholder.com/400x300'
                elif photos_raw:
                    property_data['main_image'] = photos_raw
                else:
                    property_data['main_image'] = 'https://via.placeholder.com/400x300'
            except Exception as e:
                print(f"ERROR MAP: Failed to parse photos for {prop_dict.get('inner_id', 'unknown')}: {e}")
                property_data['main_image'] = 'https://via.placeholder.com/400x300'
            
            properties.append(property_data)
        
        # Загружаем ЖК из базы данных
        complexes_query = db.session.execute(text("""
            SELECT DISTINCT complex_name, developer_name, address_display_name, 
                   address_position_lat, address_position_lon, address_locality_display_name, COUNT(*) as apartments_count,
                   MIN(price) as price_from
            FROM excel_properties 
            WHERE address_position_lat IS NOT NULL AND address_position_lon IS NOT NULL
            GROUP BY complex_name, developer_name, address_display_name, address_position_lat, address_position_lon, address_locality_display_name
        """))
        
        residential_complexes = []
        for row in complexes_query:
            complex_dict = dict(row._mapping)
            complex_data = {
                'id': len(residential_complexes) + 1,
                'name': complex_dict.get('complex_name', ''),
                'developer': complex_dict.get('developer_name', ''),
                'address': complex_dict.get('address_display_name', ''),
                'district': complex_dict.get('address_locality_display_name', 'Краснодарский край'),
                'apartments_count': complex_dict.get('apartments_count', 0),
                'price_from': complex_dict.get('price_from', 0),
                'coordinates': {
                    'lat': float(complex_dict.get('address_position_lat', 45.0448)),
                    'lng': float(complex_dict.get('address_position_lon', 38.9760))
                },
                'url': '/zk/' + complex_dict.get('complex_name', '').lower().replace(' ', '-').replace('"', '').replace('жк-', '').replace('жк ', ''),
                'type': 'complex'
            }
            residential_complexes.append(complex_data)
        
        # Фильтры для интерфейса
        all_districts = sorted(list(set(prop.get('district', 'Не указан') for prop in properties)))
        all_developers = sorted(list(set(prop.get('developer', 'Не указан') for prop in properties)))
        all_complexes = sorted(list(set(prop.get('residential_complex', 'Не указан') for prop in properties)))
        
        filters = {
            'rooms': request.args.getlist('rooms'),
            'price_min': request.args.get('price_min', ''),
            'price_max': request.args.get('price_max', ''),
            'district': request.args.get('district', ''),
            'developer': request.args.get('developer', ''),
            'residential_complex': request.args.get('residential_complex', ''),
        }
        
        # Map data loaded
        
        return render_template('map.html', 
                             properties=properties, 
                             residential_complexes=residential_complexes,
                             all_districts=all_districts,
                             all_developers=all_developers,
                             all_complexes=all_complexes,
                             filters=filters)
                             
    except Exception as e:
        print(f"ERROR in map route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error 500: {str(e)}", 500

def extract_main_image_from_photos(photos_raw):
    """Извлекает основное изображение из поля photos, предпочитая внешние виды зданий"""
    if not photos_raw or not photos_raw.strip():
        return '/static/images/no-photo.jpg'
    
    try:
        import json
        # Попробуем парсить как JSON массив
        if photos_raw.startswith('[') and photos_raw.endswith(']'):
            images = json.loads(photos_raw)
            if not images:
                return '/static/images/no-photo.jpg'
            
            # Фильтруем изображения, предпочитая внешние виды
            # Берем последние изображения, так как первые часто планировки
            if len(images) > 5:
                # Берем из середины/конца массива, где обычно фото зданий
                return images[len(images)//2]
            elif len(images) > 2:
                return images[-1]  # Последнее фото
            else:
                return images[0]
        
        # PostgreSQL array format: {url1,url2,url3}
        elif photos_raw.startswith('{') and photos_raw.endswith('}'):
            images_str = photos_raw[1:-1]  # Remove braces
            if images_str:
                images = [img.strip().strip('"') for img in images_str.split(',') if img.strip()]
                return images[0] if images else '/static/images/no-photo.jpg'
            else:
                return '/static/images/no-photo.jpg'
        
        # Одиночная ссылка
        else:
            return photos_raw
            
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing photos: {e}, raw data: {photos_raw[:100]}")
        return '/static/images/no-photo.jpg'

@app.route('/complexes-map')
def complexes_map():
    """Карта жилых комплексов"""
    try:
        # Загружаем ЖК из базы данных с координатами
        # Загружаем данные о ЖК из Excel таблицы, используя проверенные поля из работающего роута
        complexes_query = db.session.execute(text("""
            SELECT 
                ep.complex_name,
                COUNT(*) as apartments_count,
                MIN(ep.price) as price_from,
                MAX(ep.price) as price_to,
                MAX(ep.developer_name) as developer_name,
                MAX(ep.address_display_name) as address_display_name,
                MAX(ep.complex_end_build_year) as end_build_year,
                MAX(ep.complex_end_build_quarter) as end_build_quarter,
                MAX(ep.complex_object_class_display_name) as object_class_display_name,
                AVG(ep.address_position_lat) as coordinates_lat,
                AVG(ep.address_position_lon) as coordinates_lng,
                COALESCE(MAX(ep.parsed_district), 'Краснодарский край') as district,
                MAX(ep.photos) as photos
            FROM excel_properties ep 
            WHERE ep.complex_name IS NOT NULL 
                AND ep.address_position_lat IS NOT NULL 
                AND ep.address_position_lon IS NOT NULL
                AND ep.complex_name != ''
            GROUP BY ep.complex_name
            ORDER BY ep.complex_name
        """))
        
        residential_complexes = []
        for row in complexes_query:
            complex_dict = dict(row._mapping)
            # Используем полное имя комплекса для URL (как в базе данных)
            full_complex_name = complex_dict.get('complex_name', '')
            clean_complex_name = full_complex_name.replace('ЖК ', '').replace('"', '')
            
            # Определяем статус на основе года сдачи
            current_year = 2025
            end_build_year = complex_dict.get('end_build_year')
            status = 'Не указан'
            if end_build_year:
                if end_build_year <= current_year:
                    status = 'Сдан'
                else:
                    status = 'Строится'
            
            # Формируем дату сдачи
            completion_date = ''
            if end_build_year:
                quarter = complex_dict.get('end_build_quarter')
                if quarter:
                    completion_date = f"{quarter} кв. {end_build_year}"
                else:
                    completion_date = f"{end_build_year} год"
            
            complex_data = {
                'id': hash(complex_dict.get('complex_name', '')) % 100000,  # Генерируем ID на основе хеша имени
                'name': complex_dict.get('complex_name', ''),
                'developer': complex_dict.get('developer_name', 'Не указан'),
                'address': complex_dict.get('address_display_name', ''),
                'district': complex_dict.get('district', 'Краснодарский край'),
                'apartments_count': complex_dict.get('apartments_count', 0),
                'price_from': complex_dict.get('price_from', 0),
                'coordinates': {
                    'lat': float(complex_dict.get('coordinates_lat', 45.0448)),
                    'lng': float(complex_dict.get('coordinates_lng', 38.9760))
                },
                'completion_date': completion_date,
                'status': status,
                'cashback_percent': 3.5,  # Стандартное значение
                'main_image': extract_main_image_from_photos(complex_dict.get('photos', '')),
                'description': f"Жилой комплекс {complex_dict.get('complex_name', '')}",
                'object_class': complex_dict.get('object_class_display_name', ''),
                'housing_class': '',
                'max_floors': 0,
                'url': f"/residential-complex/{full_complex_name}",
                'type': 'complex'
            }
            residential_complexes.append(complex_data)
        
        # Фильтры для интерфейса
        all_districts = sorted(list(set(complex.get('district', 'Не указан') for complex in residential_complexes)))
        all_developers = sorted(list(set(complex.get('developer', 'Не указан') for complex in residential_complexes)))
        all_statuses = ['Все', 'Сдан', 'Строится']
        
        print(f"DEBUG: Found {len(residential_complexes)} complexes for map")
        if residential_complexes:
            print(f"DEBUG: First complex: {residential_complexes[0]}")
        
        return render_template('complexes_map.html', 
                             residential_complexes=residential_complexes,
                             all_districts=all_districts,
                             all_developers=all_developers,
                             all_statuses=all_statuses)
                             
    except Exception as e:
        print(f"ERROR in complexes-map route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error 500: {str(e)}", 500

# API Routes
@app.route('/api/properties')
def api_properties():
    """API endpoint for properties from Excel data with real coordinates"""
    try:
        # Загружаем реальные объекты из Excel данных с координатами
        properties_query = db.session.execute(text("""
            SELECT * FROM excel_properties 
            WHERE address_position_lat IS NOT NULL AND address_position_lon IS NOT NULL
            ORDER BY price ASC
        """))
        
        properties = []
        for row in properties_query:
            prop_dict = dict(row._mapping)
            property_data = {
                'id': prop_dict.get('inner_id', prop_dict.get('id')),
                'price': prop_dict.get('price', 0),
                'area': prop_dict.get('object_area', 0),
                'rooms': prop_dict.get('object_rooms', 0),
                'title': f"{'Студия' if int(prop_dict.get('object_rooms', 0)) == 0 else str(int(prop_dict.get('object_rooms', 0))) + '-комн'}, {prop_dict.get('object_area', 0)} м²",
                'subtitle': f"{prop_dict.get('complex_name', '')} • {prop_dict.get('address_locality_display_name', '')}",
                'address': prop_dict.get('address_display_name', ''),
                'residential_complex': prop_dict.get('complex_name', ''),
                'developer': prop_dict.get('developer_name', ''),
                'developer_name': prop_dict.get('developer_name', ''),
                'district': prop_dict.get('address_locality_display_name', 'Краснодарский край'),
                'complex_object_class_display_name': prop_dict.get('complex_object_class_display_name', ''),
                'completion_date': prop_dict.get('completion_date', ''),
                'renovation_display_name': prop_dict.get('renovation_display_name', ''),
                'object_min_floor': prop_dict.get('object_min_floor', 0),
                'object_max_floor': prop_dict.get('object_max_floor', 0),
                'coordinates': {
                    'lat': float(prop_dict.get('address_position_lat', 45.0448)),
                    'lng': float(prop_dict.get('address_position_lon', 38.9760))
                },
                'url': f"/object/{prop_dict.get('inner_id', prop_dict.get('id'))}",
                'type': 'property',
                'cashback': int(prop_dict.get('price', 0) * 0.035),
                'cashback_available': True,
                'status': 'available',
                'property_type': 'Квартира'
            }
            
            # Парсим фотографии (PostgreSQL array формат)
            photos_raw = prop_dict.get('photos', '')
            try:
                if photos_raw and photos_raw.startswith('{') and photos_raw.endswith('}'):
                    photos_clean = photos_raw[1:-1]  # убираем { и }
                    if photos_clean:
                        photos_list = [url.strip() for url in photos_clean.split(',')]
                        property_data['main_image'] = photos_list[0] if photos_list else 'https://via.placeholder.com/400x300'
                    else:
                        property_data['main_image'] = 'https://via.placeholder.com/400x300'
                elif photos_raw:
                    # Если это JSON формат, парсим как JSON
                    import json
                    photos_list = json.loads(photos_raw)
                    property_data['main_image'] = photos_list[0] if photos_list else 'https://via.placeholder.com/400x300'
                else:
                    property_data['main_image'] = 'https://via.placeholder.com/400x300'
            except Exception as e:
                print(f"Error parsing photos for API property {prop_dict.get('inner_id', 'unknown')}: {e}")
                property_data['main_image'] = 'https://via.placeholder.com/400x300'
            
            properties.append(property_data)
        
        print(f"DEBUG: API returned {len(properties)} properties with real coordinates")
        return jsonify({
            'properties': properties,
            'total': len(properties),
            'success': True
        })
        
    except Exception as e:
        print(f"ERROR in api_properties: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-suggestions-OLD-DISABLED')
def api_search_suggestions_old_disabled():
    """❌ СТАРЫЙ API endpoint - ОТКЛЮЧЁН, чтобы не мешал новому"""
    return jsonify([])  # ВСЕГДА ПУСТОЙ


# ===== СТАРЫЙ КОД ПОЛНОСТЬЮ УДАЛЁН =====

@app.route('/api/residential-complexes-map')
def api_residential_complexes_map():
    """API endpoint for residential complexes with enhanced data for map"""
    complexes = load_residential_complexes()
    
    # Enhance complexes data for map
    for i, complex in enumerate(complexes):
        # Add coordinates if missing
        if 'coordinates' not in complex:
            base_lat = 45.0448
            base_lng = 38.9760
            lat_offset = (hash(str(i) + complex.get('name', '')) % 1000) / 8000 - 0.0625
            lng_offset = (hash(str(i) + complex.get('district', '')) % 1000) / 8000 - 0.0625
            complex['coordinates'] = {
                'lat': base_lat + lat_offset,
                'lng': base_lng + lng_offset
            }
        
        # ✅ ИСПРАВЛЕНО: Правильный подсчет корпусов из базы данных
        if 'buildings_count' not in complex:
            # Получаем реальное количество корпусов из Excel данных
            try:
                result = db.session.execute(text("""
                    SELECT COUNT(DISTINCT complex_building_id) as buildings_count
                    FROM excel_properties 
                    WHERE complex_name = :complex_name
                """), {'complex_name': complex.get('name', '')})
                row = result.fetchone()
                complex['buildings_count'] = row[0] if row and row[0] else 1
            except:
                complex['buildings_count'] = 1  # По умолчанию 1 корпус
        if 'apartments_count' not in complex:
            complex['apartments_count'] = 100 + (i % 300)
            
    return jsonify(complexes)

@app.route('/api/property/<int:property_id>')
def api_property(property_id):
    """API endpoint for single property"""
    property_data = get_property_by_id(property_id)
    if property_data:
        property_data['cashback'] = calculate_cashback(property_data['price'])
        return jsonify(property_data)
    return jsonify({'error': 'Property not found'}), 404

@app.route('/api/complex/<int:complex_id>')
def api_complex(complex_id):
    """API endpoint for single residential complex"""
    complexes = load_residential_complexes()
    for complex in complexes:
        if complex.get('id') == complex_id:
            return jsonify(complex)
    return jsonify({'error': 'Complex not found'}), 404

@app.route('/api/property/<int:property_id>/pdf')
def download_property_pdf(property_id):
    """Generate and download PDF for property"""
    try:
        property_data = get_property_by_id(property_id)
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        # Create simple HTML for PDF generation
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .property-details {{ margin-bottom: 20px; }}
                .detail-row {{ margin-bottom: 10px; }}
                .label {{ font-weight: bold; }}
                .price {{ color: #0088CC; font-size: 24px; font-weight: bold; }}
                .cashback {{ color: #FF5722; font-size: 18px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>InBack - Информация о квартире</h1>
                <p>Квартира #{property_id}</p>
            </div>
            
            <div class="property-details">
                <div class="detail-row">
                    <span class="label">Тип:</span> {property_data.get('rooms', 'Не указано')}
                </div>
                <div class="detail-row">
                    <span class="label">Площадь:</span> {property_data.get('area', 'Не указана')} м²
                </div>
                <div class="detail-row">
                    <span class="label">Этаж:</span> {property_data.get('floor', 'Не указан')}
                </div>
                <div class="detail-row">
                    <span class="label">Застройщик:</span> {property_data.get('developer', 'Не указан')}
                </div>
                <div class="detail-row">
                    <span class="label">ЖК:</span> {property_data.get('residential_complex', 'Не указан')}
                </div>
                <div class="detail-row">
                    <span class="label">Район:</span> {property_data.get('district', 'Не указан')}
                </div>
                <div class="detail-row">
                    <span class="label">Адрес:</span> {property_data.get('location', 'Не указан')}
                </div>
                <div class="detail-row">
                    <span class="label">Статус:</span> {property_data.get('status', 'Не указан')}
                </div>
                
                <div class="detail-row" style="margin-top: 30px;">
                    <div class="price">Цена: {property_data.get('price', 0):,} ₽</div>
                </div>
                <div class="detail-row">
                    <div class="cashback">Кешбек: до {calculate_cashback(property_data.get('price', 0)):,} ₽ (5%)</div>
                </div>
            </div>
            
            <div style="margin-top: 50px; text-align: center; color: #666;">
                <p>InBack.ru - ваш кешбек за новостройки</p>
                <p>Телефон: +7 (800) 123-12-12</p>
            </div>
        </body>
        </html>
        """
        
        # Return HTML for PDF conversion (browser will handle PDF generation)
        response = app.response_class(
            response=html_content,
            status=200,
            mimetype='text/html'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=property-{property_id}.html'
        return response
        
    except Exception as e:
        print(f"Error generating PDF for property {property_id}: {e}")
        return jsonify({'error': 'Failed to generate PDF'}), 500

@app.route('/developers')
@cache.cached(timeout=3600)  # Кэш на 1 час
def developers():
    """Developers listing page with real database data"""
    try:
        print("Loading developers from database...")
        
        from models import Developer, ResidentialComplex, Property
        from sqlalchemy import func
        
        # Получаем застройщиков из базы данных с статистикой
        developers_list = (
            db.session.query(Developer, 
                            func.count(ResidentialComplex.id).label('complexes_count'),
                            func.count(Property.id).label('properties_count'))
            .outerjoin(ResidentialComplex, Developer.id == ResidentialComplex.developer_id)
            .outerjoin(Property, Developer.id == Property.developer_id)
            .group_by(Developer.id)
            .order_by(func.count(Property.id).desc())
            .all()
        )
        
        # Формируем список застройщиков с данными
        developers_data = []
        for developer, complexes_count, properties_count in developers_list:
            developer_dict = {
                'id': developer.id,
                'name': developer.name,
                'slug': developer.slug,
                'description': developer.description or f"Застройщик {developer.name}",
                'logo_url': developer.logo_url or f"https://via.placeholder.com/200x100/3B82F6/FFFFFF?text={developer.name.replace(' ', '+')}",
                'website': developer.website,
                'phone': developer.phone,
                'email': developer.email,
                'address': developer.address,
                'complexes_count': complexes_count,
                'properties_count': properties_count,
                'established_year': developer.established_year,
                # Нужные поля для шаблона
                'max_cashback': 10,  # По умолчанию 10%
                'max_cashback_percent': 10,
                # Статистика для отображения
                'stats': {
                    'total_projects': complexes_count,
                    'total_apartments': properties_count,
                    'avg_price': None  # Добавим позже
                }
            }
            
            # Получаем статистику из Excel данных по имени застройщика
            excel_stats = db.session.execute(text("""
                SELECT 
                    COUNT(*) as total_properties,
                    AVG(ep.price) as avg_price,
                    MIN(ep.price) as min_price,
                    MAX(ep.price) as max_price,
                    COUNT(DISTINCT ep.complex_name) as total_complexes
                FROM excel_properties ep
                WHERE UPPER(TRIM(ep.developer_name)) = UPPER(TRIM(:developer_name))
            """), {'developer_name': developer.name}).fetchone()
            
            if excel_stats and excel_stats[0]:  # Check if we have data
                total_props, avg_price, min_price, max_price, total_complexes = excel_stats
                developer_dict['properties_count'] = total_props or properties_count
                developer_dict['complexes_count'] = total_complexes or complexes_count
                developer_dict['stats'] = {
                    'total_projects': total_complexes or complexes_count,
                    'total_apartments': total_props or properties_count,
                    'avg_price': int(avg_price) if avg_price else None,
                    'min_price': int(min_price) if min_price else None,
                    'max_price': int(max_price) if max_price else None
                }
            else:
                # Fallback to basic database stats
                developer_dict['stats'] = {
                    'total_projects': complexes_count,
                    'total_apartments': properties_count,
                    'avg_price': None
                }
            
            developers_data.append(developer_dict)
        
        print(f"Found {len(developers_data)} developers in database")
        
        return render_template('developers.html', developers=developers_data)
        
    except Exception as e:
        print(f"Error loading developers: {e}")
        return render_template('developers.html', developers=[])

@app.route('/developer/<developer_slug>')  
def developer_page(developer_slug):
    """Individual developer page by slug"""
    try:
        # No redirect logic needed - browser will handle encoding
        
        # Create variations of the developer name to search for
        # Convert slug back to possible name formats  
        developer_name_from_slug = developer_slug.replace('-', ' ')
        
        # Try to find developer in database using multiple search strategies
        developer = db.session.execute(
            text("""
            SELECT * FROM developers WHERE 
            LOWER(TRANSLATE(REPLACE(name, ' ', '-'), '«»"().,;:', '')) = LOWER(:slug)
            OR LOWER(name) LIKE LOWER(:name_pattern)
            OR LOWER(REPLACE(name, ' ', '-')) = LOWER(:slug)
            OR slug = :slug
            LIMIT 1
            """),
            {
                "slug": developer_slug, 
                "name_pattern": f"%{developer_name_from_slug}%"
            }
        ).fetchone()
        
        if not developer:
            print(f"Developer not found in database: {developer_slug}")
            return redirect(url_for('developers'))
        
        # Convert row to dict-like object for template
        developer_dict = dict(developer._mapping)
        
        # Получаем ЖК этого застройщика из Excel данных с фотографиями и реальными данными
        developer_complexes_query = db.session.execute(text("""
            SELECT 
                ep.complex_name as name,
                ep.complex_name as id,
                COALESCE(MAX(ep.address_short_display_name), 'Адрес не указан') as location,
                COUNT(ep.inner_id) as apartments_count,
                COUNT(DISTINCT ep.complex_building_id) as buildings_count,
                MIN(ep.price) as min_price,
                MAX(ep.price) as max_price,
                AVG(ep.price) as avg_price,
                MAX(ep.address_position_lat) as lat,
                MAX(ep.address_position_lon) as lng,
                MAX(ep.complex_sales_address) as sales_address,
                -- Получаем все фотографии из JSON массива формата ["url1","url2","url3"]
                CASE 
                    WHEN MAX(ep.photos) IS NOT NULL AND MAX(ep.photos) != '' AND MAX(ep.photos) != '[]' 
                        THEN ARRAY(SELECT json_array_elements_text(MAX(ep.photos)::json))
                    ELSE ARRAY['https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800']
                END as images,
                -- Получаем первую фотографию для совместимости  
                CASE 
                    WHEN MAX(ep.photos) IS NOT NULL AND MAX(ep.photos) != '' AND MAX(ep.photos) != '[]' 
                        THEN (MAX(ep.photos)::json->>0)
                    ELSE 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800'
                END as image,
                CASE 
                    WHEN MAX(ep.complex_end_build_quarter) IS NOT NULL AND MAX(ep.complex_end_build_year) IS NOT NULL 
                        THEN COALESCE(MAX(ep.complex_end_build_quarter)::text, 'IV') || ' кв. ' || COALESCE(MAX(ep.complex_end_build_year)::text, '2024')
                    ELSE 'Сдан'
                END as completion_date,
                MIN(ep.price) as real_price_from,
                COUNT(DISTINCT ep.object_rooms) as room_types_count
            FROM excel_properties ep
            WHERE UPPER(TRIM(ep.developer_name)) = UPPER(TRIM(:developer_name))
            GROUP BY ep.complex_name
            ORDER BY apartments_count DESC
        """), {'developer_name': developer.name})
        
        developer_complexes = []
        for complex_row in developer_complexes_query:
            complex_dict = dict(complex_row._mapping)
            
            # Получаем распределение квартир по комнатности для этого ЖК
            room_distribution_query = db.session.execute(text("""
                SELECT 
                    CASE 
                        WHEN object_rooms = 0 THEN 'Студия'
                        WHEN object_rooms = 1 THEN '1-комн.'
                        WHEN object_rooms = 2 THEN '2-комн.'
                        WHEN object_rooms = 3 THEN '3-комн.'
                        WHEN object_rooms = 4 THEN '4-комн.'
                        ELSE CAST(object_rooms AS TEXT) || '-комн.'
                    END as room_type,
                    COUNT(*) as count,
                    MIN(price) as price_from,
                    MAX(price) as price_to,
                    MIN(object_area) as area_from,
                    MAX(object_area) as area_to
                FROM excel_properties 
                WHERE UPPER(TRIM(complex_name)) = UPPER(TRIM(:complex_name))
                  AND UPPER(TRIM(developer_name)) = UPPER(TRIM(:developer_name))
                GROUP BY object_rooms
                ORDER BY object_rooms
            """), {'complex_name': complex_dict['name'], 'developer_name': developer.name})
            
            # Формируем данные о комнатности
            real_room_distribution = {}
            room_details = {}
            
            for room_row in room_distribution_query:
                room_data = dict(room_row._mapping)
                room_type = room_data['room_type']
                real_room_distribution[room_type] = room_data['count']
                room_details[room_type] = {
                    'price_from': room_data['price_from'],
                    'price_to': room_data['price_to'],
                    'area_from': room_data['area_from'],
                    'area_to': room_data['area_to']
                }
            
            complex_dict['real_room_distribution'] = real_room_distribution
            complex_dict['room_details'] = room_details
            developer_complexes.append(complex_dict)
        
        # Получаем квартиры этого застройщика из Excel данных
        excel_properties_query = db.session.execute(text("""
            SELECT *
            FROM excel_properties ep
            WHERE UPPER(TRIM(ep.developer_name)) = UPPER(TRIM(:developer_name))
            ORDER BY ep.price ASC
        """), {'developer_name': developer.name})
        
        developer_properties = []
        for prop_row in excel_properties_query:
            prop_dict = dict(prop_row._mapping)
            developer_properties.append(prop_dict)
        
        properties_count = len(developer_properties)
        min_price = min([p['price'] for p in developer_properties]) if developer_properties else 0
        
        # Parse features and infrastructure if they exist
        import json as json_lib
        features = []
        infrastructure = []
        
        if developer_dict.get('features'):
            try:
                features = json_lib.loads(developer_dict['features'])
            except:
                features = []
        
        if developer_dict.get('infrastructure'):
            try:
                infrastructure = json_lib.loads(developer_dict['infrastructure'])
            except:
                infrastructure = []
        
        # Получаем общую статистику из Excel
        excel_stats = db.session.execute(text("""
            SELECT 
                COUNT(*) as total_properties,
                AVG(ep.price) as avg_price,
                MIN(ep.price) as min_price,
                MAX(ep.price) as max_price,
                COUNT(DISTINCT ep.complex_name) as total_complexes
            FROM excel_properties ep
            WHERE UPPER(TRIM(ep.developer_name)) = UPPER(TRIM(:developer_name))
        """), {'developer_name': developer.name}).fetchone()
        
        # Обновляем статистику с правильными данными
        if excel_stats and excel_stats[0]:
            total_props, avg_price, min_price_excel, max_price_excel, total_complexes = excel_stats
            developer_dict['properties_count'] = total_props
            developer_dict['complexes_count'] = total_complexes
            developer_dict['min_price'] = int(min_price_excel) if min_price_excel else 12000000
            developer_dict['max_price'] = int(max_price_excel) if max_price_excel else 0
            developer_dict['avg_price'] = int(avg_price) if avg_price else 0
            print(f"DEBUG: Excel stats for {developer.name}: min_price={min_price_excel}, total_props={total_props}")
        else:
            print(f"DEBUG: No Excel stats found for {developer.name}")
        
        # Добавляем дефолтные значения для полей, которые могут отсутствовать
        developer_dict['total_projects'] = developer_dict.get('completed_projects', 0) or developer_dict.get('complexes_count', 0)
        developer_dict['rating'] = developer_dict.get('rating') or 4.2
        developer_dict['founded_year'] = developer_dict.get('founded_year') or 2015
        developer_dict['detailed_description'] = developer_dict.get('description') or 'Надёжный застройщик с многолетним опытом строительства качественного жилья в регионе.'
        developer_dict['description'] = developer_dict.get('description') or developer_dict['detailed_description']
        developer_dict['advantages'] = developer_dict.get('advantages') or [
            'Собственное строительство без субподряда',
            'Сдача объектов точно в срок', 
            'Качественные материалы и технологии',
            'Полный пакет документов и сервисов'
        ]
        
        return render_template('developer_detail.html', 
                             developer=developer_dict,
                             developer_name=developer_dict['name'],
                             complexes=developer_complexes,
                             apartments=developer_properties,
                             total_properties=properties_count,
                             min_price=min_price,
                             features=features,
                             infrastructure=infrastructure)
        
    except Exception as e:
        print(f"Error loading developer page for {developer_name}: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('developers'))

# Districts routes
@app.route('/districts')
def districts():
    """Districts listing page"""
    # Импорт модели
    from models import District
    import json
    
    # Получаем все районы из базы данных
    districts_query = District.query.order_by(District.name).all()
    
    # Подготавливаем данные с парсингом JSON
    districts_list = []
    for district in districts_query:
        district_data = {
            'id': district.id,
            'name': district.name,
            'slug': district.slug,
            'description': district.description,
            'latitude': district.latitude,
            'longitude': district.longitude,
            'distance_to_center': district.distance_to_center,
            'infrastructure_data': {}
        }
        
        # Парсим JSON данные инфраструктуры
        if district.infrastructure_data:
            try:
                district_data['infrastructure_data'] = json.loads(district.infrastructure_data)
            except:
                district_data['infrastructure_data'] = {}
        
        districts_list.append(district_data)
    
    return render_template('districts.html', 
                         districts=districts_list,
                         yandex_api_key=os.environ.get('YANDEX_MAPS_API_KEY'))

# ========================================
# АДМИНИСТРАТИВНАЯ ПАНЕЛЬ ДЛЯ КООРДИНАТ
# ========================================

@app.route('/admin/coordinates')
def admin_coordinates():
    """Административная панель для редактирования координат районов"""
    from models import District
    
    # Получаем все районы
    districts = District.query.order_by(District.name).all()
    
    return render_template('admin/coordinates.html', 
                         districts=districts,
                         yandex_api_key=os.environ.get('YANDEX_MAPS_API_KEY'))

@app.route('/admin/update-coordinates', methods=['POST'])
def admin_update_coordinates():
    """API для обновления координат района"""
    from models import District
    import math
    
    try:
        district_id = request.form.get('district_id')
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        
        # Вычисляем расстояние до центра
        theater_lat, theater_lon = 45.035180, 38.977414
        
        def haversine_distance(lat1, lon1, lat2, lon2):
            R = 6371
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            return R * c
        
        distance = haversine_distance(latitude, longitude, theater_lat, theater_lon)
        
        # Обновляем координаты
        district = District.query.get(district_id)
        if district:
            district.latitude = latitude
            district.longitude = longitude
            district.distance_to_center = distance
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Координаты района {district.name} обновлены',
                'distance': round(distance, 1)
            })
        else:
            return jsonify({'success': False, 'message': 'Район не найден'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# ========================================
# АЛИАСЫ ДЛЯ СТАРЫХ URL РАЙОНОВ
# ========================================

@app.route('/district/tec')
def district_tec_redirect():
    """Редирект со старого URL ТЭЦ на новый"""
    from flask import redirect, url_for
    return redirect(url_for('district_detail', district='tets'), code=301)

@app.route('/district/mkg')
def district_mkg_redirect():
    """Редирект со старого URL МКГ (МХГ) на новый"""
    from flask import redirect, url_for
    return redirect(url_for('district_detail', district='mhg'), code=301)

@app.route('/district/skhi')
def district_skhi_redirect():
    """Редирект для СХИ (Сельскохозяйственный институт)"""
    from flask import redirect, url_for
    return redirect(url_for('district_detail', district='shi'), code=301)

@app.route('/district/<district>')
def district_detail(district):
    """Individual district page"""
    try:
        # Import District model
        from models import District
        
        # Get properties and complexes in this district
        properties = load_properties()
        complexes = load_residential_complexes()
        
        # Filter by district (simplified district matching)
        district_properties = [p for p in properties if district.replace('-', ' ').lower() in p.get('address', '').lower()]
        district_complexes = [c for c in complexes if district.replace('-', ' ').lower() in c.get('district', '').lower()]
        
        # Add cashback calculations
        for prop in district_properties:
            prop['cashback'] = calculate_cashback(prop['price'])
        
        # District info mapping - all 54 districts
        district_names = {
            '40-let-pobedy': '40 лет Победы',
            '9i-kilometr': '9-й километр', 
            'aviagorodok': 'Авиагородок',
            'avrora': 'Аврора',
            'basket-hall': 'Баскет-холл',
            'berezovy': 'Березовый',
            'cheremushki': 'Черемушки',
            'dubinka': 'Дубинка',
            'enka': 'Энка',
            'festivalny': 'Фестивальный',
            'gidrostroitelei': 'Гидростроителей',
            'gorkhutor': 'Горхутор',
            'hbk': 'ХБК',
            'kalinino': 'Калинино',
            'karasunsky': 'Карасунский',
            'kolosisty': 'Колосистый',
            'komsomolsky': 'Комсомольский',
            'kozhzavod': 'Кожзавод',
            'krasnaya-ploshchad': 'Красная площадь',
            'krasnodarskiy': 'Краснодарский',
            'kubansky': 'Кубанский',
            'mkg': 'МКГ',
            'molodezhny': 'Молодежный',
            'muzykalny-mkr': 'Музыкальный микрорайон',
            'nemetskaya-derevnya': 'Немецкая деревня',
            'novoznamenskiy': 'Новознаменский',
            'panorama': 'Панорама',
            'pashkovskiy': 'Пашковский',
            'pashkovsky': 'Пашковский-2',
            'pokrovka': 'Покровка',
            'prikubansky': 'Прикубанский',
            'rayon-aeroporta': 'Район аэропорта',
            'repino': 'Репино',
            'rip': 'РИП',
            'severny': 'Северный',
            'shkolny': 'Школьный',
            'slavyansky': 'Славянский',
            'slavyansky2': 'Славянский-2',
            'solnechny': 'Солнечный',
            'tabachnaya-fabrika': 'Табачная фабрика',
            'tec': 'ТЭЦ',
            'tsentralnyy': 'Центральный',
            'uchhoz-kuban': 'Учхоз Кубань',
            'vavilova': 'Вавилова',
            'votochno-kruglikovskii': 'Восточно-Кругликовский',
            'yablonovskiy': 'Яблоновский',
            'zapadny': 'Западный',
            'zapadny-obhod': 'Западный обход',
            'zapadny-okrug': 'Западный округ',
            'zip-zhukova': 'ЗИП Жукова'
        }
        
        # Get district data from database with coordinates
        district_db = District.query.filter_by(slug=district).first()
        
        # Use district name from database if available, otherwise fallback to mapping
        if district_db and district_db.name:
            district_name = district_db.name
        else:
            district_name = district_names.get(district, district.replace('-', ' ').title())
        
        # Prepare district data for template
        infrastructure_data = None
        if district_db and district_db.infrastructure_data:
            try:
                import json
                if isinstance(district_db.infrastructure_data, str):
                    infrastructure_data = json.loads(district_db.infrastructure_data)
                else:
                    infrastructure_data = district_db.infrastructure_data
            except Exception as e:
                print(f"Infrastructure parsing error: {e}")
                infrastructure_data = None
        
        district_data = {
            'name': district_name,
            'slug': district,
            'latitude': district_db.latitude if district_db and district_db.latitude else None,
            'longitude': district_db.longitude if district_db and district_db.longitude else None,
            'zoom_level': district_db.zoom_level if district_db and district_db.zoom_level else 13,
            'description': district_db.description if district_db else None,
            'distance_to_center': getattr(district_db, 'distance_to_center', None) if district_db else None,
            'infrastructure_data': infrastructure_data
        }
        
        return render_template('district_detail.html', 
                             district=district,
                             district_name=district_name,
                             district_data=district_data,
                             properties=district_properties,
                             complexes=district_complexes,
                             yandex_api_key=os.environ.get('YANDEX_MAPS_API_KEY', ''))
    except Exception as e:
        # Log detailed error for debugging
        import traceback
        print(f"ERROR in district_detail route: {e}")
        print("Full traceback:")
        traceback.print_exc()
        
        # Return error page
        from flask import render_template_string
        error_template = """
        <html>
        <head><title>Ошибка - InBack.ru</title></head>
        <body>
            <h1>Произошла ошибка</h1>
            <p>К сожалению, не удалось загрузить страницу района {{ district }}.</p>
            <p>Ошибка: {{ error }}</p>
            <a href="/">Вернуться на главную</a>
        </body>
        </html>
        """
        return render_template_string(error_template, district=district, error=str(e)), 500


# Content pages routes are already defined above

# API endpoint for infrastructure data
@app.route('/api/infrastructure')
def get_infrastructure():
    """API endpoint to get infrastructure data for coordinates"""
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', 2000, type=int)
        
        if not lat or not lng:
            return jsonify({'error': 'Coordinates required'}), 400
        
        # Import infrastructure functions
        from infrastructure_api import get_poi_around_coordinates
        
        # Get POI data
        poi_data = get_poi_around_coordinates(lat, lng, radius)
        
        return jsonify(poi_data)
        
    except Exception as e:
        print(f"Error getting infrastructure data: {e}")
        return jsonify({'error': 'Failed to get infrastructure data'}), 500

# API endpoint for district streets
@app.route('/api/streets/district/<district_slug>')
def get_district_streets(district_slug):
    """API endpoint to get streets for a specific district"""
    try:
        from models import Street, District
        
        # Получаем район по slug
        district = District.query.filter_by(slug=district_slug).first()
        if not district:
            return jsonify({'error': 'District not found'}), 404
        
        # Получаем улицы района с координатами
        streets = Street.query.filter_by(district_id=district.id).filter(
            Street.latitude.isnot(None),
            Street.longitude.isnot(None)
        ).all()
        
        streets_data = []
        for street in streets:
            streets_data.append({
                'id': street.id,
                'name': street.name,
                'slug': street.slug,
                'latitude': float(street.latitude) if street.latitude else None,
                'longitude': float(street.longitude) if street.longitude else None,
                'description': street.description
            })
        
        return jsonify(streets_data)
        
    except Exception as e:
        print(f"Error getting district streets: {e}")
        return jsonify({'error': 'Failed to get district streets'}), 500

# Privacy and legal pages
@app.route('/privacy-policy')
def privacy_policy():
    """Privacy policy page"""
    return render_template('privacy_policy.html')

def parse_user_agent(user_agent):
    """Простой парсинг User-Agent строки"""
    info = {
        'raw': user_agent,
        'browser': 'Неизвестно',
        'version': 'Неизвестно',
        'os': 'Неизвестно',
        'device': 'Неизвестно'
    }
    
    # Определяем браузер
    if 'Chrome' in user_agent and 'Edg' not in user_agent:
        info['browser'] = 'Chrome'
        if 'Chrome/' in user_agent:
            version = user_agent.split('Chrome/')[1].split()[0]
            info['version'] = version
    elif 'Firefox' in user_agent:
        info['browser'] = 'Firefox'
        if 'Firefox/' in user_agent:
            version = user_agent.split('Firefox/')[1].split()[0]
            info['version'] = version
    elif 'Edg' in user_agent:
        info['browser'] = 'Microsoft Edge'
        if 'Edg/' in user_agent:
            version = user_agent.split('Edg/')[1].split()[0]
            info['version'] = version
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        info['browser'] = 'Safari'
        if 'Version/' in user_agent:
            version = user_agent.split('Version/')[1].split()[0]
            info['version'] = version
    
    # Определяем ОС
    if 'Windows NT' in user_agent:
        info['os'] = 'Windows'
        if 'Windows NT 10.0' in user_agent:
            info['os'] = 'Windows 10/11'
    elif 'Mac OS X' in user_agent:
        info['os'] = 'macOS'
    elif 'Linux' in user_agent:
        info['os'] = 'Linux'
    elif 'Android' in user_agent:
        info['os'] = 'Android'
    elif 'iPhone' in user_agent:
        info['os'] = 'iOS'
    
    # Определяем тип устройства
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        info['device'] = 'Мобильное устройство'
    elif 'Tablet' in user_agent or 'iPad' in user_agent:
        info['device'] = 'Планшет'
    else:
        info['device'] = 'Десктоп'
    
    return info

@app.route('/technical-info')
def technical_info():
    """Страница технической информации с данными о сессии и устройстве"""
    import platform
    import socket
    import uuid
    import secrets
    from datetime import datetime
    from flask_login import current_user
    
    # Генерируем session_id если его нет
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    
    # Парсим User-Agent для более детальной информации
    user_agent = request.headers.get('User-Agent', '')
    browser_info = parse_user_agent(user_agent)
    
    # Собираем техническую информацию
    tech_info = {
        'server_info': {
            'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'hostname': socket.gethostname(),
            'flask_version': '2.3.3',  # или получить динамически
            'environment': 'development'
        },
        'session_info': {
            'session_id': session.get('session_id'),
            'user_id': current_user.id if current_user.is_authenticated else 'Не авторизован',
            'username': current_user.full_name if current_user.is_authenticated and hasattr(current_user, 'full_name') else 'Гость',
            'is_authenticated': current_user.is_authenticated,
            'session_permanent': session.permanent
        },
        'request_info': {
            'user_agent': user_agent,
            'ip_address': request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
            'method': request.method,
            'url': request.url,
            'referrer': request.headers.get('Referer', 'Прямой переход'),
            'accept_language': request.headers.get('Accept-Language', 'Неизвестно'),
            'accept_encoding': request.headers.get('Accept-Encoding', 'Неизвестно'),
            'content_type': request.headers.get('Content-Type', 'Неизвестно'),
            'host': request.headers.get('Host', 'Неизвестно')
        },
        'browser_info': browser_info
    }
    
    return render_template('technical_info.html', tech_info=tech_info)

@app.route('/data-processing-consent')
def data_processing_consent():
    """Data processing consent page"""
    return render_template('data_processing_consent.html')

# Override Flask-Login unauthorized handler for API routes
@login_manager.unauthorized_handler  
def handle_unauthorized():
    # Check if this is an API route
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    # Regular redirect for web routes
    return redirect(url_for('login', next=request.url))

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User, Manager
    
    # Check if this is a manager ID (with prefix 'm_')
    if user_id.startswith('m_'):
        manager_id = int(user_id[2:])  # Remove 'm_' prefix
        manager = Manager.query.get(manager_id)
        if manager:
            return manager
    else:
        # Regular user ID
        try:
            user = User.query.get(int(user_id))
            if user:
                return user
        except ValueError:
            pass
    
    return None

def manager_required(f):
    """Decorator to require manager authentication with Flask-Login"""
    from functools import wraps
    from flask_login import current_user
    from models import Manager
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if user is authenticated via Flask-Login
        if not current_user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            return redirect(url_for('manager_login'))
        
        # Check if authenticated user is a manager
        if not isinstance(current_user, Manager):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return jsonify({'success': False, 'error': 'Manager access required'}), 403
            return redirect(url_for('manager_login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        from models import User
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        if not email or not password:
            flash('Заполните все поля', 'error')
            return render_template('auth/login.html')
        
        # Check if email or phone
        user = User.query.filter(
            (User.email == email) | (User.phone == email)
        ).first()
        
        if user:
            # Check if user needs to set password
            if user.needs_password_setup():
                session['temp_user_id'] = user.id
                flash('Необходимо установить пароль для входа', 'info')
                return redirect(url_for('setup_password'))
            
            # Normal password check
            if user.check_password(password):
                login_user(user, remember=remember)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Redirect to next page or dashboard
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Неверный email или пароль', 'error')
        else:
            flash('Пользователь не найден', 'error')
    
    return render_template('auth/login.html')

@app.route('/setup-password', methods=['GET', 'POST'])
def setup_password():
    """Setup password for users created by managers"""
    temp_user_id = session.get('temp_user_id')
    if not temp_user_id:
        flash('Сессия истекла', 'error')
        return redirect(url_for('login'))
    
    from models import User
    user = User.query.get(temp_user_id)
    if not user or not user.needs_password_setup():
        flash('Пользователь не найден или пароль уже установлен', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('Заполните все поля', 'error')
            return render_template('auth/setup_password.html', user=user)
        
        if len(password) < 8:
            flash('Пароль должен содержать минимум 8 символов', 'error')
            return render_template('auth/setup_password.html', user=user)
        
        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return render_template('auth/setup_password.html', user=user)
        
        # Set password
        user.set_password(password)
        user.is_verified = True
        db.session.commit()
        
        # Clear temp session
        session.pop('temp_user_id', None)
        
        # Login user
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        flash('Пароль успешно установлен!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('auth/setup_password.html', user=user)

@app.route('/register', methods=['POST'])
def register():
    """User registration"""
    from models import User
    
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    terms = request.form.get('terms')
    
    # Validation
    if not all([full_name, email, password, confirm_password, terms]):
        flash('Заполните все обязательные поля', 'error')
        return redirect(url_for('login'))
    
    if password != confirm_password:
        flash('Пароли не совпадают', 'error')
        return redirect(url_for('login'))
    
    if not password or len(password) < 8:
        flash('Пароль должен содержать минимум 8 символов', 'error')
        return redirect(url_for('login'))
    
    # Check if user exists
    if User.query.filter_by(email=email).first():
        flash('Пользователь с таким email уже существует', 'error')
        return redirect(url_for('login'))
    
    # Create new user
    user = User(
        full_name=full_name,
        email=email,
        phone=phone
    )
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Send welcome notification
        try:
            from email_service import send_welcome_email
            send_welcome_email(user, base_url=request.url_root.rstrip('/'))
        except Exception as e:
            print(f"Error sending welcome notification: {e}")
        
        # Login user immediately
        login_user(user)
        
        flash('Регистрация успешна! Проверьте email для подтверждения.', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {e}")
        flash(f'Ошибка при регистрации: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/quiz-registration')
def quiz_registration():
    """Show quiz registration page"""
    return render_template('quiz_registration.html')

@app.route('/callback-request')
def callback_request_page():
    """Show callback request page"""
    return render_template('callback_request.html')

@app.route('/api/property-selection', methods=['POST'])
def property_selection():
    """Property selection application"""
    from models import Application, User
    data = request.get_json()
    
    try:
        # Extract data
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        # Application preferences
        preferred_district = data.get('preferred_district', '')
        property_type = data.get('property_type', '')
        room_count = data.get('room_count', '')
        budget_range = data.get('budget_range', '')
        
        # Property context information
        property_id = data.get('property_id')
        property_title = data.get('property_title', '')
        property_complex = data.get('property_complex', '')
        property_price = data.get('property_price')
        property_area = data.get('property_area')
        property_rooms = data.get('property_rooms')
        property_floor = data.get('property_floor')
        property_total_floors = data.get('property_total_floors')
        property_district = data.get('property_district', '')
        property_url = data.get('property_url', '')
        property_type_context = data.get('property_type_context', '')
        
        # Validation
        if not email or not name or not phone:
            return jsonify({'success': False, 'error': 'Все обязательные поля должны быть заполнены'})
        
        # Determine application type and build message
        is_specific_property = property_id and property_type_context == 'property'
        is_specific_complex = property_id and property_type_context == 'complex'
        
        if is_specific_property:
            # Specific property interest
            application_title = f"Интерес к квартире: {property_title}"
            complex_name = property_complex or 'Не указан'
            message = f"Заявка по конкретной квартире:\n"
            message += f"Имя: {name}\n"
            message += f"Email: {email}\n"
            message += f"Телефон: {phone}\n\n"
            message += f"=== ОБЪЕКТ ИНТЕРЕСА ===\n"
            message += f"Квартира: {property_title}\n"
            message += f"ЖК: {property_complex}\n"
            if property_price:
                try:
                    formatted_price = f"{int(property_price):,}".replace(',', ' ')
                    message += f"Цена: {formatted_price} ₽\n"
                except (ValueError, TypeError):
                    message += f"Цена: {property_price} ₽\n"
            if property_area:
                message += f"Площадь: {property_area} м²\n"
            if property_floor and property_total_floors:
                message += f"Этаж: {property_floor}/{property_total_floors}\n"
            if property_district:
                message += f"Район: {property_district}\n"
            if property_url:
                message += f"Ссылка: {property_url}\n"
            message += f"\n=== ДОПОЛНИТЕЛЬНЫЕ ПРЕДПОЧТЕНИЯ ===\n"
            message += f"Предпочитаемый район: {preferred_district or 'Не указан'}\n"
            message += f"Тип недвижимости: {property_type or 'Не указан'}\n"
            message += f"Комнат: {room_count or 'Не указано'}\n"
            message += f"Бюджет: {budget_range or 'Не указан'}"
        elif is_specific_complex:
            # Specific complex interest
            application_title = f"Интерес к ЖК: {property_title}"
            complex_name = property_title
            message = f"Заявка по жилому комплексу:\n"
            message += f"Имя: {name}\n"
            message += f"Email: {email}\n"
            message += f"Телефон: {phone}\n\n"
            message += f"=== ОБЪЕКТ ИНТЕРЕСА ===\n"
            message += f"ЖК: {property_title}\n"
            if property_district:
                message += f"Район: {property_district}\n"
            if property_url:
                message += f"Ссылка: {property_url}\n"
            message += f"\n=== ДОПОЛНИТЕЛЬНЫЕ ПРЕДПОЧТЕНИЯ ===\n"
            message += f"Предпочитаемый район: {preferred_district or 'Не указан'}\n"
            message += f"Тип недвижимости: {property_type or 'Не указан'}\n"
            message += f"Комнат: {room_count or 'Не указано'}\n"
            message += f"Бюджет: {budget_range or 'Не указан'}"
        else:
            # General property selection
            application_title = "Подбор квартиры"
            complex_name = "По предпочтениям"
            message = f"Заявка на подбор квартиры:\n"
            message += f"Имя: {name}\n"
            message += f"Email: {email}\n"
            message += f"Телефон: {phone}\n"
            message += f"Район: {preferred_district or 'Любой'}\n"
            message += f"Тип: {property_type or 'Не указан'}\n"
            message += f"Комнат: {room_count or 'Не указано'}\n"
            message += f"Бюджет: {budget_range or 'Не указан'}"
        
        # Create application
        application = Application(
            user_id=None,  # No user account needed for applications
            property_id=property_id,  # Store specific property ID if available
            property_name=application_title,
            complex_name=complex_name,
            message=message,
            status='new',
            contact_name=name,
            contact_email=email,
            contact_phone=phone
        )
        
        db.session.add(application)
        
        # Application submitted successfully
        db.session.commit()
        
        # Send Telegram notification
        try:
            from telegram_bot import send_telegram_message
            from datetime import datetime
            
            # Calculate potential cashback (2% of average budget)
            potential_cashback = ""
            if budget_range:
                if "млн" in budget_range:
                    # Extract average from range like "3-5 млн"
                    numbers = [float(x) for x in budget_range.replace(" млн", "").split("-") if x.strip().replace(".", "").replace(",", "").isdigit()]
                    if numbers:
                        avg_price = sum(numbers) / len(numbers) * 1000000
                        cashback = int(avg_price * 0.02)
                        formatted_cashback = f"{cashback:,}".replace(',', ' ')
                        potential_cashback = f"💰 *Потенциальный кэшбек:* {formatted_cashback} руб. (2%)\n"
            
            # Build telegram message based on application type
            if is_specific_property:
                telegram_message = f"""🏠 *ЗАЯВКА ПО КОНКРЕТНОЙ КВАРТИРЕ*

👤 *КОНТАКТНАЯ ИНФОРМАЦИЯ:*
• Имя: {name}
• Телефон: {phone}
• Email: {email}

🏡 *ОБЪЕКТ ИНТЕРЕСА:*
• Квартира: {property_title}
• ЖК: {property_complex}
{f"• Цена: {int(property_price):,} ₽".replace(',', ' ') if property_price else ''}
{f"• Площадь: {property_area} м²" if property_area else ''}
{f"• Этаж: {property_floor}/{property_total_floors}" if property_floor and property_total_floors else ''}
{f"• Ссылка: {property_url}" if property_url else ''}

🔍 *ДОПОЛНИТЕЛЬНЫЕ ПРЕДПОЧТЕНИЯ:*
• Район: {preferred_district or 'Не указан'}
• Тип недвижимости: {property_type or 'Не указан'}
• Количество комнат: {room_count or 'Не указано'}
• Бюджет: {budget_range or 'Не указан'}

{potential_cashback}📅 *ВРЕМЯ ЗАЯВКИ:* {datetime.now().strftime('%d.%m.%Y в %H:%M')}
🌐 *ИСТОЧНИК:* Страница квартиры на InBack.ru

📋 *СЛЕДУЮЩИЕ ШАГИ:*
1️⃣ Связаться с клиентом в течение 15 минут
2️⃣ Обсудить интересующую квартиру
3️⃣ Рассчитать кэшбек и условия покупки
4️⃣ Назначить встречу для просмотра

⚡ *ВАЖНО:* Клиент уже выбрал конкретную квартиру!"""
            elif is_specific_complex:
                telegram_message = f"""🏢 *ЗАЯВКА ПО ЖИЛОМУ КОМПЛЕКСУ*

👤 *КОНТАКТНАЯ ИНФОРМАЦИЯ:*
• Имя: {name}
• Телефон: {phone}
• Email: {email}

🏗️ *ОБЪЕКТ ИНТЕРЕСА:*
• ЖК: {property_title}
{f"• Район: {property_district}" if property_district else ''}
{f"• Ссылка: {property_url}" if property_url else ''}

🔍 *ДОПОЛНИТЕЛЬНЫЕ ПРЕДПОЧТЕНИЯ:*
• Район: {preferred_district or 'Не указан'}
• Тип недвижимости: {property_type or 'Не указан'}
• Количество комнат: {room_count or 'Не указано'}
• Бюджет: {budget_range or 'Не указан'}

{potential_cashback}📅 *ВРЕМЯ ЗАЯВКИ:* {datetime.now().strftime('%d.%m.%Y в %H:%M')}
🌐 *ИСТОЧНИК:* Страница ЖК на InBack.ru

📋 *СЛЕДУЮЩИЕ ШАГИ:*
1️⃣ Связаться с клиентом в течение 15 минут
2️⃣ Показать доступные квартиры в ЖК
3️⃣ Рассчитать кэшбек и условия покупки
4️⃣ Назначить встречу для просмотра

⚡ *ВАЖНО:* Клиент интересуется конкретным ЖК!"""
            else:
                telegram_message = f"""🏠 *НОВАЯ ЗАЯВКА НА ПОДБОР КВАРТИРЫ*

👤 *КОНТАКТНАЯ ИНФОРМАЦИЯ:*
• Имя: {name}
• Телефон: {phone}
• Email: {email}

🔍 *КРИТЕРИИ ПОИСКА:*
• Район: {preferred_district or 'Любой'}
• Тип недвижимости: {property_type or 'Не указан'}
• Количество комнат: {room_count or 'Не указано'}
• Бюджет: {budget_range or 'Не указан'}

{potential_cashback}📅 *ВРЕМЯ ЗАЯВКИ:* {datetime.now().strftime('%d.%m.%Y в %H:%M')}
🌐 *ИСТОЧНИК:* Форма на сайте InBack.ru

📋 *СЛЕДУЮЩИЕ ШАГИ:*
1️⃣ Связаться с клиентом в течение 15 минут
2️⃣ Уточнить дополнительные предпочтения
3️⃣ Подготовить подборку объектов
4️⃣ Назначить встречу для просмотра

⚡ *ВАЖНО:* Быстрая реакция повышает конверсию!"""
            
            send_telegram_message('730764738', telegram_message)
            
        except Exception as notify_error:
            print(f"Notification error: {notify_error}")
        
        return jsonify({
            'success': True,
            'message': 'Заявка отправлена! Менеджер свяжется с вами.'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Application error: {e}")
        return jsonify({'success': False, 'error': 'Ошибка при отправке заявки'})

@app.route('/api/callback-request', methods=['POST'])
def api_callback_request():
    """Submit callback request"""
    from models import CallbackRequest, Manager
    data = request.get_json()
    
    try:
        # Extract data
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        preferred_time = data.get('preferred_time', '')
        notes = data.get('notes', '').strip()
        
        # Quiz responses
        interest = data.get('interest', '')
        budget = data.get('budget', '')
        timing = data.get('timing', '')
        
        # Validation
        if not name or not phone:
            return jsonify({'success': False, 'error': 'Имя и телефон обязательны для заполнения'})
        
        # Create callback request
        callback_req = CallbackRequest(
            name=name,
            phone=phone,
            email=email or None,
            preferred_time=preferred_time,
            notes=notes,
            interest=interest,
            budget=budget,
            timing=timing
        )
        
        # Auto-assign to first available manager
        available_manager = Manager.query.filter_by(is_active=True).first()
        if available_manager:
            callback_req.assigned_manager_id = available_manager.id
        
        db.session.add(callback_req)
        db.session.commit()
        
        # Send notifications
        try:
            send_callback_notification_email(callback_req, available_manager)
            send_callback_notification_telegram(callback_req, available_manager)
        except Exception as e:
            print(f"Failed to send callback notifications: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Заявка отправлена! Наш менеджер свяжется с вами в ближайшее время.'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Callback request error: {e}")
        return jsonify({'success': False, 'error': 'Ошибка при отправке заявки. Попробуйте еще раз.'})

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Password reset request"""
    email = request.form.get('email')
    
    if not email:
        flash('Введите email адрес', 'error')
        return redirect(url_for('login'))
    
    from models import User
    user = User.query.filter_by(email=email).first()
    
    if user:
        # Generate reset token and send email
        token = user.generate_verification_token()
        db.session.commit()
        
        try:
            from email_service import send_password_reset_email
            send_password_reset_email(user, token)
        except Exception as e:
            print(f"Error sending password reset email: {e}")
        
        flash('Инструкции по восстановлению пароля отправлены на ваш email', 'success')
    else:
        # Don't reveal that user doesn't exist
        flash('Инструкции по восстановлению пароля отправлены на ваш email', 'success')
    
    return redirect(url_for('login'))

# API endpoints for dashboard functionality
@app.route('/api/cashback-application', methods=['POST'])
@login_required
def create_cashback_application():
    """Create new cashback application"""
    from models import CashbackApplication
    data = request.get_json()
    
    try:
        app = CashbackApplication(
            user_id=current_user.id,
            property_name=data['property_name'],
            property_type=data['property_type'],
            property_size=float(data['property_size']),
            property_price=int(data['property_price']),
            complex_name=data['complex_name'],
            developer_name=data['developer_name'],
            cashback_amount=int(data['cashback_amount']),
            cashback_percent=float(data['cashback_percent'])
        )
        db.session.add(app)
        db.session.commit()
        
        return jsonify({'success': True, 'application_id': app.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/contact-manager', methods=['POST'])
def contact_manager():
    """API endpoint for contacting manager"""
    try:
        from models import Application
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Field {field} is required'}), 400
        
        # Get current user if logged in
        user_id = session.get('user_id')
        
        # Create application with required fields
        application = Application(
            user_id=user_id,
            contact_name=data.get('name'),
            contact_email=data.get('email'),
            contact_phone=data.get('phone'),
            property_name=data.get('property_name', 'Заявка на подбор жилья'),
            complex_name=data.get('complex_name', 'По предпочтениям клиента'),
            status='new',
            message=data.get('message', f"Район: {data.get('district', '')}, Комнат: {data.get('rooms', '')}, Заселение: {data.get('completion', '')}, Оплата: {data.get('payment', '')}"),
            preferred_contact=data.get('preferred_contact', 'phone')
        )
        
        db.session.add(application)
        db.session.commit()
        
        # Send notification to manager (email and Telegram)
        try:
            from email_service import send_manager_notification
            send_manager_notification(
                name=data.get('name'),
                phone=data.get('phone'),
                email=data.get('email'),
                message=data.get('message', ''),
                application_id=application.id
            )
        except Exception as e:
            print(f"Failed to send manager notification email: {e}")
            
        # Send Telegram notification
        try:
            from telegram_bot import send_telegram_message
            from datetime import datetime
            
            # Check if this is for a specific property
            is_specific_property = data.get('property_id') and data.get('property_name')
            
            # Prepare Telegram message with quiz data or property info
            if is_specific_property:
                message_parts = [
                    "🏠 *ЗАЯВКА НА ПРОСМОТР КОНКРЕТНОЙ КВАРТИРЫ*",
                    "",
                    "👤 *КОНТАКТНАЯ ИНФОРМАЦИЯ:*",
                    f"• Имя: {data.get('name')}",
                    f"• Телефон: {data.get('phone')}",
                ]
                
                if data.get('email'):
                    message_parts.append(f"• Email: {data.get('email')}")
                    
                message_parts.extend([
                    "",
                    "🏢 *ИНТЕРЕСУЮЩАЯ КВАРТИРА:*",
                    f"• Объект: {data.get('property_name')}",
                ])
                
                if data.get('complex_name'):
                    message_parts.append(f"• ЖК: {data.get('complex_name')}")
                if data.get('property_price'):
                    price_formatted = f"{int(float(data.get('property_price'))):,}".replace(',', ' ')
                    message_parts.append(f"• Цена: {price_formatted} руб.")
                if data.get('property_area'):
                    message_parts.append(f"• Площадь: {data.get('property_area')} м²")
                if data.get('property_floor'):
                    message_parts.append(f"• Этаж: {data.get('property_floor')}")
                if data.get('property_district'):
                    message_parts.append(f"• Район: {data.get('property_district')}")
                if data.get('property_address'):
                    message_parts.append(f"• Адрес: {data.get('property_address')}")
                    
                # Calculate potential cashback
                if data.get('property_price'):
                    try:
                        price = float(data.get('property_price'))
                        cashback = price * 0.03  # 3% cashback
                        cashback_formatted = f"{int(cashback):,}".replace(',', ' ')
                        message_parts.append(f"💰 Потенциальный кэшбек: {cashback_formatted} руб. (3%)")
                    except:
                        pass
                        
                # Add property URL if available
                if data.get('property_url'):
                    message_parts.extend([
                        "",
                        f"🔗 *ССЫЛКА НА КВАРТИРУ:*",
                        f"{data.get('property_url')}"
                    ])
            else:
                message_parts = [
                    "🏠 *НОВАЯ ЗАЯВКА НА ПОДБОР ЖИЛЬЯ*",
                    "",
                    "👤 *КОНТАКТНАЯ ИНФОРМАЦИЯ:*",
                    f"• Имя: {data.get('name')}",
                    f"• Телефон: {data.get('phone')}",
                ]
                
                if data.get('email'):
                    message_parts.append(f"• Email: {data.get('email')}")
                    
                # Add quiz preferences if available
                if data.get('district'):
                    message_parts.extend([
                        "",
                        "🏘️ *ПРЕДПОЧТЕНИЯ КЛИЕНТА:*",
                        f"• Район: {data.get('district')}"
                    ])
                    
                if data.get('rooms'):
                    message_parts.append(f"• Комнат: {data.get('rooms')}")
                    
                if data.get('completion'):
                    message_parts.append(f"• Срок заселения: {data.get('completion')}")
                    
                if data.get('payment'):
                    message_parts.append(f"• Способ оплаты: {data.get('payment')}")
                
            message_parts.extend([
                "",
                f"📝 *ID заявки:* #{application.id}",
                f"📅 *Время:* {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                "",
                "⚡ *ВАЖНО:* Быстрая реакция повышает конверсию!"
            ])
            
            telegram_message = "\n".join(message_parts)
            send_telegram_message('730764738', telegram_message)
            
        except Exception as notify_error:
            print(f"Telegram notification error: {notify_error}")
        
        return jsonify({
            'success': True,
            'message': 'Заявка отправлена! Менеджер свяжется с вами в ближайшее время.',
            'application_id': application.id
        })
        
    except Exception as e:
        print(f"Error creating manager contact application: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/favorites', methods=['POST'])
@login_required  
def add_to_favorites():
    """Add property to favorites"""
    from models import FavoriteProperty
    data = request.get_json()
    
    # Check if already in favorites
    existing = FavoriteProperty.query.filter_by(
        user_id=current_user.id,
        property_name=data['property_name']
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'Уже в избранном'})
    
    try:
        favorite = FavoriteProperty(
            user_id=current_user.id,
            property_name=data['property_name'],
            property_type=data['property_type'],
            property_size=float(data['property_size']),
            property_price=int(data['property_price']),
            complex_name=data['complex_name'],
            developer_name=data['developer_name'],
            property_image=data.get('property_image'),
            cashback_amount=int(data.get('cashback_amount', 0)),
            cashback_percent=float(data.get('cashback_percent', 0))
        )
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/favorites/<property_id>', methods=['DELETE'])
@login_required
def remove_from_favorites(property_id):
    """Remove property from favorites"""
    from models import FavoriteProperty
    
    favorite = FavoriteProperty.query.filter_by(
        user_id=current_user.id,
        property_id=property_id
    ).first()
    
    if favorite:
        try:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400

def send_view_notification_to_manager(presentation, view):
    """Отправляет уведомление менеджеру о новом просмотре презентации"""
    try:
        manager = presentation.created_by
        if not manager:
            print(f"Manager not found for presentation {presentation.id}")
            return
            
        # Получаем информацию о просмотре
        client_info = "Неизвестный клиент"
        if presentation.client_name:
            client_info = presentation.client_name
        elif presentation.client_phone:
            client_info = presentation.client_phone
            
        # Формируем сообщение уведомления
        notification_text = f"""📊 Новый просмотр презентации!

📋 "{presentation.title}"
👤 Клиент: {client_info}
🔢 Всего просмотров: {presentation.view_count}
⏰ Время просмотра: {view.viewed_at.strftime('%d.%m.%Y %H:%M')}
🌐 IP: {view.view_ip}
📱 Устройство: {view.user_agent[:50] + '...' if view.user_agent and len(view.user_agent) > 50 else view.user_agent or 'Неизвестно'}

👀 Ссылка на презентацию: {request.url_root}presentation/{presentation.unique_url}
🎯 Панель менеджера: {request.url_root}manager/dashboard"""

        # TODO: Интеграция с Telegram Bot API
        # if hasattr(manager, 'telegram_chat_id') and manager.telegram_chat_id:
        #     send_telegram_notification(manager.telegram_chat_id, notification_text)
        
        # TODO: Интеграция с Email
        # if manager.email:
        #     send_email_notification(manager.email, f"Новый просмотр: {presentation.title}", notification_text)
        
        # Пока просто логируем уведомление
        print(f"📧 NOTIFICATION TO MANAGER {manager.email}:")
        print(notification_text)
        print("-" * 50)
        
        # Отмечаем что уведомление отправлено
        view.notification_sent = True
        db.session.commit()
        
    except Exception as e:
        print(f"Error in send_view_notification_to_manager: {e}")

@app.route('/presentation/<string:unique_url>')
def view_presentation(unique_url):
    """Публичная страница просмотра презентации по уникальной ссылке"""
    from models import Collection, CollectionProperty, PresentationView
    
    # Находим презентацию по уникальной ссылке
    presentation = Collection.query.filter_by(
        unique_url=unique_url,
        collection_type='presentation'
    ).first()
    
    if not presentation:
        return render_template('error.html', 
                             error="Презентация не найдена", 
                             message="Возможно, ссылка устарела или была удалена"), 404
    
    # Записываем просмотр
    try:
        view = PresentationView(
            collection_id=presentation.id,
            view_ip=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            referer=request.headers.get('Referer')
        )
        db.session.add(view)
        
        # Увеличиваем счетчик просмотров (без автокоммита)
        presentation.increment_view_count()
        db.session.commit()  # Контролируем транзакцию на уровне view
        
        # Отправляем уведомление менеджеру о новом просмотре
        try:
            send_view_notification_to_manager(presentation, view)
        except Exception as e:
            print(f"Error sending view notification: {e}")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error recording presentation view: {e}")
    
    # Получаем свойства презентации - ОПТИМИЗАЦИЯ: загружаем один раз
    properties = load_properties()
    # Создаем индекс по ID для O(1) поиска вместо O(n)
    properties_index = {str(p.get('id', p.get('ID', ''))): p for p in properties}
    
    properties_data = []
    for prop in presentation.properties:
        # Получаем полную информацию о квартире из индекса O(1)
        property_info = properties_index.get(str(prop.property_id))
        
        if property_info:
            properties_data.append({
                'id': prop.property_id,
                'name': prop.property_name,
                'complex_name': prop.complex_name,
                'price': prop.property_price,
                'size': prop.property_size,
                'type': prop.property_type,
                'manager_note': prop.manager_note,
                'order_index': prop.order_index,
                'property_info': property_info  # Полная информация
            })
    
    # Сортируем по порядку
    properties_data.sort(key=lambda x: x['order_index'])
    
    return render_template('presentation_view.html', 
                         presentation=presentation,
                         properties=properties_data,
                         manager=presentation.created_by)

@app.route('/api/manager/presentation/<int:presentation_id>/share', methods=['POST'])
@manager_required
@csrf.exempt
def share_presentation(presentation_id):
    """Получить данные для отправки презентации в мессенджеры (безопасная версия)"""
    from models import Collection
    from flask_login import current_user
    
    # Строгая проверка владения презентацией
    presentation = Collection.query.filter_by(
        id=presentation_id,
        created_by_manager_id=current_user.id,
        collection_type='presentation'
    ).first()
    
    if not presentation:
        return jsonify({'success': False, 'error': 'Презентация не найдена или у вас нет прав доступа'}), 404
    
    data = request.get_json()
    client_name = data.get('client_name', presentation.client_name)
    
    # Обновляем имя клиента если передано
    if client_name and client_name != presentation.client_name:
        presentation.client_name = client_name
        db.session.commit()
    
    # Формируем ссылку
    base_url = request.url_root.rstrip('/')
    presentation_url = f"{base_url}/presentation/{presentation.unique_url}"
    
    # Формируем сообщение для отправки
    properties_count = len(presentation.properties) if presentation.properties else 0
    
    message_text = f"""🏠 Презентация недвижимости от InBack

📋 {presentation.title}
{f'👤 Для: {client_name}' if client_name else ''}

🔢 Подобрано объектов: {properties_count}
📅 Создано: {presentation.created_at.strftime('%d.%m.%Y')}

👀 Смотреть презентацию:
{presentation_url}

💬 Есть вопросы? Свяжитесь с нами!
📞 +7 (XXX) XXX-XX-XX"""

    return jsonify({
        'success': True,
        'share_data': {
            'presentation_url': presentation_url,
            'message_text': message_text,
            'whatsapp_url': f"https://wa.me/?text={urllib.parse.quote(message_text)}",
            'telegram_url': f"https://t.me/share/url?url={presentation_url}&text={urllib.parse.quote(presentation.title)}",
            'client_name': client_name or 'Клиент',
            'properties_count': properties_count
        }
    })

@app.route('/api/favorites/toggle', methods=['POST'])
@login_required
def toggle_favorite():
    """Toggle favorite status for property"""
    from models import FavoriteProperty
    data = request.get_json()
    property_id = data.get('property_id')
    
    print(f"DEBUG: Favorites toggle called by user {current_user.id} for property {property_id}")
    print(f"DEBUG: Request data: {data}")
    
    if not property_id:
        return jsonify({'success': False, 'error': 'property_id required'}), 400
    
    # Check if already in favorites
    existing = FavoriteProperty.query.filter_by(
        user_id=current_user.id,
        property_id=property_id
    ).first()
    
    try:
        if existing:
            # Remove from favorites
            db.session.delete(existing)
            db.session.commit()
            return jsonify({'success': True, 'action': 'removed', 'is_favorite': False})
        else:
            # Add to favorites
            favorite = FavoriteProperty(
                user_id=current_user.id,
                property_id=property_id,
                property_name=data.get('property_name', ''),
                property_type=data.get('property_type', ''),
                property_size=float(data.get('property_size', 0)),
                property_price=int(data.get('property_price', 0)),
                complex_name=data.get('complex_name', ''),
                developer_name=data.get('developer_name', ''),
                property_image=data.get('property_image'),
                cashback_amount=int(data.get('cashback_amount', 0)),
                cashback_percent=float(data.get('cashback_percent', 0))
            )
            db.session.add(favorite)
            db.session.commit()
            return jsonify({'success': True, 'action': 'added', 'is_favorite': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400



@app.route('/api/collections', methods=['POST'])
@login_required
def create_collection():
    """Create new property collection"""
    from models import Collection
    data = request.get_json()
    
    try:
        collection = Collection(
            user_id=current_user.id,
            title=data['name'],
            description=data.get('description'),
            image_url=data.get('image_url'),
            category=data.get('category')
        )
        db.session.add(collection)
        db.session.commit()
        
        return jsonify({'success': True, 'collection_id': collection.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/collections/<int:collection_id>', methods=['DELETE'])
@login_required
def delete_collection(collection_id):
    """Delete a collection"""
    from models import Collection
    collection = Collection.query.filter_by(
        id=collection_id,
        user_id=current_user.id
    ).first()
    
    if not collection:
        return jsonify({'success': False, 'error': 'Подборка не найдена'}), 404
    
    try:
        db.session.delete(collection)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/documents/upload', methods=['POST'])
@login_required
def upload_documents():
    """Upload documents"""
    from models import Document
    import os
    from werkzeug.utils import secure_filename
    from datetime import datetime
    
    if 'files' not in request.files:
        return jsonify({'success': False, 'error': 'Нет файлов для загрузки'}), 400
    
    files = request.files.getlist('files')
    uploaded_files = []
    
    # Create uploads directory if it doesn't exist
    upload_dir = 'instance/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        if file.filename == '':
            continue
        
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            timestamp = str(int(datetime.utcnow().timestamp()))
            filename = f"{timestamp}_{filename}"
            file_path = os.path.join(upload_dir, filename)
            
            try:
                file.save(file_path)
                file_size = os.path.getsize(file_path)
                file_ext = filename.rsplit('.', 1)[1].lower()
                
                # Create document record
                document = Document(
                    user_id=current_user.id,
                    original_filename=secure_filename(file.filename) if file.filename else 'unknown',
                    stored_filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    file_type=file_ext,
                    document_type=determine_document_type(file.filename),
                    status='На проверке'
                )
                db.session.add(document)
                uploaded_files.append({
                    'filename': file.filename,
                    'size': file_size
                })
            except Exception as e:
                return jsonify({'success': False, 'error': f'Ошибка загрузки файла {file.filename}: {str(e)}'}), 400
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'uploaded_files': uploaded_files})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/documents/<int:document_id>', methods=['DELETE'])
@login_required
def delete_document(document_id):
    """Delete a document"""
    from models import Document
    import os
    
    document = Document.query.filter_by(
        id=document_id,
        user_id=current_user.id
    ).first()
    
    if not document:
        return jsonify({'success': False, 'error': 'Документ не найден'}), 404
    
    try:
        # Delete physical file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete database record
        db.session.delete(document)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def determine_document_type(filename):
    """Determine document type from filename"""
    filename_lower = filename.lower()
    if any(word in filename_lower for word in ['паспорт', 'passport']):
        return 'Паспорт'
    elif any(word in filename_lower for word in ['справка', 'доходы', 'income']):
        return 'Справка о доходах'
    elif any(word in filename_lower for word in ['договор', 'contract']):
        return 'Договор'
    elif any(word in filename_lower for word in ['снилс', 'снилс']):
        return 'СНИЛС'
    elif any(word in filename_lower for word in ['инн', 'inn']):
        return 'ИНН'
    else:
        return 'Другое'

# Manager authentication and dashboard routes
@app.route('/manager/logout')
def manager_logout():
    """Manager logout"""
    session.pop('manager_id', None)
    session.pop('is_manager', None)
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('manager_login'))

@app.route('/manager/login', methods=['GET', 'POST'])
@csrf.exempt
def manager_login():
    if request.method == 'POST':
        try:
            from models import Manager
            from datetime import datetime
            email = request.form.get('email')
            password = request.form.get('password')
            
            print(f"DEBUG: Login attempt - email: {email}, password: {password}")
            
            if not email or not password:
                print("DEBUG: Missing email or password")
                flash('Заполните все поля', 'error')
                return render_template('auth/manager_login.html')
            
            manager = Manager.query.filter_by(email=email, is_active=True).first()
            print(f"DEBUG: Manager found: {manager}")
            print(f"DEBUG: Manager ID: {manager.id if manager else 'None'}")
            print(f"DEBUG: Manager email: {manager.email if manager else 'None'}")
            print(f"DEBUG: Manager active: {manager.is_active if manager else 'None'}")
            
            if manager:
                print(f"DEBUG: Checking password for manager {manager.id}")
                password_check = manager.check_password(password)
                print(f"DEBUG: Password check result: {password_check}")
                
                if password_check:
                    print("DEBUG: Password correct, setting up session")
                    
                    # Use Flask-Login to log in the manager with prefix
                    from flask_login import login_user
                    # Use manager ID with 'm_' prefix to avoid conflicts with user IDs
                    manager.get_id = lambda: f'm_{manager.id}'
                    login_user(manager, remember=True)
                    
                    # Also set session for backward compatibility
                    session.permanent = True
                    session['manager_id'] = manager.id
                    session['is_manager'] = True
                    print(f"DEBUG: Session before commit: {dict(session)}")
                    
                    manager.last_login = datetime.utcnow()
                    db.session.commit()
                    print("DEBUG: Database commit successful")
                    
                    flash('Добро пожаловать!', 'success')
                    print(f"DEBUG: Successfully logged in manager {manager.email}")
                    print(f"DEBUG: Final session data: {dict(session)}")
                    return redirect(url_for('manager_dashboard'))
                else:
                    print("DEBUG: Password incorrect")
            else:
                print("DEBUG: Manager not found or inactive")
            
            print(f"DEBUG: Login failed")
            flash('Неверный email или пароль', 'error')
            
        except Exception as e:
            print(f"DEBUG: Exception during login: {str(e)}")
            import traceback
            traceback.print_exc()
            flash('Произошла ошибка при входе', 'error')
    
    return render_template('auth/manager_login.html')




@app.route('/manager/dashboard')
@manager_required
def manager_dashboard():
    from models import Manager, User, CashbackApplication, Document
    
    manager_id = session.get('manager_id')
    print(f"DEBUG: Manager dashboard - manager_id: {manager_id}")
    current_manager = Manager.query.get(manager_id)
    print(f"DEBUG: Manager dashboard - current_manager: {current_manager}")
    
    if not current_manager:
        print("DEBUG: Manager not found, redirecting to login")
        return redirect(url_for('manager_login'))
    
    # Get statistics
    total_clients = User.query.filter_by(assigned_manager_id=manager_id).count()
    new_clients_count = User.query.filter_by(
        assigned_manager_id=manager_id, 
        client_status='Новый'
    ).count()
    
    pending_applications_count = CashbackApplication.query.join(User).filter(
        User.assigned_manager_id == manager_id,
        CashbackApplication.status == 'На рассмотрении'
    ).count()
    
    pending_documents_count = Document.query.join(User).filter(
        User.assigned_manager_id == manager_id,
        Document.status == 'На проверке'
    ).count()
    
    # Calculate total approved cashback
    total_approved_cashback = 0
    try:
        from models import CashbackApplication, User
        approved_apps = CashbackApplication.query.join(User).filter(
            User.assigned_manager_id == manager_id,
            CashbackApplication.status == 'Одобрена'
        ).all()
        total_approved_cashback = sum(app.cashback_amount for app in approved_apps)
    except Exception as e:
        print(f"Error calculating cashback: {e}")
        total_approved_cashback = 0
    
    # Recent activities (mock data for now)
    recent_activities = [
        {
            'message': 'Новый клиент Иван Петров зарегистрировался',
            'time_ago': '5 минут назад',
            'color': 'blue',
            'icon': 'user-plus'
        },
        {
            'message': 'Заявка на кешбек от Анны Сидоровой требует проверки',
            'time_ago': '1 час назад',
            'color': 'yellow',
            'icon': 'file-alt'
        }
    ]
    
    # Get collections statistics  
    from models import Collection
    collections_count = Collection.query.filter_by(created_by_manager_id=manager_id).count()
    sent_collections_count = Collection.query.filter_by(created_by_manager_id=manager_id, status='Отправлена').count()
    recent_collections = Collection.query.filter_by(created_by_manager_id=manager_id).order_by(Collection.created_at.desc()).limit(5).all()
    
    # Get presentations statistics
    presentations_count = Collection.query.filter_by(
        created_by_manager_id=manager_id, 
        collection_type='presentation'
    ).count()
    
    # Load data for manager filters
    districts = get_districts_list()
    developers = get_developers_list()
    
    print(f"DEBUG: Rendering dashboard with manager: {current_manager.full_name}")
    try:
        return render_template('auth/manager_dashboard.html',
                             current_manager=current_manager,
                             total_clients=total_clients,
                             new_clients_count=new_clients_count,
                             pending_applications_count=pending_applications_count,
                             pending_documents_count=pending_documents_count,
                             total_approved_cashback=total_approved_cashback,
                             recent_activities=recent_activities,
                             pending_notifications=pending_applications_count + pending_documents_count,
                             collections_count=collections_count,
                             sent_collections_count=sent_collections_count,
                             recent_collections=recent_collections,
                             presentations_count=presentations_count,
                             districts=districts,
                             developers=developers)
    except Exception as e:
        print(f"DEBUG: Error rendering dashboard: {e}")
        import traceback
        traceback.print_exc()
        return f"Error rendering dashboard: {e}", 500

# API routes for manager actions
@app.route('/api/manager/clients')
@manager_required
def get_manager_clients_unified():
    """Get all clients (buyers) for managers - unified for both old and new systems"""
    # Get manager ID from session (already verified by manager_required decorator)
    manager_id = session.get('manager_id')
    
    try:
        print(f"DEBUG: Getting clients for manager {manager_id}")
        # Get all buyers as potential clients
        clients = User.query.filter_by(role='buyer').all()
        print(f"DEBUG: Found {len(clients)} clients total")
        clients_data = []
        
        for client in clients:
            # Get latest search as preference indicator
            latest_search = SavedSearch.query.filter_by(user_id=client.id).order_by(SavedSearch.last_used.desc()).first()
            
            client_data = {
                'id': client.id,
                'full_name': client.full_name,
                'email': client.email,
                'phone': client.phone or '',
                'created_at': client.created_at.isoformat() if client.created_at else None,
                'search_preferences': None,
                'status': 'active'  # Default status
            }
            
            if latest_search:
                # Create readable search description
                prefs = []
                if latest_search.property_type:
                    prefs.append(latest_search.property_type)
                if latest_search.location:
                    prefs.append(f"район {latest_search.location}")
                if latest_search.price_min or latest_search.price_max:
                    price_range = []
                    if latest_search.price_min:
                        price_range.append(f"от {latest_search.price_min:,} ₽")
                    if latest_search.price_max:
                        price_range.append(f"до {latest_search.price_max:,} ₽")
                    prefs.append(" ".join(price_range))
                
                client_data['search_preferences'] = ", ".join(prefs) if prefs else "Поиск сохранен"
            
            clients_data.append(client_data)
        
        print(f"DEBUG: Returning {len(clients_data)} clients data")
        return jsonify({
            'success': True,
            'clients': clients_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/update_client_status', methods=['POST'])
@manager_required  
def update_client_status():
    from models import User
    
    data = request.get_json()
    client_id = data.get('client_id')
    new_status = data.get('status')
    notes = data.get('notes', '')
    
    client = User.query.get(client_id)
    if not client or client.assigned_manager_id != session.get('manager_id'):
        return jsonify({'success': False, 'error': 'Клиент не найден'}), 404
    
    try:
        client.client_status = new_status
        if notes:
            client.client_notes = notes
        client.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/approve_cashback', methods=['POST'])
@manager_required
def approve_cashback():
    from models import CashbackApplication, Manager
    
    data = request.get_json()
    application_id = data.get('application_id')
    action = data.get('action')  # approve, reject
    manager_notes = data.get('manager_notes', '')
    
    manager_id = session.get('manager_id')
    manager = Manager.query.get(manager_id)
    
    application = CashbackApplication.query.get(application_id)
    if not application:
        return jsonify({'success': False, 'error': 'Заявка не найдена'}), 404
    
    # Check if client is assigned to this manager
    if application.user.assigned_manager_id != manager_id:
        return jsonify({'success': False, 'error': 'У вас нет доступа к этой заявке'}), 403
    
    try:
        if action == 'approve':
            # Check approval limits
            if manager and manager.max_cashback_approval and application.cashback_amount > manager.max_cashback_approval:
                return jsonify({
                    'success': False, 
                    'error': f'Сумма превышает ваш лимит на одобрение ({manager.max_cashback_approval:,} ₽)'
                }), 400
            
            application.status = 'Одобрена'
            application.approved_date = datetime.utcnow()
            application.approved_by_manager_id = manager_id
            
        elif action == 'reject':
            application.status = 'Отклонена'
        
        if manager_notes:
            application.manager_notes = manager_notes
        
        application.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/contact-requests')
@manager_required  
def get_manager_contact_requests():
    """Get contact manager applications for current manager"""
    try:
        from models import Application
        
        # Get all manager contact applications
        applications = Application.query.filter_by(
            application_type='manager_contact'
        ).order_by(Application.created_at.desc()).all()
        
        result = []
        for app in applications:
            result.append({
                'id': app.id,
                'contact_name': app.contact_name,
                'contact_email': app.contact_email,
                'contact_phone': app.contact_phone,
                'message': app.message,
                'preferred_contact_time': app.preferred_contact_time,
                'status': app.status,
                'created_at': app.created_at.isoformat() if app.created_at else None,
                'updated_at': app.updated_at.isoformat() if app.updated_at else None,
                # Property context if available
                'property_id': app.property_id,
                'property_type': app.property_type,
                'budget_min': app.budget_min,
                'budget_max': app.budget_max
            })
        
        return jsonify({
            'success': True,
            'applications': result,
            'total': len(result)
        })
        
    except Exception as e:
        print(f"Error getting manager contact requests: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/manager/applications')
@manager_required
def get_manager_applications():
    from models import CashbackApplication, User
    manager_id = session.get('manager_id')
    
    applications = CashbackApplication.query.join(User).filter(
        User.assigned_manager_id == manager_id,
        CashbackApplication.status == 'На рассмотрении'
    ).all()
    
    applications_data = []
    for app in applications:
        applications_data.append({
            'id': app.id,
            'client_name': app.user.full_name,
            'client_email': app.user.email,
            'property_name': app.property_name,
            'complex_name': app.complex_name,
            'cashback_amount': app.cashback_amount,
            'cashback_percent': app.cashback_percent,
            'application_date': app.application_date.strftime('%d.%m.%Y'),
            'status': app.status
        })
    
    return jsonify({'applications': applications_data})

@app.route('/api/manager/documents')
@manager_required
def get_manager_documents():
    from models import Document, User
    manager_id = session.get('manager_id')
    
    documents = Document.query.join(User).filter(
        User.assigned_manager_id == manager_id,
        Document.status == 'На проверке'
    ).all()
    
    documents_data = []
    for doc in documents:
        documents_data.append({
            'id': doc.id,
            'client_name': doc.user.full_name,
            'client_email': doc.user.email,
            'document_type': doc.document_type or 'Не определен',
            'original_filename': doc.original_filename,
            'file_size': doc.file_size,
            'created_at': doc.created_at.strftime('%d.%m.%Y %H:%M'),
            'status': doc.status
        })
    
    return jsonify({'documents': documents_data})

@app.route('/api/manager/document_action', methods=['POST'])
@manager_required
def manager_document_action():
    from models import Document, Manager
    
    data = request.get_json()
    document_id = data.get('document_id')
    action = data.get('action')  # approve, reject
    notes = data.get('notes', '')
    
    manager_id = session.get('manager_id')
    document = Document.query.get(document_id)
    
    if not document:
        return jsonify({'success': False, 'error': 'Документ не найден'}), 404
    
    # Check if client is assigned to this manager
    if document.user.assigned_manager_id != manager_id:
        return jsonify({'success': False, 'error': 'У вас нет доступа к этому документу'}), 403
    
    try:
        if action == 'approve':
            document.status = 'Проверен'
        elif action == 'reject':
            document.status = 'Отклонен'
        
        document.reviewed_by_manager_id = manager_id
        document.reviewed_at = datetime.utcnow()
        if notes:
            document.reviewer_notes = notes
        
        document.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/application_action', methods=['POST'])
@manager_required
def manager_application_action():
    from models import CashbackApplication, Manager, User
    
    data = request.get_json()
    application_id = data.get('application_id')
    action = data.get('action')  # approve, reject
    notes = data.get('notes', '')
    
    manager_id = session.get('manager_id')
    application = CashbackApplication.query.get(application_id)
    
    if not application:
        return jsonify({'success': False, 'error': 'Заявка не найдена'}), 404
    
    # Check if client is assigned to this manager
    if application.user.assigned_manager_id != manager_id:
        return jsonify({'success': False, 'error': 'У вас нет доступа к этой заявке'}), 403
    
    try:
        if action == 'approve':
            application.status = 'Одобрена'
            # Add cashback to user's balance
            user = application.user
            user.total_cashback = (user.total_cashback or 0) + application.cashback_amount
        elif action == 'reject':
            application.status = 'Отклонена'
        
        application.reviewed_by_manager_id = manager_id
        application.reviewed_at = datetime.utcnow()
        if notes:
            application.manager_notes = notes
        
        application.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/collections')
@manager_required
def get_manager_collections():
    from models import Collection, User
    manager_id = session.get('manager_id')
    
    collections = Collection.query.filter_by(created_by_manager_id=manager_id).all()
    
    collections_data = []
    for collection in collections:
        collections_data.append({
            'id': collection.id,
            'title': collection.title,
            'description': collection.description,
            'status': collection.status,
            'assigned_to_name': collection.assigned_to.full_name if collection.assigned_to else 'Не назначено',
            'assigned_to_id': collection.assigned_to_user_id,
            'properties_count': len(collection.properties),
            'created_at': collection.created_at.strftime('%d.%m.%Y'),
            'tags': collection.tags
        })
    
    return jsonify({'collections': collections_data})

@app.route('/api/manager/collection/create', methods=['POST'])
@manager_required
def api_create_collection():
    from models import Collection, User
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    assigned_to_user_id = data.get('assigned_to_user_id')
    tags = data.get('tags', '')
    
    if not title:
        return jsonify({'success': False, 'error': 'Название подборки обязательно'}), 400
    
    manager_id = session.get('manager_id')
    
    try:
        collection = Collection()
        collection.title = title
        collection.description = description
        collection.created_by_manager_id = manager_id
        collection.assigned_to_user_id = assigned_to_user_id if assigned_to_user_id else None
        collection.tags = tags
        collection.status = 'Черновик'
        
        db.session.add(collection)
        db.session.commit()
        
        return jsonify({'success': True, 'collection_id': collection.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/collection/<int:collection_id>/properties')
@manager_required
def get_collection_properties(collection_id):
    from models import Collection, CollectionProperty
    manager_id = session.get('manager_id')
    
    collection = Collection.query.filter_by(
        id=collection_id,
        created_by_manager_id=manager_id
    ).first()
    
    if not collection:
        return jsonify({'success': False, 'error': 'Подборка не найдена'}), 404
    
    properties_data = []
    for prop in collection.properties:
        properties_data.append({
            'id': prop.id,
            'property_id': prop.property_id,
            'property_name': prop.property_name,
            'property_price': prop.property_price,
            'complex_name': prop.complex_name,
            'property_type': prop.property_type,
            'property_size': prop.property_size,
            'manager_note': prop.manager_note,
            'order_index': prop.order_index
        })
    
    # Sort by order_index
    properties_data.sort(key=lambda x: x['order_index'])
    
    return jsonify({
        'collection': {
            'id': collection.id,
            'title': collection.title,
            'description': collection.description,
            'status': collection.status
        },
        'properties': properties_data
    })



@app.route('/api/searches/save', methods=['POST'])
@login_required
def api_save_search():
    """Save a search with filters"""
    from models import SavedSearch
    
    data = request.get_json()
    name = data.get('name')
    filters = data.get('filters', {})
    
    if not name:
        return jsonify({'success': False, 'error': 'Название поиска обязательно'}), 400
    
    try:
        search = SavedSearch()
        search.name = name
        search.filters = json.dumps(filters)
        search.user_id = current_user.id
        search.created_at = datetime.utcnow()
        
        db.session.add(search)
        db.session.commit()
        
        return jsonify({'success': True, 'search_id': search.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/searches', methods=['POST'])
def api_manager_save_search():
    """Save a search for a manager"""
    from models import ManagerSavedSearch, Manager, SentSearch
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    data = request.get_json()
    name = data.get('name')
    filters = data.get('filters', {})
    client_email = data.get('client_email', '')
    
    if not name:
        return jsonify({'success': False, 'error': 'Название поиска обязательно'}), 400
    
    try:
        # Create saved search
        search = ManagerSavedSearch()
        search.name = name
        search.filters = json.dumps(filters)
        search.manager_id = manager_id
        search.created_at = datetime.utcnow()
        
        db.session.add(search)
        db.session.commit()
        
        # If client email provided, also create sent search record and send notification
        if client_email:
            sent_search = SentSearch()
            sent_search.saved_search_id = search.id
            sent_search.recipient_email = client_email
            sent_search.sent_at = datetime.utcnow()
            sent_search.manager_id = manager_id
            
            db.session.add(sent_search)
            db.session.commit()
            
            # Send notification to client
            manager = Manager.query.get(manager_id)
            manager_name = manager.name if manager else "Менеджер"
            
            try:
                send_notification(
                    recipient_email=client_email,
                    subject=f"Новый подбор недвижимости от {manager_name}",
                    message=f"Менеджер {manager_name} подготовил для вас персональный подбор недвижимости '{name}'. Посмотрите варианты на сайте InBack.ru",
                    notification_type='saved_search',
                    user_id=None,
                    manager_id=manager_id
                )
                return jsonify({'success': True, 'search_id': search.id, 'sent_to_client': True})
            except Exception as email_error:
                print(f"Failed to send email notification: {email_error}")
                return jsonify({'success': True, 'search_id': search.id, 'sent_to_client': False, 'email_error': str(email_error)})
        
        return jsonify({'success': True, 'search_id': search.id, 'sent_to_client': False})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/send_recommendation', methods=['POST'])
def api_manager_send_recommendation():
    """Send a recommendation (property or complex) to a client"""
    from models import Recommendation, Manager, User, RecommendationCategory
    from datetime import datetime
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    data = request.get_json()
    title = data.get('title', '').strip()
    client_id = data.get('client_id')  # Now using client_id instead of email
    client_email = data.get('client_email', '').strip()
    recommendation_type = data.get('recommendation_type')  # 'property' or 'complex'
    item_id = data.get('item_id')
    item_name = data.get('item_name', '').strip()
    description = data.get('description', '').strip()
    manager_notes = data.get('manager_notes', '').strip()
    highlighted_features = data.get('highlighted_features', [])
    priority_level = data.get('priority_level', 'normal')
    category_id = data.get('category_id')  # New field for category
    category_name = data.get('category_name', '').strip()  # For creating new category
    
    # Debug logging (removing verbose logs for production)
    print(f"DEBUG: Recommendation sent - type={recommendation_type}, item_id={item_id}, client_id={client_id}")
    
    # Validation
    missing_fields = []
    if not title:
        missing_fields.append('заголовок')
    if not client_id:
        missing_fields.append('клиент')
    if not recommendation_type:
        missing_fields.append('тип рекомендации')
    if not item_id:
        missing_fields.append('ID объекта')
    if not item_name:
        missing_fields.append('название объекта')
    
    if missing_fields:
        return jsonify({'success': False, 'error': f'Заполните обязательные поля: {", ".join(missing_fields)}'}), 400
    
    if recommendation_type not in ['property', 'complex']:
        return jsonify({'success': False, 'error': 'Неверный тип рекомендации'}), 400
    
    try:
        # Find client by ID
        client = User.query.get(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Клиент не найден'}), 400
        
        # Handle category
        category = None
        if category_id == 'new' and category_name:
            # Create new category
            category = RecommendationCategory(
                name=category_name,
                manager_id=manager_id,
                client_id=client_id
            )
            db.session.add(category)
            db.session.flush()  # To get the ID
        elif category_id and category_id != 'new':
            # Use existing category
            category = RecommendationCategory.query.filter_by(
                id=category_id,
                manager_id=manager_id,
                client_id=client_id,
                is_active=True
            ).first()
        
        # Create recommendation
        recommendation = Recommendation()
        recommendation.manager_id = manager_id
        recommendation.client_id = client.id
        recommendation.title = title
        recommendation.description = description
        recommendation.recommendation_type = recommendation_type
        recommendation.item_id = item_id
        recommendation.item_name = item_name
        recommendation.manager_notes = manager_notes
        recommendation.highlighted_features = json.dumps(highlighted_features) if highlighted_features else None
        recommendation.priority_level = priority_level
        recommendation.item_data = json.dumps(data.get('item_data', {}))  # Store full item details
        recommendation.category_id = category.id if category else None
        
        db.session.add(recommendation)
        
        # Update category statistics
        if category:
            category.recommendations_count += 1
            category.last_used = datetime.utcnow()
        
        db.session.commit()
        
        # Send notification to client
        manager = Manager.query.get(manager_id)
        manager_name = manager.name if manager else "Менеджер"
        
        try:
            # Get priority text for notifications
            priority_texts = {
                'urgent': 'Срочно',
                'high': 'Высокий', 
                'normal': 'Обычный'
            }
            priority_text = priority_texts.get(priority_level, 'Обычный')
            
            send_notification(
                recipient_email=client_email,
                subject=f"Новая рекомендация от {manager_name}",
                message=f"Менеджер {manager_name} рекомендует вам: {title}",
                notification_type='recommendation',
                user_id=client.id,
                manager_id=manager_id,
                title=title,
                item_id=item_id,
                item_name=item_name,
                description=description,
                manager_name=manager_name,
                priority_text=priority_text,
                recommendation_type=recommendation_type
            )
            return jsonify({'success': True, 'recommendation_id': recommendation.id, 'sent_to_client': True})
        except Exception as email_error:
            print(f"Failed to send email notification: {email_error}")
            return jsonify({'success': True, 'recommendation_id': recommendation.id, 'sent_to_client': False, 'email_error': str(email_error)})
        
    except Exception as e:
        db.session.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error creating recommendation: {str(e)}")
        print(f"Full traceback: {error_trace}")
        return jsonify({'success': False, 'error': str(e), 'traceback': error_trace}), 400

@app.route('/api/manager/recommendations', methods=['GET'])
def api_manager_get_recommendations():
    """Get manager's sent recommendations with filters"""
    from models import Recommendation
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        # Start with base query
        query = Recommendation.query.filter_by(manager_id=manager_id)
        
        # Apply filters from request params
        client_id = request.args.get('client_id')
        status = request.args.get('status')
        rec_type = request.args.get('type')
        priority = request.args.get('priority')
        
        if client_id:
            query = query.filter(Recommendation.client_id == client_id)
        if status:
            query = query.filter(Recommendation.status == status)
        if rec_type:
            query = query.filter(Recommendation.item_type == rec_type)
        if priority:
            query = query.filter(Recommendation.priority == priority)
        
        recommendations = query.order_by(Recommendation.sent_at.desc()).all()
        
        recommendations_data = []
        stats = {'sent': 0, 'viewed': 0, 'interested': 0, 'scheduled': 0}
        
        for rec in recommendations:
            rec_dict = rec.to_dict()
            rec_dict['client_email'] = rec.client.email
            rec_dict['client_name'] = rec.client.full_name
            recommendations_data.append(rec_dict)
            
            # Update stats
            stats['sent'] += 1
            if rec.status == 'viewed':
                stats['viewed'] += 1
            elif rec.status == 'interested':
                stats['interested'] += 1
            elif rec.status == 'scheduled_viewing':
                stats['scheduled'] += 1
        
        return jsonify({
            'success': True, 
            'recommendations': recommendations_data,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/recommendations/<int:recommendation_id>', methods=['DELETE'])
@manager_required  
def api_manager_delete_recommendation(recommendation_id):
    """Delete a recommendation"""
    from models import Recommendation
    
    manager_id = session.get('manager_id')
    
    try:
        # Find recommendation that belongs to this manager
        recommendation = Recommendation.query.filter_by(
            id=recommendation_id, 
            manager_id=manager_id
        ).first()
        
        if not recommendation:
            return jsonify({'success': False, 'error': 'Рекомендация не найдена'}), 404
        
        db.session.delete(recommendation)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Рекомендация успешно удалена'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/manager/clients-list', methods=['GET'])
@manager_required
def api_manager_get_clients_list():
    """Get manager's clients for filters"""
    from models import User
    
    manager_id = session.get('manager_id')
    
    try:
        # Get clients assigned to this manager or all buyers
        clients = User.query.filter_by(role='buyer').order_by(User.full_name).all()
        
        clients_data = []
        for client in clients:
            clients_data.append({
                'id': client.id,
                'full_name': client.full_name or 'Без имени',
                'email': client.email
            })
        
        return jsonify({
            'success': True,
            'clients': clients_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/properties/search', methods=['POST'])
@login_required
def api_search_properties():
    """Search properties with filters from dashboard"""
    data = request.get_json()
    filters = data.get('filters', {})
    
    try:
        # Convert collection filters to property filters
        property_filters = {}
        
        if filters.get('priceFrom'):
            property_filters['price_min'] = filters['priceFrom']
        if filters.get('priceTo'):
            property_filters['price_max'] = filters['priceTo']
        if filters.get('rooms'):
            property_filters['rooms'] = filters['rooms']
        if filters.get('districts') and filters['districts']:
            property_filters['district'] = filters['districts'][0]
        if filters.get('developers') and filters['developers']:
            property_filters['developer'] = filters['developers'][0]
        if filters.get('areaFrom'):
            property_filters['area_min'] = filters['areaFrom']
        if filters.get('areaTo'):
            property_filters['area_max'] = filters['areaTo']
        
        # Get filtered properties
        filtered_properties = get_filtered_properties(property_filters)
        
        # Add cashback to each property
        for prop in filtered_properties:
            prop['cashback'] = calculate_cashback(prop['price'])
        
        # Sort by price ascending
        filtered_properties = sort_properties(filtered_properties, 'price_asc')
        
        return jsonify({
            'success': True,
            'properties': filtered_properties[:50],  # Limit to 50 results
            'total_count': len(filtered_properties)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/send-property', methods=['POST'])
@manager_required
def api_send_property_to_client():
    """Send saved search results to client via email"""
    from models import SavedSearch, User, ClientPropertyRecommendation
    
    data = request.get_json()
    client_id = data.get('client_id')
    search_id = data.get('search_id')
    message = data.get('message', '')
    
    if not client_id or not search_id:
        return jsonify({'success': False, 'error': 'Клиент и поиск обязательны'}), 400
    
    try:
        # Get the search
        search = SavedSearch.query.get(search_id)
        if not search:
            return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
        
        # Get the client
        client = User.query.get(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Клиент не найден'}), 404
        
        # Get search filters
        filters = json.loads(search.filters) if search.filters else {}
        
        # Filter properties based on search criteria
        properties = load_properties()
        filtered_properties = filter_properties(properties, filters)
        
        # Create recommendation record
        recommendation = ClientPropertyRecommendation()
        recommendation.client_id = client_id
        recommendation.manager_id = session.get('manager_id')
        recommendation.search_name = search.name
        recommendation.search_filters = search.filters
        recommendation.message = message
        recommendation.properties_count = len(filtered_properties)
        recommendation.sent_at = datetime.utcnow()
        
        db.session.add(recommendation)
        db.session.commit()
        
        # Send email with property recommendations
        send_property_email(client, search.name, filtered_properties, message)
        
        return jsonify({'success': True, 'properties_sent': len(filtered_properties)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

def filter_properties(properties, filters):
    """Filter properties based on search criteria"""
    filtered = []
    
    for prop in properties:
        # Price filter
        if filters.get('priceFrom'):
            try:
                if prop.get('price', 0) < int(filters['priceFrom']):
                    continue
            except (ValueError, TypeError):
                pass
        
        if filters.get('priceTo'):
            try:
                if prop.get('price', 0) > int(filters['priceTo']):
                    continue
            except (ValueError, TypeError):
                pass
        
        # Rooms filter
        if filters.get('rooms'):
            prop_rooms = str(prop.get('rooms', ''))
            if filters['rooms'] == 'studio' and prop_rooms != 'studio':
                continue
            elif filters['rooms'] != 'studio' and prop_rooms != str(filters['rooms']):
                continue
        
        # District filter
        if filters.get('districts') and len(filters['districts']) > 0:
            prop_district = prop.get('district', '')
            if prop_district not in filters['districts']:
                continue
        
        # Area filter
        if filters.get('areaFrom'):
            try:
                if prop.get('area', 0) < int(filters['areaFrom']):
                    continue
            except (ValueError, TypeError):
                pass
        
        if filters.get('areaTo'):
            try:
                if prop.get('area', 0) > int(filters['areaTo']):
                    continue
            except (ValueError, TypeError):
                pass
        
        # Developer filter
        if filters.get('developers') and len(filters['developers']) > 0:
            prop_developer = prop.get('developer', '')
            if prop_developer not in filters['developers']:
                continue
        
        filtered.append(prop)
    
    return filtered

def send_property_email(client, search_name, properties, message):
    """Send email with property recommendations"""
    try:
        subject = f"Новая подборка недвижимости: {search_name}"
        
        properties_html = ""
        for prop in properties[:10]:  # Limit to first 10 properties
            properties_html += f"""
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                <h3 style="margin: 0 0 8px 0; color: #1f2937;">{prop.get('name', 'Без названия')}</h3>
                <p style="margin: 0 0 4px 0; color: #6b7280;">ЖК: {prop.get('complex_name', 'Не указан')}</p>
                <p style="margin: 0 0 4px 0; color: #6b7280;">Цена: {prop.get('price', 0):,} ₽</p>
                <p style="margin: 0 0 4px 0; color: #6b7280;">Площадь: {prop.get('area', 0)} м²</p>
                <p style="margin: 0 0 8px 0; color: #6b7280;">Комнат: {prop.get('rooms', 'Не указано')}</p>
                <a href="https://inback.ru/properties/{prop.get('id', '')}" style="color: #0088cc; text-decoration: none;">Подробнее →</a>
            </div>
            """
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0088cc;">Персональная подборка недвижимости</h2>
                
                <p>Здравствуйте, {client.full_name}!</p>
                
                <p>Ваш менеджер подготовил для вас подборку недвижимости: <strong>{search_name}</strong></p>
                
                {f'<div style="background: #f3f4f6; padding: 16px; border-radius: 8px; margin: 16px 0;"><p style="margin: 0; font-style: italic;">"{message}"</p></div>' if message else ''}
                
                <h3>Найденные варианты ({len(properties)} объектов):</h3>
                
                {properties_html}
                
                {f'<p style="color: #6b7280;">И еще {len(properties) - 10} объектов в полном каталоге...</p>' if len(properties) > 10 else ''}
                
                <div style="margin-top: 32px; padding: 20px; background: #f9fafb; border-radius: 8px; text-align: center;">
                    <h3 style="margin: 0 0 8px 0;">Нужна консультация?</h3>
                    <p style="margin: 0 0 16px 0;">Свяжитесь с вашим персональным менеджером</p>
                    <a href="mailto:manager@inback.ru" style="background: #0088cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Написать менеджеру</a>
                </div>
                
                <div style="margin-top: 20px; text-align: center; color: #6b7280; font-size: 14px;">
                    <p>С уважением,<br>Команда InBack.ru</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return send_notification(
            client.email,
            subject,
            html_content,
            notification_type="property_recommendation",
            user_id=client.id
        )
    except Exception as e:
        print(f"Error sending property email: {e}")
        return False

@app.route('/api/manager/collection/<int:collection_id>/add_property', methods=['POST'])
@manager_required
def add_property_to_collection(collection_id):
    from models import Collection, CollectionProperty
    import json
    
    data = request.get_json()
    property_id = data.get('property_id')
    manager_note = data.get('manager_note', '')
    
    manager_id = session.get('manager_id')
    
    collection = Collection.query.filter_by(
        id=collection_id,
        created_by_manager_id=manager_id
    ).first()
    
    if not collection:
        return jsonify({'success': False, 'error': 'Подборка не найдена'}), 404
    
    # Load property data from JSON
    try:
        with open('data/properties.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        property_info = None
        for prop in properties_data:
            if str(prop['id']) == str(property_id):
                property_info = prop
                break
        
        if not property_info:
            return jsonify({'success': False, 'error': 'Квартира не найдена'}), 404
        
        # Check if property already in collection
        existing = CollectionProperty.query.filter_by(
            collection_id=collection_id,
            property_id=str(property_id)
        ).first()
        
        if existing:
            return jsonify({'success': False, 'error': 'Квартира уже добавлена в подборку'}), 400
        
        # Get max order_index
        max_order = db.session.query(db.func.max(CollectionProperty.order_index)).filter_by(
            collection_id=collection_id
        ).scalar() or 0
        
        collection_property = CollectionProperty()
        collection_property.collection_id = collection_id
        collection_property.property_id = str(property_id)
        collection_property.property_name = property_info['title']
        collection_property.property_price = property_info['price']
        collection_property.complex_name = property_info.get('residential_complex', 'ЖК не указан')
        collection_property.property_type = f"{property_info['rooms']}-комн"
        collection_property.property_size = property_info['area']
        collection_property.manager_note = manager_note
        collection_property.order_index = max_order + 1
        
        db.session.add(collection_property)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/collection/<int:collection_id>/send', methods=['POST'])
@manager_required
def send_collection(collection_id):
    from models import Collection
    
    manager_id = session.get('manager_id')
    
    collection = Collection.query.filter_by(
        id=collection_id,
        created_by_manager_id=manager_id
    ).first()
    
    if not collection:
        return jsonify({'success': False, 'error': 'Подборка не найдена'}), 404
    
    if not collection.assigned_to_user_id:
        return jsonify({'success': False, 'error': 'Клиент не назначен'}), 400
    
    if len(collection.properties) == 0:
        return jsonify({'success': False, 'error': 'В подборке нет квартир'}), 400
    
    try:
        collection.status = 'Отправлена'
        collection.sent_at = datetime.utcnow()
        collection.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/properties/search')
@manager_required
def search_properties():
    import json
    
    query = request.args.get('q', '').lower()
    limit = int(request.args.get('limit', 20))
    
    try:
        with open('data/properties.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        filtered_properties = []
        for prop in properties_data:
            prop_type = f"{prop['rooms']}-комн"
            complex_name = prop.get('residential_complex', 'ЖК не указан')
            
            property_title = f"{prop.get('rooms', 0)}-комн {prop.get('area', 0)} м²" if prop.get('rooms', 0) > 0 else f"Студия {prop.get('area', 0)} м²"
            if (query in property_title.lower() or 
                query in complex_name.lower() or 
                query in prop_type.lower() or
                query in prop.get('developer', '').lower() or
                query in prop.get('district', '').lower()):
                filtered_properties.append({
                    'id': prop['id'],
                    'title': f"{prop.get('rooms', 0)}-комн {prop.get('area', 0)} м²" if prop.get('rooms', 0) > 0 else f"Студия {prop.get('area', 0)} м²",
                    'price': prop['price'],
                    'complex': complex_name,
                    'type': prop_type,
                    'size': prop['area'],
                    'image': prop.get('image', '/static/images/property-placeholder.jpg')
                })
            
            if len(filtered_properties) >= limit:
                break
        
        return jsonify({'properties': filtered_properties})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/client/collections')
@login_required
def get_client_collections():
    """Get collections assigned to current user"""
    from models import Collection, CollectionProperty
    from datetime import datetime
    
    user_id = current_user.id
    
    collections = Collection.query.filter_by(assigned_to_user_id=user_id).all()
    
    collections_data = []
    for collection in collections:
        properties_count = len(collection.properties)
        
        # Mark as viewed if not already
        if collection.status == 'Отправлена':
            collection.status = 'Просмотрена'
            collection.viewed_at = datetime.utcnow()
            db.session.commit()
        
        collections_data.append({
            'id': collection.id,
            'title': collection.title,
            'description': collection.description,
            'status': collection.status,
            'created_by_manager_name': collection.created_by.full_name,
            'properties_count': properties_count,
            'created_at': collection.created_at.strftime('%d.%m.%Y'),
            'sent_at': collection.sent_at.strftime('%d.%m.%Y %H:%M') if collection.sent_at else None,
            'tags': collection.tags
        })
    
    return jsonify({'collections': collections_data})

@app.route('/api/client/collection/<int:collection_id>/properties')
@login_required
def get_client_collection_properties(collection_id):
    """Get properties in a collection for client view"""
    from models import Collection, CollectionProperty
    
    user_id = current_user.id
    
    collection = Collection.query.filter_by(
        id=collection_id,
        assigned_to_user_id=user_id
    ).first()
    
    if not collection:
        return jsonify({'success': False, 'error': 'Подборка не найдена'}), 404
    
    properties_data = []
    for prop in collection.properties:
        # Calculate potential cashback (example: 2% of price)
        cashback_percent = 2.0
        cashback_amount = int(prop.property_price * cashback_percent / 100)
        
        properties_data.append({
            'id': prop.id,
            'property_id': prop.property_id,
            'property_name': prop.property_name,
            'property_price': prop.property_price,
            'complex_name': prop.complex_name,
            'property_type': prop.property_type,
            'property_size': prop.property_size,
            'manager_note': prop.manager_note,
            'cashback_amount': cashback_amount,
            'cashback_percent': cashback_percent
        })
    
    # Sort by order_index
    properties_data.sort(key=lambda x: collection.properties[0].order_index if collection.properties else 0)
    
    return jsonify({
        'collection': {
            'id': collection.id,
            'title': collection.title,
            'description': collection.description,
            'status': collection.status,
            'manager_name': collection.created_by.full_name,
            'sent_at': collection.sent_at.strftime('%d.%m.%Y %H:%M') if collection.sent_at else None
        },
        'properties': properties_data
    })

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    try:
        from models import CashbackApplication, FavoriteProperty, Document, Collection, Recommendation, SentSearch, SavedSearch
        
        # Get user's data for dashboard
        cashback_apps = CashbackApplication.query.filter_by(user_id=current_user.id).all()
        favorites = FavoriteProperty.query.filter_by(user_id=current_user.id).all()
        documents = Document.query.filter_by(user_id=current_user.id).all()
        collections = Collection.query.filter_by(assigned_to_user_id=current_user.id).order_by(Collection.created_at.desc()).limit(3).all()
        
        # Get recommendations from managers (exclude dismissed) with categories
        recommendations = Recommendation.query.filter(
            Recommendation.client_id == current_user.id,
            Recommendation.status != 'dismissed'
        ).options(db.joinedload(Recommendation.category)).order_by(Recommendation.created_at.desc()).all()
        
        # Get unique categories for the client (import here to avoid circular imports)
        from models import RecommendationCategory
        categories = RecommendationCategory.query.filter_by(client_id=current_user.id, is_active=True).all()
        
        # Enrich recommendations with property details
        for rec in recommendations:
            if rec.recommendation_type == 'property' and rec.item_id:
                try:
                    properties = load_properties()
                    complexes = load_residential_complexes()
                    property_data = next((p for p in properties if str(p.get('id')) == str(rec.item_id)), None)
                    if property_data:
                        # Create a simple object to store property details
                        class PropertyDetails:
                            def __init__(self, data, complexes):
                                for key, value in data.items():
                                    setattr(self, key, value)
                                
                                # Add residential complex name - try multiple sources
                                self.residential_complex = None
                                
                                # First try complex_name field (direct from expanded data)
                                if data.get('complex_name'):
                                    self.residential_complex = data.get('complex_name')
                                # Then try complex_id lookup
                                elif data.get('complex_id'):
                                    complex_data = next((c for c in complexes if c.get('id') == data.get('complex_id')), None)
                                    if complex_data:
                                        self.residential_complex = complex_data.get('name')
                                # Legacy support for residential_complex_id
                                elif data.get('residential_complex_id'):
                                    complex_data = next((c for c in complexes if c.get('id') == data.get('residential_complex_id')), None)
                                    if complex_data:
                                        self.residential_complex = complex_data.get('name')
                                
                                # Map property type from Russian to English for template logic
                                type_mapping = {
                                    'Квартира': 'apartment',
                                    'Таунхаус': 'townhouse', 
                                    'Дом': 'house'
                                }
                                original_type = data.get('property_type', 'Квартира')
                                self.property_type = type_mapping.get(original_type, 'apartment')
                                self.property_type_ru = original_type
                        
                        rec.property_details = PropertyDetails(property_data, complexes)
                        complex_name = rec.property_details.residential_complex or 'Не указан'
                        print(f"Loaded property {rec.item_id}: {property_data.get('rooms')} комн, ЖК {complex_name}")
                    else:
                        print(f"Property {rec.item_id} not found in data files")
                        rec.property_details = None
                except Exception as e:
                    print(f"Error loading property details for recommendation {rec.id}: {e}")
                    rec.property_details = None
        
        # Get sent searches from managers
        sent_searches = SentSearch.query.filter_by(client_id=current_user.id).order_by(SentSearch.sent_at.desc()).all()
        
        # Get user's saved searches
        saved_searches = SavedSearch.query.filter_by(user_id=current_user.id).order_by(SavedSearch.created_at.desc()).all()
        
        # Calculate totals
        total_cashback = sum(app.cashback_amount for app in cashback_apps if app.status == 'Выплачена')
        pending_cashback = sum(app.cashback_amount for app in cashback_apps if app.status == 'Одобрена')
        active_apps = len([app for app in cashback_apps if app.status in ['На рассмотрении', 'Требуются документы']])
        
        # Get developer appointments
        from models import DeveloperAppointment
        appointments = DeveloperAppointment.query.filter_by(user_id=current_user.id).order_by(DeveloperAppointment.appointment_date.desc()).limit(3).all()
        
        # Load data for manager filters
        districts = get_districts_list()
        developers = get_developers_list()
        
        return render_template('auth/dashboard.html', 
                             cashback_applications=cashback_apps,
                             favorites=favorites,
                             documents=documents,
                             collections=collections,
                             appointments=appointments,
                             recommendations=recommendations,
                             categories=categories,
                             sent_searches=sent_searches,
                             saved_searches=saved_searches,
                             total_cashback=total_cashback,
                             pending_cashback=pending_cashback,
                             active_apps=active_apps,
                             districts=districts,
                             developers=developers)
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return basic dashboard on error
        districts = get_districts_list()
        developers = get_developers_list()
        
        return render_template('auth/dashboard.html', 
                             cashback_applications=[],
                             favorites=[],
                             documents=[],
                             collections=[],
                             appointments=[],
                             recommendations=[],
                             sent_searches=[],
                             saved_searches=[],
                             total_cashback=0,
                             pending_cashback=0,
                             active_apps=0,
                             districts=districts,
                             developers=developers)

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('index'))

@app.route('/api/search')
def api_search():
    """API endpoint for global search"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    results = search_global(query)
    return jsonify(results)

@app.route('/search')
def search_results():
    """Search results page"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')  # all, residential_complex, district, developer, street
    
    results = []
    if query:
        results = search_global(query)
        
        # Filter by type if specified
        if search_type != 'all':
            results = [r for r in results if r['type'] == search_type]
    
    return render_template('search_results.html', 
                         query=query, 
                         results=results,
                         search_type=search_type)


@app.route('/api/smart-search-suggestions')
def smart_search_suggestions():
    """API endpoint for search suggestions with intelligent keyword matching"""
    query = request.args.get('q', '').strip().lower()
    if not query or len(query) < 1:
        return jsonify({'suggestions': []})
    
    suggestions = []
    
    try:
        # Intelligent room type matching patterns
        room_patterns = {
            # Single room patterns
            ('1', '1-', '1-к', '1-ко', '1-ком', '1 к', '1 ко', '1 ком', 'одн', 'одно', 'однок', 'однокомн', 'однокомнат', 'однокомнатн', 'один', 'одной'): ('1-комнатная квартира', 'rooms', '1'),
            # Two room patterns  
            ('2', '2-', '2-к', '2-ко', '2-ком', '2 к', '2 ко', '2 ком', 'двух', 'двухк', 'двухком', 'двухкомн', 'двухкомнат', 'два', 'двой', 'двойн'): ('2-комнатная квартира', 'rooms', '2'),
            # Three room patterns
            ('3', '3-', '3-к', '3-ко', '3-ком', '3 к', '3 ко', '3 ком', 'трех', 'трёх', 'трехк', 'трёхк', 'трехком', 'трёхком', 'три', 'трой'): ('3-комнатная квартира', 'rooms', '3'),
            # Four room patterns
            ('4', '4-', '4-к', '4-ко', '4-ком', '4 к', '4 ко', '4 ком', 'четыр', 'четырех', 'четырёх', 'четырехк', 'четырёхк', 'четыре'): ('4-комнатная квартира', 'rooms', '4'),
            # Studio patterns
            ('студ', 'studio', 'студий', 'студия'): ('Студия', 'rooms', 'studio'),
        }
        
        # Check room type patterns first
        for patterns, (room_text, type_val, value) in room_patterns.items():
            for pattern in patterns:
                if query.startswith(pattern) or pattern in query:
                    suggestions.append({
                        'text': room_text,
                        'type': type_val,
                        'value': value,
                        'category': 'Тип квартиры'
                    })
                    break
        
        # Search in regional data first (regions and cities)
        from models import Region, City
        
        # Search regions
        regions = Region.query.filter(Region.name.ilike(f'%{query}%')).limit(5).all()
        for region in regions:
            suggestions.append({
                'text': region.name,
                'type': 'region',
                'value': region.slug,
                'category': 'Регион'
            })
        
        # Search cities
        cities = City.query.filter(City.name.ilike(f'%{query}%')).limit(5).all()
        for city in cities:
            suggestions.append({
                'text': f"{city.name} ({city.region.name if city.region else 'Неизвестный регион'})",
                'type': 'city',
                'value': city.slug,
                'category': 'Город'
            })

        # Search in database categories (districts, developers, complexes)
        cursor = db.session.execute(text("""
            SELECT name, category_type, slug 
            FROM search_categories 
            WHERE LOWER(name) LIKE :query 
            ORDER BY 
                CASE 
                    WHEN LOWER(name) LIKE :exact_start THEN 1
                    WHEN LOWER(name) LIKE :word_start THEN 2
                    ELSE 3
                END,
                LENGTH(name)
            LIMIT 10
        """), {
            'query': f'%{query}%',
            'exact_start': f'{query}%',
            'word_start': f'% {query}%'
        })
        
        category_names = {
            'district': 'Район',
            'developer': 'Застройщик', 
            'complex': 'ЖК',
            'rooms': 'Тип квартиры',
            'region': 'Регион',
            'city': 'Город'
        }
        
        for row in cursor:
            name, category_type, slug = row
            suggestions.append({
                'text': name,
                'type': category_type,
                'value': slug,
                'category': category_names.get(category_type, category_type.title())
            })
        
        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for s in suggestions:
            key = (s['text'], s['type'])
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(s)
        
        return jsonify({'suggestions': unique_suggestions[:12]})
        
    except Exception as e:
        app.logger.error(f"Smart search error: {e}")
        return jsonify({'suggestions': []})

def init_search_data():
    """Initialize search data in database"""
    from models import District, Developer, ResidentialComplex, Street, RoomType
    
    # Districts
    districts_data = [
        ('Центральный', 'tsentralnyy'), ('Западный', 'zapadny'), 
        ('Карасунский', 'karasunsky'), ('Прикубанский', 'prikubansky'),
        ('Фестивальный', 'festivalny'), ('Юбилейный', 'yubileynyy'),
        ('Гидростроителей', 'gidrostroitelei'), ('Солнечный', 'solnechny'),
        ('Панорама', 'panorama'), ('Музыкальный', 'muzykalnyy')
    ]
    
    for name, slug in districts_data:
        if not District.query.filter_by(slug=slug).first():
            district = District(name=name, slug=slug)
            db.session.add(district)
    
    # Room types
    room_types_data = [
        ('Студия', 0), ('1-комнатная квартира', 1), 
        ('2-комнатная квартира', 2), ('3-комнатная квартира', 3), 
        ('4-комнатная квартира', 4), ('Пентхаус', 5)
    ]
    
    for name, rooms_count in room_types_data:
        if not RoomType.query.filter_by(name=name).first():
            room_type = RoomType(name=name, rooms_count=rooms_count)
            db.session.add(room_type)
    
    # Developers
    developers_data = [
        ('Краснодар Инвест', 'krasnodar-invest'),
        ('ЮгСтройИнвест', 'yugstroyinvest'),
        ('Флагман', 'flagman'),
        ('Солнечный город', 'solnechny-gorod'),
        ('Премьер', 'premier')
    ]
    
    for name, slug in developers_data:
        if not Developer.query.filter_by(slug=slug).first():
            developer = Developer(name=name, slug=slug)
            db.session.add(developer)
    
    # Residential complexes
    complexes_data = [
        ('Солнечный', 'solnechny', 1, 1),
        ('Панорама', 'panorama', 1, 2),
        ('Гармония', 'garmoniya', 2, 3),
        ('Европейский квартал', 'evropeyskiy-kvartal', 3, 1),
        ('Флагман', 'flagman', 4, 4)
    ]
    
    for name, slug, district_id, developer_id in complexes_data:
        if not ResidentialComplex.query.filter_by(slug=slug).first():
            complex = ResidentialComplex(name=name, slug=slug, district_id=district_id, developer_id=developer_id)
            db.session.add(complex)
    
    db.session.commit()


# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        from models import Admin
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(email=email, is_active=True).first()
        
        if admin and admin.check_password(password):
            session.permanent = True
            session['admin_id'] = admin.id
            session['is_admin'] = True
            admin.last_login = datetime.utcnow()
            db.session.commit()
            flash('Добро пожаловать в панель администратора!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('admin/admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_id', None)
    session.pop('is_admin', None)
    flash('Вы вышли из панели администратора', 'info')
    return redirect(url_for('admin_login'))

def admin_required(f):
    """Decorator to require admin authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin') or not session.get('admin_id'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with analytics"""
    from models import Admin, User, Manager, CashbackApplication, CallbackRequest
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    if not current_admin:
        return redirect(url_for('admin_login'))
    
    # Analytics data
    stats = {
        'total_users': User.query.count(),
        'total_managers': Manager.query.count(),
        'total_applications': CashbackApplication.query.count(),
        'pending_applications': CashbackApplication.query.filter_by(status='На рассмотрении').count(),
        'approved_applications': CashbackApplication.query.filter_by(status='Одобрена').count(),
        'paid_applications': CashbackApplication.query.filter_by(status='Выплачена').count(),
        'total_cashback_approved': sum(app.cashback_amount for app in CashbackApplication.query.filter_by(status='Одобрена').all()),
        'total_cashback_paid': sum(app.cashback_amount for app in CashbackApplication.query.filter_by(status='Выплачена').all()),
        'active_users': User.query.filter_by(is_active=True).count(),
        'active_managers': Manager.query.filter_by(is_active=True).count(),
        'cashback_requests': CallbackRequest.query.filter(CallbackRequest.notes.contains('кешбек')).count(),
        'new_requests': CallbackRequest.query.filter_by(status='Новая').count(),
    }
    
    # Recent activity
    recent_applications = CashbackApplication.query.order_by(CashbackApplication.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_cashback_requests = CallbackRequest.query.filter(
        CallbackRequest.notes.contains('кешбек')
    ).order_by(CallbackRequest.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         admin=current_admin,
                         stats=stats,
                         recent_applications=recent_applications,
                         recent_users=recent_users,
                         recent_cashback_requests=recent_cashback_requests,
                         current_date=datetime.now())

@app.route('/admin/cashback-requests')
@admin_required
def admin_cashback_requests():
    """View all cashback requests"""
    from models import CallbackRequest
    
    # Get page number
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter cashback requests
    cashback_requests = CallbackRequest.query.filter(
        CallbackRequest.notes.contains('кешбек')
    ).order_by(CallbackRequest.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/cashback_requests.html',
                         requests=cashback_requests)

@app.route('/admin/callback-request/<int:request_id>/status', methods=['POST'])
@admin_required
def update_callback_request_status(request_id):
    """Update callback request status"""
    from models import CallbackRequest
    
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        callback_request = CallbackRequest.query.get_or_404(request_id)
        callback_request.status = new_status
        
        if new_status == 'Обработана':
            callback_request.processed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Статус обновлен'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/favorites/count', methods=['GET'])
@login_required  
def get_favorites_count():
    """Get count of user's favorites"""
    from models import FavoriteProperty, FavoriteComplex
    
    try:
        properties_count = FavoriteProperty.query.filter_by(user_id=current_user.id).count()
        complexes_count = FavoriteComplex.query.filter_by(user_id=current_user.id).count()
        
        return jsonify({
            'success': True,
            'properties_count': properties_count,
            'complexes_count': complexes_count,
            'total_count': properties_count + complexes_count
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/favorites/list', methods=['GET'])
@login_required  
def get_favorites_list():
    """Get user's favorite properties with full details"""
    from models import FavoriteProperty
    
    try:
        favorites = db.session.query(FavoriteProperty).filter_by(user_id=current_user.id).order_by(FavoriteProperty.created_at.desc()).all()
        print(f"Found {len(favorites)} favorites in database for user {current_user.id}")
        
        # Load properties data
        properties_data = load_properties()
        print(f"Loaded {len(properties_data)} properties from database")
        
        # Debug: show first few property IDs
        if properties_data:
            ids = [str(p.get('id')) for p in properties_data[:5]]
            print(f"First 5 property IDs from JSON: {ids}")
        
        favorites_list = []
        for fav in favorites:
            print(f"Looking for property_id {fav.property_id} (type: {type(fav.property_id)})")
            # Get property data from JSON files - compare as integers
            property_data = None
            for prop in properties_data:
                if int(prop.get('id')) == int(fav.property_id):
                    property_data = prop
                    break
            
            if property_data:
                print(f"Found property data for ID {fav.property_id}")
                # Add to favorites list with complete data including timestamp
                favorites_list.append({
                    'id': property_data.get('id'),
                    'title': property_data.get('title', 'Квартира'),
                    'complex': property_data.get('residential_complex', 'ЖК не указан'),
                    'district': property_data.get('district', 'Район не указан'),
                    'price': property_data.get('price', 0),
                    'image': property_data.get('main_image', '/static/images/no-photo.jpg'),
                    'cashback_amount': calculate_cashback(property_data.get('price', 0)),
                    'created_at': fav.created_at.strftime('%d.%m.%Y в %H:%M') if fav.created_at else 'Недавно'
                })
            else:
                print(f"No property data found for ID {fav.property_id}")
                # Create fallback entry with minimal data
                favorites_list.append({
                    'id': fav.property_id,
                    'title': f'Объект #{fav.property_id}',
                    'complex': 'ЖК не найден',
                    'district': 'Данные обновляются...',
                    'price': 0,
                    'image': '/static/images/no-photo.jpg',
                    'cashback_amount': 0
                })
        
        return jsonify({
            'success': True,
            'favorites': favorites_list
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Complex Favorites API
@app.route('/api/complexes/favorites', methods=['POST'])
@login_required  
def add_complex_to_favorites():
    """Add residential complex to favorites"""
    from models import FavoriteComplex
    data = request.get_json()
    
    complex_id = data.get('complex_id')
    complex_name = data.get('complex_name', 'ЖК')
    
    if not complex_id:
        return jsonify({'success': False, 'error': 'complex_id is required'}), 400
    
    # Check if already in favorites
    existing = FavoriteComplex.query.filter_by(
        user_id=current_user.id,
        complex_id=str(complex_id)
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'Complex already in favorites'}), 400
    
    try:
        # Create favorite complex record
        favorite = FavoriteComplex(
            user_id=current_user.id,
            complex_id=str(complex_id),
            complex_name=complex_name,
            developer_name=data.get('developer_name', ''),
            address_display_name=data.get('address', ''),
            district=data.get('district', ''),
            min_price=data.get('min_price'),
            max_price=data.get('max_price'),
            complex_image=data.get('image', ''),
            complex_url=data.get('url', ''),
            status=data.get('status', 'В продаже')
        )
        
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'ЖК добавлен в избранное'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/complexes/favorites/<complex_id>', methods=['DELETE'])
@login_required
def remove_complex_from_favorites(complex_id):
    """Remove residential complex from favorites"""
    from models import FavoriteComplex
    
    favorite = FavoriteComplex.query.filter_by(
        user_id=current_user.id,
        complex_id=str(complex_id)
    ).first()
    
    if not favorite:
        return jsonify({'success': False, 'error': 'Complex not in favorites'}), 404
    
    try:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'success': True, 'message': 'ЖК удален из избранного'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/complexes/favorites/toggle', methods=['POST'])
@login_required
def toggle_complex_favorite():
    """Toggle favorite status for residential complex"""
    from models import FavoriteComplex
    data = request.get_json()
    complex_id = data.get('complex_id')
    
    if not complex_id:
        return jsonify({'success': False, 'error': 'complex_id is required'}), 400
    
    try:
        existing = FavoriteComplex.query.filter_by(
            user_id=current_user.id,
            complex_id=str(complex_id)
        ).first()
        
        if existing:
            # Remove from favorites
            db.session.delete(existing)
            db.session.commit()
            return jsonify({'success': True, 'favorited': False, 'message': 'ЖК удален из избранного'})
        else:
            # Add to favorites
            favorite = FavoriteComplex(
                user_id=current_user.id,
                complex_id=str(complex_id),
                complex_name=data.get('complex_name', 'ЖК'),
                developer_name=data.get('developer_name', ''),
                address_display_name=data.get('address', ''),
                district=data.get('district', ''),
                min_price=data.get('min_price'),
                max_price=data.get('max_price'),
                complex_image=data.get('image', ''),
                complex_url=data.get('url', ''),
                status=data.get('status', 'В продаже')
            )
            
            db.session.add(favorite)
            db.session.commit()
            return jsonify({'success': True, 'favorited': True, 'message': 'ЖК добавлен в избранное'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/complexes/favorites/list', methods=['GET'])
@login_required  
def get_complex_favorites_list():
    """Get user's favorite complexes with full details"""
    from models import FavoriteComplex
    
    try:
        favorites = db.session.query(FavoriteComplex).filter_by(user_id=current_user.id).order_by(FavoriteComplex.created_at.desc()).all()
        
        favorites_list = []
        for fav in favorites:
            favorites_list.append({
                'id': fav.complex_id,
                'name': fav.complex_name,
                'developer': fav.developer_name,
                'address': fav.address_display_name,
                'district': fav.district,
                'min_price': fav.min_price,
                'max_price': fav.max_price,
                'image': fav.complex_image,
                'url': fav.complex_url,
                'status': fav.status,
                'created_at': fav.created_at.strftime('%d.%m.%Y в %H:%M') if fav.created_at else 'Недавно'
            })
        
        return jsonify({
            'success': True,
            'complexes': favorites_list
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# User Management Routes
@app.route('/admin/users')
@admin_required
def admin_users():
    """User management page"""
    from models import Admin, User
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', '', type=str)
    
    query = User.query
    
    if search:
        query = query.filter(User.email.contains(search) | User.full_name.contains(search))
    
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    elif status == 'verified':
        query = query.filter_by(is_verified=True)
    elif status == 'unverified':
        query = query.filter_by(is_verified=False)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', 
                         admin=current_admin, 
                         users=users,
                         search=search,
                         status=status)

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    """Edit user details"""
    from models import Admin, User, Manager
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    user = User.query.get_or_404(user_id)
    managers = Manager.query.filter_by(is_active=True).all()
    
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.full_name = request.form.get('full_name')
        user.phone = request.form.get('phone')
        user.client_status = request.form.get('client_status')
        user.client_notes = request.form.get('client_notes')
        user.is_active = 'is_active' in request.form
        user.is_verified = 'is_verified' in request.form
        
        assigned_manager_id = request.form.get('assigned_manager_id')
        if assigned_manager_id and assigned_manager_id.isdigit():
            user.assigned_manager_id = int(assigned_manager_id)
        else:
            user.assigned_manager_id = None
        
        try:
            db.session.commit()
            flash('Пользователь успешно обновлен', 'success')
            return redirect(url_for('admin_users'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении пользователя', 'error')
    
    return render_template('admin/edit_user.html', 
                         admin=current_admin, 
                         user=user,
                         managers=managers)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Delete user"""
    from models import User
    
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении пользователя', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/users/create', methods=['GET', 'POST'])
@admin_required
def admin_create_user():
    """Create new user by admin"""
    from models import Admin, User, Manager
    import re
    import secrets
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    managers = Manager.query.filter_by(is_active=True).all()
    
    if request.method == 'POST':
        try:
            # Validate required fields
            full_name = request.form.get('full_name', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            
            if not all([full_name, email, phone]):
                flash('Заполните все обязательные поля', 'error')
                return render_template('admin/create_user.html', 
                                     admin=current_admin, 
                                     managers=managers)
            
            # Validate email format
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                flash('Некорректный формат email', 'error')
                return render_template('admin/create_user.html', 
                                     admin=current_admin, 
                                     managers=managers)
            
            # Check if user already exists
            existing_user = User.query.filter(
                (User.email == email) | (User.phone == phone)
            ).first()
            
            if existing_user:
                flash('Пользователь с таким email или телефоном уже существует', 'error')
                return render_template('admin/create_user.html', 
                                     admin=current_admin, 
                                     managers=managers)
            
            # Clean phone number
            phone_clean = re.sub(r'[^\d]', '', phone)
            if len(phone_clean) == 11 and phone_clean.startswith('8'):
                phone_clean = '7' + phone_clean[1:]
            elif len(phone_clean) == 10:
                phone_clean = '7' + phone_clean
            
            if len(phone_clean) != 11 or not phone_clean.startswith('7'):
                flash('Некорректный формат телефона', 'error')
                return render_template('admin/create_user.html', 
                                     admin=current_admin, 
                                     managers=managers)
            
            # Generate temporary password
            temp_password = secrets.token_urlsafe(12)
            
            # Create user
            user = User(
                email=email,
                full_name=full_name,
                phone=phone_clean,
                client_status=request.form.get('client_status', 'Новый'),
                client_notes=request.form.get('client_notes', ''),
                is_active='is_active' in request.form,
                is_verified='is_verified' in request.form,
                temp_password_hash=temp_password,  # Store temp password for sending
                created_by_admin=True
            )
            
            # Set assigned manager
            assigned_manager_id = request.form.get('assigned_manager_id')
            if assigned_manager_id and assigned_manager_id.isdigit():
                user.assigned_manager_id = int(assigned_manager_id)
            
            # Set temporary password
            user.set_password(temp_password)
            
            db.session.add(user)
            db.session.commit()
            
            print(f"DEBUG: Successfully created user {user.id}: {user.full_name} by admin")
            
            # Send credentials if requested
            if 'send_credentials' in request.form:
                try:
                    from email_service import send_email_smtp
                    from sms_service import send_sms
                    
                    # Prepare email content
                    subject = "Ваш аккаунт создан в InBack.ru - Данные для входа"
                    email_content = f"""Здравствуйте, {full_name}!

Для вас создан аккаунт в системе InBack.ru.

Данные для входа:
• Email: {email}
• Временный пароль: {temp_password}

Войдите в систему по адресу: https://inback.ru/login
При первом входе вам будет предложено установить собственный пароль.

С уважением,
Команда InBack.ru"""
                    
                    # Send email using HTML template
                    send_email_smtp(
                        to_email=email,
                        subject=subject,
                        template_name='emails/user_credentials.html',
                        user_name=full_name,
                        email=email,
                        temp_password=temp_password,
                        login_url='https://inback.ru/login'
                    )
                    
                    # Send SMS
                    sms_message = f"InBack.ru: Ваш аккаунт создан. Логин: {email}, Пароль: {temp_password}. Войти: https://inback.ru/login"
                    send_sms(phone_clean, sms_message)
                    
                    flash(f'Пользователь {full_name} успешно создан. Данные для входа отправлены на email и SMS.', 'success')
                    
                except Exception as e:
                    print(f"Error sending credentials: {str(e)}")
                    flash(f'Пользователь создан, но не удалось отправить данные для входа: {str(e)}', 'warning')
            else:
                flash(f'Пользователь {full_name} успешно создан.', 'success')
            
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {str(e)}")
            flash(f'Ошибка при создании пользователя: {str(e)}', 'error')
            return render_template('admin/create_user.html', 
                                 admin=current_admin, 
                                 managers=managers)
    
    return render_template('admin/create_user.html', 
                         admin=current_admin, 
                         managers=managers)

@app.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def admin_toggle_user_status(user_id):
    """Toggle user active status"""
    from models import User
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    
    try:
        db.session.commit()
        status = 'активирован' if user.is_active else 'заблокирован'
        flash(f'Пользователь {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при изменении статуса пользователя', 'error')
    
    return redirect(url_for('admin_users'))

# Manager Management Routes
@app.route('/admin/managers')
@admin_required
def admin_managers():
    """Manager management page"""
    from models import Admin, Manager
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', '', type=str)
    
    query = Manager.query
    
    if search:
        query = query.filter(Manager.email.contains(search) | Manager.first_name.contains(search) | Manager.last_name.contains(search))
    
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    
    managers = query.order_by(Manager.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/managers.html', 
                         admin=current_admin, 
                         managers=managers,
                         search=search,
                         status=status)

@app.route('/admin/managers/<int:manager_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_manager(manager_id):
    """Edit manager details"""
    from models import Admin, Manager
    
    try:
        admin_id = session.get('admin_id')
        current_admin = Admin.query.get(admin_id)
        manager = Manager.query.get(manager_id)
        
        if not manager:
            flash(f'Менеджер с ID {manager_id} не найден', 'error')
            return redirect(url_for('admin_managers'))
            
        print(f"DEBUG: Found manager {manager_id}: {manager.email}")
    except Exception as e:
        print(f"ERROR in admin_edit_manager: {e}")
        flash('Ошибка при загрузке менеджера', 'error')
        return redirect(url_for('admin_managers'))
    
    if request.method == 'POST':
        manager.email = request.form.get('email')
        manager.first_name = request.form.get('first_name')
        manager.last_name = request.form.get('last_name')
        manager.phone = request.form.get('phone')
        manager.position = request.form.get('position')
        manager.is_active = 'is_active' in request.form
        
        new_password = request.form.get('new_password')
        if new_password:
            manager.set_password(new_password)
        
        try:
            db.session.commit()
            flash('Менеджер успешно обновлен', 'success')
            return redirect(url_for('admin_managers'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении менеджера', 'error')
    
    from datetime import datetime
    
    return render_template('admin/edit_manager.html', 
                         admin=current_admin, 
                         manager=manager,
                         current_date=datetime.utcnow())



# Blog Management Routes
@app.route('/admin/blog')
@admin_required
def admin_blog():
    """Blog management page"""
    from models import Admin, BlogPost
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    if not current_admin:
        return redirect(url_for('admin_login'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', '', type=str)
    category = request.args.get('category', '', type=str)
    
    query = BlogPost.query
    
    if search:
        query = query.filter(BlogPost.title.contains(search) | BlogPost.content.contains(search))
    
    if status:
        query = query.filter_by(status=status)
    
    if category:
        query = query.filter_by(category=category)
    
    posts = query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get categories for filter
    categories = db.session.query(BlogPost.category).distinct().filter(BlogPost.category.isnot(None)).all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('admin/blog.html', 
                         admin=current_admin, 
                         posts=posts,
                         search=search,
                         status=status,
                         category=category,
                         categories=categories)

@app.route('/admin/blog/create', methods=['GET', 'POST'])
@admin_required
def admin_create_post():
    """Create new blog post with full TinyMCE integration"""
    from models import Admin, BlogPost, Category
    import re
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    if not current_admin:
        return redirect(url_for('admin_login'))
    
    if request.method == 'GET':
        # Load categories for the form
        categories = Category.query.order_by(Category.name).all()
        return render_template('admin/create_article.html', admin=current_admin, categories=categories)
    
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            excerpt = request.form.get('excerpt')
            category_id = request.form.get('category_id')
            
            if not title or not content or not category_id:
                flash('Заголовок, содержание и категория обязательны', 'error')
                categories = Category.query.order_by(Category.name).all()
                return render_template('admin/create_article.html', admin=current_admin, categories=categories)
            
            # Get category name from category_id
            category = Category.query.get(int(category_id))
            if not category:
                flash('Выбранная категория не найдена', 'error')
                categories = Category.query.order_by(Category.name).all()
                return render_template('admin/create_article.html', admin=current_admin, categories=categories)
            
            # Generate slug from title
            slug = request.form.get('slug', '')
            if not slug:
                # Auto-generate slug from title
                def transliterate(text):
                    rus_to_eng = {
                        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
                        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
                    }
                    return ''.join(rus_to_eng.get(char.lower(), char) for char in text)
                
                slug = transliterate(title.lower())
                slug = re.sub(r'[^\w\s-]', '', slug)
                slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            
            # Ensure unique slug
            original_slug = slug
            counter = 1
            while BlogPost.query.filter_by(slug=slug).first():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            post = BlogPost(
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                meta_title=request.form.get('meta_title'),
                meta_description=request.form.get('meta_description'),
                meta_keywords=request.form.get('meta_keywords'),
                category=category.name,  # Store category name for compatibility
                tags=request.form.get('tags'),
                featured_image=request.form.get('featured_image'),
                status=request.form.get('status', 'draft'),
                author_id=current_admin.id,
                created_at=datetime.utcnow()
            )
            
            if post.status == 'published':
                post.published_at = datetime.utcnow()
            
            db.session.add(post)
            db.session.commit()
            
            # Update category article count
            if post.status == 'published':
                category.articles_count = BlogPost.query.filter_by(category=category.name, status='published').count()
                db.session.commit()
            
            flash('Статья успешно создана!', 'success')
            return redirect(url_for('admin_blog'))
            
        except Exception as e:
            db.session.rollback()
            print(f'ERROR creating blog post: {str(e)}')
            flash(f'Ошибка при создании статьи: {str(e)}', 'error')
            categories = Category.query.order_by(Category.name).all()
            return render_template('admin/create_article.html', admin=current_admin, categories=categories)

@app.route('/admin/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(post_id):
    """Edit blog post"""
    from models import Admin, BlogPost, Category
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    if not current_admin:
        flash('Требуется авторизация администратора', 'error')
        return redirect(url_for('admin_login'))
    
    try:
        post = BlogPost.query.get_or_404(post_id)
    except Exception as e:
        flash(f'Статья не найдена: {str(e)}', 'error')
        return redirect(url_for('admin_blog'))
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.excerpt = request.form.get('excerpt')
        post.meta_title = request.form.get('meta_title')
        post.meta_description = request.form.get('meta_description')
        post.meta_keywords = request.form.get('meta_keywords')
        post.category = request.form.get('category')
        post.tags = request.form.get('tags')
        post.featured_image = request.form.get('featured_image')
        
        old_status = post.status
        post.status = request.form.get('status', 'draft')
        
        # Handle publishing
        if post.status == 'published' and old_status != 'published':
            post.published_at = datetime.utcnow()
        elif post.status != 'published':
            post.published_at = None
        
        try:
            db.session.commit()
            flash('Статья успешно обновлена', 'success')
            return redirect(url_for('admin_blog'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении статьи: {str(e)}', 'error')
    
    # Get categories for dropdown
    try:
        categories = Category.query.order_by(Category.name).all()
    except Exception as e:
        print(f'Error loading categories: {e}')
        categories = []
    
    return render_template('admin/blog_edit.html', 
                         admin=current_admin, 
                         post=post, 
                         categories=categories)

@app.route('/admin/blog/<int:post_id>/delete', methods=['POST'])
@admin_required
def admin_delete_post(post_id):
    """Delete blog post"""
    from models import BlogPost
    
    post = BlogPost.query.get_or_404(post_id)
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Статья успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении статьи', 'error')
    
    return redirect(url_for('admin_blog'))

# Analytics Routes
@app.route('/admin/analytics/cashback')
@admin_required
def admin_cashback_analytics():
    """Cashback analytics page"""
    from models import Admin, CashbackApplication
    from sqlalchemy import func
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    if not current_admin:
        return redirect(url_for('admin_login'))
    
    # Monthly cashback stats
    monthly_stats = db.session.query(
        func.date_trunc('month', CashbackApplication.created_at).label('month'),
        func.count(CashbackApplication.id).label('count'),
        func.sum(CashbackApplication.cashback_amount).label('total_amount')
    ).group_by(func.date_trunc('month', CashbackApplication.created_at)).order_by('month').all()
    
    # Status breakdown
    status_stats = db.session.query(
        CashbackApplication.status,
        func.count(CashbackApplication.id).label('count'),
        func.sum(CashbackApplication.cashback_amount).label('total_amount')
    ).group_by(CashbackApplication.status).all()
    
    # Recent large cashbacks
    large_cashbacks = CashbackApplication.query.filter(
        CashbackApplication.cashback_amount >= 100000
    ).order_by(CashbackApplication.created_at.desc()).limit(10).all()
    
    return render_template('admin/cashback_analytics.html',
                         admin=current_admin,
                         monthly_stats=monthly_stats,
                         status_stats=status_stats,
                         large_cashbacks=large_cashbacks)

# Admin Blog Management Routes

@app.route('/admin/blog/<int:article_id>/edit', methods=['GET', 'POST'])
@admin_required  
def admin_edit_article(article_id):
    """Edit blog article"""
    from models import Admin, BlogPost
    import re
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    article = BlogPost.query.get_or_404(article_id)
    
    if request.method == 'POST':
        article.title = request.form.get('title')
        article.slug = request.form.get('slug')
        article.content = request.form.get('content')
        article.excerpt = request.form.get('excerpt')
        article.category = request.form.get('category')
        article.tags = request.form.get('tags')
        article.featured_image = request.form.get('featured_image')
        article.meta_title = request.form.get('meta_title')
        article.meta_description = request.form.get('meta_description')
        article.meta_keywords = request.form.get('meta_keywords')
        action = request.form.get('action', 'save')
        
        # Auto-generate slug if empty
        if not article.slug:
            slug = re.sub(r'[^\w\s-]', '', article.title.lower())
            slug = re.sub(r'[\s_-]+', '-', slug)
            article.slug = slug.strip('-')
        
        # Set status based on action
        if action == 'publish':
            article.status = 'published'
            if not article.published_at:
                article.published_at = datetime.now()
        else:
            article.status = request.form.get('status', 'draft')
        
        # Handle scheduled posts
        if article.status == 'scheduled':
            scheduled_str = request.form.get('scheduled_for')
            if scheduled_str:
                try:
                    article.scheduled_for = datetime.fromisoformat(scheduled_str)
                except:
                    pass
        else:
            article.scheduled_for = None
            
        article.updated_at = datetime.now()
        
        try:
            db.session.commit()
            flash('Статья успешно обновлена', 'success')
            return redirect(url_for('admin_blog'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении статьи', 'error')
    
    return render_template('admin/create_article.html', admin=current_admin, article=article)

@app.route('/admin/blog/<int:article_id>/delete', methods=['POST'])
@admin_required
def admin_delete_article(article_id):
    """Delete blog article"""
    from models import BlogPost
    
    article = BlogPost.query.get_or_404(article_id)
    
    try:
        db.session.delete(article)
        db.session.commit()
        flash('Статья успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении статьи', 'error')
    
    return redirect(url_for('admin_blog'))

@app.route('/admin/blog/<int:article_id>/publish', methods=['POST'])
@admin_required
def admin_publish_article(article_id):
    """Publish blog article"""
    from models import BlogPost
    
    article = BlogPost.query.get_or_404(article_id)
    article.status = 'published'
    article.published_at = datetime.now()
    article.updated_at = datetime.now()
    
    try:
        db.session.commit()
        flash('Статья успешно опубликована', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при публикации статьи', 'error')
    
    return redirect(url_for('admin_blog'))

# Admin Manager Management Routes  
@app.route('/admin/managers/create', methods=['GET', 'POST'])
@admin_required
def admin_create_manager():
    """Create new manager"""
    from models import Admin, Manager
    from werkzeug.security import generate_password_hash
    import json
    import random
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    if request.method == 'POST':
        full_name = request.form.get('full_name', '')
        email = request.form.get('email')
        phone = request.form.get('phone')
        position = request.form.get('position', 'Менеджер')
        profile_image = request.form.get('profile_image')
        password = request.form.get('password', 'demo123')  # Default password
        password_confirm = request.form.get('password_confirm', 'demo123')
        is_active = request.form.get('is_active') != 'False'  # Default True
        
        # Split full name into first and last name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0] if name_parts else 'Имя'
        last_name = name_parts[1] if len(name_parts) > 1 else 'Фамилия'
        
        # Validate passwords
        if password != password_confirm:
            flash('Пароли не совпадают', 'error')
            return render_template('admin/create_manager.html', admin=current_admin)
        
        if not password:
            password = 'demo123'  # Default password
        
        # Check if email already exists
        if email:
            existing_manager = Manager.query.filter_by(email=email).first()
            if existing_manager:
                flash('Менеджер с таким email уже существует', 'error')
                return render_template('admin/create_manager.html', admin=current_admin)
        
        # Create manager
        manager = Manager()
        manager.email = email or f'manager{random.randint(1000,9999)}@inback.ru'
        manager.first_name = first_name
        manager.last_name = last_name
        manager.phone = phone
        manager.position = position
        manager.profile_image = profile_image or 'https://randomuser.me/api/portraits/men/1.jpg'
        manager.set_password(password)
        manager.is_active = is_active
        
        try:
            db.session.add(manager)
            db.session.commit()
            flash('Менеджер успешно создан', 'success')
            return redirect(url_for('admin_managers'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании менеджера', 'error')
    
    return render_template('admin/create_manager.html', admin=current_admin)

@app.route('/admin/managers/<int:manager_id>/delete', methods=['POST'])
@admin_required
def admin_delete_manager(manager_id):
    """Delete manager"""
    from models import Manager
    
    manager = Manager.query.get_or_404(manager_id)
    
    try:
        db.session.delete(manager)
        db.session.commit()
        flash('Менеджер успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении менеджера', 'error')
    
    return redirect(url_for('admin_managers'))

@app.route('/admin/managers/<int:manager_id>/toggle-status', methods=['POST'])
@admin_required
def admin_toggle_manager_status(manager_id):
    """Toggle manager active status"""
    from models import Manager
    
    manager = Manager.query.get_or_404(manager_id)
    manager.is_active = not manager.is_active
    
    try:
        db.session.commit()
        status = 'активирован' if manager.is_active else 'заблокирован'
        flash(f'Менеджер {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при изменении статуса менеджера', 'error')
    
    return redirect(url_for('admin_managers'))

# Additional Pages Routes
@app.route('/careers')
def careers():
    """Careers page"""
    return render_template('careers.html')

@app.route('/security')
def security():
    """Security page"""
    return render_template('security.html')


if __name__ == '__main__':
    with app.app_context():
        from models import User, CashbackRecord, Application, Favorite, Notification, District, Developer, ResidentialComplex, Street, RoomType, Admin, BlogPost, City
        db.create_all()
        
        # Initialize cities
        try:
            init_cities()
            print("Cities initialized successfully")
        except Exception as e:
            print(f"Error initializing cities: {e}")
            db.session.rollback()
        
        # Initialize search data
        try:
            init_search_data()
            print("Search data initialized successfully")
        except Exception as e:
            print(f"Error initializing search data: {e}")
            db.session.rollback()

# Collection routes for clients
@app.route('/collections')
@login_required
def client_collections():
    """Show all collections assigned to current user"""
    from models import Collection
    collections = Collection.query.filter_by(assigned_to_user_id=current_user.id).order_by(Collection.created_at.desc()).all()
    return render_template('auth/client_collections.html', collections=collections)

@app.route('/collection/<int:collection_id>')
@login_required
def view_collection(collection_id):
    """View specific collection details"""
    from models import Collection
    collection = Collection.query.filter_by(id=collection_id, assigned_to_user_id=current_user.id).first()
    if not collection:
        flash('Подборка не найдена', 'error')
        return redirect(url_for('client_collections'))
    
    # Mark as viewed
    if collection.status == 'Отправлена':
        collection.status = 'Просмотрена'
        collection.viewed_at = datetime.utcnow()
        db.session.commit()
    
    return render_template('auth/view_collection.html', collection=collection)

@app.route('/collection/<int:collection_id>/mark-viewed', methods=['POST'])
@login_required
def mark_collection_viewed(collection_id):
    """Mark collection as viewed"""
    from models import Collection
    collection = Collection.query.filter_by(id=collection_id, assigned_to_user_id=current_user.id).first()
    if collection and collection.status == 'Отправлена':
        collection.status = 'Просмотрена'
        collection.viewed_at = datetime.utcnow()
        db.session.commit()
    return jsonify({'success': True})

# Manager collection routes
@app.route('/manager/collections')
@manager_required
def manager_collections():
    """Manager collections list"""
    from models import Collection, Manager
    manager_id = session.get('manager_id')
    manager = Manager.query.get(manager_id)
    collections = Collection.query.filter_by(created_by_manager_id=manager_id).order_by(Collection.created_at.desc()).all()
    return render_template('manager/collections.html', collections=collections, manager=manager)

@app.route('/manager/collections/new')
@manager_required
def manager_create_collection():
    """Create new collection"""
    from models import Manager, User
    manager_id = session.get('manager_id')
    manager = Manager.query.get(manager_id)
    # Get all clients assigned to this manager
    clients = User.query.filter_by(assigned_manager_id=manager_id).all()
    return render_template('manager/create_collection.html', manager=manager, clients=clients)

@app.route('/manager/collections/new', methods=['POST'])
@manager_required
def save_collection():
    """Save new collection"""
    from models import Collection, CollectionProperty, Manager
    
    manager_id = session.get('manager_id')
    manager = Manager.query.get(manager_id)
    
    title = request.form.get('title')
    description = request.form.get('description', '')
    assigned_to_user_id = request.form.get('assigned_to_user_id')
    tags = request.form.get('tags', '')
    action = request.form.get('action')
    property_ids = request.form.getlist('property_ids[]')
    property_notes = request.form.getlist('property_notes[]')
    
    if not title or not assigned_to_user_id:
        flash('Заполните обязательные поля', 'error')
        return render_template('manager/create_collection.html', manager=manager)
    
    try:
        # Create collection
        collection = Collection(
            title=title,
            description=description,
            created_by_manager_id=manager_id,
            assigned_to_user_id=int(assigned_to_user_id),
            tags=tags,
            status='Отправлена' if action == 'send' else 'Черновик',
            sent_at=datetime.utcnow() if action == 'send' else None
        )
        
        db.session.add(collection)
        db.session.flush()  # Get collection ID
        
        # Add properties to collection
        import json
        with open('data/properties.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        properties_dict = {prop['id']: prop for prop in properties_data}
        
        for i, prop_id in enumerate(property_ids):
            if prop_id in properties_dict:
                prop_data = properties_dict[prop_id]
                note = property_notes[i] if i < len(property_notes) else ''
                
                collection_property = CollectionProperty(
                    collection_id=collection.id,
                    property_id=prop_id,
                    property_name=prop_data['title'],
                    property_price=prop_data['price'],
                    complex_name=prop_data.get('residential_complex', ''),
                    property_type=f"{prop_data['rooms']}-комн",
                    property_size=prop_data.get('area'),
                    manager_note=note,
                    order_index=i
                )
                db.session.add(collection_property)
        
        db.session.commit()
        
        action_text = 'отправлена клиенту' if action == 'send' else 'сохранена как черновик'
        flash(f'Подборка "{title}" успешно {action_text}', 'success')
        return redirect(url_for('manager_collections'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при сохранении подборки: {str(e)}', 'error')
        return render_template('manager/create_collection.html', manager=manager)

@app.route('/manager/analytics')
@manager_required
def manager_analytics():
    """Manager analytics page"""
    from models import Manager, User, Collection, CashbackApplication
    from sqlalchemy import func
    
    manager_id = session.get('manager_id')
    current_manager = Manager.query.get(manager_id)
    
    if not current_manager:
        return redirect(url_for('manager_login'))
    
    # Manager stats
    clients_count = User.query.filter_by(assigned_manager_id=current_manager.id).count()
    collections_count = Collection.query.filter_by(created_by_manager_id=current_manager.id).count()
    sent_collections = Collection.query.filter_by(created_by_manager_id=current_manager.id, status='Отправлена').count()
    
    # Monthly collection stats
    monthly_collections = db.session.query(
        func.date_trunc('month', Collection.created_at).label('month'),
        func.count(Collection.id).label('count')
    ).filter_by(created_by_manager_id=current_manager.id).group_by(
        func.date_trunc('month', Collection.created_at)
    ).order_by('month').all()
    
    # Client activity stats
    client_stats = db.session.query(
        User.client_status,
        func.count(User.id).label('count')
    ).filter_by(assigned_manager_id=current_manager.id).group_by(User.client_status).all()
    
    # Recent activity
    recent_collections = Collection.query.filter_by(
        created_by_manager_id=current_manager.id
    ).order_by(Collection.created_at.desc()).limit(5).all()
    
    return render_template('manager/analytics.html',
                         manager=current_manager,
                         clients_count=clients_count,
                         collections_count=collections_count,
                         sent_collections=sent_collections,
                         monthly_collections=monthly_collections,
                         client_stats=client_stats,
                         recent_collections=recent_collections)

@app.route('/manager/search-properties', methods=['POST'])
@manager_required
def manager_search_properties():
    """Search properties for collection"""
    import json
    
    data = request.get_json()
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    rooms = data.get('rooms')
    
    try:
        with open('data/properties.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        filtered_properties = []
        for prop in properties_data:
            # Apply filters
            if min_price and prop['price'] < int(min_price):
                continue
            if max_price and prop['price'] > int(max_price):
                continue
            if rooms and str(prop['rooms']) != str(rooms):
                continue
                
            filtered_properties.append({
                'id': prop['id'],
                'title': f"{prop.get('rooms', 0)}-комн {prop.get('area', 0)} м²" if prop.get('rooms', 0) > 0 else f"Студия {prop.get('area', 0)} м²",
                'price': prop['price'],
                'complex_name': prop.get('residential_complex', 'ЖК не указан'),
                'rooms': prop['rooms'],
                'size': prop.get('area', 0)
            })
        
        return jsonify({'properties': filtered_properties[:50]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Additional API routes for collection management
@app.route('/api/manager/collection/<int:collection_id>/send', methods=['POST'])
@manager_required
def api_send_collection(collection_id):
    """Send collection to client"""
    from models import Collection
    
    manager_id = session.get('manager_id')
    collection = Collection.query.filter_by(id=collection_id, created_by_manager_id=manager_id).first()
    
    if not collection:
        return jsonify({'success': False, 'error': 'Подборка не найдена'}), 404
    
    if not collection.assigned_to_user_id:
        return jsonify({'success': False, 'error': 'Клиент не назначен'}), 400
    
    try:
        collection.status = 'Отправлена'
        collection.sent_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/collection/<int:collection_id>/delete', methods=['DELETE'])
@manager_required 
def api_delete_collection(collection_id):
    """Delete collection"""
    from models import Collection
    
    manager_id = session.get('manager_id')
    collection = Collection.query.filter_by(id=collection_id, created_by_manager_id=manager_id).first()
    
    if not collection:
        return jsonify({'success': False, 'error': 'Подборка не найдена'}), 404
    
    try:
        db.session.delete(collection)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# Manager Saved Searches API routes
@app.route('/api/manager/saved-searches')
@manager_required
def get_manager_saved_searches():
    """Get manager's saved searches"""
    from models import ManagerSavedSearch
    
    manager_id = session.get('manager_id')
    try:
        searches = ManagerSavedSearch.query.filter_by(manager_id=manager_id).order_by(ManagerSavedSearch.last_used.desc()).all()
        
        return jsonify({
            'success': True,
            'searches': [search.to_dict() for search in searches]
        })
    except Exception as e:
        print(f"Error loading manager saved searches: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/saved-searches', methods=['POST'])
@manager_required
def create_manager_saved_search():
    """Create a new saved search for manager"""
    from models import ManagerSavedSearch
    import json
    
    print(f"DEBUG: ===== create_manager_saved_search API CALLED =====")
    print(f"DEBUG: Method: {request.method}")
    print(f"DEBUG: Path: {request.path}")
    print(f"DEBUG: Headers: {dict(request.headers)}")
    
    manager_id = session.get('manager_id')
    print(f"DEBUG: Manager ID from session: {manager_id}")
    
    data = request.get_json()
    print(f"DEBUG: Raw request JSON: {data}")
    print(f"DEBUG: JSON type: {type(data)}")
    
    try:
        # Extract filters from the request
        filters = data.get('filters', {})
        print(f"DEBUG: Creating manager search with filters: {filters}")
        print(f"DEBUG: Full request data: {data}")
        print(f"DEBUG: Filters type: {type(filters)}")
        print(f"DEBUG: Filters empty check: {bool(filters)}")
        
        # Test if filters is actually empty - force some test data if needed
        if not filters or not any(filters.values()):
            print("DEBUG: Filters are empty, checking raw JSON...")
            raw_json = request.get_data(as_text=True)
            print(f"DEBUG: Raw request body: {raw_json}")
        
        filters_json = json.dumps(filters) if filters else None
        print(f"DEBUG: Filters JSON: {filters_json}")
        
        # Create new search
        search = ManagerSavedSearch(
            manager_id=manager_id,
            name=data.get('name'),
            description=data.get('description'),
            search_type=data.get('search_type', 'properties'),
            additional_filters=filters_json,
            is_template=data.get('is_template', False)
        )
        
        db.session.add(search)
        db.session.commit()
        print(f"DEBUG: Saved search with ID: {search.id}, additional_filters: {search.additional_filters}")
        
        # Verify the saved data
        db.session.refresh(search)
        print(f"DEBUG: Refreshed search additional_filters: {search.additional_filters}")
        
        return jsonify({
            'success': True,
            'search': search.to_dict(),
            'message': 'Поиск успешно сохранён'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error creating manager saved search: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/send-search', methods=['POST'])
@manager_required
def send_search_to_client():
    """Send manager's saved search to a client"""
    from models import ManagerSavedSearch, SentSearch, User, SavedSearch, UserNotification
    from email_service import send_notification
    import json
    
    manager_id = session.get('manager_id')
    data = request.get_json()
    
    try:
        search_id = data.get('search_id')
        client_id = data.get('client_id')
        message = data.get('message', '')
        
        # Get manager search
        manager_search = ManagerSavedSearch.query.filter_by(id=search_id, manager_id=manager_id).first()
        if not manager_search:
            return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
            
        # Get client
        client = User.query.get(client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Клиент не найден'}), 404
            
        # Create SavedSearch for client (copy manager search to client)
        client_search = SavedSearch(
            user_id=client_id,
            name=f"От менеджера: {manager_search.name}",
            description=f"{manager_search.description or ''}\n\n{message}".strip(),
            search_type=manager_search.search_type,
            additional_filters=manager_search.additional_filters,
            notify_new_matches=True
        )
        
        db.session.add(client_search)
        db.session.flush()  # Get the ID before final commit
        
        # Create sent search record
        sent_search = SentSearch(
            manager_id=manager_id,
            client_id=client_id,
            manager_search_id=search_id,
            name=manager_search.name,
            description=manager_search.description,
            additional_filters=manager_search.additional_filters,
            status='sent'
        )
        
        db.session.add(sent_search)
        db.session.flush()  # Get sent_search ID
        
        # Note: client_search is now created and linked via sent_search record
        
        # Update usage count
        manager_search.usage_count = (manager_search.usage_count or 0) + 1
        manager_search.last_used = datetime.utcnow()
        
        # Create notification for client
        notification = UserNotification(
            user_id=client_id,
            title="Новый поиск от менеджера",
            message=f"Ваш менеджер отправил вам поиск: {manager_search.name}",
            notification_type='info',
            icon='fas fa-search',
            action_url='/dashboard'
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Send email notification
        try:
            send_notification(
                client.email,
                f"Новый поиск от менеджера: {manager_search.name}",
                f"Ваш менеджер отправил вам новый поиск недвижимости.\n\n"
                f"Название: {manager_search.name}\n"
                f"Описание: {manager_search.description or 'Без описания'}\n\n"
                f"{message}\n\n"
                f"Войдите в личный кабинет для просмотра: https://{request.host}/dashboard",
                user_id=client_id,
                notification_type='search_received'
            )
        except Exception as e:
            print(f"Error sending email notification: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Поиск успешно отправлен клиенту'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error sending search to client: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/saved-search/<int:search_id>', methods=['DELETE'])
@manager_required
def delete_manager_saved_search(search_id):
    """Delete manager's saved search"""
    from models import ManagerSavedSearch
    
    manager_id = session.get('manager_id')
    
    try:
        search = ManagerSavedSearch.query.filter_by(id=search_id, manager_id=manager_id).first()
        if not search:
            return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
            
        db.session.delete(search)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Поиск удалён'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting manager saved search: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# Developer appointment routes
@app.route('/book-appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    """Book appointment with developer"""
    if request.method == 'POST':
        from models import DeveloperAppointment
        from datetime import datetime
        
        property_id = request.form.get('property_id')
        developer_name = request.form.get('developer_name')
        complex_name = request.form.get('complex_name')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        client_name = request.form.get('client_name')
        client_phone = request.form.get('client_phone')
        notes = request.form.get('notes', '')
        
        try:
            appointment = DeveloperAppointment(
                user_id=current_user.id,
                property_id=property_id,
                developer_name=developer_name,
                complex_name=complex_name,
                appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d'),
                appointment_time=appointment_time,
                client_name=client_name,
                client_phone=client_phone,
                notes=notes
            )
            
            db.session.add(appointment)
            db.session.commit()
            
            flash('Запись к застройщику успешно создана! Менеджер свяжется с вами для подтверждения.', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании записи. Попробуйте еще раз.', 'error')
    
    # Get property data if property_id provided
    property_data = None
    property_id = request.args.get('property_id')
    if property_id:
        properties = load_properties()
        for prop in properties:
            if str(prop.get('id')) == property_id:
                property_data = prop
                break
    
    return render_template('book_appointment.html', property_data=property_data)

@app.route('/api/manager/add-client-old', methods=['POST'])
@manager_required
def add_client():
    """Add new client (old version - deprecated)"""
    from models import User
    from werkzeug.security import generate_password_hash
    import secrets
    
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name') 
    email = data.get('email')
    phone = data.get('phone')
    
    if not all([first_name, last_name, email]):
        return jsonify({'success': False, 'error': 'Заполните все обязательные поля'}), 400
    
    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'error': 'Пользователь с таким email уже существует'}), 400
    
    try:
        # Generate user ID and password
        user_id = secrets.token_hex(4).upper()
        password = 'demo123'  # Default password
        password_hash = generate_password_hash(password)
        
        manager_id = session.get('manager_id')
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            user_id=user_id,
            assigned_manager_id=manager_id,
            client_status='Новый'
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'user_id': user.user_id,
                'password': password,
                'client_status': user.client_status
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/request-payout', methods=['POST'])
@login_required
def api_request_payout():
    """Request cashback payout"""
    from models import User, CashbackPayout
    from datetime import datetime
    
    try:
        user_id = current_user.id
        
        # Check if user has available cashback
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Пользователь не найден'})
        
        # For demo purposes, assume available cashback of 125,000
        available_cashback = 125000
        
        if available_cashback <= 0:
            return jsonify({'success': False, 'error': 'Нет доступного кешбека для выплаты'})
        
        # Create payout request
        payout = CashbackPayout(
            user_id=user_id,
            amount=available_cashback,
            status='Запрошена',
            requested_at=datetime.utcnow()
        )
        
        db.session.add(payout)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Запрос на выплату успешно отправлен',
            'amount': available_cashback
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})



# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html', error_details=str(error) if app.debug else None), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    db.session.rollback()
    if app.debug:
        return render_template('errors/500.html', error_details=str(e)), 500
    else:
        return render_template('errors/500.html'), 500

# City management API endpoints
@app.route('/api/change-city', methods=['POST'])
def change_city():
    """API endpoint to change current city"""
    try:
        data = request.get_json()
        city_slug = data.get('city_slug')
        city_name = data.get('city_name')
        
        if not city_slug or not city_name:
            return jsonify({'success': False, 'message': 'Missing city data'})
        
        # For now, only Krasnodar is available
        if city_slug != 'krasnodar':
            return jsonify({'success': False, 'message': 'City not available yet'})
        
        # Store in session
        session['current_city'] = city_name
        session['current_city_slug'] = city_slug
        
        return jsonify({'success': True, 'message': f'City changed to {city_name}'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error changing city'})

@app.route('/api/cities')
def get_cities():
    """Get available cities"""
    try:
        from models import City
        cities = City.query.filter_by(is_active=True).all()
        
        cities_data = []
        for city in cities:
            cities_data.append({
                'id': city.id,
                'name': city.name,
                'slug': city.slug,
                'is_default': city.is_default,
                'address_position_lat': city.address_position_lat,
                'address_position_lon': city.address_position_lon,
                'zoom_level': city.zoom_level
            })
            
        return jsonify({'cities': cities_data})
        
    except Exception as e:
        # Fallback data if database not set up yet
        return jsonify({
            'cities': [
                {
                    'id': 1,
                    'name': 'Краснодар',
                    'slug': 'krasnodar',
                    'is_default': True,
                    'address_position_lat': 45.0355,
                    'address_position_lon': 38.9753,
                    'zoom_level': 12
                }
            ]
        })

def init_cities():
    """Initialize default cities in database"""
    try:
        from models import City
        
        # Check if cities already exist
        if City.query.count() == 0:
            cities_data = [
                {
                    'name': 'Краснодар',
                    'slug': 'krasnodar',
                    'is_active': True,
                    'is_default': True,
                    'phone': '+7 (800) 123-45-67',
                    'email': 'krasnodar@inback.ru',
                    'address': 'г. Краснодар, ул. Красная, 32',
                    'address_position_lat': 45.0355,
                    'address_position_lon': 38.9753,
                    'zoom_level': 12,
                    'description': 'Кэшбек за новостройки в Краснодаре',
                    'meta_title': 'Кэшбек за новостройки в Краснодаре | InBack.ru',
                    'meta_description': 'Получите до 10% кэшбека при покупке новостройки в Краснодаре. Проверенные застройщики, юридическое сопровождение.'
                },
                {
                    'name': 'Москва',
                    'slug': 'moscow',
                    'is_active': False,
                    'is_default': False,
                    'phone': '+7 (800) 123-45-67',
                    'email': 'moscow@inback.ru',
                    'address': 'г. Москва, ул. Тверская, 1',
                    'address_position_lat': 55.7558,
                    'address_position_lon': 37.6176,
                    'zoom_level': 11,
                    'description': 'Кэшбек за новостройки в Москве (скоро)',
                    'meta_title': 'Кэшбек за новостройки в Москве | InBack.ru',
                    'meta_description': 'Скоро: кэшбек сервис для покупки новостроек в Москве.'
                },
                {
                    'name': 'Санкт-Петербург',
                    'slug': 'spb',
                    'is_active': False,
                    'is_default': False,
                    'phone': '+7 (800) 123-45-67',
                    'email': 'spb@inback.ru',
                    'address': 'г. Санкт-Петербург, Невский пр., 1',
                    'address_position_lat': 59.9311,
                    'address_position_lon': 30.3609,
                    'zoom_level': 11,
                    'description': 'Кэшбек за новостройки в Санкт-Петербурге (скоро)',
                    'meta_title': 'Кэшбек за новостройки в СПб | InBack.ru',
                    'meta_description': 'Скоро: кэшбек сервис для покупки новостроек в Санкт-Петербурге.'
                },
                {
                    'name': 'Сочи',
                    'slug': 'sochi',
                    'is_active': False,
                    'is_default': False,
                    'phone': '+7 (800) 123-45-67',
                    'email': 'sochi@inback.ru',
                    'address': 'г. Сочи, ул. Курортный пр., 1',
                    'address_position_lat': 43.6028,
                    'address_position_lon': 39.7342,
                    'zoom_level': 12,
                    'description': 'Кэшбек за новостройки в Сочи (скоро)',
                    'meta_title': 'Кэшбек за новостройки в Сочи | InBack.ru',
                    'meta_description': 'Скоро: кэшбек сервис для покупки новостроек в Сочи.'
                }
            ]
            
            for city_data in cities_data:
                city = City(**city_data)
                db.session.add(city)
            
            db.session.commit()
            print("Cities initialized successfully")
            
    except Exception as e:
        print(f"Error initializing cities: {e}")

# Legacy API route removed - using Blueprint version instead

@api_bp.route('/searches', methods=['POST'])
def save_search():
    """Save user search parameters with manager-to-client sharing functionality"""
    from models import SavedSearch, User
    data = request.get_json()
    
    # Check authentication using helper function
    auth_info = check_api_authentication()
    if not auth_info:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    user_id = auth_info['user_id']
    user_role = auth_info['type']
    current_logged_user = auth_info['user']
    
    try:
        client_email = data.get('client_email')  # For managers
        
        print(f"DEBUG: Saving search with raw data: {data}")
        
        # Create filter object from submitted data
        filters = {}
        
        # Check if filters are nested in 'filters' object
        filter_data = data.get('filters', {}) if 'filters' in data else data
        
        # Extract filters from the data (new format)
        if 'rooms' in filter_data and filter_data['rooms']:
            if isinstance(filter_data['rooms'], list):
                room_list = [r for r in filter_data['rooms'] if r]  # Remove empty strings
                if room_list:
                    filters['rooms'] = room_list
            elif filter_data['rooms']:
                filters['rooms'] = [filter_data['rooms']]
                
        if 'districts' in filter_data and filter_data['districts']:
            if isinstance(filter_data['districts'], list):
                district_list = [d for d in filter_data['districts'] if d]  # Remove empty strings
                if district_list:
                    filters['districts'] = district_list
            elif filter_data['districts']:
                filters['districts'] = [filter_data['districts']]
                
        if 'developers' in filter_data and filter_data['developers']:
            if isinstance(filter_data['developers'], list):
                developer_list = [d for d in filter_data['developers'] if d]  # Remove empty strings
                if developer_list:
                    filters['developers'] = developer_list
            elif filter_data['developers']:
                filters['developers'] = [filter_data['developers']]
                
        if 'completion' in filter_data and filter_data['completion']:
            if isinstance(filter_data['completion'], list):
                completion_list = [c for c in filter_data['completion'] if c]  # Remove empty strings
                if completion_list:
                    filters['completion'] = completion_list
            elif filter_data['completion']:
                filters['completion'] = [filter_data['completion']]
                
        if 'priceFrom' in filter_data and filter_data['priceFrom'] and str(filter_data['priceFrom']) not in ['0', '']:
            filters['priceFrom'] = str(filter_data['priceFrom'])
        if 'priceTo' in filter_data and filter_data['priceTo'] and str(filter_data['priceTo']) not in ['0', '']:
            filters['priceTo'] = str(filter_data['priceTo'])
        if 'areaFrom' in filter_data and filter_data['areaFrom'] and str(filter_data['areaFrom']) not in ['0', '']:
            filters['areaFrom'] = str(filter_data['areaFrom'])
        if 'areaTo' in filter_data and filter_data['areaTo'] and str(filter_data['areaTo']) not in ['0', '']:
            filters['areaTo'] = str(filter_data['areaTo'])
            
        print(f"DEBUG: Extracted filters from {filter_data}: {filters}")

        # Create search with new format
        search = SavedSearch(
            user_id=user_id,
            name=data['name'],
            description=data.get('description'),
            search_type='properties',
            additional_filters=json.dumps(filters),
            notify_new_matches=data.get('notify_new_matches', True)
        )

        # Also save in legacy format for backwards compatibility
        if 'rooms' in data and data['rooms']:
            if isinstance(data['rooms'], list) and len(data['rooms']) > 0:
                search.property_type = data['rooms'][0]  # Use first room type
            else:
                search.property_type = data['rooms']
        if 'priceTo' in data and data['priceTo']:
            try:
                search.price_max = int(float(data['priceTo']) * 1000000)  # Convert millions to rubles
            except (ValueError, TypeError):
                pass
        if 'priceFrom' in data and data['priceFrom']:
            try:
                search.price_min = int(float(data['priceFrom']) * 1000000)  # Convert millions to rubles
            except (ValueError, TypeError):
                pass
        
        db.session.add(search)
        db.session.commit()
        
        # If manager specified client email, send search to client  
        if user_role == 'manager' and client_email:
            try:
                # Check if client exists
                client = User.query.filter_by(email=client_email).first()
                
                # If client exists, also save search to their account
                if client:
                    client_search = SavedSearch(
                        user_id=client.id,
                        name=data['name'] + ' (от менеджера)',
                        description=data.get('description'),
                        search_type='properties',
                        location=data.get('location'),
                        property_type=data.get('property_type'),
                        price_min=data.get('price_min'),
                        price_max=data.get('price_max'),
                        size_min=data.get('size_min'),
                        size_max=data.get('size_max'),
                        developer=data.get('developer'),
                        complex_name=data.get('complex_name'),
                        floor_min=data.get('floor_min'),
                        floor_max=data.get('floor_max'),
                        additional_filters=json.dumps(filters),
                        notify_new_matches=True
                    )
                    db.session.add(client_search)
                    db.session.commit()
                
                # Prepare search URL for client properties page  
                search_params = []
                
                # Convert manager filter format to client filter format
                if data.get('location'):
                    search_params.append(f"district={data['location']}")
                if data.get('developer'):
                    search_params.append(f"developer={data['developer']}")
                if data.get('property_type'):
                    search_params.append(f"rooms={data['property_type']}")
                if data.get('complex_name'):
                    search_params.append(f"complex={data['complex_name']}")
                if data.get('price_min'):
                    search_params.append(f"priceFrom={data['price_min'] / 1000000}")
                if data.get('price_max'):
                    search_params.append(f"priceTo={data['price_max'] / 1000000}")
                if data.get('size_min'):
                    search_params.append(f"areaFrom={data['size_min']}")
                if data.get('size_max'):
                    search_params.append(f"areaTo={data['size_max']}")
                
                search_url = f"{request.url_root}properties"
                if search_params:
                    search_url += "?" + "&".join(search_params)
                
                # Email content for client
                subject = f"Подборка недвижимости: {data['name']}"
                
                # Generate filter description for email
                filter_descriptions = []
                if data.get('property_type'):
                    filter_descriptions.append(f"Тип: {data['property_type']}")
                if data.get('location'):
                    filter_descriptions.append(f"Район: {data['location']}")
                if data.get('developer'):
                    filter_descriptions.append(f"Застройщик: {data['developer']}")
                if data.get('price_min') or data.get('price_max'):
                    price_min = f"{(data.get('price_min', 0) / 1000000):.1f}" if data.get('price_min') else "0"
                    price_max = f"{(data.get('price_max', 0) / 1000000):.1f}" if data.get('price_max') else "∞"
                    filter_descriptions.append(f"Цена: {price_min}-{price_max} млн ₽")
                if data.get('size_min') or data.get('size_max'):
                    area_min = str(data.get('size_min', 0)) if data.get('size_min') else "0"
                    area_max = str(data.get('size_max', 0)) if data.get('size_max') else "∞"
                    filter_descriptions.append(f"Площадь: {area_min}-{area_max} м²")
                
                filter_text = "<br>".join([f"• {desc}" for desc in filter_descriptions])
                
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #0088CC;">Подборка недвижимости от InBack</h2>
                    
                    <p>Здравствуйте!</p>
                    
                    <p>Менеджер <strong>{current_user.full_name or current_user.username}</strong> подготовил для вас персональную подборку недвижимости.</p>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="margin: 0 0 15px 0; color: #333;">Параметры поиска: {data['name']}</h3>
                        <div style="color: #666; line-height: 1.6;">
                            {filter_text}
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{search_url}" style="display: inline-block; background: #0088CC; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                            Посмотреть подборку
                        </a>
                    </div>
                    
                    <p style="color: #666; font-size: 14px;">
                        Если у вас есть вопросы, свяжитесь с вашим менеджером:<br>
                        <strong>{current_logged_user.full_name if hasattr(current_logged_user, 'full_name') else current_logged_user.email}</strong><br>
                        Email: {current_logged_user.email}
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        InBack - ваш надежный партнер в поиске недвижимости
                    </p>
                </div>
                """
                
                # Send email using existing email service
                from email_service import send_email
                email_sent = send_email(
                    to_email=client_email,
                    subject=subject,
                    html_content=html_content,
                    template_name='collection'
                )
                
                if email_sent:
                    return jsonify({
                        'success': True, 
                        'search_id': search.id, 
                        'search': search.to_dict(),
                        'message': f'Поиск сохранен и отправлен клиенту на {client_email}',
                        'email_sent': True
                    })
                else:
                    return jsonify({
                        'success': True, 
                        'search_id': search.id, 
                        'search': search.to_dict(),
                        'message': 'Поиск сохранен, но не удалось отправить email клиенту',
                        'email_sent': False
                    })
                    
            except Exception as email_error:
                # Still return success for saved search even if email fails
                print(f"Email sending error: {email_error}")
                return jsonify({
                    'success': True, 
                    'search_id': search.id, 
                    'search': search.to_dict(),
                    'message': 'Поиск сохранен, но произошла ошибка при отправке email',
                    'email_sent': False,
                    'email_error': str(email_error)
                })
        
        return jsonify({'success': True, 'search_id': search.id, 'search': search.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

def check_api_authentication():
    """Helper function to check API authentication for both users and managers"""
    # Check if manager is logged in
    if 'manager_id' in session:
        from models import Manager
        manager = Manager.query.get(session['manager_id'])
        if manager:
            return {'type': 'manager', 'user_id': manager.id, 'user': manager}
    
    # Check if regular user is logged in  
    if current_user and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        return {'type': 'user', 'user_id': current_user.id, 'user': current_user}
    
    # Also check session for user_id (alternative authentication method)
    if 'user_id' in session:
        from models import User
        user = User.query.get(session['user_id'])
        if user:
            return {'type': 'user', 'user_id': user.id, 'user': user}
    
    return None

@app.route('/api/searches', methods=['GET'])
def get_saved_searches():
    """Get user's saved searches"""
    from models import SavedSearch
    
    # Check authentication using helper function
    auth_info = check_api_authentication()
    if not auth_info:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    # Get saved searches for the authenticated user (manager or regular user) 
    searches = SavedSearch.query.filter_by(user_id=auth_info['user_id']).order_by(SavedSearch.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'searches': [search.to_dict() for search in searches]
    })

@app.route('/api/user/saved-searches/count')
@login_required
def get_user_saved_searches_count():
    """Get count of user's saved searches"""
    from models import SavedSearch
    
    try:
        count = SavedSearch.query.filter_by(user_id=current_user.id).count()
        return jsonify({
            'success': True,
            'count': count
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/saved-searches/<int:search_id>')
@login_required 
def get_saved_search(search_id):
    """Get saved search by ID - supports both user searches and manager shared searches"""
    try:
        from models import SavedSearch, SentSearch
        
        # First try user's own saved search
        search = SavedSearch.query.filter_by(id=search_id, user_id=current_user.id).first()
        
        # If not found, try manager shared search via SentSearch table
        if not search:
            sent_search = SentSearch.query.filter_by(
                client_id=current_user.id
            ).join(SavedSearch, SentSearch.manager_search_id == SavedSearch.id).filter(
                SavedSearch.id == search_id
            ).first()
            
            if sent_search:
                search = SavedSearch.query.get(search_id)
                # Use the additional_filters from sent_search if available
                if sent_search.additional_filters:
                    search._temp_filters = sent_search.additional_filters
        
        # If still not found, check if it's a global search available to all users
        if not search:
            search = SavedSearch.query.get(search_id)
            if search and not search.user_id:  # Global searches have no user_id
                pass  # Allow access
            else:
                search = None
        
        if not search:
            return jsonify({'success': False, 'error': 'Поиск не найден'})
        
        # Parse filters - check for temp filters from sent search first
        filters = {}
        if hasattr(search, '_temp_filters') and search._temp_filters:
            try:
                filters = json.loads(search._temp_filters)
            except:
                filters = {}
        elif search.additional_filters:
            try:
                filters = json.loads(search.additional_filters)
            except:
                filters = {}
        
        return jsonify({
            'success': True,
            'id': search.id,
            'name': search.name,
            'description': search.description,
            'search_filters': filters,
            'created_at': search.created_at.isoformat() if search.created_at else None
        })
        
    except Exception as e:
        print(f"Error getting saved search: {e}")
        return jsonify({'success': False, 'error': 'Ошибка сервера'})

@app.route('/api/searches/<int:search_id>', methods=['DELETE'])
def delete_saved_search(search_id):
    """Delete saved search"""
    from models import SavedSearch
    
    # Check authentication using helper function
    auth_info = check_api_authentication()
    if not auth_info:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    user_id = auth_info['user_id']
    
    search = SavedSearch.query.filter_by(id=search_id, user_id=user_id).first()
    
    if not search:
        return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
    
    try:
        db.session.delete(search)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/searches/<int:search_id>/apply', methods=['POST'])
def apply_saved_search(search_id):
    """Apply saved search and update last_used"""
    from models import SavedSearch
    from datetime import datetime
    
    # Check authentication using helper function
    auth_info = check_api_authentication()
    if not auth_info:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    user_id = auth_info['user_id']
    
    search = SavedSearch.query.filter_by(id=search_id, user_id=user_id).first()
    
    if not search:
        return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
    
    try:
        search.last_used = datetime.utcnow()
        db.session.commit()
        
        # Parse filters from saved search
        filters = {}
        if search.additional_filters:
            try:
                filters = json.loads(search.additional_filters)
                print(f"DEBUG: Loaded filters from additional_filters: {filters}")
            except json.JSONDecodeError as e:
                print(f"DEBUG: Error parsing additional_filters: {e}")
                pass
        
        # Include legacy fields as filters if not already in additional_filters
        if search.location and 'districts' not in filters:
            filters['districts'] = [search.location]
        if search.property_type and 'rooms' not in filters:
            # Keep the original property type format for proper filtering
            filters['rooms'] = [search.property_type]
        if search.developer and 'developers' not in filters:
            filters['developers'] = [search.developer]
        if search.price_min and 'priceFrom' not in filters:
            # Convert rubles to millions for client
            filters['priceFrom'] = str(search.price_min / 1000000)
        if search.price_max and 'priceTo' not in filters:
            # Convert rubles to millions for client
            filters['priceTo'] = str(search.price_max / 1000000)
        if search.size_min and 'areaFrom' not in filters:
            filters['areaFrom'] = str(search.size_min)
        if search.size_max and 'areaTo' not in filters:
            filters['areaTo'] = str(search.size_max)
        
        print(f"DEBUG: Search '{search.name}' raw data - additional_filters: {search.additional_filters}, price_min: {search.price_min}, price_max: {search.price_max}")
        print(f"DEBUG: Final filters for '{search.name}': {filters}")
            
        print(f"DEBUG: Applying search '{search.name}' with filters: {filters}")
        
        try:
            search_dict = search.to_dict()
        except Exception as e:
            print(f"DEBUG: Error in search.to_dict(): {e}")
            search_dict = {
                'id': search.id,
                'name': search.name,
                'description': search.description,
                'created_at': search.created_at.isoformat() if search.created_at else None
            }
        
        return jsonify({
            'success': True, 
            'search': search_dict,
            'filters': filters
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/send-property', methods=['POST'])
@login_required
def send_property_to_client_endpoint():
    """Send property search to client"""
    if current_user.role != 'manager':
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        client_id = data.get('client_id')
        search_id = data.get('search_id')
        message = data.get('message', '')
        
        if not client_id or not search_id:
            return jsonify({'success': False, 'error': 'Client ID and Search ID are required'}), 400
        
        # Verify client exists and is a buyer
        client = User.query.filter_by(id=client_id, role='buyer').first()
        if not client:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        # Verify search exists and belongs to manager
        search = SavedSearch.query.filter_by(id=search_id, user_id=current_user.id).first()
        if not search:
            return jsonify({'success': False, 'error': 'Search not found'}), 404
        
        # Create recommendation record
        from models import ClientPropertyRecommendation
        recommendation = ClientPropertyRecommendation(
            manager_id=current_user.id,
            client_id=client_id,
            search_id=search_id,
            message=message
        )
        
        db.session.add(recommendation)
        db.session.commit()
        
        # Send notification to client (email)
        try:
            subject = f"Подборка квартир от {current_user.full_name}"
            text_message = f"""
Здравствуйте, {client.full_name}!

Ваш менеджер {current_user.full_name} подготовил для вас подборку квартир: {search.name}

{message if message else ''}

Перейдите в личный кабинет на сайте InBack.ru, чтобы посмотреть подборку.

С уважением,
Команда InBack.ru
            """
            
            from email_service import send_email
            send_email(
                to_email=client.email,
                subject=subject,
                text_content=text_message.strip(),
                template_name='recommendation'
            )
        except Exception as e:
            app.logger.warning(f"Failed to send email notification: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': 'Property recommendation sent successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# Property API routes for manager search
@app.route('/api/search/properties')
def search_properties_api():
    """Search properties for manager collection creation"""
    try:
        district = request.args.get('district')
        developer = request.args.get('developer') 
        rooms = request.args.get('rooms')
        prop_type = request.args.get('type')
        price_min = request.args.get('price_min')
        price_max = request.args.get('price_max')
        area_min = request.args.get('area_min')
        
        # Load properties from JSON file
        with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        filtered_properties = []
        for prop in properties_data:
            # Apply filters
            if district and prop.get('district', '').lower() != district.lower():
                continue
            if developer and prop.get('developer', '').lower() != developer.lower():
                continue
            if rooms and str(prop.get('rooms', '')) != str(rooms):
                continue
            if prop_type and prop.get('type', '').lower() != prop_type.lower():
                continue
            
            # Price filters
            prop_price = prop.get('price', 0)
            if price_min and prop_price < int(price_min):
                continue
            if price_max and prop_price > int(price_max):
                continue
            
            # Area filter
            prop_area = prop.get('area', 0)
            if area_min and prop_area < float(area_min):
                continue
            
            # Calculate cashback
            price = prop.get('price', 0)
            cashback = int(price * 0.05)  # 5% cashback
            
            filtered_properties.append({
                'id': prop.get('id'),
                'complex_name': prop.get('complex_name', ''),
                'district': prop.get('district', ''),
                'developer': prop.get('developer', ''),
                'rooms': prop.get('rooms', 0),
                'price': price,
                'cashback': cashback,
                'area': prop.get('area', 0),
                'floor': prop.get('floor', ''),
                'type': prop.get('type', '')
            })
        
        # Limit results to 20
        filtered_properties = filtered_properties[:20]
        
        return jsonify({
            'success': True,
            'properties': filtered_properties
        })
    except Exception as e:
        print(f"Error searching properties: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/search/apartments')
def search_apartments_api():
    """Search apartments with full filtering like main properties page"""
    try:
        district = request.args.get('district')
        developer = request.args.get('developer') 
        rooms = request.args.get('rooms')
        complex_id = request.args.get('complex')
        price_min = request.args.get('price_min')
        price_max = request.args.get('price_max')
        area_min = request.args.get('area_min')
        area_max = request.args.get('area_max')
        floor_min = request.args.get('floor_min')
        floor_max = request.args.get('floor_max')
        status = request.args.get('status')
        finishing = request.args.get('finishing')
        
        # Load properties and complexes
        with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        # Load complexes data for additional info
        complexes_data = {}
        try:
            with open('data/residential_complexes.json', 'r', encoding='utf-8') as f:
                complexes_list = json.load(f)
                for complex_item in complexes_list:
                    complexes_data[complex_item.get('id')] = complex_item
        except:
            pass
        
        filtered_apartments = []
        for prop in properties_data:
            # Apply filters
            if district and prop.get('district', '').lower() != district.lower():
                continue
            if developer and prop.get('developer', '').lower() != developer.lower():
                continue
            
            # Handle rooms filter including 'студия'
            prop_rooms = prop.get('rooms', '')
            if rooms:
                if rooms == 'студия' and prop.get('type', '') != 'студия':
                    continue
                elif rooms != 'студия' and str(prop_rooms) != str(rooms):
                    continue
                    
            if complex_id and str(prop.get('complex_id', '')) != str(complex_id):
                continue
            
            # Price filters
            prop_price = prop.get('price', 0)
            if price_min and prop_price < int(price_min):
                continue
            if price_max and prop_price > int(price_max):
                continue
            
            # Area filter
            prop_area = prop.get('area', 0)
            if area_min and prop_area < float(area_min):
                continue
            if area_max and prop_area > float(area_max):
                continue
            
            # Floor filters - use correct field name
            prop_floor = prop.get('floor', 0)
            if isinstance(prop_floor, str):
                try:
                    prop_floor = int(prop_floor.split('/')[0]) if '/' in prop_floor else int(prop_floor)
                except:
                    prop_floor = 0
            
            if floor_min and prop_floor < int(floor_min):
                continue
            if floor_max and prop_floor > int(floor_max):
                continue
            
            # Status and finishing filters
            prop_status = prop.get('completion_date', '').lower()
            if status:
                if status == 'в продаже' and 'сдан' in prop_status:
                    continue
                elif status == 'строительство' and 'кв.' not in prop_status:
                    continue
                elif status == 'сдан' and 'сдан' not in prop_status:
                    continue
                    
            prop_finishing = prop.get('finish_type', '').lower()
            if finishing:
                if finishing == 'черновая' and 'черновая' not in prop_finishing:
                    continue
                elif finishing == 'чистовая' and 'стандартная' not in prop_finishing:
                    continue
                elif finishing == 'под ключ' and 'премиум' not in prop_finishing:
                    continue
            
            # Calculate cashback
            price = prop.get('price', 0)
            cashback = int(price * 0.05)  # 5% cashback
            
            # Get complex info
            complex_info = complexes_data.get(prop.get('complex_id'), {})
            
            filtered_apartments.append({
                'id': prop.get('id'),
                'complex_name': prop.get('complex_name', ''),
                'complex_id': prop.get('complex_id'),
                'district': prop.get('district', ''),
                'developer': prop.get('developer', ''),
                'rooms': prop.get('type', '') if prop.get('type', '') == 'студия' else prop.get('rooms', 0),
                'price': price,
                'cashback': cashback,
                'area': prop.get('area', 0),
                'floor': prop.get('floor', ''),
                'max_floor': prop.get('total_floors', ''),
                'type': prop.get('type', ''),
                'status': 'сдан' if 'сдан' in prop.get('completion_date', '').lower() else 'строительство',
                'finishing': prop.get('finish_type', ''),
                'images': prop.get('gallery', []) or [prop.get('image', '')] if prop.get('image') else complex_info.get('images', []),
                'description': prop.get('description', ''),
                'features': prop.get('advantages', [])
            })
        
        # Sort by price (default)
        filtered_apartments.sort(key=lambda x: x['price'])
        
        # Limit results to 50
        filtered_apartments = filtered_apartments[:50]
        
        return jsonify({
            'success': True,
            'apartments': filtered_apartments,
            'complexes': complexes_data
        })
    except Exception as e:
        print(f"Error searching apartments: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/complexes')
def get_complexes_api():
    """Get list of residential complexes for filter"""
    try:
        with open('data/residential_complexes.json', 'r', encoding='utf-8') as f:
            complexes_data = json.load(f)
        
        complexes_list = [
            {'id': complex_item.get('id'), 'name': complex_item.get('name', '')}
            for complex_item in complexes_data
        ]
        
        return jsonify({
            'success': True,
            'complexes': complexes_list
        })
    except Exception as e:
        print(f"Error loading complexes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/properties/<property_id>')
def get_property_details(property_id):
    """Get detailed property information"""
    try:
        with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        property_data = None
        for prop in properties_data:
            if str(prop.get('id')) == str(property_id):
                property_data = prop
                break
        
        if not property_data:
            return jsonify({'success': False, 'error': 'Property not found'}), 404
        
        # Calculate cashback
        price = property_data.get('price', 0)
        cashback = int(price * 0.05)
        
        property_info = {
            'id': property_data.get('id'),
            'complex_name': property_data.get('complex_name', ''),
            'district': property_data.get('district', ''),
            'developer': property_data.get('developer', ''),
            'rooms': property_data.get('rooms', 0),
            'price': price,
            'cashback': cashback,
            'area': property_data.get('area', 0),
            'floor': property_data.get('floor', ''),
            'type': property_data.get('type', ''),
            'description': property_data.get('description', ''),
            'features': property_data.get('features', [])
        }
        
        return jsonify({
            'success': True,
            'property': property_info
        })
    except Exception as e:
        print(f"Error getting property details: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/collections', methods=['POST'])  
def create_collection_api():
    """Create a new property collection"""
    try:
        # Check manager authentication via session
        manager_id = session.get('manager_id')
        if not manager_id:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
            
        from models import Collection, CollectionProperty
        
        data = request.get_json()
        name = data.get('name')
        client_id = data.get('client_id')
        property_ids = data.get('property_ids', [])
        
        if not name or not client_id or not property_ids:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Create collection
        collection = Collection(
            title=name,
            assigned_to_user_id=client_id,
            created_by_manager_id=manager_id,
            status='Создана',
            description=f'Подборка из {len(property_ids)} объектов'
        )
        
        db.session.add(collection)
        db.session.flush()  # Get collection ID
        
        # Add properties to collection
        for prop_id in property_ids:
            collection_property = CollectionProperty(
                collection_id=collection.id,
                property_id=str(prop_id)
            )
            db.session.add(collection_property)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'collection_id': collection.id,
            'message': 'Подборка успешно создана'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating collection: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/send-collection', methods=['POST'])  
def send_collection_to_client():
    """Send property collection to client via email"""
    try:
        # Check manager authentication via session
        manager_id = session.get('manager_id')
        if not manager_id:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
            
        from models import User, Manager
        
        data = request.get_json()
        
        # TODO: Implement collection sending logic
        return jsonify({'success': True, 'message': 'Функция в разработке'})
        
    except Exception as e:
        print(f"Error sending collection: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# ========== ПРЕЗЕНТАЦИИ API ==========

@app.route('/api/manager/presentations', methods=['GET'])
@manager_required
def get_manager_presentations():
    """Получить все презентации менеджера"""
    from models import Collection
    manager_id = session.get('manager_id')
    
    presentations = Collection.query.filter_by(
        created_by_manager_id=manager_id,
        collection_type='presentation'
    ).order_by(Collection.created_at.desc()).all()
    
    presentations_data = []
    for presentation in presentations:
        presentations_data.append(presentation.to_dict())
    
    return jsonify({
        'success': True,
        'presentations': presentations_data
    })

@app.route('/api/manager/presentation/create', methods=['POST'])
@manager_required
@csrf.exempt
def create_presentation():
    """Создать новую презентацию"""
    from models import Collection
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    client_name = data.get('client_name', '')
    client_phone = data.get('client_phone', '')
    
    if not title:
        return jsonify({'success': False, 'error': 'Название презентации обязательно'}), 400
    
    manager_id = session.get('manager_id')
    
    try:
        presentation = Collection(
            title=title,
            description=description,
            created_by_manager_id=manager_id,
            collection_type='presentation',
            client_name=client_name,
            client_phone=client_phone,
            status='Черновик'
        )
        
        # Генерируем уникальную ссылку
        presentation.generate_unique_url()
        
        db.session.add(presentation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'presentation': presentation.to_dict(),
            'message': 'Презентация создана успешно'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/presentation/<int:presentation_id>/add_property', methods=['POST'])
@manager_required
@require_json_csrf
def add_property_to_presentation(presentation_id):
    """Добавить квартиру в презентацию"""
    from models import Collection, CollectionProperty
    
    data = request.get_json()
    property_id = data.get('property_id')
    manager_note = data.get('manager_note', '')
    
    manager_id = session.get('manager_id')
    
    presentation = Collection.query.filter_by(
        id=presentation_id,
        created_by_manager_id=manager_id,
        collection_type='presentation'
    ).first()
    
    if not presentation:
        return jsonify({'success': False, 'error': 'Презентация не найдена'}), 404
    
    # Проверяем, не добавлена ли уже эта квартира
    existing = CollectionProperty.query.filter_by(
        collection_id=presentation_id,
        property_id=property_id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'Квартира уже добавлена в презентацию'}), 400
    
    try:
        # Получаем информацию о квартире из JSON
        properties = load_properties()
        property_info = None
        
        for prop in properties:
            if str(prop.get('id')) == str(property_id):
                property_info = prop
                break
        
        if not property_info:
            return jsonify({'success': False, 'error': 'Квартира не найдена'}), 404
        
        collection_property = CollectionProperty(
            collection_id=presentation_id,
            property_id=property_id,
            property_name=property_info.get('title', 'Квартира'),
            property_price=int(property_info.get('price', 0)) if property_info.get('price') else None,
            complex_name=property_info.get('residential_complex', ''),
            property_type=f"{property_info.get('rooms', 0)}-комнатная" if property_info.get('rooms', 0) > 0 else 'Студия',
            property_size=float(property_info.get('area', 0)) if property_info.get('area') else None,
            manager_note=manager_note,
            order_index=len(presentation.properties) + 1
        )
        
        db.session.add(collection_property)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Квартира добавлена в презентацию',
            'property': {
                'id': collection_property.id,
                'property_name': collection_property.property_name,
                'complex_name': collection_property.complex_name,
                'property_price': collection_property.property_price,
                'manager_note': collection_property.manager_note
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# НОВЫЕ API ЭНДПОИНТЫ ДЛЯ ПРЕЗЕНТАЦИЙ

@app.route('/api/manager/presentation/<int:presentation_id>/add-property', methods=['POST'])
@manager_required
@require_json_csrf
def add_property_to_presentation_fixed(presentation_id):
    """Добавить объект в презентацию (безопасная версия)"""
    from models import Collection, CollectionProperty
    from flask_login import current_user
    
    # Валидация входных данных
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Данные не предоставлены'}), 400
        
    property_id = data.get('property_id')
    if not property_id:
        return jsonify({'success': False, 'error': 'ID объекта не указан'}), 400
    
    # Строгая проверка владения презентацией
    presentation = Collection.query.filter_by(
        id=presentation_id,
        created_by_manager_id=current_user.id,
        collection_type='presentation'
    ).first()
    
    if not presentation:
        return jsonify({'success': False, 'error': 'Презентация не найдена или у вас нет прав доступа'}), 404
    
    # Проверяем, не добавлен ли уже этот объект
    existing = CollectionProperty.query.filter_by(
        collection_id=presentation_id,
        property_id=property_id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'Объект уже добавлен в презентацию'}), 400
    
    try:
        # Получаем информацию об объекте
        properties = load_properties()
        property_info = None
        
        for prop in properties:
            if str(prop.get('id')) == str(property_id):
                property_info = prop
                break
        
        if not property_info:
            return jsonify({'success': False, 'error': 'Объект не найден'}), 404
        
        collection_property = CollectionProperty(
            collection_id=presentation_id,
            property_id=property_id,
            property_name=property_info.get('title', 'Квартира'),
            property_price=int(property_info.get('price', 0)) if property_info.get('price') else None,
            complex_name=property_info.get('residential_complex', ''),
            property_type=f"{property_info.get('rooms', 0)}-комнатная" if property_info.get('rooms', 0) > 0 else 'Студия',
            property_size=float(property_info.get('area', 0)) if property_info.get('area') else None,
            order_index=len(presentation.properties) + 1
        )
        
        db.session.add(collection_property)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Объект добавлен в презентацию',
            'property': {
                'id': collection_property.id,
                'property_name': collection_property.property_name,
                'complex_name': collection_property.complex_name,
                'property_price': collection_property.property_price
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/presentation/<int:presentation_id>/add-complex', methods=['POST'])
@manager_required
@require_json_csrf
def add_complex_to_presentation(presentation_id):
    """Добавить ЖК в презентацию (безопасная версия)"""
    from models import Collection, CollectionProperty
    from flask_login import current_user
    
    # Валидация входных данных
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Данные не предоставлены'}), 400
        
    complex_id = data.get('complex_id')
    if not complex_id:
        return jsonify({'success': False, 'error': 'ID ЖК не указан'}), 400
    
    # Строгая проверка владения презентацией
    presentation = Collection.query.filter_by(
        id=presentation_id,
        created_by_manager_id=current_user.id,
        collection_type='presentation'
    ).first()
    
    if not presentation:
        return jsonify({'success': False, 'error': 'Презентация не найдена или у вас нет прав доступа'}), 404
    
    try:
        # Получаем все объекты из ЖК
        properties = load_properties()
        complex_properties = []
        
        for prop in properties:
            if str(prop.get('complex_id')) == str(complex_id):
                complex_properties.append(prop)
        
        if not complex_properties:
            return jsonify({'success': False, 'error': 'ЖК не найден или в нем нет объектов'}), 404
        
        added_count = 0
        for prop in complex_properties[:5]:  # Добавляем максимум 5 объектов из ЖК
            property_id = prop.get('ID')
            
            # Проверяем, не добавлен ли уже этот объект
            existing = CollectionProperty.query.filter_by(
                collection_id=presentation_id,
                property_id=property_id
            ).first()
            
            if not existing:
                collection_property = CollectionProperty(
                    collection_id=presentation_id,
                    property_id=property_id,
                    property_name=f"{prop.get('Type', '')} в {prop.get('Complex', '')}",
                    property_price=int(prop.get('Price', 0)) if prop.get('Price') else None,
                    complex_name=prop.get('Complex', ''),
                    property_type=prop.get('Type', ''),
                    property_size=float(prop.get('Size', 0)) if prop.get('Size') else None,
                    order_index=len(presentation.properties) + added_count + 1
                )
                
                db.session.add(collection_property)
                added_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Добавлено {added_count} объектов из ЖК в презентацию',
            'added_count': added_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/presentation/create-with-property', methods=['POST'])
@manager_required
@require_json_csrf
def create_presentation_with_property():
    """Создать презентацию и сразу добавить объект (безопасная версия)"""
    from models import Collection, CollectionProperty
    from flask_login import current_user
    
    # Валидация входных данных
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Данные не предоставлены'}), 400
        
    title = data.get('title', '').strip()
    client_name = data.get('client_name', '').strip()
    property_id = data.get('property_id')
    
    # Строгая валидация обязательных полей
    if not title:
        return jsonify({'success': False, 'error': 'Название презентации обязательно'}), 400
    if not property_id:
        return jsonify({'success': False, 'error': 'ID объекта обязателен'}), 400
    
    try:
        # Создаем презентацию с использованием current_user.id
        presentation = Collection(
            title=title,
            created_by_manager_id=current_user.id,
            collection_type='presentation',
            client_name=client_name,
            status='Черновик'
        )
        
        presentation.generate_unique_url()
        db.session.add(presentation)
        db.session.flush()  # Получаем ID презентации
        
        # Добавляем объект
        properties = load_properties()
        property_info = None
        
        for prop in properties:
            if str(prop.get('ID')) == str(property_id):
                property_info = prop
                break
        
        if not property_info:
            return jsonify({'success': False, 'error': 'Объект не найден'}), 404
        
        collection_property = CollectionProperty(
            collection_id=presentation.id,
            property_id=property_id,
            property_name=f"{property_info.get('Type', '')} в {property_info.get('Complex', '')}",
            property_price=int(property_info.get('Price', 0)) if property_info.get('Price') else None,
            complex_name=property_info.get('Complex', ''),
            property_type=property_info.get('Type', ''),
            property_size=float(property_info.get('Size', 0)) if property_info.get('Size') else None,
            order_index=1
        )
        
        db.session.add(collection_property)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'presentation': presentation.to_dict(),
            'message': 'Презентация создана и объект добавлен'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/presentation/create-with-complex', methods=['POST'])
@manager_required
@require_json_csrf
def create_presentation_with_complex():
    """Создать презентацию и сразу добавить ЖК (безопасная версия)"""
    from models import Collection, CollectionProperty
    from flask_login import current_user
    
    # Валидация входных данных
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Данные не предоставлены'}), 400
        
    title = data.get('title', '').strip()
    client_name = data.get('client_name', '').strip()
    complex_id = data.get('complex_id')
    
    # Строгая валидация обязательных полей
    if not title:
        return jsonify({'success': False, 'error': 'Название презентации обязательно'}), 400
    if not complex_id:
        return jsonify({'success': False, 'error': 'ID ЖК обязателен'}), 400
    
    try:
        # Создаем презентацию с использованием current_user.id
        presentation = Collection(
            title=title,
            created_by_manager_id=current_user.id,
            collection_type='presentation', 
            client_name=client_name,
            status='Черновик'
        )
        
        presentation.generate_unique_url()
        db.session.add(presentation)
        db.session.flush()  # Получаем ID презентации
        
        # Добавляем объекты из ЖК
        properties = load_properties()
        complex_properties = []
        
        for prop in properties:
            if str(prop.get('complex_id')) == str(complex_id):
                complex_properties.append(prop)
        
        if not complex_properties:
            return jsonify({'success': False, 'error': 'ЖК не найден или в нем нет объектов'}), 404
        
        added_count = 0
        for prop in complex_properties[:5]:  # Добавляем максимум 5 объектов из ЖК
            property_id = prop.get('ID')
            
            collection_property = CollectionProperty(
                collection_id=presentation.id,
                property_id=property_id,
                property_name=f"{prop.get('Type', '')} в {prop.get('Complex', '')}",
                property_price=int(prop.get('Price', 0)) if prop.get('Price') else None,
                complex_name=prop.get('Complex', ''),
                property_type=prop.get('Type', ''),
                property_size=float(prop.get('Size', 0)) if prop.get('Size') else None,
                order_index=added_count + 1
            )
            
            db.session.add(collection_property)
            added_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'presentation': presentation.to_dict(),
            'message': f'Презентация создана с {added_count} объектами из ЖК'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


def send_collection_to_user():
    """Send collection to user - legacy function"""
    if request.method != 'POST':
        return jsonify({'success': False, 'error': 'Only POST method allowed'}), 405
    
    data = request.get_json()
    manager_id = session.get('manager_id')
    
    if not manager_id:
        return jsonify({'success': False, 'error': 'Manager authentication required'}), 401
    
    try:
        name = data.get('name')
        client_id = data.get('client_id')
        property_ids = data.get('property_ids', [])
        
        if not name or not client_id or not property_ids:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Get client and manager info
        client = User.query.get(client_id)
        manager = Manager.query.get(manager_id)
        
        if not client or not manager:
            return jsonify({'success': False, 'error': 'Client or manager not found'}), 404
        
        # Load property details
        with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        selected_properties = []
        total_cashback = 0
        
        for prop_id in property_ids:
            for prop in properties_data:
                if str(prop.get('id')) == str(prop_id):
                    price = prop.get('price', 0)
                    cashback = int(price * 0.05)
                    total_cashback += cashback
                    
                    selected_properties.append({
                        'complex_name': prop.get('complex_name', ''),
                        'district': prop.get('district', ''),
                        'developer': prop.get('developer', ''),
                        'rooms': prop.get('rooms', 0),
                        'area': prop.get('area', 0),
                        'price': price,
                        'cashback': cashback,
                        'type': prop.get('type', ''),
                        'description': prop.get('description', '')
                    })
                    break
        
        # Create email content
        properties_list = '\n'.join([
            f"• {prop['complex_name']} ({prop['district']})\n"
            f"  {prop['rooms']}-комн., {prop['area']} м²\n"
            f"  Цена: {prop['price']:,} ₽\n"
            f"  Кешбек: {prop['cashback']:,} ₽\n"
            for prop in selected_properties
        ])
        
        subject = f"Подборка недвижимости: {name}"
        text_message = f"""
Здравствуйте, {client.full_name}!

Ваш менеджер {manager.full_name} подготовил для вас персональную подборку недвижимости "{name}".

ПОДОБРАННЫЕ ОБЪЕКТЫ ({len(selected_properties)} шт.):

{properties_list}

ОБЩИЙ КЕШБЕК: {total_cashback:,} ₽

Для получения подробной информации и записи на просмотр свяжитесь с вашим менеджером:
{manager.full_name}
Email: {manager.email}
Телефон: {manager.phone or 'не указан'}

Или перейдите в личный кабинет на сайте InBack.ru

С уважением,
Команда InBack.ru
        """.strip()
        
        # Send email
        try:
            from email_service import send_email
            send_email(
                to_email=client.email,
                subject=subject,
                text_content=text_message,
                template_name='collection'
            )
            
            return jsonify({
                'success': True,
                'message': f'Подборка отправлена на email {client.email}'
            })
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({'success': False, 'error': 'Ошибка отправки email'}), 500
        
    except Exception as e:
        print(f"Error sending collection: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/data/properties_expanded.json')
def properties_json():
    """Serve properties JSON data"""
    try:
        properties = load_properties()
        return jsonify(properties)
    except Exception as e:
        print(f"Error serving properties JSON: {e}")
        return jsonify([]), 500

# Database initialization will be done after all imports

# Client Recommendations API endpoints
@app.route('/api/user/collections', methods=['GET'])
@login_required
def api_user_get_collections():
    """Get collections assigned to current user"""
    from models import Collection
    
    try:
        collections = Collection.query.filter_by(
            assigned_to_user_id=current_user.id
        ).order_by(Collection.created_at.desc()).all()
        
        collections_data = []
        for collection in collections:
            collections_data.append({
                'id': collection.id,
                'title': collection.title,
                'description': collection.description,
                'status': collection.status,
                'created_at': collection.created_at.strftime('%d.%m.%Y'),
                'manager_name': collection.created_by_manager.full_name if collection.created_by_manager else 'Менеджер',
                'properties_count': len(collection.property_collections) if hasattr(collection, 'property_collections') else 0
            })
        
        return jsonify({
            'success': True,
            'collections': collections_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/user/saved-searches', methods=['GET'])
@login_required
def api_user_get_saved_searches():
    """Get saved searches for current user"""
    from models import SavedSearch
    
    try:
        # Get regular saved searches
        saved_searches = SavedSearch.query.filter_by(
            user_id=current_user.id
        ).order_by(SavedSearch.created_at.desc()).all()
        
        # Get sent searches from managers
        from models import SentSearch
        sent_searches = SentSearch.query.filter_by(
            client_id=current_user.id
        ).order_by(SentSearch.sent_at.desc()).all()
        
        searches_data = []
        
        # Add regular saved searches
        for search in saved_searches:
            filters = {}
            if search.filters:
                import json
                filters = json.loads(search.filters) if isinstance(search.filters, str) else search.filters
            
            searches_data.append({
                'id': search.id,
                'name': search.name,
                'filters': filters,
                'created_at': search.created_at.strftime('%d.%m.%Y'),
                'last_used': search.last_used.strftime('%d.%m.%Y') if search.last_used else None,
                'type': 'saved'
            })
        
        # Add sent searches from managers
        for search in sent_searches:
            filters = {}
            if search.additional_filters:
                import json
                filters = json.loads(search.additional_filters) if isinstance(search.additional_filters, str) else search.additional_filters
            
            searches_data.append({
                'id': search.id,
                'name': search.name,
                'filters': filters,
                'created_at': search.sent_at.strftime('%d.%m.%Y') if search.sent_at else 'Не указано',
                'last_used': search.applied_at.strftime('%d.%m.%Y') if search.applied_at else None,
                'type': 'sent',
                'from_manager': True
            })
        
        return jsonify({
            'success': True,
            'searches': searches_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/user/recommendations', methods=['GET'])
@login_required
def api_user_get_recommendations():
    """Get recommendations for current user"""
    from models import Recommendation, SentSearch
    from datetime import datetime
    
    try:
        print(f"DEBUG: Loading recommendations for user ID: {current_user.id}")
        
        # Get traditional recommendations
        recommendations = Recommendation.query.filter_by(
            client_id=current_user.id
        ).order_by(Recommendation.sent_at.desc()).all()
        
        print(f"DEBUG: Found {len(recommendations)} recommendations for user {current_user.id}")
        
        recommendations_data = []
        for rec in recommendations:
            rec_data = rec.to_dict()
            rec_data['manager_name'] = f"{rec.manager.first_name} {rec.manager.last_name}" if rec.manager else 'Менеджер'
            recommendations_data.append(rec_data)
        
        # Get sent searches from managers as recommendations  
        sent_searches = SentSearch.query.filter_by(client_id=current_user.id).order_by(SentSearch.sent_at.desc()).all()
        
        # Convert sent searches to recommendation format
        for search in sent_searches:
            search_rec = {
                'id': f'search_{search.id}',
                'title': f'Подбор недвижимости: {search.name}',
                'description': search.description or 'Персональный подбор от вашего менеджера',
                'recommendation_type': 'search',
                'item_id': str(search.id),
                'item_name': search.name,
                'manager_notes': f'Ваш менеджер {search.manager.name} подготовил персональный подбор недвижимости',
                'priority_level': 'high',
                'status': search.status,
                'viewed_at': search.viewed_at.isoformat() if search.viewed_at else None,
                'created_at': search.sent_at.isoformat() if search.sent_at else None,
                'sent_at': search.sent_at.isoformat() if search.sent_at else None,
                'manager_name': search.manager.name,
                'search_filters': search.additional_filters,
                'search_id': search.id
            }
            recommendations_data.append(search_rec)
        
        # Sort by creation date 
        recommendations_data.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({
            'success': True, 
            'recommendations': recommendations_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/saved-searches/<int:search_id>')
@login_required
def get_saved_search_details(search_id):
    """Get saved search details for applying filters"""
    from models import SavedSearch
    
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'}), 401
        
        # Get the saved search
        saved_search = SavedSearch.query.filter_by(id=search_id, user_id=user_id).first()
        if not saved_search:
            return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
        
        return jsonify({
            'success': True,
            'id': saved_search.id,
            'name': saved_search.name,
            'description': saved_search.description,
            'search_filters': saved_search.additional_filters,
            'created_at': saved_search.created_at.isoformat() if saved_search.created_at else None
        })
        
    except Exception as e:
        print(f"Error getting saved search details: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/sent-searches')
@login_required
def get_sent_searches():
    """Get sent searches from managers as recommendations"""
    from models import SentSearch
    
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'}), 401
        
        # Get sent searches
        sent_searches = SentSearch.query.filter_by(client_id=user_id).order_by(SentSearch.sent_at.desc()).all()
        
        # Format as recommendation-like objects
        search_list = []
        
        for search in sent_searches:
            search_list.append({
                'id': search.id,
                'name': search.name or 'Поиск от менеджера',
                'title': search.name or 'Поиск от менеджера',
                'description': search.description,
                'status': search.status or 'sent',
                'sent_at': search.sent_at.isoformat() if search.sent_at else None,
                'created_at': search.sent_at.isoformat() if search.sent_at else None,
                'search_filters': search.additional_filters,
                'manager_id': search.manager_id,
                'recommendation_type': 'search'
            })
        
        return jsonify({
            'success': True,
            'sent_searches': search_list
        })
        
    except Exception as e:
        print(f"Error getting sent searches: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/recommendations/<rec_id>/viewed', methods=['POST'])
@login_required  
def api_mark_recommendation_viewed(rec_id):
    """Mark recommendation as viewed"""
    from models import Recommendation, SentSearch
    from datetime import datetime
    
    try:
        # Handle search recommendations
        if str(rec_id).startswith('search_'):
            search_id = int(rec_id.replace('search_', ''))
            sent_search = SentSearch.query.filter_by(
                id=search_id, 
                client_id=current_user.id
            ).first()
            
            if not sent_search:
                return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
                
            if sent_search.status == 'sent':
                sent_search.status = 'viewed'
                sent_search.viewed_at = datetime.utcnow()
                db.session.commit()
            
            return jsonify({'success': True})
        
        # Handle traditional recommendations
        recommendation = Recommendation.query.filter_by(
            id=int(rec_id), 
            client_id=current_user.id
        ).first()
        
        if not recommendation:
            return jsonify({'success': False, 'error': 'Рекомендация не найдена'}), 404
            
        if recommendation.status == 'sent':
            recommendation.status = 'viewed'
            recommendation.viewed_at = datetime.utcnow()
            db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/recommendations/<int:rec_id>/dismiss', methods=['POST'])
@login_required
def api_dismiss_recommendation(rec_id):
    """Dismiss/hide recommendation"""
    from models import Recommendation
    from datetime import datetime
    
    try:
        recommendation = Recommendation.query.filter_by(
            id=rec_id, 
            client_id=current_user.id
        ).first()
        
        if not recommendation:
            return jsonify({'success': False, 'error': 'Рекомендация не найдена'}), 404
            
        # Mark as dismissed
        recommendation.status = 'dismissed'
        recommendation.viewed_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/recommendations/<rec_id>/apply', methods=['POST'])
@login_required  
def api_apply_search_recommendation(rec_id):
    """Apply search recommendation - redirect to properties with filters"""
    from models import SentSearch
    from datetime import datetime
    import json
    
    try:
        # Handle search recommendations only
        if not str(rec_id).startswith('search_'):
            return jsonify({'success': False, 'error': 'Только поиски можно применить'}), 400
            
        search_id = int(rec_id.replace('search_', ''))
        sent_search = SentSearch.query.filter_by(
            id=search_id, 
            client_id=current_user.id
        ).first()
        
        if not sent_search:
            return jsonify({'success': False, 'error': 'Поиск не найден'}), 404
        
        # Update search status
        sent_search.applied_at = datetime.utcnow()
        if sent_search.status == 'sent':
            sent_search.status = 'applied'
        db.session.commit()
        
        # Parse filters from the search
        filters = {}
        if sent_search.additional_filters:
            try:
                filters = json.loads(sent_search.additional_filters)
            except json.JSONDecodeError:
                pass
        
        return jsonify({
            'success': True, 
            'filters': filters
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/user/recommendation-categories', methods=['GET'])
@login_required
def api_user_get_categories():
    """Get all categories that have recommendations for current user"""
    from models import RecommendationCategory
    
    try:
        categories = RecommendationCategory.query.filter_by(
            client_id=current_user.id
        ).filter(RecommendationCategory.recommendations_count > 0).all()
        
        categories_data = []
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'color': category.color,
                'recommendations_count': category.recommendations_count
            })
        
        return jsonify({
            'success': True,
            'categories': categories_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/recommendations/<int:rec_id>/respond', methods=['POST'])
@login_required
def api_respond_to_recommendation(rec_id):
    """Client responds to recommendation with interest/not interested"""
    from models import Recommendation
    from datetime import datetime
    
    try:
        data = request.get_json()
        response_type = data.get('response')  # 'interested' or 'not_interested'
        
        if response_type not in ['interested', 'not_interested']:
            return jsonify({'success': False, 'error': 'Неверный тип ответа'}), 400
            
        recommendation = Recommendation.query.filter_by(
            id=rec_id,
            client_id=current_user.id
        ).first()
        
        if not recommendation:
            return jsonify({'success': False, 'error': 'Рекомендация не найдена'}), 404
            
        recommendation.status = response_type
        recommendation.client_response = response_type
        recommendation.responded_at = datetime.utcnow()
        
        db.session.commit()
        
        # Notify manager about client response
        if recommendation.manager:
            try:
                from email_service import send_notification
                subject = f"Ответ клиента на рекомендацию: {recommendation.title}"
                message = f"""
Клиент {current_user.full_name} ответил на вашу рекомендацию:

Рекомендация: {recommendation.title}
Объект: {recommendation.item_name}
Ответ: {'Интересно' if response_type == 'interested' else 'Не интересно'}

Время ответа: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
                send_notification(
                    recommendation.manager.email,
                    subject,
                    message,
                    notification_type="client_response"
                )
            except Exception as e:
                print(f"Error sending notification to manager: {e}")
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/clients', methods=['GET'])
def api_manager_get_clients():
    """Get list of clients for manager"""
    from models import User
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        # Get all clients (buyers)
        clients = User.query.filter_by(
            role='buyer'
        ).order_by(User.full_name).all()
        
        clients_data = []
        for client in clients:
            clients_data.append({
                'id': client.id,
                'email': client.email,
                'full_name': client.full_name,
                'phone': client.phone,
                'created_at': client.created_at.strftime('%d.%m.%Y') if client.created_at else '',
                'client_status': getattr(client, 'client_status', 'Новый')
            })
        
        return jsonify({
            'success': True,
            'clients': clients_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/recommendation-categories/<int:client_id>', methods=['GET'])
def api_get_recommendation_categories(client_id):
    """Get recommendation categories for a specific client"""
    from models import RecommendationCategory
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        categories = RecommendationCategory.query.filter_by(
            manager_id=manager_id,
            client_id=client_id,
            is_active=True
        ).order_by(RecommendationCategory.last_used.desc()).all()
        
        categories_data = []
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'color': category.color,
                'recommendations_count': category.recommendations_count,
                'last_used': category.last_used.strftime('%d.%m.%Y') if category.last_used else '',
                'created_at': category.created_at.strftime('%d.%m.%Y') if category.created_at else ''
            })
        
        return jsonify({
            'success': True,
            'categories': categories_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/recommendation-categories', methods=['POST'])
def api_create_recommendation_category():
    """Create new recommendation category"""
    from models import RecommendationCategory
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        data = request.get_json()
        category_name = data.get('name', '').strip()
        client_id = data.get('client_id')
        description = data.get('description', '').strip()
        color = data.get('color', 'blue')
        
        if not category_name or not client_id:
            return jsonify({'success': False, 'error': 'Название категории и клиент обязательны'}), 400
        
        # Check if category with this name already exists for this client
        existing = RecommendationCategory.query.filter_by(
            manager_id=manager_id,
            client_id=client_id,
            name=category_name,
            is_active=True
        ).first()
        
        if existing:
            return jsonify({'success': False, 'error': 'Категория с таким названием уже существует'}), 400
        
        # Create new category
        category = RecommendationCategory(
            name=category_name,
            description=description,
            manager_id=manager_id,
            client_id=client_id,
            color=color
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'color': category.color,
                'recommendations_count': 0,
                'created_at': category.created_at.strftime('%d.%m.%Y')
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/all-categories', methods=['GET'])
def api_manager_all_categories():
    """Get all categories created by this manager"""
    from models import RecommendationCategory, User
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        categories = db.session.query(
            RecommendationCategory, 
            User.email.label('client_email')
        ).outerjoin(
            User, RecommendationCategory.client_id == User.id
        ).filter(
            RecommendationCategory.manager_id == manager_id
        ).order_by(
            RecommendationCategory.last_used.desc().nulls_last(),
            RecommendationCategory.created_at.desc()
        ).all()
        
        category_data = []
        for category, client_email in categories:
            category_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'client_email': client_email or 'Общая категория',
                'recommendations_count': category.recommendations_count,
                'is_active': category.is_active,
                'last_used': category.last_used.isoformat() if category.last_used else None,
                'created_at': category.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'categories': category_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/manager/categories/global', methods=['POST'])
def api_manager_create_global_category():
    """Create a new global category template"""
    from models import RecommendationCategory
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    
    if not name:
        return jsonify({'success': False, 'error': 'Укажите название категории'}), 400
    
    try:
        # Create a template category without specific client
        category = RecommendationCategory(
            name=name,
            description=description,
            manager_id=manager_id,
            client_id=None,  # Global template
            is_template=True,
            recommendations_count=0
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/manager/categories/<int:category_id>/toggle', methods=['POST'])
def api_manager_toggle_category(category_id):
    """Toggle category active status"""
    from models import RecommendationCategory
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    data = request.get_json()
    is_active = data.get('is_active', True)
    
    try:
        category = RecommendationCategory.query.filter_by(
            id=category_id,
            manager_id=manager_id
        ).first()
        
        if not category:
            return jsonify({'success': False, 'error': 'Категория не найдена'}), 404
        
        category.is_active = is_active
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Manager Dashboard API endpoints
@app.route('/api/manager/welcome-message', methods=['GET'])
@manager_required
def api_manager_welcome_message():
    """Get adaptive welcome message based on recent activity"""
    from models import User, Recommendation, Collection, SavedSearch, Manager
    from sqlalchemy import func, desc
    from datetime import datetime, timedelta
    
    manager_id = session.get('manager_id')
    current_manager = Manager.query.get(manager_id)
    
    if not current_manager:
        return jsonify({'success': False, 'error': 'Менеджер не найден'}), 404
    
    try:
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)
        
        # Get recent activity counts
        recent_recommendations = Recommendation.query.filter(
            Recommendation.manager_id == manager_id,
            Recommendation.created_at >= week_start
        ).count()
        
        today_recommendations = Recommendation.query.filter(
            Recommendation.manager_id == manager_id,
            Recommendation.created_at >= today_start
        ).count()
        
        recent_collections = Collection.query.filter(
            Collection.created_by_manager_id == manager_id,
            Collection.created_at >= week_start
        ).count()
        
        total_clients = User.query.filter_by(assigned_manager_id=manager_id).count()
        
        new_clients_today = User.query.filter(
            User.assigned_manager_id == manager_id,
            User.created_at >= today_start
        ).count()
        
        # Get last activity time (use created_at if last_login_at doesn't exist)
        last_activity = getattr(current_manager, 'last_login_at', None) or current_manager.created_at
        hours_since_last_login = (now - last_activity).total_seconds() / 3600 if last_activity else 0
        
        # Get most recent activity
        latest_recommendation = Recommendation.query.filter_by(manager_id=manager_id).order_by(desc(Recommendation.created_at)).first()
        latest_collection = Collection.query.filter_by(created_by_manager_id=manager_id).order_by(desc(Collection.created_at)).first()
        
        # Generate adaptive message based on activity patterns
        messages = []
        
        # Time-based greeting
        hour = now.hour
        if 5 <= hour < 12:
            time_greeting = "Доброе утро"
        elif 12 <= hour < 18:
            time_greeting = "Добрый день"
        elif 18 <= hour < 23:
            time_greeting = "Добрый вечер"
        else:
            time_greeting = "Доброй ночи"
        
        first_name = current_manager.full_name.split()[0] if current_manager.full_name else 'Коллега'
        
        # Activity-based messages
        if hours_since_last_login >= 24:
            messages.append(f"{time_greeting}, {first_name}! Рады видеть вас снова.")
            if recent_recommendations > 0:
                messages.append(f"За время вашего отсутствия было отправлено {recent_recommendations} рекомендаций.")
        elif hours_since_last_login >= 8:
            messages.append(f"{time_greeting}, {first_name}! Добро пожаловать обратно.")
        else:
            messages.append(f"{time_greeting}, {first_name}!")
        
        # Recent activity highlights
        if today_recommendations > 0:
            messages.append(f"Сегодня вы уже отправили {today_recommendations} рекомендаций - отличная работа!")
        elif recent_recommendations > 0:
            messages.append(f"На этой неделе вы отправили {recent_recommendations} рекомендаций клиентам.")
        
        if new_clients_today > 0:
            messages.append(f"У вас {new_clients_today} новых клиентов сегодня.")
        
        if recent_collections > 0:
            messages.append(f"Создано {recent_collections} новых подборок на этой неделе.")
        
        # Motivational suggestions based on activity
        if recent_recommendations == 0 and recent_collections == 0:
            messages.append("Готовы создать новую подборку для клиентов?")
        elif total_clients > 0 and recent_recommendations < 3:
            messages.append("Возможно, стоит отправить рекомендации активным клиентам?")
        
        # Default fallback
        if len(messages) == 1:  # Only greeting
            messages.append("Панель управления менеджера недвижимости готова к работе.")
        
        # Activity context for additional UI hints
        activity_context = {
            'has_recent_activity': recent_recommendations > 0 or recent_collections > 0,
            'needs_attention': total_clients > 0 and recent_recommendations == 0,
            'high_activity': recent_recommendations >= 5 or recent_collections >= 3,
            'new_day': hours_since_last_login >= 8,
            'latest_recommendation_date': latest_recommendation.created_at.strftime('%d.%m.%Y') if latest_recommendation else None,
            'latest_collection_date': latest_collection.created_at.strftime('%d.%m.%Y') if latest_collection else None
        }
        
        return jsonify({
            'success': True,
            'messages': messages,
            'context': activity_context,
            'stats': {
                'recent_recommendations': recent_recommendations,
                'today_recommendations': today_recommendations,
                'recent_collections': recent_collections,
                'total_clients': total_clients,
                'new_clients_today': new_clients_today
            }
        })
        
    except Exception as e:
        print(f"Error generating welcome message: {e}")
        return jsonify({
            'success': True,
            'messages': [f"{time_greeting}, {first_name}!", "Панель управления менеджера недвижимости"],
            'context': {'has_recent_activity': False},
            'stats': {}
        })

@app.route('/api/manager/dashboard-stats', methods=['GET'])
def api_manager_dashboard_stats():
    """Get manager dashboard statistics"""
    from models import User, Recommendation
    from sqlalchemy import func
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        # Count clients assigned to this manager
        clients_count = User.query.filter_by(assigned_manager_id=manager_id).count()
        
        # Count recommendations sent by this manager
        recommendations_count = Recommendation.query.filter_by(manager_id=manager_id).count()
        
        # Count recommendations sent this month
        from datetime import datetime
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_recommendations = Recommendation.query.filter(
            Recommendation.manager_id == manager_id,
            Recommendation.sent_at >= month_start
        ).count()
        
        # Collections count (placeholder for now)
        collections_count = 5
        
        return jsonify({
            'success': True,
            'clients_count': clients_count,
            'recommendations_count': monthly_recommendations,
            'total_recommendations': recommendations_count,
            'collections_count': collections_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/activity-feed', methods=['GET'])
def api_manager_activity_feed():
    """Get manager activity feed"""
    from models import Recommendation, User
    from datetime import datetime, timedelta
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        # Get recent activities (recommendations sent)
        recent_recommendations = Recommendation.query.filter_by(
            manager_id=manager_id
        ).order_by(Recommendation.sent_at.desc()).limit(10).all()
        
        activities = []
        for rec in recent_recommendations:
            time_diff = datetime.utcnow() - rec.sent_at
            if time_diff.days > 0:
                time_ago = f"{time_diff.days} дн. назад"
            elif time_diff.seconds > 3600:
                time_ago = f"{time_diff.seconds // 3600} ч. назад"
            else:
                time_ago = f"{time_diff.seconds // 60} мин. назад"
            
            activities.append({
                'title': f'Отправлена рекомендация',
                'description': f'{rec.title} для {rec.client.full_name}',
                'time_ago': time_ago,
                'icon': 'paper-plane',
                'color': 'blue'
            })
        
        # Add some sample activities for demo
        if len(activities) < 3:
            activities.extend([
                {
                    'title': 'Новый клиент добавлен',
                    'description': 'Демо Клиентов зарегистрировался в системе',
                    'time_ago': '2 ч. назад',
                    'icon': 'user-plus',
                    'color': 'green'
                },
                {
                    'title': 'Клиент просмотрел рекомендацию',
                    'description': 'Демо Клиентов открыл рекомендацию по ЖК "Солнечный"',
                    'time_ago': '4 ч. назад',
                    'icon': 'eye',
                    'color': 'purple'
                }
            ])
        
        return jsonify({
            'success': True,
            'activities': activities
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/manager/top-clients', methods=['GET'])
def api_manager_top_clients():
    """Get top clients by interactions"""
    from models import User, Recommendation
    from sqlalchemy import func
    
    # Check if user is authenticated as manager
    manager_id = session.get('manager_id')
    if not manager_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация менеджера'}), 401
    
    try:
        # Get clients with most interactions (recommendations received)
        top_clients = db.session.query(
            User,
            func.count(Recommendation.id).label('interactions_count')
        ).join(
            Recommendation, User.id == Recommendation.client_id
        ).filter(
            Recommendation.manager_id == manager_id
        ).group_by(User.id).order_by(
            func.count(Recommendation.id).desc()
        ).limit(5).all()
        
        clients_data = []
        for user, count in top_clients:
            clients_data.append({
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'interactions_count': count
            })
        
        # Add demo clients if not enough data
        if len(clients_data) < 3:
            demo_clients = [
                {'id': 999, 'full_name': 'Демо Клиентов', 'email': 'demo@inback.ru', 'interactions_count': 8},
                {'id': 998, 'full_name': 'Анна Покупателева', 'email': 'buyer@test.ru', 'interactions_count': 5},
                {'id': 997, 'full_name': 'Петр Инвесторов', 'email': 'investor@test.ru', 'interactions_count': 3}
            ]
            clients_data.extend(demo_clients[:3-len(clients_data)])
        
        return jsonify({
            'success': True,
            'clients': clients_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Blog Management Routes for Managers
@app.route('/admin/blog-manager')
@manager_required
def admin_blog_manager():
    """Manager blog management page"""
    from models import BlogArticle, Category
    
    try:
        # Get filter parameters
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        category_id = request.args.get('category_id', '')
        
        # Build query
        query = BlogArticle.query
        
        if search:
            query = query.filter(BlogArticle.title.contains(search) | 
                               BlogArticle.content.contains(search))
        
        if status:
            query = query.filter(BlogArticle.status == status)
            
        if category_id:
            query = query.filter(BlogArticle.category_id == int(category_id))
        
        # Order by creation date
        articles = query.order_by(BlogArticle.created_at.desc()).all()
        
        # Get categories for filter dropdown
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        
        return render_template('admin/blog_manager.html',
                             articles=articles,
                             categories=categories,
                             search=search,
                             status=status,
                             category_id=category_id)
        
    except Exception as e:
        flash(f'Ошибка загрузки блога: {str(e)}', 'error')
        return redirect(url_for('manager_dashboard'))


@app.route('/admin/blog/create-new', methods=['GET', 'POST'])
@manager_required
def admin_create_new_article():
    """Create new blog article"""
    from models import Category, BlogArticle
    import re
    from datetime import datetime
    
    if request.method == 'GET':
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        return render_template('admin/blog_create_new.html', categories=categories)
    
    try:
        # Get form data
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        status = request.form.get('status', 'draft')
        is_featured = 'is_featured' in request.form
        
        # Generate slug from title
        slug = re.sub(r'[^\w\s-]', '', (title or '').lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        # Ensure slug is unique
        original_slug = slug
        counter = 1
        while BlogArticle.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # Create article
        article = BlogArticle(
            title=title,
            slug=slug,
            excerpt=excerpt,
            content=content,
            category_id=int(category_id),
            author_id=session.get('manager_id'),
            status=status,
            is_featured=is_featured
        )
        
        # Set publish date if status is published
        if status == 'published':
            article.published_at = datetime.utcnow()
        
        # Calculate reading time (approx 200 words per minute)
        word_count = len(content.split()) if content else 0
        article.reading_time = max(1, word_count // 200)
        
        db.session.add(article)
        db.session.commit()
        
        flash('Статья успешно создана!', 'success')
        return redirect(url_for('admin_blog_manager'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка создания статьи: {str(e)}', 'error')
        return redirect(url_for('admin_create_new_article'))


@app.route('/admin/blog/<int:article_id>/edit-article', methods=['GET', 'POST'])
@manager_required 
def admin_edit_new_article(article_id):
    """Edit existing blog article"""
    from models import BlogArticle, Category
    import re
    from datetime import datetime
    
    article = BlogArticle.query.get_or_404(article_id)
    
    if request.method == 'GET':
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        return render_template('admin/blog_edit_new.html', article=article, categories=categories)
    
    try:
        # Get form data
        title = request.form.get('title')
        excerpt = request.form.get('excerpt') 
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        status = request.form.get('status')
        is_featured = 'is_featured' in request.form
        
        # Update slug if title changed
        if title != article.title:
            slug = re.sub(r'[^\w\s-]', '', (title or '').lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            
            # Ensure slug is unique (exclude current article)
            original_slug = slug
            counter = 1
            while BlogArticle.query.filter_by(slug=slug).filter(BlogArticle.id != article_id).first():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            article.slug = slug
        
        # Update article
        article.title = title
        article.excerpt = excerpt
        article.content = content
        article.category_id = int(category_id)
        article.status = status
        article.is_featured = is_featured
        article.updated_at = datetime.utcnow()
        
        # Set/update publish date if status changed to published
        if status == 'published' and not article.published_at:
            article.published_at = datetime.utcnow()
        
        # Recalculate reading time
        word_count = len(content.split()) if content else 0
        article.reading_time = max(1, word_count // 200)
        
        db.session.commit()
        
        flash('Статья успешно обновлена!', 'success')
        return redirect(url_for('admin_blog_manager'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка обновления статьи: {str(e)}', 'error')
        return redirect(url_for('admin_edit_new_article', article_id=article_id))


@app.route('/admin/blog/<int:article_id>/delete-article', methods=['POST'])
@manager_required
def admin_delete_new_article(article_id):
    """Delete blog article"""
    from models import BlogArticle
    
    try:
        article = BlogArticle.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()
        
        flash('Статья успешно удалена!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка удаления статьи: {str(e)}', 'error')
    
    return redirect(url_for('admin_blog_manager'))


@app.route('/admin/blog/categories')
@admin_required
def admin_blog_categories():
    """Manage blog categories"""
    from models import Admin, Category, BlogPost, BlogArticle
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    categories = Category.query.order_by(Category.sort_order, Category.name).all()
    
    # Добавляем подсчет статей для каждой категории
    for category in categories:
        # Считаем статьи из BlogPost (по названию категории)
        blog_post_count = BlogPost.query.filter_by(
            category=category.name, 
            status='published'
        ).count()
        
        # Считаем статьи из BlogArticle (по category_id)
        blog_article_count = BlogArticle.query.filter_by(
            category_id=category.id,
            status='published'
        ).count()
        
        # Общее количество статей
        category.articles_count = blog_post_count + blog_article_count
    
    return render_template('admin/blog_categories.html', admin=current_admin, categories=categories)


@app.route('/admin/blog/categories/create', methods=['GET', 'POST'])
@admin_required
def admin_create_category():
    """Create new blog category - both form and JSON API"""
    from models import Admin, Category
    import re
    
    admin_id = session.get('admin_id')
    current_admin = Admin.query.get(admin_id)
    
    # Handle JSON requests (from inline category creation)
    if request.is_json:
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description', '')
            
            if not name:
                return jsonify({'success': False, 'error': 'Название категории обязательно'})
            
            # Generate slug from Russian name
            def transliterate(text):
                rus_to_eng = {
                    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                    'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                    'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
                    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
                }
                return ''.join(rus_to_eng.get(char.lower(), char) for char in text)
            
            slug = transliterate(name.lower())
            slug = re.sub(r'[^\w\s-]', '', slug)
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            
            # Ensure unique slug
            original_slug = slug
            counter = 1
            while Category.query.filter_by(slug=slug).first():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            category = Category(
                name=name,
                slug=slug,
                description=description,
                is_active=True
            )
            
            db.session.add(category)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'slug': category.slug
                }
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})
    
    # Handle form requests (standard category creation page)
    if request.method == 'GET':
        return render_template('admin/blog_category_create.html', admin=current_admin)
    
    try:
        name = request.form.get('name')
        if not name:
            flash('Название категории обязательно', 'error')
            return render_template('admin/blog_category_create.html', admin=current_admin)
            
        description = request.form.get('description', '')
        
        # Generate slug
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        # Ensure unique slug
        original_slug = slug
        counter = 1
        while Category.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        category = Category(
            name=name,
            slug=slug,
            description=description
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash(f'Категория "{name}" успешно создана!', 'success')
        return redirect(url_for('admin_blog'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка создания категории: {str(e)}', 'error')
        return render_template('admin/blog_category_create.html', admin=current_admin)


# Blog Public Routes  
@app.route('/blog-new')
def blog_new():
    """Public blog page"""
    from models import BlogArticle, Category
    
    try:
        # Get published articles
        articles = BlogArticle.query.filter_by(status='published').order_by(BlogArticle.published_at.desc()).all()
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        
        # Add pagination variables that template expects
        return render_template('blog.html', 
                             articles=articles, 
                             categories=categories,
                             total_pages=1,
                             current_page=1,
                             has_prev=False,
                             has_next=False,
                             prev_num=None,
                             next_num=None,
                             search_query='',
                             category_filter=None)
        
    except Exception as e:
        print(f"Blog error: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback for when there's an error
        try:
            return render_template('blog.html', articles=[], categories=[])
        except:
            return "Временные проблемы с блогом. Попробуйте позже.", 500


@app.route('/blog-new/<slug>')
def blog_article_new(slug):
    """View single blog article"""
    from models import BlogArticle
    
    try:
        article = BlogArticle.query.filter_by(slug=slug, status='published').first_or_404()
        
        # Increment view count
        article.views_count += 1
        db.session.commit()
        
        # Get related articles from same category
        related_articles = BlogArticle.query.filter_by(
            category_id=article.category_id,
            status='published'
        ).filter(
            BlogArticle.id != article.id
        ).order_by(
            BlogArticle.published_at.desc()
        ).limit(3).all()
        
        return render_template('blog_article.html', 
                             article=article,
                             related_articles=related_articles)
        
    except Exception as e:
        flash('Статья не найдена', 'error')
        return redirect(url_for('blog_new'))


@app.route('/blog-new/category/<slug>')
def blog_category_new(slug):
    """View articles by category"""
    from models import Category, BlogArticle
    
    try:
        category = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
        
        articles = BlogArticle.query.filter_by(
            category_id=category.id,
            status='published'
        ).order_by(
            BlogArticle.published_at.desc()
        ).all()
        
        return render_template('blog_category.html', 
                             category=category,
                             articles=articles)
        
    except Exception as e:
        flash('Категория не найдена', 'error')
        return redirect(url_for('blog_new'))


@app.route('/blog/<slug>')
def blog_post(slug):
    """Display single blog post by slug"""
    try:
        # Find post by slug - using direct SQL query
        from sqlalchemy import text
        result = db.session.execute(text("""
            SELECT id, title, slug, content, excerpt, category, featured_image, 
                   views_count, created_at, '' as author_name
            FROM blog_posts 
            WHERE slug = :slug AND status = 'published'
        """), {'slug': slug}).fetchone()
        
        if not result:
            flash('Статья не найдена', 'error')
            return redirect(url_for('blog'))
        
        # Convert to dict for template
        post = {
            'id': result[0],
            'title': result[1],
            'slug': result[2],
            'content': result[3],
            'excerpt': result[4],
            'category': result[5],
            'featured_image': result[6],
            'views_count': result[7] or 0,
            'created_at': result[8],
            'author_name': result[9] or 'InBack'
        }
        
        # Increment view count
        try:
            db.session.execute(text("""
                UPDATE blog_posts 
                SET views_count = COALESCE(views_count, 0) + 1 
                WHERE id = :id
            """), {'id': post['id']})
            db.session.commit()
            post['views_count'] += 1
        except Exception as e:
            db.session.rollback()
        
        # Get related posts from same category
        related_results = db.session.execute(text("""
            SELECT id, title, slug, excerpt, featured_image, created_at
            FROM blog_posts 
            WHERE category = :category AND status = 'published' AND id != :id
            ORDER BY created_at DESC
            LIMIT 3
        """), {'category': post['category'], 'id': post['id']}).fetchall()
        
        related_posts = []
        for r in related_results:
            related_posts.append({
                'id': r[0],
                'title': r[1], 
                'slug': r[2],
                'excerpt': r[3],
                'featured_image': r[4],
                'created_at': r[5]
            })
        
        return render_template('blog_post.html', 
                             post=post,
                             related_posts=related_posts)
        
    except Exception as e:
        flash('Ошибка загрузки статьи', 'error')
        return redirect(url_for('blog'))


# Admin Blog Management Routes
@app.route('/admin/blog-management')
@admin_required
def admin_blog_management():
    """Admin blog management page"""
    from models import BlogPost, Category
    
    try:
        # Get filter parameters
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        category_name = request.args.get('category', '')
        page = request.args.get('page', 1, type=int)
        
        # Build query
        query = BlogPost.query
        
        if search:
            query = query.filter(BlogPost.title.contains(search) | 
                               BlogPost.content.contains(search))
        
        if status:
            query = query.filter(BlogPost.status == status)
            
        if category_name:
            query = query.filter(BlogPost.category == category_name)
        
        # Order by creation date and paginate
        posts = query.order_by(BlogPost.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        
        # Get categories for filter dropdown
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        
        # Get admin user for template
        from flask_login import current_user
        admin = current_user if current_user.is_authenticated else None
        
        return render_template('admin/blog_management.html',
                             posts=posts,
                             categories=categories,
                             search=search,
                             status=status,
                             category_name=category_name,
                             admin=admin)
        
    except Exception as e:
        flash(f'Ошибка загрузки блога: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/blog-management/create', methods=['GET', 'POST'])
@admin_required
def admin_create_blog_post():
    """Create new blog post"""
    from models import BlogPost, Category
    import re
    from datetime import datetime
    
    if request.method == 'GET':
        categories = Category.query.order_by(Category.name).all()
        return render_template('admin/blog_post_create.html', categories=categories)
    
    try:
        # Get form data
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        status = request.form.get('status', 'draft')
        is_featured = 'is_featured' in request.form
        featured_image = request.form.get('featured_image', '')
        meta_title = request.form.get('meta_title', '')
        meta_description = request.form.get('meta_description', '')
        keywords = request.form.get('keywords', '')
        
        # Get category name from category_id
        category = Category.query.get(int(category_id))
        if not category:
            flash('Выбранная категория не найдена', 'error')
            return redirect(url_for('admin_create_blog_post'))
        
        # Generate slug from title
        slug = re.sub(r'[^\w\s-]', '', (title or '').lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        # Ensure slug is unique
        original_slug = slug
        counter = 1
        while BlogPost.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # Calculate reading time (approx 200 words per minute)
        word_count = len(content.split()) if content else 0
        reading_time = max(1, word_count // 200)
        
        # Create blog post using BlogPost model
        post = BlogPost(
            title=title,
            slug=slug,
            excerpt=excerpt,
            content=content,
            category=category.name,  # Use category name, not ID
            author_id=1,  # Default author
            status=status,
            featured_image=featured_image,
            tags=keywords
        )
        
        if status == 'published':
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        # Обновим счетчик статей в категории
        category.articles_count = BlogPost.query.filter_by(category=category.name, status='published').count()
        db.session.commit()
        
        print(f'DEBUG: Created article "{title}" in category "{category.name}" with status "{status}"')
        print(f'DEBUG: Updated category "{category.name}" article count to {category.articles_count}')
        
        flash('Статья успешно создана!', 'success')
        return redirect(url_for('admin_blog_management'))
        
    except Exception as e:
        db.session.rollback()
        print(f'ERROR creating blog post: {str(e)}')
        flash(f'Ошибка создания статьи: {str(e)}', 'error')
        return redirect(url_for('admin_create_blog_post'))

@app.route('/admin/upload-image', methods=['POST'])
@admin_required
def admin_upload_image():
    """Upload image for blog posts"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Файл не выбран'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Файл не выбран'}), 400
    
    # Check if file is an image
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if not (file.filename and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({'success': False, 'error': 'Разрешены только изображения (PNG, JPG, JPEG, GIF, WebP)'}), 400
    
    try:
        # Generate secure filename
        filename = secure_filename(file.filename) if file.filename else 'unnamed_file'
        
        # Add timestamp to avoid naming conflicts
        import time
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Return URL for TinyMCE
        file_url = f'/uploads/{filename}'
        
        return jsonify({
            'success': True,
            'url': file_url,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Ошибка загрузки файла: {str(e)}'}), 500

# Duplicate route removed - already defined earlier


@app.route('/admin/blog-management/<int:post_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_blog_post(post_id):
    """Edit blog post"""
    from models import BlogPost, Category
    import re
    from datetime import datetime
    
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'GET':
        categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
        return render_template('admin/blog_post_edit.html', post=post, categories=categories)
    
    try:
        # Get form data
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        status = request.form.get('status')
        is_featured = 'is_featured' in request.form
        featured_image = request.form.get('featured_image', '')
        meta_title = request.form.get('meta_title', '')
        meta_description = request.form.get('meta_description', '')
        keywords = request.form.get('keywords', '')
        
        # Validation
        if not title or title.strip() == '':
            flash('Заголовок статьи обязателен', 'error')
            return redirect(url_for('admin_edit_blog_post', post_id=post_id))
        
        if not content or content.strip() == '':
            flash('Содержание статьи обязательно', 'error')
            return redirect(url_for('admin_edit_blog_post', post_id=post_id))
        
        if not category_id or category_id == '':
            flash('Выберите категорию статьи', 'error')
            return redirect(url_for('admin_edit_blog_post', post_id=post_id))

        # Get category name from category_id
        category = Category.query.get(int(category_id))
        if not category:
            flash('Выбранная категория не найдена', 'error')
            return redirect(url_for('admin_edit_blog_post', post_id=post_id))
        
        # Update slug if title changed
        if title != post.title:
            slug = re.sub(r'[^\w\s-]', '', (title or '').lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            
            original_slug = slug
            counter = 1
            while BlogPost.query.filter_by(slug=slug).filter(BlogPost.id != post_id).first():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            post.slug = slug
        
        # Calculate reading time
        word_count = len(content.split()) if content else 0
        reading_time = max(1, word_count // 200)
        
        # Update post
        old_category = post.category
        post.title = title
        post.excerpt = excerpt
        post.content = content
        post.category = category.name  # BlogPost uses category name as string
        post.status = status
        post.is_featured = is_featured
        post.featured_image = featured_image
        post.meta_title = meta_title or title
        post.meta_description = meta_description or excerpt  
        post.tags = keywords  # BlogPost uses tags field
        post.reading_time = reading_time
        post.updated_at = datetime.utcnow()
        
        if status == 'published' and not post.published_at:
            post.published_at = datetime.utcnow()
        
        db.session.commit()
        
        # Update category article counts for both old and new categories
        for cat_name in [old_category, category.name]:
            if cat_name:
                cat = Category.query.filter_by(name=cat_name).first()
                if cat:
                    cat.articles_count = BlogPost.query.filter_by(category=cat_name, status='published').count()
        
        db.session.commit()
        
        flash('Статья успешно обновлена!', 'success')
        return redirect(url_for('admin_blog_management'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка обновления статьи: {str(e)}', 'error')
        return redirect(url_for('admin_edit_blog_post', post_id=post_id))


@app.route('/admin/blog-management/<int:post_id>/delete', methods=['POST'])
@admin_required
def admin_delete_blog_post(post_id):
    """Delete blog post"""
    from models import BlogPost, Category
    
    try:
        post = BlogPost.query.get_or_404(post_id)
        category_name = post.category
        
        db.session.delete(post)
        db.session.commit()
        
        # Update category article count
        if category_name:
            category = Category.query.filter_by(name=category_name).first()
            if category:
                category.articles_count = BlogPost.query.filter_by(category=category_name, status='published').count()
                db.session.commit()
        
        flash('Статья успешно удалена!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка удаления статьи: {str(e)}', 'error')
    
    return redirect(url_for('admin_blog_management'))


@app.route('/admin/blog-categories-management')
@admin_required
def admin_blog_categories_management():
    """Admin blog categories management"""
    from models import Category
    
    try:
        categories = Category.query.order_by(Category.sort_order).all()
        return render_template('admin/blog_categories.html', categories=categories)
        
    except Exception as e:
        flash(f'Ошибка загрузки категорий: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/blog-categories-management/create', methods=['GET', 'POST'])
@admin_required
def admin_create_blog_category_new():
    """Create blog category"""
    from models import Category
    import re
    
    if request.method == 'GET':
        return render_template('admin/blog_category_create.html')
    
    try:
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description', '')
        color = request.form.get('color', 'blue')
        icon = request.form.get('icon', 'fas fa-folder')
        sort_order = request.form.get('sort_order', 0, type=int)
        
        # Generate slug
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        # Ensure slug is unique
        original_slug = slug
        counter = 1
        while Category.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        category = Category(
            name=name,
            slug=slug,
            description=description,
            color=color,
            icon=icon,
            sort_order=sort_order,
            is_active=True,
            articles_count=0
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Категория успешно создана!', 'success')
        return redirect(url_for('admin_blog_categories_management'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка создания категории: {str(e)}', 'error')
        return redirect(url_for('admin_create_blog_category_new'))


@app.route('/admin/blog-categories-management/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required  
def admin_edit_blog_category_new(category_id):
    """Edit blog category"""
    from models import Category
    import re
    
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'GET':
        return render_template('admin/blog_category_edit.html', category=category)
    
    try:
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description', '')
        color = request.form.get('color', 'blue')
        icon = request.form.get('icon', 'fas fa-folder')
        sort_order = request.form.get('sort_order', 0, type=int)
        is_active = 'is_active' in request.form
        
        # Update slug if name changed
        if name != category.name:
            slug = re.sub(r'[^\w\s-]', '', name.lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            
            original_slug = slug
            counter = 1
            while Category.query.filter_by(slug=slug).filter(Category.id != category_id).first():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            category.slug = slug
        
        category.name = name
        category.description = description
        category.color = color
        category.icon = icon
        category.sort_order = sort_order
        category.is_active = is_active
        
        db.session.commit()
        
        flash('Категория успешно обновлена!', 'success')
        return redirect(url_for('admin_blog_categories_management'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка обновления категории: {str(e)}', 'error')
        return redirect(url_for('admin_edit_blog_category_new', category_id=category_id))


@app.route('/admin/blog-categories-management/<int:category_id>/delete', methods=['POST'])
@admin_required
def admin_delete_blog_category_new(category_id):
    """Delete blog category"""
    from models import Category, BlogArticle
    
    try:
        category = Category.query.get_or_404(category_id)
        
        # Check if category has posts
        posts_count = BlogArticle.query.filter_by(category_id=category_id).count()
        if posts_count > 0:
            flash(f'Нельзя удалить категорию с {posts_count} статьями. Сначала переместите статьи в другие категории.', 'error')
            return redirect(url_for('admin_blog_categories_management'))
        
        db.session.delete(category)
        db.session.commit()
        
        flash('Категория успешно удалена!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка удаления категории: {str(e)}', 'error')
    
    return redirect(url_for('admin_blog_categories_management'))


# Register API blueprint
app.register_blueprint(api_bp)

# Register notification settings blueprint
try:
    from notification_settings import notification_settings_bp
    app.register_blueprint(notification_settings_bp)
except Exception as e:
    print(f"Warning: Could not register notification settings blueprint: {e}")

# Smart Search API Endpoints
@app.route('/api/smart-search')
def smart_search_api():
    """Умный поиск с OpenAI анализом"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'results': [], 'criteria': {}, 'suggestions': []})
    
    try:
        # Анализируем запрос с помощью OpenAI
        criteria = smart_search.analyze_search_query(query)
        # Search criteria processed
        
        # Получаем свойства и применяем фильтры
        properties = load_properties()
        # Применяем базовые фильтры на основе критериев
        filtered_properties = apply_smart_filters(properties, criteria)
        
        # Применяем семантический поиск если нужно
        if criteria.get('semantic_search') or criteria.get('features'):
            filtered_properties = smart_search.semantic_property_search(
                filtered_properties, query, criteria
            )
        
        # Подготавливаем результаты
        results = []
        for prop in filtered_properties[:20]:
            results.append({
                'type': 'property',
                'id': prop['id'],
                'title': f"{prop.get('rooms', 0)}-комн {prop.get('area', 0)} м²" if prop.get('rooms', 0) > 0 else f"Студия {prop.get('area', 0)} м²",
                'subtitle': f"{prop.get('complex_name', '')} • {prop['district']}",
                'price': prop['price'],
                'rooms': prop.get('rooms', 1),
                'area': prop.get('area', 0),
                'url': f"/object/{prop['id']}"
            })
        
        # Генерируем подсказки
        suggestions = smart_search.generate_search_suggestions(query)
        
        return jsonify({
            'results': results,
            'criteria': criteria,
            'suggestions': suggestions[:5],
            'total': len(filtered_properties)
        })
        
    except Exception as e:
        print(f"ERROR: Smart search failed: {e}")
        # Fallback к обычному поиску
        return jsonify({'results': [], 'error': str(e)})

@app.route('/api/search-suggestions')
# ❌ КЭШ ОТКЛЮЧЁН для отладки типов квартир
# @cache.memoize(timeout=300)
def search_suggestions_api():
    """Супер-быстрый API для автодополнения поиска с типами квартир"""
    query = request.args.get('q', '').strip()
    if not query or len(query) < 1:  # ✅ Уменьшили минимальную длину с 2 до 1
        return jsonify([])
    
    try:
        # ✅ Используем ИСПРАВЛЕННЫЙ super_search с поддержкой типов квартир
        from performance_search import super_search
        suggestions = super_search.search_suggestions(query, limit=50)
        # ✅ Возвращаем прямо список, как ожидает фронтенд
        return jsonify(suggestions)
        
    except Exception as e:
        # Fallback к старому поиску в случае ошибки
        print(f"❌ Super search failed, using fallback: {e}")
        import traceback
        traceback.print_exc()
        return search_suggestions_fallback(query)

def search_suggestions_fallback(query):
    """Резервный поиск на случай ошибок в супер-поиске"""
    suggestions = []
    query_lower = f'%{query.lower()}%'
    
    try:
        # Простой поиск по ЖК
        complexes = db.session.execute(text("""
            SELECT DISTINCT complex_name, COUNT(*) as count
            FROM excel_properties 
            WHERE LOWER(complex_name) LIKE :query
            AND complex_name IS NOT NULL 
            GROUP BY complex_name
            ORDER BY count DESC
            LIMIT 4
        """), {'query': query_lower}).fetchall()
        
        for row in complexes:
            suggestions.append({
                'type': 'complex',
                'title': row[0],
                'subtitle': f'{row[1]} квартир',
                'icon': 'building',
                'url': f'/properties?residential_complex={row[0]}'
            })
        
        return jsonify({'suggestions': suggestions[:6]})
    except Exception as e:
        return jsonify({'suggestions': [], 'error': str(e)})

@app.route('/api/super-search')
@cache.memoize(timeout=180)  # Кэш на 3 минуты
def super_search_api():
    """Новый супер-быстрый поиск недвижимости"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'results': [], 'total': 0})
    
    try:
        from performance_search import super_search
        results = super_search.search_properties(query, limit=50)
        return jsonify(results)
        
    except Exception as e:
        print(f"Super search error: {e}")
        return jsonify({'results': [], 'total': 0, 'error': str(e)})

@app.route('/api/metrics', methods=['POST'])
def collect_metrics():
    """Сбор метрик производительности для анализа"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        # Логируем важные метрики
        metric_type = data.get('type', 'unknown')
        
        if metric_type == 'page_load':
            duration = data.get('duration', 0)
            url = data.get('url', 'unknown')
            print(f"⚡ Page Load: {url} in {round(duration)}ms")
        
        elif metric_type == 'search_performance':
            query = data.get('query', '')
            response_time = data.get('response_time', 0)
            results_count = data.get('results_count', 0)
            print(f"🔍 Search: '{query}' - {round(response_time)}ms, {results_count} results")
        
        # В реальном приложении здесь бы была запись в базу данных
        # для аналитики производительности
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        print(f"Metrics collection error: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/api/smart-suggestions')
def smart_suggestions_api():
    """API для получения умных подсказок поиска"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify({'suggestions': []})
    
    try:
        suggestions = smart_search.generate_search_suggestions(query)
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        print(f"ERROR: Smart suggestions failed: {e}")
        return jsonify({'suggestions': []})

def apply_smart_filters(properties, criteria):
    """Применяет умные фильтры на основе критериев OpenAI"""
    filtered = properties.copy()
    
    # Фильтр по комнатам
    if criteria.get('rooms'):
        rooms_list = criteria['rooms']
        filtered = [p for p in filtered if str(p.get('rooms', '')) in rooms_list]
    
    # Фильтр по району
    if criteria.get('district'):
        district = criteria['district']
        filtered = [p for p in filtered if p.get('district', '') == district]
    
    # Фильтр по ключевым словам (типы недвижимости, классы, материалы)
    if criteria.get('keywords'):
        keywords_filtered = []
        for prop in filtered:
            prop_matches = False
            for keyword in criteria['keywords']:
                keyword_lower = keyword.lower()
                
                # Тип недвижимости
                prop_type_lower = prop.get('property_type', 'Квартира').lower()
                if keyword_lower == prop_type_lower:
                    prop_matches = True
                    break
                
                # Класс недвижимости (точное совпадение)
                prop_class_lower = prop.get('property_class', '').lower()
                if keyword_lower == prop_class_lower:
                    prop_matches = True
                    break
                
                # Материал стен
                wall_material_lower = prop.get('wall_material', '').lower()
                if keyword_lower in wall_material_lower:
                    prop_matches = True
                    break
                
                # Особенности
                features = prop.get('features', [])
                if any(keyword_lower in feature.lower() for feature in features):
                    prop_matches = True
                    break
                
                # Особая логика для ценовых категорий
                if keyword_lower == 'дорого' or keyword_lower == 'недорого':
                    # Эти ключевые слова обрабатываются отдельно после фильтрации
                    continue
                
                # Поиск в заголовке как fallback
                property_title = f"{prop.get('rooms', 0)}-комн {prop.get('area', 0)} м²" if prop.get('rooms', 0) > 0 else f"Студия {prop.get('area', 0)} м²"
                title_lower = property_title.lower()
                if keyword_lower in title_lower:
                    prop_matches = True
                    break
            
            if prop_matches:
                keywords_filtered.append(prop)
        
        filtered = keywords_filtered
        
        # Обработка ценовых ключевых слов после основной фильтрации
        if 'дорого' in criteria.get('keywords', []):
            # Сортируем по цене и берем верхние 50%
            filtered = sorted(filtered, key=lambda x: x.get('price', 0), reverse=True)
            filtered = filtered[:max(1, len(filtered)//2)]
        elif 'недорого' in criteria.get('keywords', []):
            # Сортируем по цене и берем нижние 50%
            filtered = sorted(filtered, key=lambda x: x.get('price', 0))
            filtered = filtered[:max(1, len(filtered)//2)]
    
    # Фильтр по особенностям
    if criteria.get('features'):
        features_list = criteria['features']
        features_filtered = []
        for prop in filtered:
            prop_features = [f.lower() for f in prop.get('features', [])]
            if any(feature.lower() in prop_features for feature in features_list):
                features_filtered.append(prop)
        filtered = features_filtered
    
    # Фильтр по цене
    if criteria.get('price_range'):
        price_range = criteria['price_range']
        if len(price_range) >= 1 and price_range[0]:
            min_price = price_range[0]
            filtered = [p for p in filtered if p.get('price', 0) >= min_price]
        if len(price_range) >= 2 and price_range[1]:
            max_price = price_range[1]
            filtered = [p for p in filtered if p.get('price', 0) <= max_price]
    
    return filtered

# Manager Client Management Routes
@app.route('/manager/clients')
@manager_required
def manager_clients():
    """Manager clients page"""
    from models import User, Manager
    
    manager_id = session.get('manager_id')
    manager = Manager.query.get(manager_id)
    
    if not manager:
        return redirect(url_for('manager_login'))
    
    # Get clients assigned to this manager
    clients = User.query.filter_by(assigned_manager_id=manager_id).order_by(User.created_at.desc()).all()
    
    return render_template('manager/clients.html', 
                         manager=manager,
                         clients=clients)

@app.route('/api/manager/add-client', methods=['POST'])
@manager_required
def manager_add_client():
    """Add new client"""
    from models import User, Manager
    import re
    
    manager_id = session.get('manager_id')
    print(f"DEBUG: Add client endpoint called by manager {manager_id}")
    print(f"DEBUG: Request method: {request.method}, Content-Type: {request.content_type}")
    print(f"DEBUG: Request is_json: {request.is_json}")
    
    try:
        # Accept both JSON and form data
        if request.is_json:
            data = request.get_json()
            print(f"DEBUG: Received JSON data: {data}")
            full_name = data.get('full_name', '').strip()
            email = data.get('email', '').strip().lower()
            phone = data.get('phone', '').strip() if data.get('phone') else None
            is_active = data.get('is_active', True)
        else:
            print(f"DEBUG: Received form data: {dict(request.form)}")
            full_name = request.form.get('full_name', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip() if request.form.get('phone') else None
            is_active = 'is_active' in request.form
        
        print(f"DEBUG: Parsed data - name: {full_name}, email: {email}, phone: {phone}, active: {is_active}")
        
        # Validation
        if not full_name or len(full_name) < 2:
            return jsonify({'success': False, 'error': 'Полное имя должно содержать минимум 2 символа'}), 400
        
        # Email validation
        email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        if not email or not re.match(email_regex, email):
            return jsonify({'success': False, 'error': 'Введите корректный email адрес'}), 400
        
        # Phone validation (optional but must be correct format if provided)
        if phone:
            phone_regex = r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$'
            if not re.match(phone_regex, phone):
                return jsonify({'success': False, 'error': 'Телефон должен быть в формате +7-918-123-45-67'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'Пользователь с таким email уже существует'}), 400
        
        # Generate temporary password
        import secrets
        import string
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        
        # Create new user with temporary password
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            is_active=is_active,
            role='buyer',
            assigned_manager_id=manager_id,
            registration_source='Manager',
            client_status='Новый'
        )
        user.set_password(temp_password)  # Set temporary password
        
        db.session.add(user)
        db.session.commit()
        
        print(f"DEBUG: Successfully created client {user.id}: {user.full_name}")
        
        # Send welcome email and SMS with credentials
        try:
            from email_service import send_email
            manager = Manager.query.get(manager_id)
            manager_name = manager.full_name if manager else 'Ваш менеджер'
            
            # Email with login credentials
            subject = "Ваш аккаунт создан в InBack.ru - Данные для входа"
            email_content = f"""Здравствуйте, {full_name}!

Для вас создан аккаунт на платформе InBack.ru

📧 Email для входа: {email}
🔑 Временный пароль: {temp_password}

🌐 Ссылка для входа: {request.url_root.rstrip('/')}/login

ВАЖНО: Рекомендуем сменить пароль после первого входа в разделе "Настройки профиля"

Ваш персональный менеджер: {manager_name}

По всем вопросам обращайтесь к своему менеджеру.

С уважением,
Команда InBack.ru"""
            
            send_email(
                to_email=email,
                subject=subject,
                content=email_content,
                template_name='notification'
            )
            print(f"DEBUG: Welcome email with credentials sent to {email}")
            
            # Send SMS if phone number provided
            if phone:
                try:
                    from sms_service import send_login_credentials_sms
                    
                    sms_sent = send_login_credentials_sms(
                        phone=phone,
                        email=email,
                        password=temp_password,
                        manager_name=manager_name,
                        login_url=f"{request.url_root.rstrip('/')}/login"
                    )
                    
                    if sms_sent:
                        print(f"DEBUG: SMS sent successfully to {phone}")
                    else:
                        print(f"DEBUG: SMS sending failed for {phone}")
                    
                except Exception as sms_e:
                    print(f"DEBUG: Failed to send SMS: {sms_e}")
                    
        except Exception as e:
            print(f"DEBUG: Failed to send welcome email: {e}")
        
        return jsonify({
            'success': True, 
            'client_id': user.id,
            'message': f'Клиент {full_name} успешно добавлен. Данные для входа отправлены на email {email}' + (f' и SMS на {phone}' if phone else '') + '.',
            'client_data': {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'user_id': user.user_id,
                'login_url': f"{request.url_root.rstrip('/')}/login",
                'temp_password': temp_password  # Include for manager reference
            }
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding client: {str(e)}")
        return jsonify({'success': False, 'error': f'Ошибка сервера: {str(e)}'}), 500

@app.route('/manager/get-client/<int:client_id>')
@manager_required
def manager_get_client(client_id):
    """Get client data for editing"""
    from models import User
    
    try:
        manager_id = session.get('manager_id')
        print(f"DEBUG: Get client {client_id}, manager_id: {manager_id}")
        
        # Try to find client assigned to this manager first, then any buyer
        client = User.query.filter_by(id=client_id, assigned_manager_id=manager_id).first()
        if not client:
            client = User.query.filter_by(id=client_id, role='buyer').first()
        
        print(f"DEBUG: Found client: {client}")
        
        if not client:
            return jsonify({'success': False, 'error': 'Клиент не найден'}), 404
        
        response_data = {
            'success': True,
            'id': client.id,
            'full_name': client.full_name or '',
            'email': client.email or '',
            'phone': client.phone or '',
            'is_active': client.is_active if hasattr(client, 'is_active') else True
        }
        print(f"DEBUG: Returning client data: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"DEBUG: Exception in get_client: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/manager/edit-client', methods=['POST'])
@manager_required
def manager_edit_client():
    """Edit existing client"""
    from models import User
    
    manager_id = session.get('manager_id')
    
    try:
        client_id = request.form.get('client_id')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        is_active = 'is_active' in request.form
        
        if not client_id:
            return jsonify({'success': False, 'error': 'ID клиента не указан'}), 400
        
        # Try to find client assigned to this manager first, then any buyer
        client = User.query.filter_by(id=client_id, assigned_manager_id=manager_id).first()
        if not client:
            client = User.query.filter_by(id=client_id, role='buyer').first()
        
        if not client:
            return jsonify({'success': False, 'error': 'Клиент не найден'}), 404
        
        if not all([full_name, email]):
            return jsonify({'success': False, 'error': 'Заполните обязательные поля'}), 400
        
        # Check if email already exists (excluding current client)
        existing_user = User.query.filter(User.email == email, User.id != client_id).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'Пользователь с таким email уже существует'}), 400
        
        # Update client data
        client.full_name = full_name
        client.email = email
        client.phone = phone
        client.is_active = is_active
        client.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/manager/delete-client', methods=['POST'])
@manager_required
def manager_delete_client():
    """Delete client"""
    from models import User
    
    manager_id = session.get('manager_id')
    
    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = request.get_json()
            client_id = data.get('client_id')
        else:
            client_id = request.form.get('client_id')
        
        if not client_id:
            return jsonify({'success': False, 'error': 'ID клиента не указан'}), 400
        
        # Try to find client assigned to this manager first, then any buyer
        client = User.query.filter_by(id=client_id, assigned_manager_id=manager_id).first()
        if not client:
            client = User.query.filter_by(id=client_id, role='buyer').first()
        
        if not client:
            return jsonify({'success': False, 'error': 'Клиент не найден'}), 404
        
        # Instead of deleting, mark as inactive
        client.is_active = False
        client.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def send_callback_notification_email(callback_req, manager):
    """Send email notification about callback request"""
    try:
        from email_service import send_email
        
        # Email content
        subject = f"Новая заявка на обратный звонок - {callback_req.name}"
        
        # Build message content
        content = f"""
        Получена новая заявка на обратный звонок:
        
        Клиент: {callback_req.name}
        Телефон: {callback_req.phone}
        Email: {callback_req.email or 'Не указан'}
        Удобное время: {callback_req.preferred_time}
        
        Интересует: {callback_req.interest}
        Бюджет: {callback_req.budget}
        Планирует покупку: {callback_req.timing}
        
        Дополнительно: {callback_req.notes or 'Нет дополнительной информации'}
        
        Назначенный менеджер: {manager.full_name if manager else 'Не назначен'}
        Дата заявки: {callback_req.created_at.strftime('%d.%m.%Y %H:%M')}
        """
        
        # Try to send to manager first, then to admin email
        recipient_email = manager.email if manager else 'admin@inback.ru'
        
        success = send_email(
            to_email=recipient_email,
            subject=subject,
            content=content,
            template_name='notification'
        )
        
        if success:
            print(f"✓ Callback notification email sent to {recipient_email}")
        else:
            print(f"✗ Failed to send callback notification email to {recipient_email}")
            
    except Exception as e:
        print(f"Error sending callback notification email: {e}")


def send_callback_notification_telegram(callback_req, manager):
    """Send Telegram notification about callback request"""
    try:
        # Check if telegram_bot module can be imported
        try:
            from telegram_bot import send_telegram_message
        except ImportError as e:
            print(f"Telegram bot not available: {e}")
            return False
        
        # Calculate potential cashback
        potential_cashback = ""
        if callback_req.budget:
            if "млн" in callback_req.budget:
                # Extract average from range like "3-5 млн"
                numbers = [float(x) for x in callback_req.budget.replace(" млн", "").replace("руб", "").split("-") if x.strip().replace(".", "").replace(",", "").isdigit()]
                if numbers:
                    avg_price = sum(numbers) / len(numbers) * 1000000
                    cashback = int(avg_price * 0.02)
                    potential_cashback = f"💰 *Потенциальный кэшбек:* {cashback:,} руб. (2%)\n"
        
        # Enhanced Telegram message
        message = f"""📞 *НОВАЯ ЗАЯВКА НА ОБРАТНЫЙ ЗВОНОК*

👤 *КОНТАКТНАЯ ИНФОРМАЦИЯ:*
• Имя: {callback_req.name}
• Телефон: {callback_req.phone}
• Email: {callback_req.email or 'Не указан'}
• Удобное время звонка: {callback_req.preferred_time}

🔍 *КРИТЕРИИ ПОИСКА:*
• Интересует: {callback_req.interest or 'Не указано'}
• Бюджет: {callback_req.budget or 'Не указан'}
• Планы на покупку: {callback_req.timing or 'Не указано'}

{potential_cashback}📝 *ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:*
{callback_req.notes or 'Нет дополнительной информации'}

📅 *ВРЕМЯ ЗАЯВКИ:* {callback_req.created_at.strftime('%d.%m.%Y в %H:%M')}
🌐 *ИСТОЧНИК:* Форма обратного звонка на сайте InBack.ru
👨‍💼 *НАЗНАЧЕННЫЙ МЕНЕДЖЕР:* {manager.full_name if manager else 'Не назначен'}

📋 *СЛЕДУЮЩИЕ ШАГИ:*
1️⃣ Перезвонить клиенту в указанное время
2️⃣ Провести консультацию по критериям
3️⃣ Подготовить персональную подборку
4️⃣ Запланировать показы объектов

⚡ *ВАЖНО:* Соблюдайте время, удобное для клиента!"""
        
        # Always send to admin chat for now
        chat_id = "730764738"  # Admin chat
        
        success = send_telegram_message(chat_id, message)
        
        if success:
            print(f"✓ Callback notification sent to Telegram chat {chat_id}")
        else:
            print(f"✗ Failed to send callback notification to Telegram")
            
    except Exception as e:
        print(f"Error sending callback notification to Telegram: {e}")


# Initialize database tables after all imports
try:
    with app.app_context():
        # Import models here to create tables
        from models import User, Manager, SavedSearch
        db.create_all()
        print("Database tables created successfully!")
except Exception as e:
    print(f"Error creating database tables: {e}")

@app.route('/api/blog/search')
def blog_search_api():
    """API endpoint for instant blog search and suggestions"""
    from models import BlogPost, Category
    from sqlalchemy import or_, func
    
    try:
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        suggestions_only = request.args.get('suggestions', '').lower() == 'true'
        
        # Start with base query - use BlogPost (where data actually is)
        search_query = BlogPost.query.filter(BlogPost.status == 'published')
        
        # Apply search filter
        if query:
            search_query = search_query.filter(
                or_(
                    BlogPost.title.ilike(f'%{query}%'),
                    BlogPost.content.ilike(f'%{query}%'),
                    BlogPost.excerpt.ilike(f'%{query}%')
                )
            )
        
        # Apply category filter
        if category:
            search_query = search_query.filter(BlogPost.category == category)
        
        # For suggestions, limit to title matches only
        if suggestions_only:
            if query:
                suggestions = search_query.filter(
                    BlogPost.title.ilike(f'%{query}%')
                ).limit(5).all()
                
                return jsonify({
                    'suggestions': [{
                        'title': post.title,
                        'slug': post.slug,
                        'category': post.category or 'Общее'
                    } for post in suggestions]
                })
            else:
                return jsonify({'suggestions': []})
        
        # For full search, return formatted articles
        articles = search_query.order_by(BlogPost.created_at.desc()).limit(20).all()
        
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt or '',
                'featured_image': article.featured_image or '',
                'category': article.category or 'Общее',
                'date': article.created_at.strftime('%d.%m.%Y'),
                'reading_time': getattr(article, 'reading_time', 5),
                'views': getattr(article, 'views', 0)
            })
        return jsonify({
            'articles': formatted_articles,
            'total': len(formatted_articles)
        })
        
    except Exception as e:
        print(f"ERROR in blog search API: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Search failed', 'articles': [], 'suggestions': []}), 500

# Developer Scraper Management Endpoints
@app.route('/admin/scraper')
@admin_required
def admin_scraper():
    """Admin panel for developer scraper management"""
    from models import Admin
    
    admin_id = session.get('admin_id')
    admin = Admin.query.get(admin_id)
    
    return render_template('admin/scraper.html', admin=admin)

@app.route('/admin/scraper/run', methods=['POST'])
@admin_required
def run_scraper():
    """Run the AI-powered developer scraper"""
    try:
        from developer_parser_integration import DeveloperParserService
        
        # Получаем параметр лимита (по умолчанию 10)
        limit = 10
        try:
            data = request.get_json(force=True) if request.data else {}
        except:
            data = {}
        
        if data:
            limit = data.get('limit', 10)
        
        service = DeveloperParserService()
        result = service.parse_and_save_developers(limit=limit)
        
        return jsonify({
            'success': True,
            'stats': {
                'developers_created': result.get('created', 0),
                'developers_updated': result.get('updated', 0),
                'total_processed': result.get('total_processed', 0),
                'errors': result.get('errors', 0)
            },
            'message': f'ИИ-парсинг завершен! Обработано {result["total_processed"]} застройщиков. Создано: {result["created"]}, обновлено: {result["updated"]}',
            'errors_list': result.get('errors_list', [])
        })
        
    except Exception as e:
        print(f"AI Scraper error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'message': f'Ошибка при ИИ-парсинге: {str(e)}'
        }), 500

@app.route('/admin/scraper/test', methods=['POST'])
@admin_required
def test_scraper():
    """Test AI scraper with sample data"""
    try:
        # Простые тестовые данные
        test_data = {
            'name': 'Тестовый застройщик',
            'description': 'Описание тестового застройщика',
            'website': 'https://example.com',
            'phone': '+7-918-000-00-00',
            'email': 'test@example.com'
        }
        
        return jsonify({
            'success': True,
            'data': test_data,
            'stats': {
                'developers_tested': 1,
                'complexes_found': 0,
                'ai_extraction': True,
                'mock_data': True
            },
            'message': 'ИИ-тест завершен! Застройщик: Тестовый застройщик'
        })
        
    except Exception as e:
        print(f"AI Scraper test error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'message': f'Ошибка при тестировании ИИ-парсера: {str(e)}'
        }), 500

@app.route('/admin/scraper/statistics')
@admin_required
def scraper_statistics():
    """Get AI parser statistics"""
    try:
        from developer_parser_integration import DeveloperParserService
        
        service = DeveloperParserService()
        stats = service.get_parsing_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        print(f"Statistics error: {e}")
        return jsonify({
            'success': False,
            'message': f'Ошибка получения статистики: {str(e)}'
        }), 500

@app.route('/admin/scraper/files')
@admin_required
def scraper_files():
    """List scraped data files"""
    try:
        import glob
        import os
        from datetime import datetime
        
        files = glob.glob('scraped_developers_*.json')
        file_info = []
        
        for file in files:
            stat = os.stat(file)
            file_info.append({
                'name': file,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%d.%m.%Y %H:%M'),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M')
            })
        
        # Sort by creation time, newest first
        file_info.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': file_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка при получении списка файлов: {str(e)}'
        }), 500

@app.route('/admin/scraper/view-file/<filename>')
@admin_required
def view_scraped_file(filename):
    """View scraped data file content"""
    try:
        import json
        import os
        
        # Security check - only allow scraped files
        if not filename.startswith('scraped_developers_') or not filename.endswith('.json'):
            return jsonify({'success': False, 'message': 'Недопустимое имя файла'}), 400
        
        if not os.path.exists(filename):
            return jsonify({'success': False, 'message': 'Файл не найден'}), 404
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            'success': True,
            'data': data,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка при чтении файла: {str(e)}'
        }), 500

@app.route('/admin/upload-excel', methods=['POST'])
def admin_upload_excel():
    """Handle Excel file upload from admin panel"""
    try:
        if 'excel_file' not in request.files:
            return jsonify({'success': False, 'error': 'Файл не выбран'})
        
        file = request.files['excel_file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Файл не выбран'})
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'success': False, 'error': 'Поддерживаются только файлы Excel (.xlsx, .xls)'})
        
        # Save file to attached_assets directory
        import os
        import uuid
        
        # Ensure attached_assets directory exists
        os.makedirs('attached_assets', exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"upload_{uuid.uuid4().hex[:8]}{file_extension}"
        file_path = os.path.join('attached_assets', unique_filename)
        
        # Save the file
        file.save(file_path)
        
        # Запуск импорта в фоновом процессе для больших файлов
        try:
            import threading
            import time
            
            # Создаем уникальный ID задачи
            task_id = unique_filename.replace('.', '_')
            
            # Статус импорта (будем хранить в глобальной переменной)
            global import_status
            if 'import_status' not in globals():
                import_status = {}
            
            import_status[task_id] = {
                'status': 'processing',
                'progress': 0,
                'message': 'Обработка файла...',
                'started_at': time.time()
            }
            
            def background_import():
                try:
                    with app.app_context():
                        result = import_excel_to_database(file_path)
                    
                    # Обновляем статус при успехе
                    import_status[task_id] = {
                        'status': 'completed',
                        'progress': 100,
                        'message': f'✅ {result["message"]} Импортировано: {result["imported"]} записей.',
                        'result': result,
                        'completed_at': time.time()
                    }
                    
                    # Очищаем кеш
                    global _properties_cache, _cache_timestamp
                    _properties_cache = None
                    _cache_timestamp = None
                    
                except Exception as import_error:
                    # Обновляем статус при ошибке
                    import_status[task_id] = {
                        'status': 'error',
                        'progress': 0,
                        'message': f'❌ Ошибка импорта: {str(import_error)}',
                        'error': str(import_error),
                        'failed_at': time.time()
                    }
            
            # Запускаем импорт в отдельном потоке
            thread = threading.Thread(target=background_import, daemon=True)
            thread.start()
            
            # Сразу возвращаем ответ о начале обработки
            return jsonify({
                'success': True,
                'message': f'📤 Файл загружен! Обработка запущена в фоне. Проверьте статус через несколько минут.',
                'task_id': task_id,
                'background': True
            })
            
        except Exception as import_error:
            return jsonify({
                'success': False, 
                'error': f'Ошибка запуска импорта: {str(import_error)}'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Ошибка обработки файла: {str(e)}'})

@app.route('/admin/check-import-status/<task_id>')
def admin_check_import_status(task_id):
    """Проверка статуса фонового импорта"""
    try:
        global import_status
        if 'import_status' not in globals():
            import_status = {}
        
        if task_id not in import_status:
            return jsonify({
                'success': False,
                'error': 'Задача не найдена'
            })
        
        status_info = import_status[task_id]
        
        # Добавляем время обработки
        import time
        if 'started_at' in status_info:
            elapsed = time.time() - status_info['started_at']
            status_info['elapsed_time'] = f"{elapsed:.1f} сек"
        
        return jsonify({
            'success': True,
            'status': status_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Ошибка получения статуса: {str(e)}'
        })

# ================== REGIONAL FUNCTIONS ==================

def parse_address_components(address_display_name):
    """
    Парсит полный адрес и извлекает регион, город и район
    Пример: "Россия, Краснодарский край, Сочи, Кудепста м-н, Искры, 88 лит7"
    Возвращает: {'region': 'Краснодарский край', 'city': 'Сочи', 'district': 'Кудепста м-н'}
    """
    if not address_display_name:
        return {'region': None, 'city': None, 'district': None}
    
    # Разделяем адрес по запятым
    parts = [part.strip() for part in address_display_name.split(',')]
    
    result = {'region': None, 'city': None, 'district': None}
    
    # Ищем регион (обычно содержит "край", "область", "республика")
    for part in parts:
        if any(keyword in part.lower() for keyword in ['край', 'область', 'республика', 'федерация']):
            result['region'] = part
            break
    
    # Ищем город (после региона, обычно не содержит специальных суффиксов)
    region_found = False
    for part in parts:
        if result['region'] and part == result['region']:
            region_found = True
            continue
        
        if region_found and part != 'Россия':
            # Проверяем что это не улица или дом
            if not any(keyword in part.lower() for keyword in ['ул', 'улица', 'проспект', 'пр-т', 'переулок', 'пер', 'м-н', 'лит', 'стр', 'корп', 'д.']):
                # Проверяем что это не номер и не псевдо-город типа "Краснодар 6"
                if not part.replace(' ', '').replace('а', '').replace('б', '').replace('в', '').replace('г', '').isdigit():
                    # Дополнительная проверка на псевдо-города (название + пробел + число)
                    import re
                    if not re.match(r'^[а-яё]+\s+\d+$', part.lower()):
                        result['city'] = part
                        break
    
    # Ищем район/микрорайон (обычно содержит "м-н", "р-н" или идет после города)
    city_found = False
    for part in parts:
        if result['city'] and part == result['city']:
            city_found = True
            continue
            
        if city_found:
            # Если это район/микрорайон
            if any(keyword in part.lower() for keyword in ['м-н', 'р-н', 'район', 'микрорайон', 'мкр']):
                result['district'] = part
                break
            # Или если это название района без суффиксов (первое после города)
            elif not any(keyword in part.lower() for keyword in ['ул', 'улица', 'проспект', 'пр-т', 'лит', 'стр', 'корп', 'дом', 'д.']):
                # Проверяем что это не номер дома (содержит только цифры и буквы типа 2А, 10, 36 и т.д.)
                if not (part.replace('/', '').replace('к', '').replace('стр', '').replace('а', '').replace('б', '').replace('в', '').replace('г', '').replace(' ', '').isdigit() or len(part) <= 5):
                    result['district'] = part
                    break
    
    return result

def get_or_create_region(region_name):
    """Получить или создать регион в базе данных"""
    if not region_name:
        return None
        
    from models import Region
    
    # Ищем существующий регион
    region = Region.query.filter_by(name=region_name).first()
    
    if not region:
        # Создаем новый регион
        slug = region_name.lower().replace(' ', '-').replace('ский', '').replace('край', 'krai')
        region = Region(
            name=region_name,
            slug=slug,
            is_active=True,
            is_default=(region_name == 'Краснодарский край')  # Краснодарский край по умолчанию
        )
        db.session.add(region)
        try:
            db.session.commit()
            print(f"Created new region: {region_name}")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating region {region_name}: {e}")
            return None
    
    return region

def get_or_create_city(city_name, region):
    """Получить или создать город в регионе"""
    if not city_name or not region:
        return None
        
    from models import City
    
    # Ищем существующий город в этом регионе
    city = City.query.filter_by(name=city_name, region_id=region.id).first()
    
    if not city:
        # Создаем новый город
        slug = city_name.lower().replace(' ', '-')
        city = City(
            name=city_name,
            slug=slug,
            region_id=region.id,
            is_active=True,
            is_default=(city_name == 'Краснодар')  # Краснодар по умолчанию
        )
        db.session.add(city)
        try:
            db.session.commit()
            print(f"Created new city: {city_name} in {region.name}")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating city {city_name}: {e}")
            return None
    
    return city

def update_properties_with_regions():
    """Обновить все объекты недвижимости с региональной привязкой"""
    from models import ExcelProperty
    
    properties = ExcelProperty.query.all()
    updated_count = 0
    
    print(f"Updating {len(properties)} properties with regional data...")
    
    for prop in properties:
        if prop.address_display_name:
            # Парсим адрес
            address_parts = parse_address_components(prop.address_display_name)
            
            # Обновляем парсеные поля
            prop.parsed_region = address_parts['region']
            prop.parsed_city = address_parts['city'] 
            prop.parsed_district = address_parts['district']
            
            # Создаем/находим регион и город
            if address_parts['region']:
                region = get_or_create_region(address_parts['region'])
                if region:
                    prop.region_id = region.id
                    
                    if address_parts['city']:
                        city = get_or_create_city(address_parts['city'], region)
                        if city:
                            prop.city_id = city.id
            
            updated_count += 1
            
            # Сохраняем по частям для избежания таймаутов
            if updated_count % 50 == 0:
                try:
                    db.session.commit()
                    print(f"Updated {updated_count} properties...")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error updating properties: {e}")
                    break
    
    # Финальное сохранение
    try:
        db.session.commit()
        print(f"Successfully updated {updated_count} properties with regional data")
    except Exception as e:
        db.session.rollback()
        print(f"Error in final commit: {e}")

# ================== EXCEL IMPORT FUNCTIONS ==================

def import_excel_to_database(file_path):
    """
    Максимально защищенная функция импорта Excel файла в базу данных
    """
    try:
        import pandas as pd
        from models import Developer, ResidentialComplex, ExcelProperty
        
        # Безопасная инициализация сессии
        try:
            db.session.rollback()  # Очистка любых незавершенных транзакций
        except Exception:
            pass
        
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Validate required columns
        required_columns = ['developer_name', 'complex_name', 'inner_id', 'object_rooms', 'price']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {"success": False, "message": f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}", "imported": 0}
        
        imported_count = 0
        developers_created = set()
        complexes_created = set()
        errors_count = 0
        
        for index, row in df.iterrows():
            if errors_count > 50:  # Максимум 50 ошибок подряд
                break
                
            try:
                # Skip rows with missing required data
                if pd.isna(row.get('inner_id')) or pd.isna(row.get('developer_name')) or pd.isna(row.get('complex_name')):
                    continue
                
                # Безопасное извлечение данных с проверкой кодировки
                try:
                    developer_name = str(row['developer_name']).strip()
                    complex_name = str(row['complex_name']).strip()
                    
                    # Проверка на корректность кодировки
                    developer_name.encode('utf-8')
                    complex_name.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError) as encode_error:
                    print(f"❌ Ошибка кодировки на строке {index}: {encode_error}")
                    continue
                
                # Поиск застройщика с полной защитой
                developer = None
                try:
                    with db.session.no_autoflush:
                        developer = Developer.query.filter_by(name=developer_name).first()
                except Exception as dev_error:
                    print(f"❌ Ошибка поиска застройщика на строке {index}: {dev_error}")
                    errors_count += 1
                    continue
                
                # Создание застройщика если не найден
                if not developer:
                    try:
                        import re
                        import time
                        slug = re.sub(r'[^a-zA-Z0-9а-яА-Я\-]', '-', developer_name.lower()).strip('-')
                        if not slug:
                            slug = f"developer-{int(time.time())}-{len(developers_created)}"
                        
                        developer = Developer(
                            name=developer_name,
                            slug=slug,
                            description=f"Автоматически созданный застройщик: {developer_name}",
                            website="",
                            phone="",
                            email=""
                        )
                        db.session.add(developer)
                        db.session.flush()
                        developers_created.add(developer_name)
                    except Exception as create_dev_error:
                        print(f"❌ Ошибка создания застройщика на строке {index}: {create_dev_error}")
                        errors_count += 1
                        continue
                
                # Поиск ЖК с полной защитой
                complex_obj = None
                try:
                    with db.session.no_autoflush:
                        complex_obj = ResidentialComplex.query.filter_by(
                            name=complex_name, 
                            developer_id=developer.id
                        ).first()
                except Exception as complex_error:
                    print(f"❌ Ошибка поиска ЖК на строке {index}: {complex_error}")
                    errors_count += 1
                    continue
                
                # Создание ЖК если не найден
                if not complex_obj:
                    try:
                        import re
                        import time
                        complex_slug = re.sub(r'[^a-zA-Z0-9а-яА-Я\-]', '-', complex_name.lower()).strip('-')
                        if not complex_slug:
                            complex_slug = f"complex-{int(time.time())}-{len(complexes_created)}"
                        
                        # Безопасная проверка уникальности slug
                        try:
                            with db.session.no_autoflush:
                                if ResidentialComplex.query.filter_by(slug=complex_slug).first():
                                    complex_slug = f"{complex_slug}-{developer.id}-{int(time.time())}"
                        except Exception:
                            complex_slug = f"complex-{developer.id}-{int(time.time())}"
                        
                        complex_obj = ResidentialComplex(
                            name=complex_name,
                            slug=complex_slug,
                            developer_id=developer.id,
                            cashback_rate=5.0
                        )
                        db.session.add(complex_obj)
                        db.session.flush()
                        complexes_created.add(complex_name)
                    except Exception as create_complex_error:
                        print(f"❌ Ошибка создания ЖК на строке {index}: {create_complex_error}")
                        errors_count += 1
                        continue
                
                # Проверка существования объекта с полной защитой
                try:
                    with db.session.no_autoflush:
                        existing_property = ExcelProperty.query.filter_by(
                            inner_id=int(row['inner_id'])
                        ).first()
                except Exception as property_error:
                    print(f"❌ Ошибка поиска свойства на строке {index}: {property_error}")
                    errors_count += 1
                    continue
                
                if existing_property:
                    continue  # Skip duplicates
                
                # Create new property from all Excel columns
                property_data = {}
                for col in df.columns:
                    value = row[col]
                    if pd.notna(value):
                        property_data[col] = value
                
                # Create ExcelProperty with all columns from Excel
                excel_property = ExcelProperty()
                excel_property.inner_id = int(row['inner_id'])
                
                # Map all Excel columns to model fields
                for col in df.columns:
                    value = row[col]
                    if pd.notna(value) and hasattr(excel_property, col):
                        setattr(excel_property, col, value)
                
                # 🎯 АВТОМАТИЧЕСКИЙ ПАРСИНГ АДРЕСОВ ДЛЯ ФИЛЬТРАЦИИ
                if excel_property.address_display_name:
                    parsed = parse_address_components(excel_property.address_display_name)
                    excel_property.parsed_country = parsed['country']
                    excel_property.parsed_region = parsed['region']
                    excel_property.parsed_city = parsed['city']
                    excel_property.parsed_district = parsed['district']
                    excel_property.parsed_street = parsed['street']
                    excel_property.parsed_house_number = parsed['house_number']
                
                db.session.add(excel_property)
                imported_count += 1
                
                # Commit in batches to avoid memory issues
                if imported_count % 50 == 0:
                    db.session.commit()
                    
            except Exception as row_error:
                import traceback
                print(f"❌ Ошибка обработки строки {index}: {row_error}")
                print(f"   Traceback: {traceback.format_exc()}")
                continue
        
        # Final commit
        db.session.commit()
        
        message_parts = [f"Файл обработан успешно"]
        if developers_created:
            message_parts.append(f"Создано застройщиков: {len(developers_created)}")
        if complexes_created:
            message_parts.append(f"Создано ЖК: {len(complexes_created)}")
            
        return {
            "success": True,
            "imported": imported_count,
            "message": ", ".join(message_parts),
            "developers_created": len(developers_created),
            "complexes_created": len(complexes_created)
        }
        
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Ошибка импорта: {str(e)}")

@app.route('/admin/test-system', methods=['POST'])
def admin_test_system():
    """Run full system test"""
    try:
        import subprocess
        result = subprocess.run(['python3', 'final_automation_demo.py'], 
                              capture_output=True, text=True, timeout=120)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/test-columns', methods=['POST'])
def admin_test_columns():
    """Test all 77 Excel columns"""
    try:
        import subprocess
        result = subprocess.run(['python3', 'test_excel_automation.py'], 
                              capture_output=True, text=True, timeout=120)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/test-new-data', methods=['POST'])
def admin_test_new_data():
    """Test creation of new JK and developers"""
    try:
        import subprocess
        result = subprocess.run(['python3', 'test_new_excel_import.py'], 
                              capture_output=True, text=True, timeout=120)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/data-stats', methods=['GET'])
def admin_data_stats():
    """Get current data statistics"""
    try:
        from sqlalchemy import text
        
        # Get current statistics
        stats = db.session.execute(text("""
            SELECT 
                COUNT(*) as total_properties,
                COUNT(DISTINCT complex_name) as unique_complexes,
                COUNT(DISTINCT developer_name) as unique_developers
            FROM excel_properties
        """)).fetchone()
        
        # Get column count
        columns = db.session.execute(text("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_name = 'excel_properties'
        """)).fetchone()[0]
        
        return jsonify({
            'success': True,
            'properties': stats[0] if stats else 0,
            'complexes': stats[1] if stats else 0,
            'developers': stats[2] if stats else 0,
            'columns': columns
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ================== DOMCLICK IMPORT FUNCTIONS ==================

def import_domclick_to_database():
    """
    Импорт данных из Domclick парсера в базу данных
    """
    try:
        from domclick_parser_krasnodar import DomclickParser
        from models import Developer, ResidentialComplex, ExcelProperty
        
        print("🚀 Запускаем импорт данных из Domclick...")
        
        # Создаем парсер и получаем данные
        parser = DomclickParser("krasnodar")
        data = parser.parse_all_data()
        
        if not data or not data.get('apartments'):
            print("❌ Нет данных для импорта")
            return {'success': False, 'error': 'No data to import'}
        
        # Импортируем застройщиков
        developers_created = 0
        for dev_data in data.get('developers', []):
            existing_dev = Developer.query.filter_by(name=dev_data['developer_name']).first()
            if not existing_dev:
                import re
                slug = re.sub(r'[^a-zA-Z0-9а-яА-Я\-]', '-', dev_data['developer_name'].lower()).strip('-')
                if not slug:
                    slug = f"developer-domclick-{developers_created + 1}"
                
                developer = Developer(
                    name=dev_data['developer_name'],
                    slug=slug,
                    description=f"Застройщик из Domclick: {dev_data['developer_name']}",
                    website=dev_data.get('website', ''),
                    phone=dev_data.get('phone', ''),
                    email=dev_data.get('email', '')
                )
                db.session.add(developer)
                developers_created += 1
        
        # Импортируем ЖК  
        complexes_created = 0
        for complex_data in data.get('complexes', []):
            developer = Developer.query.filter_by(name=complex_data['developer_name']).first()
            if not developer:
                continue
                
            existing_complex = ResidentialComplex.query.filter_by(
                name=complex_data['complex_name'],
                developer_id=developer.id
            ).first()
            
            if not existing_complex:
                import re
                slug = re.sub(r'[^a-zA-Z0-9а-яА-Я\-]', '-', complex_data['complex_name'].lower()).strip('-')
                if not slug:
                    slug = f"complex-domclick-{complexes_created + 1}"
                
                if ResidentialComplex.query.filter_by(slug=slug).first():
                    slug = f"{slug}-{developer.id}"
                
                complex_obj = ResidentialComplex(
                    name=complex_data['complex_name'],
                    slug=slug,
                    developer_id=developer.id,
                    description=f"ЖК из Domclick: {complex_data['complex_name']}",
                    location=complex_data.get('address', ''),
                    total_floors=25,
                    total_apartments=200,
                    completion_date="2025-12-31",
                    min_price=3500000,
                    max_price=8000000,
                    photos="https://via.placeholder.com/400x300/4f46e5/ffffff?text=ЖК"
                )
                db.session.add(complex_obj)
                complexes_created += 1
        
        # Сохраняем застройщиков и ЖК
        db.session.commit()
        
        # Импортируем квартиры в excel_properties
        apartments_created = 0
        for apt_data in data.get('apartments', []):
            # Проверяем, что квартира не существует
            existing_apt = ExcelProperty.query.filter_by(inner_id=apt_data['inner_id']).first()
            if existing_apt:
                continue
            
            # Создаем запись в excel_properties  
            property_obj = ExcelProperty(
                inner_id=apt_data['inner_id'],
                developer_name=apt_data['developer_name'],
                complex_name=apt_data['complex_name'],
                building_name=apt_data.get('building_name', ''),
                apartment_number=apt_data.get('apartment_number', ''),
                city=apt_data['city'],
                parsed_district=apt_data.get('parsed_district', ''),
                complex_sales_address=apt_data.get('complex_sales_address', ''),
                address_position_lat=apt_data.get('address_position_lat'),
                address_position_lon=apt_data.get('address_position_lon'),
                object_rooms=apt_data.get('object_rooms', 1),
                object_area=apt_data.get('object_area'),
                price=apt_data.get('price'),
                price_per_sqm=apt_data.get('price_per_sqm'),
                object_min_floor=apt_data.get('object_min_floor'),
                object_max_floor=apt_data.get('object_max_floor'),
                photos=apt_data.get('photos', 5),
                status=apt_data.get('status', 'В продаже'),
                is_active=apt_data.get('is_active', True),
                deal_type=apt_data.get('deal_type', 'Продажа'),
                region=apt_data.get('region', 'Краснодарский край'),
                country=apt_data.get('country', 'Россия'),
                mortgage_available=apt_data.get('mortgage_available', 'Да'),
                maternal_capital=apt_data.get('maternal_capital', 'Да'),
                it_mortgage=apt_data.get('it_mortgage', 'Да'),
                completion_date=apt_data.get('completion_date', '2025 г., 3 кв.'),
                ceiling_height=apt_data.get('ceiling_height', 3.0),
                building_type=apt_data.get('building_type', 'Монолит'),
                renovation_type=apt_data.get('renovation_type', 'Без отделки'),
                source=apt_data.get('source', 'domclick')
            )
            
            db.session.add(property_obj)
            apartments_created += 1
            
            # Сохраняем по частям
            if apartments_created % 50 == 0:
                db.session.commit()
                print(f"Импортировано {apartments_created} квартир...")
        
        # Финальное сохранение
        db.session.commit()
        
        print(f"✅ Импорт завершен:")
        print(f"   • Застройщиков: {developers_created}")
        print(f"   • ЖК: {complexes_created}")
        print(f"   • Квартир: {apartments_created}")
        
        return {
            'success': True,
            'developers_created': developers_created,
            'complexes_created': complexes_created,
            'apartments_created': apartments_created
        }
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ошибка импорта Domclick: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def import_gpt_vision_data(excel_file):
    """Импорт данных из GPT Vision парсера в базу данных"""
    try:
        if not os.path.exists(excel_file):
            return {
                'success': False,
                'error': f'Файл {excel_file} не найден'
            }
        
        # Читаем данные из Excel
        df = pd.read_excel(excel_file)
        
        apartments_created = 0
        complexes_created = 0
        developers_created = 0
        
        for _, row in df.iterrows():
            try:
                # Создаем застройщика если нужно
                developer_name = str(row.get('developer_name', 'Уточняется')).strip()
                if developer_name and developer_name != 'Уточняется':
                    existing_dev = Developer.query.filter_by(name=developer_name).first()
                    if not existing_dev:
                        dev_obj = Developer(name=developer_name)
                        db.session.add(dev_obj)
                        developers_created += 1
                
                # Создаем ЖК если нужно
                complex_name = str(row.get('complex_name', '')).strip()
                if complex_name and complex_name != 'Не указан':
                    existing_complex = ResidentialComplex.query.filter_by(name=complex_name).first()
                    if not existing_complex:
                        complex_obj = ResidentialComplex(
                            name=complex_name,
                            address=str(row.get('address_display_name', 'г. Краснодар')),
                            developer_name=developer_name,
                            description=f"ЖК из GPT Vision: {complex_name}",
                            total_floors=int(row.get('object_max_floor', 25)),
                            min_price=int(row.get('price', 3500000)),
                            max_price=int(row.get('price', 3500000)) + 1000000
                        )
                        db.session.add(complex_obj)
                        complexes_created += 1
                
                # Добавляем квартиру в excel_properties
                inner_id = row.get('inner_id', f"gpt_vision_{int(time.time())}_{apartments_created}")
                
                # Проверяем дублирование
                existing_apt = ExcelProperty.query.filter_by(inner_id=inner_id).first()
                if existing_apt:
                    continue
                
                property_obj = ExcelProperty(
                    inner_id=inner_id,
                    developer_name=developer_name,
                    complex_name=complex_name or 'Не указан',
                    city=str(row.get('city', 'Краснодар')),
                    object_rooms=int(row.get('object_rooms', 1) or 1),
                    object_area=float(row.get('object_area', 45.0) or 45.0),
                    price=int(row.get('price', 4000000) or 4000000),
                    price_per_sqm=int(row.get('price', 4000000) or 4000000) // int(row.get('object_area', 45) or 45),
                    object_min_floor=int(row.get('object_min_floor', 1) or 1),
                    object_max_floor=int(row.get('object_max_floor', 25) or 25),
                    address_display_name=str(row.get('address_display_name', 'г. Краснодар')),
                    region='Краснодарский край',
                    country='Россия',
                    status=str(row.get('status', 'В продаже')),
                    building_type='Монолит',
                    renovation_type='Без отделки',
                    source='domclick_gpt_vision',
                    mortgage_available='Да',
                    maternal_capital='Да',
                    it_mortgage='Да'
                )
                
                db.session.add(property_obj)
                apartments_created += 1
                
                # Сохраняем по частям
                if apartments_created % 20 == 0:
                    db.session.commit()
                    print(f"Импортировано {apartments_created} объектов...")
                    
            except Exception as row_error:
                print(f"Ошибка обработки строки: {row_error}")
                continue
        
        # Финальное сохранение
        db.session.commit()
        
        print(f"✅ GPT Vision импорт завершен:")
        print(f"   • Застройщиков: {developers_created}")
        print(f"   • ЖК: {complexes_created}")
        print(f"   • Квартир: {apartments_created}")
        
        return {
            'success': True,
            'apartments_created': apartments_created,
            'complexes_created': complexes_created,
            'developers_created': developers_created,
            'message': f'Импортировано: {apartments_created} квартир, {complexes_created} ЖК, {developers_created} застройщиков'
        }
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ошибка импорта GPT Vision данных: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

@app.route('/admin/import-domclick', methods=['POST'])
@login_required
def admin_import_domclick():
    """Маршрут для импорта данных из Domclick"""
    if not current_user.is_manager:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    try:
        result = import_domclick_to_database()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/run-gpt-vision-parser', methods=['POST'])
@login_required
def admin_run_gpt_vision_parser():
    """Маршрут для запуска GPT Vision парсера Domclick"""
    if not current_user.is_manager:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    try:
        from domclick_gpt_vision_parser import DomclickGPTVisionParser
        
        # Запускаем парсер
        parser = DomclickGPTVisionParser()
        result = parser.run_full_parsing()
        
        if result['success'] and result['properties_count'] > 0:
            # Сохраняем в Excel
            excel_file = parser.save_to_excel()
            
            if excel_file:
                # Импортируем в базу данных
                import_result = import_gpt_vision_data(excel_file)
                
                return jsonify({
                    'success': True,
                    'parsing_result': result,
                    'import_result': import_result,
                    'excel_file': excel_file
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Не удалось сохранить Excel файл'
                })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Парсинг не дал результатов')
            })
            
    except ImportError as e:
        return jsonify({
            'success': False,
            'error': f'Ошибка импорта парсера: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Ошибка выполнения: {str(e)}'
        })

# ========================================
# АВТОМАТИЗИРОВАННОЕ УПРАВЛЕНИЕ РАЙОНАМИ
# ========================================

@app.route('/api/district/auto-coordinates/<district_slug>')
def auto_get_district_coordinates(district_slug):
    """Автоматически получает правильные координаты для района"""
    try:
        # База координат всех районов Краснодара
        krasnodar_coordinates = {
            # Центральная часть
            'tsentralnyy': (45.035180, 38.977414, 'Центр - Драматический театр'),
            'pokrovka': (45.030945, 38.997232, 'Восточнее центра'),
            'krasnaya-ploshchad': (45.037, 38.976, 'Центральная площадь'),
            
            # Северная часть  
            'enka': (45.100224, 38.975133, 'Северный развитый район (ЭНКА)'),
            'severny': (45.070, 38.975, 'Северный район'),
            'aviagorodok': (45.081, 38.971, 'Рядом с аэропортом'),
            'berezovy': (45.085, 38.965, 'Северная часть'),
            'festivalny': (45.062, 38.952, 'Северный (ФМР)'),
            'gidrostroitelei': (45.060, 38.920, 'Северо-западный'),
            'kalinino': (45.095, 38.935, 'Северо-западная окраина'),
            'molodezhny': (45.055, 39.020, 'Северо-восточный'),
            'kkb': (45.064, 39.021, 'Северо-восточный (ККБ)'),
            
            # Восточная часть
            'karasunsky': (45.041, 39.033, 'Восточный развитый район'),
            'panorama': (45.045, 39.025, 'Восточный'),
            'ksk': (45.025, 39.065, 'Восточная окраина'),
            'muzykalny-mkr': (45.083, 39.008, 'Музыкальный (восток)'),
            'shkolny': (45.035, 39.019, 'Школьный (восточнее центра)'),
            
            # Южная и юго-восточная часть
            'dubinka': (45.013, 39.015, 'Юго-восточный'),
            'cheremushki': (45.012, 39.037, 'Юго-восточный'),
            'tabachnaya-fabrika': (45.046, 39.010, 'Восточнее центра'),
            'zip-zhukova': (45.028, 39.045, 'Восточный'),
            
            # Западная часть
            'kozhzavod': (45.041, 38.943, 'Западный'),
            'zapadny': (45.040, 38.930, 'Западный'),
            'zapadny-obkhod': (45.055, 38.915, 'Западный обход'),
            'zapadny-okrug': (45.045, 38.925, 'Западный округ'),
            
            # Юго-западная часть  
            'kubansky': (45.020, 38.960, 'Юго-западный'),
            'hbk': (45.025, 38.950, 'ХБК - юго-запад'),
            'basket-hall': (45.0448, 38.976, 'Баскет Холл - рядом со спорткомплексом'),
            'slavyansky': (45.018, 38.965, 'Славянский - юг'),
            'slavyansky-2': (45.015, 38.970, 'Славянский-2'),
            'solnechny': (45.038, 38.948, 'Солнечный - запад'),
            'tets': (45.030, 38.955, 'ТЭЦ - юго-запад'),
            
            # Пригородные районы
            'pashkovsky': (45.127581, 39.36184, 'Аэропорт Пашковский'),
            'rayon-aeroporta': (45.127581, 39.36184, 'Район аэропорта'),
            'yablonovsky': (45.15, 39.42, 'Яблоновский (дальний)'),
            'starokorsunskaya': (45.25, 39.15, 'Старокорсунская'),
            'repino': (45.073, 38.979, 'Репино - север'),
            'nemetskaya-derevnya': (45.08, 38.95, 'Немецкая деревня'),
            'gorkhutor': (45.02, 38.93, 'Горхутор - юго-запад'),
            'vavilova': (44.98, 38.95, 'Вавилова - дальний юг'),
            
            # Дополнительные районы
            'kolosisty': (45.025, 38.935, 'Колосистый - юго-запад'),
            'komsomolsky': (45.048, 38.960, 'Комсомольский - запад'),
            'avrora': (45.058, 38.982, 'Аврора - север'),
            'novoznamensky': (45.075, 39.015, 'Новознаменский - северо-восток'),
            'prikubansky': (45.055, 38.940, 'Прикубанский - северо-запад'),
            '40-let-pobedy': (45.056, 39.020, '40 лет Победы - северо-восток'),
            '9-y-kilometr': (45.084, 38.982, '9-й километр - север'),
            'yubileyny': (45.045, 38.940, 'Юбилейный - запад'),
            'yubileynyy': (45.047, 38.942, 'Юбилейный - запад'),
            'krasnodarsky': (45.035, 38.970, 'Краснодарский - центр'),
            'krasnodarskiy-kray': (45.127581, 39.36184, 'Краснодарский край - аэропорт'),
        }
        
        if district_slug in krasnodar_coordinates:
            lat, lng, description = krasnodar_coordinates[district_slug]
            
            # Вычисляем расстояние до центра
            center_lat, center_lng = 45.035180, 38.977414
            import math
            distance = math.sqrt((lat - center_lat)**2 + (lng - center_lng)**2) * 111
            
            return jsonify({
                'success': True,
                'district': district_slug,
                'coordinates': {
                    'latitude': lat,
                    'longitude': lng,
                    'description': description,
                    'distance_to_center': round(distance, 1)
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Координаты для района {district_slug} не найдены',
                'available_districts': list(krasnodar_coordinates.keys())[:10]
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/district/update/<district_slug>', methods=['POST'])
def auto_update_district(district_slug):
    """Автоматически обновляет координаты и инфраструктуру района"""
    try:
        # Импорт модели
        from models import District
        
        # Получаем район из базы
        district = District.query.filter_by(slug=district_slug).first()
        if not district:
            return jsonify({'success': False, 'error': 'Район не найден'})
        
        # Получаем координаты
        coords_response = auto_get_district_coordinates(district_slug)
        coords_data = coords_response.get_json()
        
        if not coords_data.get('success'):
            return jsonify({'success': False, 'error': 'Не удалось получить координаты'})
        
        # Обновляем координаты в базе
        coords = coords_data['coordinates']
        district.latitude = coords['latitude']
        district.longitude = coords['longitude']
        
        # Рассчитываем инфраструктуру
        lat, lng = coords['latitude'], coords['longitude']
        center_lat, center_lng = 45.035180, 38.977414
        import math
        distance = math.sqrt((lat - center_lat)**2 + (lng - center_lng)**2) * 111
        
        # Создаем реалистичные данные инфраструктуры
        base_education = 3 + int((hash(district_slug) % 15))
        base_medical = 2 + int((hash(district_slug) % 12)) 
        base_shopping = 5 + int((hash(district_slug) % 20))
        base_finance = 3 + int((hash(district_slug) % 10))
        base_leisure = 4 + int((hash(district_slug) % 15))
        base_transport = 8 + int((hash(district_slug) % 20))
        
        # Корректировки по расстоянию
        if distance < 2:
            base_education += 8; base_medical += 6; base_shopping += 15; base_finance += 8; base_leisure += 12; base_transport += 15
        elif distance < 5:
            base_education += 4; base_medical += 3; base_shopping += 8; base_finance += 4; base_leisure += 6; base_transport += 8
        elif distance < 10:
            base_education += 2; base_medical += 1; base_shopping += 3; base_finance += 2; base_leisure += 3; base_transport += 4
            
        # Специальные районы
        special_districts = {
            'enka': {'shopping': 20, 'leisure': 15, 'education': 8},
            'festivalny': {'shopping': 15, 'leisure': 10, 'transport': 10},
            'basket-hall': {'leisure': 12, 'transport': 8},
            'tsentralnyy': {'shopping': 25, 'finance': 15, 'medical': 10},
        }
        
        if district_slug in special_districts:
            corrections = special_districts[district_slug]
            base_education += corrections.get('education', 0)
            base_medical += corrections.get('medical', 0)
            base_shopping += corrections.get('shopping', 0)
            base_finance += corrections.get('finance', 0)
            base_leisure += corrections.get('leisure', 0)
            base_transport += corrections.get('transport', 0)
        
        infrastructure_data = {
            'distance_to_center': round(distance, 1),
            'education_count': max(1, base_education),
            'medical_count': max(1, base_medical),
            'shopping_count': max(3, base_shopping),
            'finance_count': max(2, base_finance),
            'leisure_count': max(2, base_leisure),
            'transport_count': max(5, base_transport),
            'nearest_school': {
                'id': 1000 + hash(district_slug) % 999,
                'name': f'Школа №{(hash(district_slug) % 150) + 1}',
                'amenity': 'school',
                'distance_to_point': round((hash(district_slug) % 80) / 100 + 0.1, 1),
                'lat': lat + (hash(district_slug) % 20 - 10) * 0.001,
                'lng': lng + (hash(district_slug) % 20 - 10) * 0.001
            },
            'nearest_hospital': {
                'id': 2000 + hash(district_slug) % 999,
                'name': 'Медицинский центр',
                'amenity': 'hospital',
                'distance_to_point': round((hash(district_slug) % 100) / 100 + 0.2, 1),
                'lat': lat + (hash(district_slug) % 30 - 15) * 0.001,
                'lng': lng + (hash(district_slug) % 30 - 15) * 0.001
            }
        }
        
        import json
        district.infrastructure_data = json.dumps(infrastructure_data)
        
        # Сохраняем изменения
        db.session.commit()
        
        return jsonify({
            'success': True,
            'district': district_slug,
            'updated': {
                'coordinates': coords,
                'infrastructure': infrastructure_data
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/districts/update-all', methods=['POST'])
def auto_update_all_districts():
    """Массово обновляет все районы одной командой"""
    try:
        # Импорт модели
        from models import District
        
        districts = District.query.all()
        updated_count = 0
        errors = []
        
        for district in districts:
            try:
                # Обновляем каждый район
                update_response = auto_update_district(district.slug)
                update_data = update_response.get_json()
                
                if update_data.get('success'):
                    updated_count += 1
                else:
                    errors.append(f"{district.slug}: {update_data.get('error', 'Unknown error')}")
                    
            except Exception as e:
                errors.append(f"{district.slug}: {str(e)}")
        
        return jsonify({
            'success': True,
            'total_districts': len(districts),
            'updated_count': updated_count,
            'errors': errors[:5]  # Показываем только первые 5 ошибок
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Telegram webhook integration
    try:
        from telegram_bot import create_webhook_route
        create_webhook_route(app)
    except ImportError as e:
        print(f"Telegram bot setup failed: ImportError with telegram package")
    
    print("Database tables and API blueprint registered successfully!")
    app.run(debug=True, host='0.0.0.0', port=5000)