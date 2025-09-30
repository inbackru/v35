# Полная интеграция квиз-заявок на всех страницах - Инструкции

## Выполненные изменения

### 1. Исправлена глобальная функция openApplicationModal()
В `templates/header.html` заменено перенаправление на /properties на:
```javascript
window.openApplicationModal = function() {
    console.log('Header: Opening quiz modal');
    if (typeof openQuizModal === 'function') {
        openQuizModal();
    } else {
        // Fallback - load modals.js if not available
        const script = document.createElement('script');
        script.src = '/static/js/modals.js';
        script.onload = function() {
            if (typeof openQuizModal === 'function') {
                openQuizModal();
            }
        };
        document.head.appendChild(script);
    }
};
```

### 2. Подключены квиз-кнопки на страницах:

#### Страницы "О нас" и информационные:
- `templates/about.html` - добавлена CTA секция с кнопкой "Рассчитать мой кешбек" 
- `templates/security.html` - обновлена кнопка "Получить кешбек" в hero + добавлена "Получить консультацию"
- `templates/contacts.html` - добавлена кнопка "Подобрать квартиру" к контактам

#### Страницы ипотеки (уже были подключены):
- `templates/it-mortgage.html` - "Подать заявку на IT-ипотеку"
- `templates/military_mortgage.html` - все кнопки военной ипотеки
- `templates/family_mortgage.html` - кнопки семейной ипотеки  
- `templates/it_mortgage.html` - дублирующие кнопки IT-ипотеки
- `templates/how-it-works.html` - "Рассчитать мой кешбек"

### 3. Удалены заглушки функций:
Во всех mortgage страницах заменены старые alert'ы на комментарии:
```javascript
// БЫЛО:
function openApplicationModal() {
    alert('Функция подачи заявки в разработке');
}

// СТАЛО:
// openApplicationModal function is defined globally in base.html
```

## Структура работы квиз-формы

### Компоненты:
1. **Глобальная функция** - `templates/base.html` и `templates/header.html`
2. **Модальная система** - `static/js/modals.js` 
3. **Контент квиза** - `templates/quiz_registration.html`
4. **Контейнер модала** - `templates/base.html` (#quiz-modal-container)

### Технический процесс:
1. Кнопка вызывает `openApplicationModal()`
2. Функция вызывает `openQuizModal()` из modals.js
3. modals.js загружает контент из /quiz-registration
4. Отображается пошаговая форма с прогресс-баром
5. Данные отправляются через Telegram API

## Файлы изменений:
```
templates/header.html - исправлена openApplicationModal()
templates/about.html - добавлена CTA секция  
templates/security.html - обновлены кнопки
templates/contacts.html - добавлена кнопка "Подобрать квартиру"
templates/it-mortgage.html - подключен onclick
templates/military_mortgage.html - обновлены кнопки
templates/family_mortgage.html - подключена функция
templates/it_mortgage.html - удалена заглушка
templates/how-it-works.html - удалена заглушка
templates/maternal_capital.html - удалена заглушка  
templates/developer_mortgage.html - удалена заглушка
templates/ipoteka.html - удалена заглушка
templates/how-it-works_my.html - удалена заглушка
```

## Результат:
✓ Единая рабочая квиз-форма на всех ключевых страницах
✓ Логичное размещение кнопок в контексте контента
✓ Устранены все заглушки "в разработке"
✓ Стабильная система подачи заявок