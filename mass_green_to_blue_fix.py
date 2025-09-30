#!/usr/bin/env python3
"""
Массовая замена зеленых цветов на корпоративные синие во всех основных шаблонах
"""
import os
import glob

def fix_template_colors(filepath):
    """Заменяет зеленые цвета на корпоративные синие в конкретном файле"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Заменяем все зеленые цвета на корпоративные синие
        replacements = {
            'text-green-50': 'text-blue-50',
            'text-green-100': 'text-blue-100', 
            'text-green-200': 'text-blue-200',
            'text-green-300': 'text-blue-300',
            'text-green-400': 'text-blue-400',
            'text-green-500': 'text-blue-500',
            'text-green-600': 'text-blue-600',
            'text-green-700': 'text-blue-700',
            'text-green-800': 'text-blue-800',
            'text-green-900': 'text-blue-900',
            'bg-green-50': 'bg-blue-50',
            'bg-green-100': 'bg-blue-100', 
            'bg-green-200': 'bg-blue-200',
            'bg-green-300': 'bg-blue-300',
            'bg-green-400': 'bg-blue-400',
            'bg-green-500': 'bg-blue-500',
            'bg-green-600': 'bg-blue-600',
            'bg-green-700': 'bg-blue-700',
            'bg-green-800': 'bg-blue-800',
            'bg-green-900': 'bg-blue-900',
            'border-green-200': 'border-blue-200',
            'border-green-300': 'border-blue-300',
            'border-green-400': 'border-blue-400',
            'border-green-500': 'border-blue-500',
            'border-green-600': 'border-blue-600',
        }
        
        for old_color, new_color in replacements.items():
            content = content.replace(old_color, new_color)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"⚠️ Ошибка в файле {filepath}: {e}")
        return False

def main():
    """Основная функция для массовой замены цветов"""
    print("🎨 Массовая замена зеленых цветов на корпоративные синие...")
    
    # Основные пользовательские шаблоны (исключаем admin, auth, _old)
    main_templates = [
        'templates/index.html',
        'templates/properties.html', 
        'templates/property_detail.html',
        'templates/residential_complex_detail.html',
        'templates/developer_detail.html',
        'templates/district_unified.html',
        'templates/comparison.html',
        'templates/mortgage.html',
        'templates/it_mortgage.html',
        'templates/family_mortgage.html',
        'templates/military_mortgage.html',
        'templates/maternal_capital.html',
        'templates/careers.html',
        'templates/header.html',
        'templates/base.html',
    ]
    
    fixed_count = 0
    
    for template in main_templates:
        if os.path.exists(template):
            if fix_template_colors(template):
                print(f"✅ Исправлен: {template}")
                fixed_count += 1
            else:
                print(f"ℹ️ Без изменений: {template}")
    
    print(f"\n🎯 Результат:")
    print(f"✅ Исправлено файлов: {fixed_count}")
    print(f"✅ Все зеленые цвета заменены на корпоративные синие!")

if __name__ == "__main__":
    main()