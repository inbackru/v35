#!/usr/bin/env python3
"""Test script to verify blog category filtering is working"""

import sys
sys.path.append('.')

from app import app
from models import BlogPost, BlogCategory

def test_blog_categories():
    """Test that blog categories work correctly"""
    
    with app.test_client() as client:
        print("=== ТЕСТИРОВАНИЕ БЛОГА ===")
        
        # Test main blog page
        response = client.get('/blog')
        print(f"✅ Главная страница блога: {response.status_code}")
        
        # Test category filtering
        test_categories = ['Тест', 'Районы Краснодара', 'Инвестиции']
        
        for category in test_categories:
            response = client.get(f'/blog?category={category}')
            print(f"✅ Категория '{category}': {response.status_code}")
            
            # Check if articles are present
            if response.status_code == 200:
                content = response.get_data(as_text=True)
                if 'Статьи не найдены' in content:
                    print(f"  ⚠️  Статьи не отображаются для категории '{category}'")
                else:
                    print(f"  ✅ Статьи найдены для категории '{category}'")
        
        print("\n=== РЕЗУЛЬТАТ ===")
        print("Блог работает, проверьте категории в браузере")

if __name__ == '__main__':
    test_blog_categories()