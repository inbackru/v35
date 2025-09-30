
	
        // Typewriter animation
        function setupTypewriter() {
            const el = document.getElementById('typewriter');
            const changingTexts = [
                "кэшбеком до 5%",
                "платежами в подарок",
                "выгодой до 500 000 ₽"
            ];
            
            let part = '';
            const staticPrefix = 'с ';
            let textIndex = 0;
            let isDeleting = false;
            let typingSpeed = 100;
            let deletingSpeed = 50;
            let pauseAfterType = 2000;
            let pauseAfterDelete = 500;

            function tick() {
                const fullChangingText = changingTexts[textIndex];
                
                if (isDeleting) {
                    part = fullChangingText.substring(0, part.length - 1);
                    el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
                    
                    if (part === '') {
                        isDeleting = false;
                        textIndex = (textIndex + 1) % changingTexts.length;
                        setTimeout(tick, pauseAfterDelete);
                    } else {
                        setTimeout(tick, deletingSpeed);
                    }
                } else {
                    part = fullChangingText.substring(0, part.length + 1);
                    el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
                    
                    if (part === fullChangingText) {
                        isDeleting = true;
                        setTimeout(tick, pauseAfterType);
                    } else {
                        setTimeout(tick, typingSpeed);
                    }
                }
            }

            el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
            setTimeout(tick, 1000); // Start animation after 1 second
        }

        // Loading animation
        window.addEventListener('load', function() {
            setTimeout(function() {
                document.querySelector('.loading-animation').style.display = 'none';
            }, 2000);
        });

        // Mobile menu toggle
        function toggleMobileMenu() {
            const menu = document.getElementById('mobileMenu');
            menu.classList.toggle('hidden');
            // Close all submenus when closing main menu
            if (menu.classList.contains('hidden')) {
                document.querySelectorAll('.mobile-submenu').forEach(submenu => {
                    submenu.classList.add('hidden');
                });
            }
        }

        // Mobile submenu toggle
        function toggleSubMenu(id) {
            const submenu = document.getElementById(id);
            submenu.classList.toggle('hidden');
        }

        // Modal functions
        function openApplicationModal() {
            document.getElementById('applicationModal').classList.remove('hidden');
        }

        function openLoginModal() {
            document.getElementById('loginModal').classList.remove('hidden');
        }

        function openRegisterModal() {
            closeModal('loginModal');
            document.getElementById('registerModal').classList.remove('hidden');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.add('hidden');
        }

        // Login/logout simulation
        function loginUser() {
            closeModal('loginModal');
            document.getElementById('accountModal').classList.remove('hidden');
        }

        function logoutUser() {
            closeModal('accountModal');
        }

        // Toggle filters panel
        const el_toggleFilters = document.getElementById("toggleFilters");
