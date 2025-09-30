"""
Telegram Bot для интеграции с InBack
Обрабатывает команды пользователей и связывает Telegram аккаунты с профилями InBack
"""

import os
import asyncio
import logging
import requests

# Try importing telegram modules with error handling
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
    TELEGRAM_AVAILABLE = True
except ImportError as e:
    print(f"Telegram library not available: {e}")
    TELEGRAM_AVAILABLE = False
    # Create dummy classes to prevent errors
    class Update:
        pass
    class ContextTypes:
        DEFAULT_TYPE = None
    
from app import app, db
from models import User

# Конфигурация
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')  # URL для webhook

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def send_telegram_message(chat_id, message):
    """Send telegram message using simple HTTP API"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Telegram bot token not configured in environment")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'  # Changed to HTML for better formatting
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Telegram message sent successfully to {chat_id}")
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending telegram message: {e}")
        return False

def send_recommendation_notification(user_telegram_id, recommendation_data):
    """Send recommendation notification via Telegram"""
    if not user_telegram_id:
        print("No Telegram ID for user")
        return False
    
    message = f"""🏠 <b>Новая рекомендация от менеджера</b>

📋 <b>{recommendation_data.get('title', 'Новая рекомендация')}</b>
🏢 {recommendation_data.get('item_name', 'Объект')}
📝 {recommendation_data.get('description', '')}

💡 <i>Приоритет:</i> {recommendation_data.get('priority_level', 'Обычный').title()}

🔗 <a href="https://inback.ru/{recommendation_data.get('recommendation_type', 'property')}/{recommendation_data.get('item_id')}">Посмотреть объект</a>
💼 <a href="https://inback.ru/dashboard">Личный кабинет</a>"""
    
    return send_telegram_message(user_telegram_id, message)

class InBackBot:
    def __init__(self):
        if not TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN не установлен")
            return
        
        if not TELEGRAM_AVAILABLE:
            logger.error("Telegram library not available")
            return
        
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("link", self.link_command))
        self.application.add_handler(CommandHandler("unlink", self.unlink_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        self.application.add_handler(CommandHandler("favorites", self.favorites_command))
        self.application.add_handler(CommandHandler("notifications", self.notifications_command))
        
        # Обработчик текстовых сообщений
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        chat_id = update.effective_chat.id
        user_name = update.effective_user.first_name
        
        welcome_message = f"""
🏠 <b>Добро пожаловать в InBack Bot, {user_name}!</b>

Я помогу вам получать уведомления о:
• 🆕 Новых объектах недвижимости
• 💰 Статусе вашего кэшбека
• 📅 Назначенных встречах
• ✅ Обновлениях заявок

<b>Доступные команды:</b>
/link - Привязать ваш аккаунт InBack
/profile - Информация о профиле
/favorites - Избранные объекты
/notifications - Настройки уведомлений
/help - Помощь

Чтобы начать получать уведомления, используйте команду /link с вашим email адресом.
        """
        
        await update.message.reply_text(welcome_message, parse_mode='HTML')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help"""
        help_message = """
📋 <b>Справка по командам InBack Bot:</b>

🔗 <b>/link email@example.com</b>
   Привязать Telegram к аккаунту InBack

👤 <b>/profile</b>
   Показать информацию о профиле

❤️ <b>/favorites</b>
   Список избранных объектов

🔔 <b>/notifications on/off</b>
   Включить/выключить уведомления

🔓 <b>/unlink</b>
   Отвязать аккаунт от Telegram

<b>Примеры использования:</b>
• <code>/link demo@inback.ru</code>
• <code>/notifications on</code>
• <code>/profile</code>

<b>Поддержка:</b>
💬 Telegram: @inback_support
📧 Email: support@inback.ru
📞 Телефон: +7 (861) 234-56-78
        """
        
        await update.message.reply_text(help_message, parse_mode='HTML')
    
    async def link_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /link для привязки аккаунта"""
        chat_id = update.effective_chat.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Укажите ваш email адрес.\n\n"
                "Пример: <code>/link demo@inback.ru</code>",
                parse_mode='HTML'
            )
            return
        
        email = context.args[0].lower().strip()
        
        # Проверяем формат email
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            await update.message.reply_text(
                "❌ Неверный формат email адреса.\n\n"
                "Пример: <code>/link demo@inback.ru</code>",
                parse_mode='HTML'
            )
            return
        
        with app.app_context():
            # Ищем пользователя по email
            user = User.query.filter_by(email=email).first()
            
            if not user:
                await update.message.reply_text(
                    f"❌ Аккаунт с email {email} не найден.\n\n"
                    "Зарегистрируйтесь на сайте InBack.ru и повторите попытку."
                )
                return
            
            # Проверяем, не привязан ли уже другой Telegram
            if user.telegram_id and user.telegram_id != str(chat_id):
                await update.message.reply_text(
                    "❌ Этот аккаунт уже привязан к другому Telegram.\n\n"
                    "Для смены привязки обратитесь в поддержку."
                )
                return
            
            # Привязываем аккаунт
            user.telegram_id = str(chat_id)
            user.telegram_notifications = True
            db.session.commit()
            
            success_message = f"""
