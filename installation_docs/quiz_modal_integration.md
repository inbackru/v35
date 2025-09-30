# Интеграция квиз-модала с кнопками заявок - Инструкции

## Цель
Подключить все кнопки "подать заявку" к единой рабочей квиз-форме из header.

## Выполненные изменения

### 1. Обновлена глобальная функция в base.html
```javascript
window.openApplicationModal = function() {
    // Использует рабочую квиз-систему через openQuizModal()
    if (typeof openQuizModal === 'function') {
        openQuizModal();
    }
}
```

### 2. Подключены страницы ипотеки
- `templates/it-mortgage.html` - кнопка "Подать заявку на IT-ипотеку"
- `templates/military_mortgage.html` - все кнопки военной ипотеки  
- `templates/family_mortgage.html` - кнопки семейной ипотеки
- `templates/it_mortgage.html` - дублирующие кнопки IT-ипотеки

### 3. Удалены старые заглушки
Во всех mortgage страницах заменены:
```javascript
// БЫЛО:
function openApplicationModal() {
    alert('Функция подачи заявки в разработке');
}

// СТАЛО:
// openApplicationModal function is defined globally in base.html
```

### 4. Рабочая квиз-система
- Базируется на `static/js/modals.js`
- Использует `templates/quiz_registration.html`
- Пошаговая форма с прогресс-баром
- Интеграция с Telegram API

## Файлы изменений
```
templates/base.html - обновлена openApplicationModal()
templates/it-mortgage.html - добавлен onclick
templates/military_mortgage.html - обновлены кнопки
templates/family_mortgage.html - подключена функция
templates/it_mortgage.html - удалена заглушка
templates/how-it-works.html - удалена заглушка  
templates/maternal_capital.html - удалена заглушка
templates/developer_mortgage.html - удалена заглушка
templates/ipoteka.html - удалена заглушка
```

## Результат
✓ Единая квиз-форма для всех кнопок заявок
✓ Удалены все заглушки "в разработке"
✓ Работающая система подачи заявок