if (el_toggleFilters) el_toggleFilters.addEventListener('click', function() {
            const panel = document.getElementById('filtersPanel');
            panel.classList.toggle('hidden');
            this.querySelector('i').classList.toggle('fa-sliders-h');
            this.querySelector('i').classList.toggle('fa-times');
        });

        // Initialize all carousels
        function initCarousels() {
            document.querySelectorAll('.carousel').forEach(carousel => {
                const inner = carousel.querySelector('.carousel-inner');
                const items = inner.querySelectorAll('.carousel-item');
                const dots = carousel.querySelectorAll('.carousel-dot');
                
                // Set initial active dot
                dots[0].classList.add('active');
                
                // Clone first and last items for infinite scroll
                const firstClone = inner.firstElementChild.cloneNode(true);
                const lastClone = inner.lastElementChild.cloneNode(true);
                inner.appendChild(firstClone);
                inner.insertBefore(lastClone, inner.firstElementChild);
                
                let currentIndex = 1;
                const itemWidth = items[0].clientWidth;
                inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                
                // Auto-rotate every 5 seconds
                let interval = setInterval(nextSlide, 5000);
                
                function nextSlide() {
                    currentIndex++;
                    inner.style.transition = 'transform 0.5s ease-in-out';
                    inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    updateDots();
                }
                
                function prevSlide() {
                    currentIndex--;
                    inner.style.transition = 'transform 0.5s ease-in-out';
                    inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    updateDots();
                }
                
                function updateDots() {
                    let realIndex = currentIndex;
                    if (currentIndex === 0) realIndex = items.length - 2;
                    if (currentIndex === items.length - 1) realIndex = 1;
                    
                    dots.forEach((dot, index) => {
                        dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
                    });
                }
                
                // Reset position when reaching clones
                inner.addEventListener('transitionend', () => {
                    if (currentIndex === 0) {
                        inner.style.transition = 'none';
                        currentIndex = items.length - 2;
                        inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    } else if (currentIndex === items.length - 1) {
                        inner.style.transition = 'none';
                        currentIndex = 1;
                        inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    }
                });
                
                // Navigation buttons
                if (carousel.querySelector('.carousel-next')) {
                    carousel.querySelector('.carousel-next').addEventListener('click', () => {
                        clearInterval(interval);
                        nextSlide();
                        interval = setInterval(nextSlide, 5000);
                    });
                }
                
                if (carousel.querySelector('.carousel-prev')) {
                    carousel.querySelector('.carousel-prev').addEventListener('click', () => {
                        clearInterval(interval);
                        prevSlide();
                        interval = setInterval(nextSlide, 5000);
                    });
                }
                
                // Dot navigation
                dots.forEach((dot, index) => {
                    dot.addEventListener('click', () => {
                        clearInterval(interval);
                        currentIndex = index + 1;
                        inner.style.transition = 'transform 0.5s ease-in-out';
                        inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                        updateDots();
                        interval = setInterval(nextSlide, 5000);
                    });
                });
            });
        }
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            setupDropdowns();
            setupTypewriter();
            initCarousels();
            
            // Filter buttons functionality
            document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    if (this.classList.contains('active')) {
                        this.classList.remove('active');
                    } else {
                        // For radio-like behavior (only one active in group)
                        if (btn.classList.contains('class-filter-btn')) {
                            btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
                        }
                        this.classList.add('active');
                    }
                    updateSelectedFilters();
                });
            });
            
            function updateSelectedFilters() {
                const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
                if (activeFilters.length > 0) {
                    document.getElementById('selectedFilters').classList.remove('hidden');
                } else {
                    document.getElementById('selectedFilters').classList.add('hidden');
                }
            }
        });

        // Calculator functionality
        const priceRange = document.getElementById('priceRange');
        const priceValue = document.getElementById('priceValue');
        const downPaymentRange = document.getElementById('downPaymentRange');
        const downPaymentValue = document.getElementById('downPaymentValue');
        const termRange = document.getElementById('termRange');
        const termValue = document.getElementById('termValue');
        const cashbackAmount = document.getElementById('cashbackAmount');
        const monthlyPayment = document.getElementById('monthlyPayment');

        function updateCalculator() {
            const price = parseInt(priceRange.value);
            const downPayment = parseInt(downPaymentRange.value);
            const downPaymentPercent = Math.round((downPayment / price) * 100);
            const term = parseInt(termRange.value);
            const cashbackPercent = 2.5; // Fixed at 2.5%
            
            // Format values
            priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
            downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
            termValue.textContent = term + ' лет';
            
            // Calculate cashback amount
            const cashback = price * cashbackPercent / 100;
            cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
            
            // Calculate monthly payment at 6% rate (family mortgage)
            const loanAmount = price - downPayment;
            const monthlyRate = 0.06 / 12; // 6% annual rate
            const payments = term * 12;
            const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
            monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
        }

        // Add event listeners
        priceRange.addEventListener('input', updateCalculator);
        downPaymentRange.addEventListener('input', updateCalculator);
        termRange.addEventListener('input', updateCalculator);
        cashbackRange.addEventListener('input', updateCalculator);

        // Initialize calculator
        updateCalculator();

        // Property carousel functionality
        document.querySelectorAll('.carousel').forEach(carousel => {
            const inner = carousel.querySelector('.carousel-inner');
            const prev = carousel.querySelector('.carousel-prev');
            const next = carousel.querySelector('.carousel-next');
            const items = carousel.querySelectorAll('img');
            let currentIndex = 0;
            
            function updateCarousel() {
                inner.style.transform = `translateX(-${currentIndex * 100}%)`;
            }
            
            prev.addEventListener('click', () => {
                currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
                updateCarousel();
            });
            
            next.addEventListener('click', () => {
                currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                updateCarousel();
            });
            
            // Auto-rotate every 5 seconds
            setInterval(() => {
                currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                updateCarousel();
            }, 5000);
        });

        // Close modal when clicking outside
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.classList.add('hidden');
                }
            });
        });
    </script>
    
    <script>
        // Dropdown menu functionality
        function setupDropdowns() {
            document.querySelectorAll('.dropdown-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const menu = this.nextElementSibling;
                    const isOpen = menu.classList.contains('open');
                    
                    // Close all other dropdowns
                    document.querySelectorAll('.dropdown-menu.open').forEach(m => {
                        if (m !== menu) {
                            m.classList.remove('open');
                            m.previousElementSibling.classList.remove('open');
                        }
                    });

                    // Toggle current dropdown
                    menu.classList.toggle('open');
                    this.classList.toggle('open');
                });
            });

            // Close dropdowns when clicking outside
            document.addEventListener('click', function() {
                document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
                    menu.classList.remove('open');
                    menu.previousElementSibling.classList.remove('open');
                });
            });
        }

        // Footer menu functionality
        function toggleFooterMenu(header) {
            if (window.innerWidth >= 768) return;
            
            const group = header.closest('.footer-menu-group');
            const submenu = group.querySelector('.footer-submenu');
            const icon = header.querySelector('svg');
            
            // Toggle submenu
            submenu.classList.toggle('hidden');
            
            // Rotate icon
            icon.classList.toggle('rotate-180');
        }
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    menu.classList.remove('open');
                    menu.previousElementSibling.classList.remove('open');
                });
            }
        });

        // Initialize all carousels on page
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.carousel').forEach(carousel => {
                const inner = carousel.querySelector('.carousel-inner');
                const items = inner.querySelectorAll('.carousel-item');
                const dots = carousel.querySelectorAll('.carousel-dot');
                const prevBtn = carousel.querySelector('.carousel-prev');
                const nextBtn = carousel.querySelector('.carousel-next');
                
                let currentIndex = 0;
                
                function updateCarousel() {
                    inner.style.transform = `translateX(-${currentIndex * 100}%)`;
                    
                    // Update dots
                    dots.forEach((dot, index) => {
                        dot.classList.toggle('active', index === currentIndex);
                    });
                }
                
                // Navigation buttons
                if (prevBtn) {
                    prevBtn.addEventListener('click', () => {
                        currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
                        updateCarousel();
                    });
                }
                
                if (nextBtn) {
                    nextBtn.addEventListener('click', () => {
                        currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                        updateCarousel();
                    });
                }
                
                // Dot navigation
                dots.forEach((dot, index) => {
                    dot.addEventListener('click', () => {
                        currentIndex = index;
                        updateCarousel();
                    });
                });
                
                // Auto-rotate every 5 seconds
                let interval = setInterval(() => {
                    currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                    updateCarousel();
                }, 5000);
                
                // Pause on hover
                carousel.addEventListener('mouseenter', () => clearInterval(interval));
                carousel.addEventListener('mouseleave', () => {
                    interval = setInterval(() => {
                        currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                        updateCarousel();
                    }, 5000);
                });
            });
        });
		
		 // Telegram bot configuration
        const TELEGRAM_BOT_TOKEN = '7210651587:AAEx05tkpKveOIqPpDtwXOY8UGkhwYeCxmE';
        const TELEGRAM_CHAT_ID = '730764738';
        const EMAIL_API_URL = 'YOUR_EMAIL_SERVICE_ENDPOINT'; // For example, a serverless function URL

        document.addEventListener('DOMContentLoaded', function() {
            // Modal elements
            const modal = document.getElementById('quiz-modal');
            const backdrop = document.getElementById('modal-backdrop');
            const openBtns = document.querySelectorAll('.open-quiz');
            const modalContainer = document.getElementById('modal-container');

            // Open modal function
            function openModal() {
                modalContainer.classList.remove('hidden');
                backdrop.classList.remove('hidden');
                modal.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
                
                // Reset form if needed
                goToStep(0);
                
                // Trigger animation
                setTimeout(() => {
                    modal.classList.add('show');
                }, 10);
            }

            function closeModal() {
                modal.classList.remove('show');
                setTimeout(() => {
                    modalContainer.classList.add('hidden');
                    backdrop.classList.add('hidden');
                    modal.classList.add('hidden');
                    document.body.style.overflow = '';
                }, 300);
            }

            // Close modal function
            function closeModal() {
                modal.classList.remove('show');
                backdrop.classList.remove('show');
                setTimeout(() => {
                    modalContainer.classList.add('hidden');
                    backdrop.classList.add('hidden');
                    modal.classList.add('hidden');
                    document.body.style.overflow = '';
                }, 300);
            }

            // Добавляем обработчик для кнопки закрытия
            const el_close-modal = document.getElementById("close-modal");
if (el_close-modal) el_close-modal.addEventListener('click', closeModal);

            // Add swipe down to close on mobile
            let touchStartY = 0;
            modal.addEventListener('touchstart', (e) => {
                touchStartY = e.touches[0].clientY;
            }, {passive: true});

            modal.addEventListener('touchmove', (e) => {
                const touchY = e.touches[0].clientY;
                const touchDiff = touchY - touchStartY;
                
                if (touchDiff > 50 && window.scrollY <= 0) {
                    closeModal();
                }
            }, {passive: true});

            // Добавляем обработчик свайпа вниз для закрытия
            let startY = 0;
            modal.addEventListener('touchstart', (e) => {
                startY = e.touches[0].clientY;
            }, {passive: true});

            modal.addEventListener('touchmove', (e) => {
                const y = e.touches[0].clientY;
                if (y - startY > 100 && window.scrollY === 0) {
                    closeModal();
                }
            }, {passive: true});

            // Event listeners for modal (for all buttons)
            openBtns.forEach(btn => {
                btn.addEventListener('click', openModal);
            });
            backdrop.addEventListener('click', closeModal);

            // Close modal when clicking outside content
            modalContainer.addEventListener('click', function(e) {
                if (e.target === modalContainer) {
                    closeModal();
                }
            });

            // Close modal on Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && !modalContainer.classList.contains('hidden')) {
                    closeModal();
                }
            });



            const form = document.getElementById('quiz-form');
            const steps = document.querySelectorAll('.step');
            const nextButtons = document.querySelectorAll('.next-step');
            const prevButtons = document.querySelectorAll('.prev-step');
            const optionCards = document.querySelectorAll('.option-card');
            const progressFill = document.getElementById('progress');
            const currentStepDisplay = document.getElementById('current-step');
            
            let currentStep = 0;
            const totalSteps = steps.length - 1; // минус 1, так как последний шаг - благодарность
            
            // Инициализация данных формы
            const formData = {
                districts: null,
                rooms: null,
                completion: null,
                payment: null,
                name: null,
                phone: null,
                email: null
            };
            
            // Переключение шагов вперед
            nextButtons.forEach(button => {
                button.addEventListener('click', function() {
                    if (validateStep(currentStep)) {
                        goToStep(currentStep + 1);
                    }
                });
            });
            
            // Переключение шагов назад
            prevButtons.forEach(button => {
                button.addEventListener('click', function() {
                    goToStep(currentStep - 1);
                });
            });
            
            // Выбор опций
            optionCards.forEach(card => {
                card.addEventListener('click', function() {
                    const stepId = this.closest('.step').id;
                    const value = this.getAttribute('data-value');
                    
                    // Сброс выделения всех карточек в текущем шаге
                    const allCardsInStep = this.closest('.step').querySelectorAll('.option-card');
                    allCardsInStep.forEach(c => c.classList.remove('selected'));
                    
                    // Выделение выбранной карточки
                    this.classList.add('selected');
                    
                    // Сохранение выбранного значения
                    switch(stepId) {
                        case 'step-1':
                            formData.districts = value;
                            break;
                        case 'step-2':
                            formData.rooms = value;
                            break;
                        case 'step-3':
                            formData.completion = value;
                            break;
                        case 'step-4':
                            formData.payment = value;
                            break;
                    }
                });
            });
            
            // Валидация шага
            function validateStep(stepIndex) {
                switch(stepIndex) {
                    case 0:
                        if (!formData.districts) {
                            alert('Пожалуйста, выберите количество районов');
                            return false;
                        }
                        return true;
                    case 1:
                        if (!formData.rooms) {
                            alert('Пожалуйста, выберите количество комнат');
                            return false;
                        }
                        return true;
                    case 2:
                        if (!formData.completion) {
                            alert('Пожалуйста, выберите срок сдачи');
                            return false;
                        }
                        return true;
                    case 3:
                        if (!formData.payment) {
                            alert('Пожалуйста, выберите способ оплаты');
                            return false;
                        }
                        return true;
                    case 4:
                        const name = document.getElementById('name').value;
                        const phone = document.getElementById('phone').value;
                        const consent = document.getElementById('consent').checked;
                        
                        if (!name || !phone) {
                            alert('Пожалуйста, заполните обязательные поля');
                            return false;
                        }
                        
                        if (!consent) {
                            alert('Необходимо согласие на обработку данных');
                            return false;
                        }
                        
                        formData.name = name;
                        formData.phone = phone;
                        formData.email = document.getElementById('email').value;
                        return true;
                    default:
                        return true;
                }
            }
            
            // Переход к конкретному шагу
            function goToStep(stepIndex) {
                if (stepIndex < 0 || stepIndex > totalSteps) return;
                
                // Скрыть текущий шаг
                steps[currentStep].classList.remove('active');
                
                // Показать новый шаг
                steps[stepIndex].classList.add('active');
                
                // Обновить текущий шаг
                currentStep = stepIndex;
                
                // Обновить прогресс бар
                const progressPercent = (stepIndex / totalSteps) * 100;
                progressFill.style.width = `${progressPercent}%`;
                
                // Обновить отображение текущего шага
                currentStepDisplay.textContent = stepIndex + 1;
                
                // Прокрутить вверх
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            
            // Обработка отправки формы
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const submitBtn = document.getElementById('submit-btn');
                const submitText = document.getElementById('submit-text');
                const submitSpinner = document.getElementById('submit-spinner');
                
                // Показать индикатор загрузки
                submitBtn.disabled = true;
                submitText.classList.add('hidden');
                submitSpinner.classList.remove('hidden');
                
                if (validateStep(currentStep)) {
                    // Собираем все данные формы
                    const formData = {
                        districts: getSelectedOptionText('step-1') || 'Не указано',
                        rooms: getSelectedOptionText('step-2') || 'Не указано',
                        completion: getSelectedOptionText('step-3') || 'Не указано',
                        payment: getSelectedOptionText('step-4') || 'Не указано',
                        name: document.getElementById('name').value,
                        phone: document.getElementById('phone').value,
                        email: document.getElementById('email').value || 'Не указано'
                    };

                    // Формируем сообщение для Telegram
                    const telegramMessage = `
📌 *Новая заявка на подбор жилья*:
🏙 *Районы*: ${formData.districts}
🏠 *Комнат*: ${formData.rooms}
📅 *Срок сдачи*: ${formData.completion}
💳 *Способ оплаты*: ${formData.payment}
👤 *Имя*: ${formData.name}
📞 *Телефон*: ${formData.phone}
📧 *Email*: ${formData.email}
                    `;

                    // Отправляем в Telegram
                    axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
                        chat_id: TELEGRAM_CHAT_ID,
                        text: telegramMessage,
                        parse_mode: 'Markdown'
                    })
                    .then(() => {
                        console.log('Сообщение отправлено в Telegram');
                    })
                    .catch(error => {
                        console.error('Ошибка отправки в Telegram:', error);
                    });

                    // Отправляем на email (через серверный эндпоинт)
                    axios.post(EMAIL_API_URL, {
                        subject: 'Новая заявка на подбор жилья',
                        text: telegramMessage,
                        to: 'your@email.com', // Адрес для получения заявок
                        formData: formData
                    })
                    .then(() => {
                        console.log('Сообщение отправлено на email');
                    })
                    .catch(error => {
                        console.error('Ошибка отправки на email:', error);
                    });

                    // Перейти к шагу благодарности
                    goToStep(totalSteps);
                    
                    // Восстановить кнопку
                    submitBtn.disabled = false;
                    submitText.classList.remove('hidden');
                    submitSpinner.classList.add('hidden');
                }
            });

            // Функция для получения текста выбранной опции
            function getSelectedOptionText(stepId) {
                const step = document.getElementById(stepId);
                if (!step) return null;
                const selectedCard = step.querySelector('.option-card.selected');
                if (!selectedCard) return null;
                return selectedCard.querySelector('h3').textContent;
            }
            
            // Маска для телефона
            const phoneInput = document.getElementById('phone');
            phoneInput.addEventListener('input', function(e) {
                let x = e.target.value.replace(/\D/g, '').match(/(\d{0,1})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})/);
                e.target.value = !x[2] ? x[1] : x[1] + ' (' + x[2] + ') ' + x[3] + (x[4] ? '-' + x[4] : '') + (x[5] ? '-' + x[5] : '');
            });
        });
		
document.addEventListener('DOMContentLoaded', setupTypewriter);
window.onload = setupTypewriter;