✅ <b>Аккаунт успешно привязан!</b>

👤 <b>Профиль:</b> {user.full_name}
📧 <b>Email:</b> {email}
🔔 <b>Уведомления:</b> Включены

Теперь вы будете получать уведомления о новых объектах, обновлениях заявок и статусе кэшбека.

Управляйте настройками: /notifications
            """
            
            await update.message.reply_text(success_message, parse_mode='HTML')
    
    async def unlink_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /unlink для отвязки аккаунта"""
        chat_id = update.effective_chat.id
        
        with app.app_context():
            user = User.query.filter_by(telegram_id=str(chat_id)).first()
            
            if not user:
                await update.message.reply_text(
                    "❌ Аккаунт не привязан к этому Telegram.\n\n"
                    "Используйте /link для привязки аккаунта."
                )
                return
            
            user.telegram_id = None
            user.telegram_notifications = False
            db.session.commit()
            
            await update.message.reply_text(
                "✅ Аккаунт успешно отвязан от Telegram.\n\n"
                "Уведомления больше не будут приходить в этот чат."
            )
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /profile"""
        chat_id = update.effective_chat.id
        
        with app.app_context():
            user = User.query.filter_by(telegram_id=str(chat_id)).first()
            
            if not user:
                await update.message.reply_text(
                    "❌ Аккаунт не привязан.\n\n"
                    "Используйте /link для привязки аккаунта."
                )
                return
            
            profile_message = f"""
👤 <b>Ваш профиль InBack</b>

<b>Имя:</b> {user.full_name}
<b>Email:</b> {user.email}
<b>Телефон:</b> {user.phone or 'Не указан'}
<b>ID пользователя:</b> {user.user_id}

📊 <b>Статистика:</b>
• Избранных объектов: {len(user.favorites)}
• Активных заявок: {len([app for app in user.applications if app.status in ['new', 'in_progress']])}
• Общий кэшбек: {user.get_total_cashback():,} ₽

🔔 <b>Уведомления:</b> {'Включены' if user.telegram_notifications else 'Выключены'}

<a href="https://inback.ru/dashboard">Перейти в личный кабинет</a>
            """
            
            await update.message.reply_text(profile_message, parse_mode='HTML')
    
    async def favorites_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /favorites"""
        chat_id = update.effective_chat.id
        
        with app.app_context():
            user = User.query.filter_by(telegram_id=str(chat_id)).first()
            
            if not user:
                await update.message.reply_text(
                    "❌ Аккаунт не привязан.\n\n"
                    "Используйте /link для привязки аккаунта."
                )
                return
            
            if not user.favorites:
                await update.message.reply_text(
                    "📭 У вас пока нет избранных объектов.\n\n"
                    "Добавляйте понравившиеся квартиры в избранное на сайте InBack.ru"
                )
                return
            
            favorites_message = f"❤️ <b>Ваши избранные объекты ({len(user.favorites)}):</b>\n\n"
            
            # Загружаем данные об объектах
            from app import load_properties
            properties = load_properties()
            
            for i, favorite in enumerate(user.favorites[:5], 1):  # Показываем первые 5
                # Находим объект по ID
                property_data = next((p for p in properties if p['id'] == favorite.property_id), None)
                if property_data:
                    price = f"{property_data.get('price', 0):,}".replace(',', ' ')
                    favorites_message += f"{i}. <b>{property_data.get('title', 'Объект')}</b>\n"
                    favorites_message += f"   💰 {price} ₽\n"
                    favorites_message += f"   📍 {property_data.get('location', 'Краснодар')}\n\n"
            
            if len(user.favorites) > 5:
                favorites_message += f"... и еще {len(user.favorites) - 5} объектов\n\n"
            
            favorites_message += "<a href='https://inback.ru/favorites'>Посмотреть все избранные</a>"
            
            await update.message.reply_text(favorites_message, parse_mode='HTML')
    
    async def notifications_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /notifications"""
        chat_id = update.effective_chat.id
        
        with app.app_context():
            user = User.query.filter_by(telegram_id=str(chat_id)).first()
            
            if not user:
                await update.message.reply_text(
                    "❌ Аккаунт не привязан.\n\n"
                    "Используйте /link для привязки аккаунта."
                )
                return
            
            if context.args:
                action = context.args[0].lower()
                if action == 'on':
                    user.telegram_notifications = True
                    db.session.commit()
                    await update.message.reply_text("✅ Уведомления включены!")
                    return
                elif action == 'off':
                    user.telegram_notifications = False
                    db.session.commit()
                    await update.message.reply_text("❌ Уведомления выключены.")
                    return
            
            status = "включены" if user.telegram_notifications else "выключены"
            message = f"""
