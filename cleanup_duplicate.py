#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для удаления дублированной функции renderFilteredProperties
"""

def cleanup_properties_template():
    """Найти и удалить весь фрагмент дублированного кода"""
    
    with open('templates/properties.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Исходное количество строк: {len(lines)}")
    
    # Найти строки для удаления
    start_idx = -1
    end_idx = -1
    
    # Ищем начало проблемного блока
    for i, line in enumerate(lines):
        if "// DELETED - Duplicate function removed to fix flickering" in line:
            start_idx = i
            break
    
    # Ищем конец блока (до следующего комментария "// Advanced Filters System")
    if start_idx >= 0:
        for i in range(start_idx + 1, len(lines)):
            if "// Advanced Filters System" in lines[i] and i != start_idx:
                end_idx = i - 1  # Не включаем строку с комментарием
                break
    
    print(f"Найден блок со строки {start_idx+1} по {end_idx+1}")
    
    if start_idx >= 0 and end_idx > start_idx:
        # Создаем новый список строк без проблемного блока
        new_lines = lines[:start_idx] + [
            "// DELETED - Duplicate function removed to fix flickering\n",
            "\n"
        ] + lines[end_idx+1:]
        
        # Записываем обратно
        with open('templates/properties.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        removed_lines = end_idx - start_idx + 1
        print(f"✅ Удалено {removed_lines} строк дублированного кода")
        print(f"Новое количество строк: {len(new_lines)}")
        return True
    else:
        print("❌ Не удалось найти границы блока для удаления")
        return False

if __name__ == "__main__":
    cleanup_properties_template()