#!/usr/bin/env python3
"""
РЕАЛЬНЫЙ тест отправки email с настройкой SMTP
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_real_email_direct(recipient_email, smtp_user=None, smtp_password=None):
    """Отправляем email напрямую через SMTP без Flask контекста"""
    
    print("=" * 60)
    print("📧 ПРЯМАЯ ОТПРАВКА EMAIL ЧЕРЕЗ SMTP")
    print("=" * 60)
    print(f"📬 Получатель: {recipient_email}")
    print(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Настройки SMTP
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    
    if not smtp_user:
        smtp_user = input("📧 Введите Gmail (для отправки): ").strip()
    if not smtp_password:
        smtp_password = input("🔐 Введите App Password: ").strip()
    
    # Создаем HTML письмо
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Тест InBack Email</title>
        <style>
            body {{
                font-family: 'Inter', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #0088CC 0%, #006699 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background: white;
                padding: 30px;
                border: 1px solid #ddd;
                border-radius: 0 0 8px 8px;
            }}
            .logo {{
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .btn {{
                display: inline-block;
                background: #0088CC;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 14px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">InBack</div>
            <p>Тест Email Системы</p>
        </div>
        
        <div class="content">
            <h1>🎉 Email система работает!</h1>
            
            <p>Это тестовое письмо от InBack - платформы недвижимости с кэшбеком.</p>
            
            <div style="background: #f0f9ff; border-left: 4px solid #0088CC; padding: 15px; margin: 20px 0;">
                <h3>✅ Что протестировано:</h3>
                <ul>
                    <li>✓ SMTP соединение</li>
                    <li>✓ HTML шаблоны</li>
                    <li>✓ Кодировка UTF-8</li>
                    <li>✓ Реальная доставка</li>
                </ul>
            </div>
            
            <p><strong>Детали отправки:</strong></p>
            <ul>
                <li>Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li>Получатель: {recipient_email}</li>
                <li>Отправитель: InBack Email System</li>
                <li>Метод: Direct SMTP</li>
            </ul>
            
            <p>Если вы получили это письмо, значит email система InBack настроена корректно и готова для реальных пользователей!</p>
            
            <div style="text-align: center;">
                <a href="https://inback.ru" class="btn">Перейти на InBack.ru</a>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 InBack. Тестовое письмо email системы.</p>
        </div>
    </body>
    </html>
    """
    
    try:
        # Создаем сообщение
        message = MIMEMultipart('alternative')
        message['Subject'] = "🏠 InBack Email System - Тест успешен!"
        message['From'] = f"InBack Test <{smtp_user}>"
        message['To'] = recipient_email
        
        # Добавляем HTML
        html_part = MIMEText(html_content, 'html', 'utf-8')
        message.attach(html_part)
        
        print(f"\n🔄 Подключаемся к {smtp_host}:{smtp_port}...")
        
        # Отправляем через Gmail SMTP
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            print("🔐 Авторизуемся...")
            server.login(smtp_user, smtp_password)
            print("📤 Отправляем email...")
            server.send_message(message)
        
        print("✅ EMAIL ОТПРАВЛЕН УСПЕШНО!")
        print(f"📧 Проверьте почту: {recipient_email}")
        print("📁 Проверьте папку СПАМ если не видите письмо")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ ОШИБКА АВТОРИЗАЦИИ!")
        print("🔧 Проверьте:")
        print("  1. Правильность email и пароля")
        print("  2. Включена ли двухфакторная аутентификация")
        print("  3. Используете ли App Password (не обычный пароль)")
        return False
        
    except Exception as e:
        print(f"❌ ОШИБКА ОТПРАВКИ: {e}")
        return False

if __name__ == "__main__":
    print("РЕАЛЬНАЯ ОТПРАВКА EMAIL ЧЕРЕЗ SMTP")
    print("Для Gmail нужен App Password (не обычный пароль)")
    print("Создайте его в настройках Google Account > Security > App passwords")
    print()
    
    email = input("📧 Email получателя: ").strip()
    
    if not email or '@' not in email:
        print("❌ Некорректный email!")
        sys.exit(1)
    
    success = send_real_email_direct(email)
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 РЕАЛЬНАЯ ОТПРАВКА УСПЕШНА!")
        print("📬 InBack email система готова к работе")
    else:
        print("❌ ОТПРАВКА НЕ УДАЛАСЬ")
        print("🔧 Настройте SMTP параметры")
    print("=" * 60)