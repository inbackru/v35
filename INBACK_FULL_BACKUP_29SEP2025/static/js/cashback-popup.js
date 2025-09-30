/**
 * Cashback Popup Gamification System
 * InBack.ru - Мотивационный всплывающий элемент для привлечения внимания к кешбеку
 */

class CashbackPopup {
    constructor() {
        this.popup = null;
        this.showTimer = null;
        this.hideTimer = null;
        this.intervalTimer = null;
        this.isShown = false;
        this.isUserClosed = false;
        
        // Настройки
        this.config = {
            showInterval: this.getRandomInterval(30, 45), // 30-45 секунд
            autoHideDelay: 10000, // 10 секунд
            pulseDelay: 3000, // Пульсация через 3 секунды после показа
            storageKey: 'inback_cashback_popup_closed',
            minPageTime: 15000 // Минимальное время на странице перед первым показом (15 сек)
        };
        
        this.init();
    }
    
    init() {
        // Проверяем, не закрыл ли пользователь попап в текущей сессии
        if (sessionStorage.getItem(this.config.storageKey)) {
            console.log('🚫 Cashback popup: Пользователь уже закрывал в этой сессии');
            return;
        }
        
        // Ждем загрузки DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.startSystem());
        } else {
            this.startSystem();
        }
    }
    
    startSystem() {
        this.createPopupHTML();
        this.bindEvents();
        
        // Запускаем систему через минимальное время на странице
        setTimeout(() => {
            if (!this.isUserClosed) {
                this.startPeriodicShow();
            }
        }, this.config.minPageTime);
        
        console.log('🎮 Cashback Popup System инициализирован');
    }
    
    createPopupHTML() {
        // Создаем HTML структуру всплывающего элемента
        const popupHTML = `
            <div id="cashbackPopup" class="cashback-popup">
                <div class="close-btn" id="cashbackCloseBtn" title="Закрыть">×</div>
                
                <div class="popup-header">
                    <div class="wallet-icon">😊</div>
                    
                    <h3 class="popup-title">Кэшбек до 5%</h3>
                </div>
                
                <div class="popup-content">
                    <p class="popup-text">
                        При покупке новостройки в Краснодаре вы можете получить 
                        <span class="highlight-text">до 500 000 ₽</span> кэшбека!
                    </p>
                    
                    <button class="action-btn" id="cashbackActionBtn">
                        <i class="fas fa-info-circle" style="margin-right: 8px;"></i>
                        Узнать больше
                    </button>
                </div>
                
                <div class="progress-bar"></div>
            </div>
        `;
        
        // Добавляем в конец body
        document.body.insertAdjacentHTML('beforeend', popupHTML);
        this.popup = document.getElementById('cashbackPopup');
    }
    
    bindEvents() {
        // Кнопка закрытия
        const closeBtn = document.getElementById('cashbackCloseBtn');
        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.closePopup();
            });
        }
        
        // Основная кнопка - переход на страницу "Как это работает"
        const actionBtn = document.getElementById('cashbackActionBtn');
        if (actionBtn) {
            actionBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleActionClick();
            });
        }
        
        // Закрытие по ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isShown) {
                this.closePopup();
            }
        });
        
        // Пауза при наведении мыши
        if (this.popup) {
            this.popup.addEventListener('mouseenter', () => {
                this.clearHideTimer();
            });
            
            this.popup.addEventListener('mouseleave', () => {
                if (this.isShown) {
                    this.startHideTimer();
                }
            });
        }
    }
    
    startPeriodicShow() {
        // Показываем сразу
        this.showPopup();
        
        // Настраиваем периодическое появление
        this.intervalTimer = setInterval(() => {
            if (!this.isUserClosed && !this.isShown) {
                this.showPopup();
            }
        }, this.getRandomInterval(30, 45) * 1000);
    }
    
    showPopup() {
        if (!this.popup || this.isShown || this.isUserClosed) return;
        
        console.log('💰 Показываем Cashback Popup');
        
        // Показываем попап
        this.popup.classList.add('show');
        this.isShown = true;
        
        // Трекинг событий
        this.trackEvent('popup_shown');
        
        // Запускаем пульсацию через несколько секунд
        setTimeout(() => {
            if (this.isShown) {
                this.popup.classList.add('pulse');
            }
        }, this.config.pulseDelay);
        
        // Автоматическое скрытие через 10 секунд
        this.startHideTimer();
    }
    
    hidePopup() {
        if (!this.popup || !this.isShown) return;
        
        console.log('🫥 Скрываем Cashback Popup (автоматически)');
        
        // Убираем классы
        this.popup.classList.remove('show', 'pulse');
        this.isShown = false;
        
        // Очищаем таймеры
        this.clearHideTimer();
        
        // Трекинг событий
        this.trackEvent('popup_auto_hidden');
    }
    
    closePopup() {
        if (!this.popup || !this.isShown) return;
        
        console.log('❌ Закрываем Cashback Popup (пользователь)');
        
        // Скрываем попап
        this.popup.classList.remove('show', 'pulse');
        this.isShown = false;
        this.isUserClosed = true;
        
        // Сохраняем в sessionStorage что пользователь закрыл
        sessionStorage.setItem(this.config.storageKey, 'true');
        
        // Очищаем все таймеры
        this.clearAllTimers();
        
        // Трекинг событий
        this.trackEvent('popup_user_closed');
    }
    
    handleActionClick() {
        console.log('🔗 Переход на страницу заявки');
        
        // Трекинг клика
        this.trackEvent('popup_action_clicked');
        
        // Закрываем попап
        this.closePopup();
        
        // Переходим на страницу заявки
        // Проверяем текущий URL чтобы не перезагружать если уже на целевой странице
        const currentPath = window.location.pathname;
        const targetPath = '/contacts';
        
        if (currentPath !== targetPath) {
            window.location.href = targetPath;
        }
    }
    
    startHideTimer() {
        this.clearHideTimer();
        this.hideTimer = setTimeout(() => {
            this.hidePopup();
        }, this.config.autoHideDelay);
    }
    
    clearHideTimer() {
        if (this.hideTimer) {
            clearTimeout(this.hideTimer);
            this.hideTimer = null;
        }
    }
    
    clearAllTimers() {
        this.clearHideTimer();
        
        if (this.intervalTimer) {
            clearInterval(this.intervalTimer);
            this.intervalTimer = null;
        }
        
        if (this.showTimer) {
            clearTimeout(this.showTimer);
            this.showTimer = null;
        }
    }
    
    getRandomInterval(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    trackEvent(eventName) {
        // Yandex Metrika трекинг
        if (typeof ym !== 'undefined') {
            try {
                ym(104270300, 'reachGoal', `cashback_popup_${eventName}`);
            } catch (e) {
                console.warn('Ошибка Yandex Metrika трекинга:', e);
            }
        }
        
        // Google Analytics трекинг (если есть)
        if (typeof gtag !== 'undefined') {
            try {
                gtag('event', 'cashback_popup', {
                    'event_category': 'gamification',
                    'event_label': eventName,
                    'value': 1
                });
            } catch (e) {
                console.warn('Ошибка Google Analytics трекинга:', e);
            }
        }
        
        // Консольный лог для разработки
        console.log(`📊 Cashback Popup Event: ${eventName}`);
    }
    
    // Методы для управления извне (если нужно)
    forceShow() {
        if (!this.isUserClosed) {
            this.showPopup();
        }
    }
    
    forceHide() {
        this.hidePopup();
    }
    
    destroy() {
        console.log('🗑️ Уничтожаем Cashback Popup System');
        this.clearAllTimers();
        if (this.popup) {
            this.popup.remove();
        }
    }
}

// Инициализация системы
let cashbackPopupSystem = null;

// Запускаем только если не на странице презентации
if (!window.SKIP_MAIN_JS && 
    document.documentElement?.dataset.page !== 'presentation' && 
    document.body?.dataset.page !== 'presentation') {
    
    // Инициализируем систему после загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            cashbackPopupSystem = new CashbackPopup();
        });
    } else {
        cashbackPopupSystem = new CashbackPopup();
    }
}

// Экспорт для глобального доступа
window.CashbackPopup = CashbackPopup;
window.cashbackPopupSystem = cashbackPopupSystem;