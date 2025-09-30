"""Application notification functions"""
import requests
import os
from datetime import datetime

def notify_application_submitted(application, user):
    """Send notifications about new application to Telegram and email"""
    
    # Prepare message
    message = f"""🏠 Новая заявка на подбор квартиры!

👤 Клиент: {user.full_name}
📧 Email: {user.email}
📱 Телефон: {user.phone}

📋 Детали заявки:
{application.message}

⏰ Время: {application.created_at.strftime('%d.%m.%Y %H:%M')}
"""
    
    # Send to Telegram (manager/admin)
    try:
        telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        admin_chat_id = '730764738'  # Stanislaw's chat ID
        
        if telegram_token and admin_chat_id:
            telegram_url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
            telegram_data = {
                'chat_id': admin_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(telegram_url, data=telegram_data, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram notification sent successfully")
            else:
                print(f"❌ Telegram notification failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Telegram notification error: {e}")
    
    # Send email notification
    try:
        send_application_email_notification(application, user)
        print("✅ Email notification sent successfully")
    except Exception as e:
        print(f"❌ Email notification error: {e}")

def send_application_email_notification(application, user):
    """Send email notification about new application"""
    
    # Email to admin/manager
    admin_subject = f"Новая заявка на подбор квартиры от {user.full_name}"
    admin_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #0088CC;">🏠 Новая заявка на подбор квартиры</h2>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3>Информация о клиенте:</h3>
            <p><strong>Имя:</strong> {user.full_name}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Телефон:</strong> {user.phone}</p>
        </div>
        
        <div style="background: #fff; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <h3>Детали заявки:</h3>
            <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{application.message}</pre>
        </div>
        
        <div style="margin: 20px 0; padding: 15px; background: #e3f2fd; border-radius: 8px;">
            <p><strong>Время подачи:</strong> {application.created_at.strftime('%d.%m.%Y в %H:%M')}</p>
        </div>
        
        <div style="margin-top: 30px; text-align: center;">
            <a href="https://inback.ru/manager/dashboard" 
               style="background: #0088CC; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Открыть панель менеджера
            </a>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px; text-align: center;">
            InBack.ru - недвижимость с кэшбэком
        </p>
    </body>
    </html>
    """
    
    # Confirmation email to user
    user_subject = "Ваша заявка принята - InBack.ru"
    user_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #0088CC;">Спасибо за вашу заявку!</h2>
        
        <p>Здравствуйте, {user.full_name}!</p>
        
        <p>Мы получили вашу заявку на подбор квартиры. Наш менеджер свяжется с вами в ближайшее время для обсуждения деталей.</p>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3>Ваши предпочтения:</h3>
            <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{application.message}</pre>
        </div>
        
        <p>Пока мы готовим подборку, вы можете:</p>
        <ul>
            <li><a href="https://inback.ru/properties" style="color: #0088CC;">Изучить каталог недвижимости</a></li>
            <li><a href="https://inback.ru/complexes" style="color: #0088CC;">Посмотреть жилые комплексы</a></li>
            <li><a href="https://inback.ru/blog" style="color: #0088CC;">Прочитать полезные статьи</a></li>
        </ul>
        
        <div style="margin: 20px 0; padding: 15px; background: #e8f5e8; border-radius: 8px;">
            <p><strong>🎁 Кэшбэк до 300 000 ₽</strong> при покупке недвижимости через InBack!</p>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px; text-align: center;">
            С уважением,<br>
            Команда InBack.ru
        </p>
    </body>
    </html>
    """
    
    try:
        # Send admin notification
        from email_service import send_html_email
        send_html_email("info@inback.ru", admin_subject, admin_html)
        
        # Send user confirmation
        send_html_email(user.email, user_subject, user_html)
        
    except Exception as e:
        print(f"Email sending failed: {e}")
        raise