🔔 <b>Настройки уведомлений</b>

<b>Статус:</b> {status}

<b>Управление:</b>
• <code>/notifications on</code> - включить
• <code>/notifications off</code> - выключить

<b>Вы получаете уведомления о:</b>
• 🆕 Новых объектах по вашим критериям
• 💰 Изменении статуса кэшбека
• 📅 Назначенных встречах
• ✅ Обновлениях заявок
            """
            
            await update.message.reply_text(message, parse_mode='HTML')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        message_text = update.message.text.lower()
        
        if any(word in message_text for word in ['привет', 'здравствуй', 'hi', 'hello']):
            await update.message.reply_text(
                "Привет! 👋\n\n"
                "Я бот InBack для уведомлений о недвижимости.\n"
                "Используйте /help для списка команд."
            )
        elif any(word in message_text for word in ['помощь', 'команды', 'help']):
            await self.help_command(update, context)
        else:
            await update.message.reply_text(
                "Извините, я не понимаю эту команду. 🤖\n\n"
                "Используйте /help для списка доступных команд."
            )
    
    async def run_webhook(self, webhook_url: str, port: int = 8443):
        """Запуск бота в режиме webhook"""
        try:
            await self.application.initialize()
            await self.application.start()
            
            # Устанавливаем webhook
            await self.application.bot.set_webhook(url=webhook_url)
            logger.info(f"Webhook установлен: {webhook_url}")
            
            # Запускаем webhook сервер
            await self.application.run_webhook(
                listen="0.0.0.0",
                port=port,
                webhook_url=webhook_url
            )
        except Exception as e:
            logger.error(f"Ошибка webhook: {e}")
    
    async def run_polling(self):
        """Запуск бота в режиме polling (для разработки)"""
        try:
            logger.info("Запуск бота в режиме polling...")
            await self.application.run_polling()
        except Exception as e:
            logger.error(f"Ошибка polling: {e}")

# Flask маршрут для webhook
def create_webhook_route(app):
    """Создаёт маршрут webhook в Flask приложении"""
    from flask import request, jsonify
    
    @app.route('/webhook/telegram', methods=['POST'])
    def telegram_webhook():
        try:
            if not TELEGRAM_BOT_TOKEN:
                return jsonify({'error': 'Bot token not configured'}), 400
            
            # Получаем данные от Telegram
            json_data = request.get_json()
            
            # Обрабатываем через bot application
            bot = InBackBot()
            update = Update.de_json(json_data, bot.application.bot)
            
            # Обрабатываем в контексте asyncio
            asyncio.run(bot.application.process_update(update))
            
            return jsonify({'status': 'ok'})
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return jsonify({'error': str(e)}), 500

# Главная функция для запуска
async def main():
    """Главная функция для запуска бота"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не установлен в переменных окружения")
        return
    
    bot = InBackBot()
    
    if WEBHOOK_URL:
        print(f"🚀 Запуск бота в режиме webhook: {WEBHOOK_URL}")
        await bot.run_webhook(WEBHOOK_URL)
    else:
        print("🚀 Запуск бота в режиме polling...")
        await bot.run_polling()

if __name__ == '__main__':
    # Запуск бота
    asyncio.run(main())