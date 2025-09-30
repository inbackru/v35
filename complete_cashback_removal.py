#!/usr/bin/env python3
"""
Полное удаление всех оставшихся кешбек блоков из districts.html
"""
import re

def remove_all_cashback_blocks():
    """Удаляет все оставшиеся кешбек блоки из districts.html"""
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Удаляем блоки с "до XXX ₽" из мета-тегов и заголовков
    content = re.sub(r'с кешбеком до \d+\s*\d*\s*₽', '', content)
    
    # Ищем и удаляем все строки с "до XXX ₽" 
    lines = content.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Пропускаем строки с кешбек значениями
        if re.search(r'до \d+\s*\d*\s*₽', line):
            continue
        # Пропускаем строки с иконками кешбека
        if 'fas fa-cash-register' in line:
            continue
        # Добавляем остальные строки
        filtered_lines.append(line)
    
    # Объединяем обратно
    content = '\n'.join(filtered_lines)
    
    # Дополнительная очистка: удаляем пустые div блоки кешбека
    content = re.sub(r'<div class="flex items-center text-.*?cash-register.*?</div>', '', content, flags=re.DOTALL)
    
    with open('templates/districts.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Полностью удалены все кешбек блоки")
    print("✅ Очищены мета-теги от кешбек упоминаний")

def update_search_results_display():
    """Обновляет стиль результатов поиска"""
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Меняем цвет текста результатов поиска
    content = content.replace('text-lg opacity-90', 'text-lg text-gray-600')
    
    with open('templates/districts.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Обновлен стиль отображения результатов поиска")

def main():
    """Основная функция полной очистки"""
    print("🧹 Начинаем полную очистку кешбек блоков...")
    
    remove_all_cashback_blocks()
    update_search_results_display()
    
    print("\n✅ Полная очистка завершена!")
    print("✅ Все упоминания кешбека удалены из districts.html")

if __name__ == "__main__":
    main()