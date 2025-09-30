// Lightweight form validation
(function() {
    'use strict';

    // Simple email validation
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Simple phone validation (Russian format)
    function isValidPhone(phone) {
        return /^\+7\s?\(\d{3}\)\s?\d{3}-?\d{2}-?\d{2}$/.test(phone);
    }

    // Form validation
    function validateForm(form) {
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;

        inputs.forEach(input => {
            const value = input.value.trim();
            
            if (!value) {
                input.classList.add('error');
                isValid = false;
            } else if (input.type === 'email' && !isValidEmail(value)) {
                input.classList.add('error');
                isValid = false;
            } else if (input.type === 'tel' && !isValidPhone(value)) {
                input.classList.add('error');
                isValid = false;
            } else {
                input.classList.remove('error');
            }
        });

        return isValid;
    }

    // Initialize validation
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
        console.log('Form validation initialized');
    });
})();