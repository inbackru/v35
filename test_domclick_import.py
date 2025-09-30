#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование импорта данных из Domclick
"""

from app import app, import_domclick_to_database

def test_import():
    """Тестируем импорт данных из Domclick"""
    with app.app_context():
        print("🧪 Тестируем импорт данных из Domclick...")
        
        result = import_domclick_to_database()
        
        if result['success']:
            print("✅ Импорт успешен!")
            print(f"   • Застройщиков создано: {result['developers_created']}")
            print(f"   • ЖК создано: {result['complexes_created']}")
            print(f"   • Квартир импортировано: {result['apartments_created']}")
        else:
            print(f"❌ Ошибка импорта: {result['error']}")

if __name__ == "__main__":
    test_import()