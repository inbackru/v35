/**
 * InBack Form Validation and Phone Formatting
 * Автоматическое форматирование телефонов и валидация форм
 */

class FormValidator {
    constructor() {
        this.init();
    }

    init() {
        // Инициализация при загрузке DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupValidation());
        } else {
            this.setupValidation();
        }
    }

    setupValidation() {
        this.setupPhoneFormatting();
        this.setupEmailValidation();
        this.setupNameValidation();
        this.setupFormSubmission();
        console.log('InBack form validation initialized');
    }

    /**
     * Настройка форматирования телефонных номеров
     */
    setupPhoneFormatting() {
        const phoneInputs = document.querySelectorAll('input[inputmode="tel"], input[name="phone"], input[id="phone"]');
        
        phoneInputs.forEach(input => {
            // Устанавливаем маску для телефона
            input.placeholder = '+7 (999) 999-99-99';
            
            // Форматирование по маске при вводе
            input.addEventListener('input', (e) => {
                this.formatPhoneWithMask(e);
            });
            
            // Валидация при потере фокуса
            input.addEventListener('blur', (e) => this.validatePhone(e));
            
            // При фокусе устанавливаем начальное значение если поле пустое
            input.addEventListener('focus', (e) => {
                if (e.target.value.trim() === '') {
                    e.target.value = '+7 (';
                    setTimeout(() => {
                        e.target.setSelectionRange(4, 4);
                    }, 0);
                }
            });

            console.log('Phone formatting setup for:', input.id || input.name || 'phone input');
        });
    }

    /**
     * Форматирование номера телефона по маске +7 (999) 999-99-99
     */
    formatPhoneWithMask(event) {
        const input = event.target;
        const currentValue = input.value;
        
        // Сохраняем позицию курсора
        const cursorPosition = input.selectionStart;
        
        // Извлекаем только цифры
        let digits = currentValue.replace(/\D/g, '');
        
        // Если начинается с 8, заменяем на 7
        if (digits.startsWith('8')) {
            digits = '7' + digits.slice(1);
        }
        
        // Если не начинается с 7, добавляем 7
        if (!digits.startsWith('7') && digits.length > 0) {
            digits = '7' + digits;
        }
        
        // Ограничиваем до 11 цифр
        if (digits.length > 11) {
            digits = digits.slice(0, 11);
        }
        
        // Форматируем
        let formatted = '';
        if (digits.length > 0) {
            formatted = '+7';
            if (digits.length > 1) {
                const phone = digits.slice(1); // Убираем первую 7
                if (phone.length > 0) {
                    formatted += ' (' + phone.slice(0, 3);
                    if (phone.length > 3) {
                        formatted += ') ' + phone.slice(3, 6);
                        if (phone.length > 6) {
                            formatted += '-' + phone.slice(6, 8);
                            if (phone.length > 8) {
                                formatted += '-' + phone.slice(8, 10);
                            }
                        }
                    }
                    if (phone.length === 3) {
                        formatted += ')';
                    }
                }
            }
        }
        
        // Обновляем значение только если оно изменилось
        if (formatted !== currentValue) {
            input.value = formatted;
            
            // Восстанавливаем курсор в конец
            const newPosition = formatted.length;
            setTimeout(() => {
                input.setSelectionRange(newPosition, newPosition);
            }, 0);
        }
        
        this.updateValidationState(input, this.isValidPhone(input.value));
    }

    /**
     * Проверка корректности номера телефона
     */
    isValidPhone(phone) {
        if (!phone || phone.trim() === '') return false;
        // Простая проверка - должно быть 10-11 цифр
        const cleanPhone = phone.replace(/\D/g, '');
        return cleanPhone.length >= 10 && cleanPhone.length <= 11;
    }

    /**
     * Валидация телефона при потере фокуса
     */
    validatePhone(event) {
        const input = event.target;
        const isValid = this.isValidPhone(input.value);
        
        this.updateValidationState(input, isValid);
        
        if (!isValid && input.value.length > 0) {
            this.showError(input, 'Введите корректный номер телефона');
        } else {
            this.clearError(input);
        }
    }

    /**
     * Ограничение ввода для телефонных полей - ПОЛНОСТЬЮ ОТКЛЮЧЕНО
     */
    restrictPhoneInput(event) {
        console.log('Keydown event:', event.key, 'on input:', event.target.id);
        // Полностью убираем все ограничения
        return true;
    }

    /**
     * Настройка валидации email
     */
    setupEmailValidation() {
        const emailInputs = document.querySelectorAll('input[type="email"], input[placeholder*="@"], input[name*="email"]');
        
        emailInputs.forEach(input => {
            input.addEventListener('blur', (e) => this.validateEmail(e));
            input.addEventListener('input', (e) => this.clearError(e.target));
        });
    }

    /**
     * Валидация email
     */
    validateEmail(event) {
        const input = event.target;
        const email = input.value;
        const isValid = this.isValidEmail(email);
        
        this.updateValidationState(input, isValid);
        
        if (!isValid && email.length > 0) {
            this.showError(input, 'Введите корректный email адрес');
        } else {
            this.clearError(input);
        }
    }

    /**
     * Проверка корректности email
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Настройка валидации имен
     */
    setupNameValidation() {
        const nameInputs = document.querySelectorAll('input[name*="name"], input[placeholder*="имя"], input[placeholder*="Имя"]');
        
        nameInputs.forEach(input => {
            input.addEventListener('input', (e) => this.formatName(e));
            input.addEventListener('blur', (e) => this.validateName(e));
        });
    }

    /**
     * Форматирование имени (первые буквы заглавные)
     */
    formatName(event) {
        const input = event.target;
        let value = input.value;
        
        // Убираем цифры и лишние символы
        value = value.replace(/[0-9]/g, '');
        
        // Делаем первые буквы слов заглавными
        value = value.replace(/\b\w/g, char => char.toUpperCase());
        
        input.value = value;
    }

    /**
     * Валидация имени
     */
    validateName(event) {
        const input = event.target;
        const name = input.value.trim();
        const isValid = name.length >= 2 && /^[а-яёa-z\s-]+$/i.test(name);
        
        this.updateValidationState(input, isValid);
        
        if (!isValid && name.length > 0) {
            this.showError(input, 'Имя должно содержать минимум 2 буквы');
        } else {
            this.clearError(input);
        }
    }

    /**
     * Настройка валидации форм при отправке
     */
    setupFormSubmission() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => this.validateForm(e));
        });
    }

    /**
     * Валидация всей формы перед отправкой
     */
    validateForm(event) {
        const form = event.target;
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (input.type === 'tel') {
                if (!this.isValidPhone(input.value)) {
                    this.showError(input, 'Введите корректный номер телефона');
                    isValid = false;
                }
            } else if (input.type === 'email') {
                if (!this.isValidEmail(input.value)) {
                    this.showError(input, 'Введите корректный email');
                    isValid = false;
                }
            } else if (input.value.trim() === '') {
                this.showError(input, 'Это поле обязательно для заполнения');
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
            // Прокрутка к первой ошибке
            const firstError = form.querySelector('.error-message');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }

    /**
     * Обновление визуального состояния поля
     */
    updateValidationState(input, isValid) {
        input.classList.remove('border-red-500', 'border-green-500');
        
        if (input.value.length > 0) {
            if (isValid) {
                input.classList.add('border-green-500');
            } else {
                input.classList.add('border-red-500');
            }
        }
    }

    /**
     * Показ ошибки валидации
     */
    showError(input, message) {
        this.clearError(input);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message text-red-500 text-sm mt-1';
        errorDiv.textContent = message;
        
        input.parentNode.insertBefore(errorDiv, input.nextSibling);
        input.classList.add('border-red-500');
    }

    /**
     * Очистка ошибки валидации
     */
    clearError(input) {
        const errorMessage = input.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
        input.classList.remove('border-red-500');
    }
}

// Инициализация валидатора
const formValidator = new FormValidator();

// Экспорт для использования в других скриптах
window.FormValidator = FormValidator;
window.formValidator = formValidator;