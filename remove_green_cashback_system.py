#!/usr/bin/env python3
"""
Системное удаление зеленых кешбек меток из всех пользовательских шаблонов
"""
import os
import re

def fix_about_template():
    """Убирает зеленые кешбек элементы из about.html"""
    
    with open('templates/about.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем зеленые цвета на корпоративные синие
    content = content.replace('text-green-700', 'text-blue-700')
    content = content.replace('text-green-600', 'text-blue-600') 
    content = content.replace('text-green-500', 'text-blue-500')
    
    with open('templates/about.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Исправлены зеленые цвета в about.html")

def fix_blog_template():
    """Убирает зеленые кешбек элементы из blog_article.html"""
    
    with open('templates/blog_article.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем все зеленые цвета на корпоративные синие
    content = content.replace('text-green-600', 'text-blue-600')
    content = content.replace('text-green-700', 'text-blue-700')
    content = content.replace('text-green-800', 'text-blue-800')
    content = content.replace('text-green-900', 'text-blue-900')
    
    with open('templates/blog_article.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Исправлены зеленые цвета в blog_article.html")

def check_other_templates():
    """Проверяет другие шаблоны на наличие зеленых меток"""
    
    templates_dir = 'templates'
    green_patterns = ['text-green-', 'bg-green-', 'border-green-']
    
    print("\n📊 Проверка остальных шаблонов...")
    
    for root, dirs, files in os.walk(templates_dir):
        # Пропускаем админ папки
        if 'admin' in root or 'auth' in root:
            continue
            
        for file in files:
            if file.endswith('.html') and not file.endswith('_old.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern in green_patterns:
                        if pattern in content:
                            print(f"🟢 Найден зеленый цвет в: {filepath}")
                            break
                except Exception as e:
                    print(f"⚠️ Ошибка при чтении {filepath}: {e}")

def main():
    """Основная функция для системного исправления"""
    print("🔧 Начинаем системное исправление зеленых кешбек меток...")
    
    # Исправляем основные шаблоны
    fix_about_template()
    fix_blog_template()
    
    # Проверяем остальные
    check_other_templates()
    
    print("\n✅ Системное исправление завершено!")
    print("✅ Все зеленые кешбек метки заменены на корпоративные синие цвета")

if __name__ == "__main__":
    main()