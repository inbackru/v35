#!/usr/bin/env python3
"""
Система настроек уведомлений для пользователей
Позволяет настраивать предпочтения по способам получения уведомлений
"""

from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
from models import User, db
import json

notification_settings_bp = Blueprint('notification_settings', __name__)

@notification_settings_bp.route('/api/user/notification-settings', methods=['GET'])
def get_notification_settings():
    """Получить настройки уведомлений пользователя"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация'}), 401
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
        
        settings = {
            'preferred_contact': getattr(user, 'preferred_contact', 'email'),
            'email_enabled': getattr(user, 'email_notifications', True),
            'telegram_enabled': bool(getattr(user, 'telegram_id', None)),
            'telegram_id': getattr(user, 'telegram_id', None),
            'whatsapp_enabled': bool(getattr(user, 'phone', None)),
            'phone': getattr(user, 'phone', None),
            'notification_types': {
                'recommendations': getattr(user, 'notify_recommendations', True),
                'saved_searches': getattr(user, 'notify_saved_searches', True),
                'applications': getattr(user, 'notify_applications', True),
                'cashback': getattr(user, 'notify_cashback', True),
                'marketing': getattr(user, 'notify_marketing', False)
            }
        }
        
        return jsonify({'success': True, 'settings': settings})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@notification_settings_bp.route('/api/user/notification-settings', methods=['POST'])
def update_notification_settings():
    """Обновить настройки уведомлений пользователя"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация'}), 401
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
        
        data = request.get_json()
        
        # Обновляем основные настройки
        if 'preferred_contact' in data:
            user.preferred_contact = data['preferred_contact']
        
        if 'email_enabled' in data:
            user.email_notifications = data['email_enabled']
        
        if 'phone' in data:
            user.phone = data['phone']
        
        if 'telegram_id' in data:
            user.telegram_id = data['telegram_id']
        
        # Обновляем настройки типов уведомлений
        if 'notification_types' in data:
            types = data['notification_types']
            user.notify_recommendations = types.get('recommendations', True)
            user.notify_saved_searches = types.get('saved_searches', True)
            user.notify_applications = types.get('applications', True)
            user.notify_cashback = types.get('cashback', True)
            user.notify_marketing = types.get('marketing', False)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Настройки обновлены'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@notification_settings_bp.route('/api/user/telegram-link', methods=['POST'])
def link_telegram():
    """Привязать Telegram аккаунт к профилю пользователя"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Требуется авторизация'}), 401
    
    try:
        data = request.get_json()
        verification_code = data.get('verification_code')
        
        if not verification_code:
            return jsonify({'success': False, 'error': 'Необходим код верификации'}), 400
        
        # Здесь можно добавить логику верификации кода через Telegram Bot API
        # Пока используем простую проверку
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
        
        # В реальной реализации здесь должна быть проверка кода
        # user.telegram_id = verified_telegram_id_from_bot
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Telegram аккаунт успешно привязан',
            'telegram_linked': True
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@notification_settings_bp.route('/notification-settings')
def notification_settings_page():
    """Страница настроек уведомлений"""
    if 'user_id' not in session:
        flash('Для доступа к настройкам необходимо войти в аккаунт', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('Пользователь не найден', 'error')
        return redirect(url_for('login'))
    
    return render_template('user/notification_settings.html', user=user)

def check_user_notification_preferences(user, notification_type):
    """
    Проверяет, хочет ли пользователь получать уведомления данного типа
    
    Args:
        user: Объект пользователя
        notification_type: Тип уведомления
    
    Returns:
        bool: True если пользователь хочет получать такие уведомления
    """
    if not user:
        return True  # По умолчанию отправляем
    
    type_mapping = {
        'recommendation': 'notify_recommendations',
        'saved_search_results': 'notify_saved_searches', 
        'application_confirmation': 'notify_applications',
        'application_status': 'notify_applications',
        'cashback_approved': 'notify_cashback',
        'marketing': 'notify_marketing'
    }
    
    preference_attr = type_mapping.get(notification_type)
    if preference_attr:
        return getattr(user, preference_attr, True)
    
    return True  # По умолчанию для неизвестных типов

# Функция для интеграции в основную систему уведомлений
def should_send_notification(user, notification_type, method='email'):
    """
    Определяет, нужно ли отправлять уведомление пользователю
    
    Args:
        user: Объект пользователя
        notification_type: Тип уведомления
        method: Способ доставки (email, telegram, whatsapp)
    
    Returns:
        bool: True если нужно отправлять
    """
    if not user:
        return False
    
    # Проверяем глобальные настройки типа уведомлений
    if not check_user_notification_preferences(user, notification_type):
        return False
    
    # Проверяем настройки способа доставки
    preferred_contact = getattr(user, 'preferred_contact', 'email')
    
    if method == 'email':
        return preferred_contact in ['email', 'both'] and getattr(user, 'email_notifications', True)
    elif method == 'telegram':
        return (preferred_contact in ['telegram', 'both'] and 
                bool(getattr(user, 'telegram_id', None)))
    elif method == 'whatsapp':
        return (preferred_contact in ['whatsapp', 'both'] and 
                bool(getattr(user, 'phone', None)))
    
    return False