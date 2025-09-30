#!/usr/bin/env python3
"""
Сброс пароля для клиента Станислава
"""

from werkzeug.security import generate_password_hash
from app import app, db
from models import User

def reset_password():
    with app.app_context():
        # Найти пользователя
        user = User.query.filter_by(email='bithome@mail.ru').first()
        
        if user:
            # Установить простой пароль
            new_password = 'inback123'
            user.password_hash = generate_password_hash(new_password)
            
            db.session.commit()
            
            print(f"✅ Пароль для {user.full_name} ({user.email}) сброшен")
            print(f"📧 Email: {user.email}")
            print(f"🔑 Пароль: {new_password}")
            print(f"🌐 Ссылка для входа: http://localhost:5000/login")
            
            return True
        else:
            print("❌ Пользователь не найден")
            return False

if __name__ == "__main__":
    reset_password()