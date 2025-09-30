#!/usr/bin/env python3
"""
Исправление отображения транспортных данных в шаблоне
"""

def fix_transport_data_display():
    """Создает фильтр для очистки транспортных данных"""
    
    # Читаем шаблон
    with open('templates/district_unified.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем все вхождения транспортных данных на более простое форматирование
    replacements = [
        (r'\{\{(\s*)district_data\.transport\.bus_routes(\s*)\|string\|replace\([^}]+\)\}\}',
         r'{{ district_data.transport.bus_routes|e }}'),
        (r'\{\{(\s*)district_data\.transport\.tram_routes(\s*)\|string\|replace\([^}]+\)\}\}',
         r'{{ district_data.transport.tram_routes|e }}'),
        (r'\{\{(\s*)district_data\.transport\.trolleybus_routes(\s*)\|string\|replace\([^}]+\)\}\}',
         r'{{ district_data.transport.trolleybus_routes|e }}'),
    ]
    
    import re
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Записываем обратно
    with open('templates/district_unified.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Упрощено форматирование транспортных данных")

def add_transport_filter_to_app():
    """Добавляет кастомный фильтр для очистки транспортных данных"""
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже фильтр
    if 'clean_transport_data' in content:
        print("✅ Фильтр уже существует")
        return
    
    # Находим место для добавления фильтра (после создания app)
    filter_code = '''
@app.template_filter('clean_transport')
def clean_transport_data(value):
    """Очищает транспортные данные от технических символов"""
    if not value:
        return ""
    
    # Конвертируем в строку и убираем кавычки
    str_value = str(value)
    
    # Убираем одинарные и двойные кавычки в начале и конце
    str_value = str_value.strip("'\"")
    
    # Убираем словарные символы если есть
    str_value = str_value.replace("{'", "").replace("'}", "").replace('{"', "").replace('"}', "")
    
    return str_value
'''
    
    # Ищем место после создания app, но перед routes
    import re
    pattern = r'(app = Flask\(__name__\).*?\n)(.*?)(@app\.route|def.*?\(\):)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content[:match.end(1)] + filter_code + '\n' + content[match.start(3):]
    else:
        # Добавляем в конец импортов
        lines = content.split('\n')
        insert_idx = -1
        for i, line in enumerate(lines):
            if line.startswith('from ') or line.startswith('import '):
                insert_idx = i
        
        if insert_idx > 0:
            lines.insert(insert_idx + 1, filter_code)
            content = '\n'.join(lines)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Добавлен кастомный фильтр для транспортных данных")

def update_template_with_filter():
    """Обновляет шаблон для использования кастомного фильтра"""
    
    with open('templates/district_unified.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем сложные фильтры на простой кастомный
    content = content.replace('|string|replace("\'", "")|replace(\'"\'', \'\')', '|clean_transport')
    content = content.replace('district_data.transport.bus_routes|e', 'district_data.transport.bus_routes|clean_transport')
    content = content.replace('district_data.transport.tram_routes|e', 'district_data.transport.tram_routes|clean_transport')
    content = content.replace('district_data.transport.trolleybus_routes|e', 'district_data.transport.trolleybus_routes|clean_transport')
    
    with open('templates/district_unified.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Шаблон обновлен для использования кастомного фильтра")

def main():
    """Основная функция исправления"""
    print("🔧 Исправляем отображение транспортных данных...")
    
    add_transport_filter_to_app()
    update_template_with_filter()
    
    print("\n✅ Исправление завершено!")
    print("✅ Транспортные данные теперь будут отображаться без технических символов")

if __name__ == "__main__":
    main()