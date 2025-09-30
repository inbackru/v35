#!/usr/bin/env python3
"""
Быстрое исправление отображения транспортных данных
"""

def add_transport_filter():
    """Добавляет простой кастомный фильтр для транспортных данных"""
    
    filter_code = '''
@app.template_filter('clean_transport')
def clean_transport_data(value):
    """Очищает транспортные данные от технических символов"""
    if not value:
        return ""
    
    # Конвертируем в строку и убираем кавычки
    str_value = str(value).strip().strip("'\"")
    
    return str_value

'''
    
    # Читаем app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже фильтр
    if 'clean_transport' in content:
        print("✅ Фильтр уже существует")
        return True
    
    # Добавляем фильтр после импортов
    lines = content.split('\n')
    
    # Находим место для вставки (после создания app)
    insert_idx = -1
    for i, line in enumerate(lines):
        if 'app = Flask(' in line:
            insert_idx = i + 1
            break
    
    if insert_idx > 0:
        lines.insert(insert_idx, filter_code)
        content = '\n'.join(lines)
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Добавлен кастомный фильтр")
        return True
    
    return False

def update_template():
    """Обновляет шаблон для использования простого фильтра"""
    
    with open('templates/district_unified.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Простые замены
    content = content.replace('district_data.transport.bus_routes|string|replace("\'", "")|replace(\'"\'', \'\')', 'district_data.transport.bus_routes|clean_transport')
    content = content.replace('district_data.transport.tram_routes|string|replace("\'", "")|replace(\'"\'', \'\')', 'district_data.transport.tram_routes|clean_transport')
    content = content.replace('district_data.transport.trolleybus_routes|string|replace("\'", "")|replace(\'"\'', \'\')', 'district_data.transport.trolleybus_routes|clean_transport')
    
    with open('templates/district_unified.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Шаблон обновлен")

def main():
    print("🔧 Быстрое исправление транспортных данных...")
    
    if add_transport_filter():
        update_template()
        print("\n✅ Исправление завершено!")
    else:
        print("❌ Не удалось добавить фильтр")

if __name__ == "__main__":
    main()