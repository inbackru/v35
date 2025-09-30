// Consolidated JavaScript for ClickBack Real Estate Platform
// Auto-generated from multiple page-specific scripts

// Utility function to safely add event listeners
function safeAddEventListener(selector, event, handler) {
    const element = document.querySelector(selector);
    if (element) {
        element.addEventListener(event, handler);
    }
}

function safeAddEventListenerAll(selector, event, handler) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        if (element) {
            element.addEventListener(event, handler);
        }
    });
}

// Main functionality
document.addEventListener('DOMContentLoaded', function() {
    // Loading animation
    const loadingAnimation = document.querySelector('.loading-animation');
    if (loadingAnimation) {
        setTimeout(() => {
            loadingAnimation.style.display = 'none';
        }, 2000);
    }

    // Typewriter effect
    const typewriter = document.getElementById('typewriter');
    if (typewriter) {
        const texts = ['с кэшбеком до 500 000 ₽', 'с выгодой до 10%', 'от надежных застройщиков'];
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;

        function type() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                typewriter.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typewriter.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
            }

            let typeSpeed = 100;
            if (isDeleting) typeSpeed /= 2;

            if (!isDeleting && charIndex === currentText.length) {
                typeSpeed = 2000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                typeSpeed = 500;
            }

            setTimeout(type, typeSpeed);
        }
        type();
    }

    // Price calculator
    const priceSlider = document.getElementById('price');
    const priceInput = document.getElementById('price-input');
    const percentSlider = document.getElementById('percent');
    const percentInput = document.getElementById('percent-input');
    const calculateBtn = document.getElementById('calculate-btn');
    const resultElement = document.getElementById('result');

    if (priceSlider && priceInput) {
        priceSlider.addEventListener('input', function() {
            priceInput.value = this.value;
            calculateCashback();
        });

        priceInput.addEventListener('input', function() {
            if (parseInt(this.value) > 50000000) this.value = 50000000;
            if (parseInt(this.value) < 1000000) this.value = 1000000;
            priceSlider.value = this.value;
            calculateCashback();
        });
    }

    if (percentSlider && percentInput) {
        percentSlider.addEventListener('input', function() {
            percentInput.value = this.value;
            calculateCashback();
        });

        percentInput.addEventListener('input', function() {
            if (parseFloat(this.value) > 5) this.value = 5;
            if (parseFloat(this.value) < 1) this.value = 1;
            percentSlider.value = this.value;
            calculateCashback();
        });
    }

    if (calculateBtn) {
        calculateBtn.addEventListener('click', calculateCashback);
    }

    function formatCurrency(num) {
        return new Intl.NumberFormat('ru-RU').format(num) + ' ₽';
    }

    function calculateCashback() {
        if (!priceInput || !percentInput || !resultElement) return;
        
        const price = parseInt(priceInput.value) || 0;
        const percent = parseFloat(percentInput.value) || 0;
        const cashback = Math.round(price * percent / 100);
        resultElement.textContent = formatCurrency(cashback);
    }

    // Search functionality
    const searchInput = document.querySelector('input[placeholder*="Поиск"]');
    const searchButton = document.querySelector('button');
    
    if (searchInput && searchButton) {
        searchButton.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query) {
                window.location.href = `/properties.php?search=${encodeURIComponent(query)}`;
            }
        });

        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchButton.click();
            }
        });
    }

    // FAQ toggles
    window.toggleFAQ = function(id) {
        const content = document.getElementById(`faq-content-${id}`);
        const icon = document.getElementById(`faq-icon-${id}`);
        if (content) content.classList.toggle('hidden');
        if (icon) icon.classList.toggle('rotate-180');
    };

    // Dropdown functionality
    window.toggleDropdown = function(element) {
        const dropdown = element.closest('.dropdown');
        if (!dropdown) return;
        
        const menu = dropdown.querySelector('.dropdown-menu');
        if (!menu) return;

        // Close other dropdowns
        document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
            if (openMenu !== menu) {
                openMenu.classList.remove('open');
            }
        });

        menu.classList.toggle('open');
    };

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
                menu.classList.remove('open');
            });
        }
    });

    // Modal functionality
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    });

    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('[data-mobile-menu]');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
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
        document.getElementById('toggleFilters').addEventListener('click', function() {
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
		
	
// Toggle mobile filters dropdowns
document.querySelectorAll('.dropdown-btn').forEach(button => {
    button.addEventListener('click', function() {
        const menu = this.nextElementSibling;
        menu.classList.toggle('hidden');
    });
});

// Toggle desktop filters panel
document.getElementById('toggleFilters').addEventListener('click', function() {
    const filtersPanel = document.getElementById('filtersPanel');
    filtersPanel.classList.toggle('hidden');
});

// Toggle advanced parameters
document.getElementById('toggleAdvanced').addEventListener('click', function() {
    const advancedParams = document.getElementById('advancedParams');
    advancedParams.classList.toggle('hidden');
    
    // Change button text/icon
    const icon = this.querySelector('i');
    const isHidden = advancedParams.classList.contains('hidden');
    icon.className = isHidden ? 'fas fa-plus-circle mr-2' : 'fas fa-minus-circle mr-2';
    this.innerHTML = isHidden ? '<i class="fas fa-plus-circle mr-2"></i> Дополнительные параметры' : '<i class="fas fa-minus-circle mr-2"></i> Скрыть параметры';
});

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const button = dropdown.querySelector('.dropdown-btn');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (!dropdown.contains(event.target)) {
            menu.classList.add('hidden');
        }
    });
});
