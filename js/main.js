// Main JavaScript for Inback Real Estate Platform

// Presentation page guard - skip main.js on presentation pages
(function() {
    if (window.SKIP_MAIN_JS || document.documentElement?.dataset.page === 'presentation' || document.body?.dataset.page === 'presentation') {
        console.warn('🚫 Skipping main.js (js/main.js) on presentation page');
        return;
    }

// Loading animation
window.addEventListener('load', function() {
    setTimeout(function() {
        const loadingAnimation = document.querySelector('.loading-animation');
        if (loadingAnimation) {
            loadingAnimation.style.display = 'none';
        }
    }, 2000);
});

// Dropdown functionality
function toggleDropdown(button) {
    const dropdown = button.closest('.dropdown');
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
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
            menu.classList.remove('open');
        });
    }
});

// Mobile menu functions
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        menu.classList.toggle('hidden');
        // Close all submenus when closing main menu
        if (menu.classList.contains('hidden')) {
            document.querySelectorAll('.mobile-submenu').forEach(submenu => {
                submenu.classList.add('hidden');
            });
        }
    }
}

function toggleSubMenu(id) {
    const submenu = document.getElementById(id);
    if (submenu) {
        submenu.classList.toggle('hidden');
    }
}

// Modal functions
function openApplicationModal() {
    const modal = document.getElementById('applicationModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function openLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function openRegisterModal() {
    closeModal('loginModal');
    const modal = document.getElementById('registerModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Close modals when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('fixed') && e.target.classList.contains('inset-0')) {
        e.target.classList.add('hidden');
    }
});

// City change function
function changeCity(cityName) {
    console.log('Changing city to:', cityName);
    // Here you would implement city change logic
    // For now, we'll just update the dropdown button text
    const cityButton = document.querySelector('.dropdown-btn');
    if (cityButton && cityButton.textContent.includes('Краснодар')) {
        cityButton.childNodes[2].textContent = cityName;
    }
}

// Footer menu toggle for mobile
function toggleFooterMenu(header) {
    if (window.innerWidth >= 768) return;
    
    const group = header.closest('.footer-menu-group');
    const submenu = group.querySelector('.footer-submenu');
    const icon = header.querySelector('svg');
    
    if (submenu) {
        submenu.classList.toggle('hidden');
    }
    if (icon) {
        icon.classList.toggle('rotate-180');
    }
}

// Typewriter animation
function setupTypewriter() {
    const el = document.getElementById('typewriter');
    if (!el) return;
    
    const changingTexts = [
        "до 500 000 ₽",
        "до 10% стоимости",
        "гарантированно"
    ];
    
    let part = '';
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
            el.innerHTML = '<span class="typewriter-text">' + part + '</span>';
            
            if (part === '') {
                isDeleting = false;
                textIndex = (textIndex + 1) % changingTexts.length;
                setTimeout(tick, pauseAfterDelete);
            } else {
                setTimeout(tick, deletingSpeed);
            }
        } else {
            part = fullChangingText.substring(0, part.length + 1);
            el.innerHTML = '<span class="typewriter-text">' + part + '</span>';
            
            if (part === fullChangingText) {
                isDeleting = true;
                setTimeout(tick, pauseAfterType);
            } else {
                setTimeout(tick, typingSpeed);
            }
        }
    }

    el.innerHTML = '<span class="typewriter-text">' + changingTexts[0].substring(0, 1) + '</span>';
    setTimeout(tick, 1000);
}

// Price formatter
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Setup typewriter if element exists
    if (document.getElementById('typewriter')) {
        setupTypewriter();
    }
    
    // Add event listeners to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Here you would handle form submission
            console.log('Form submitted:', this);
            
            // Show success message
            alert('Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в течение 15 минут.');
            
            // Close modal if form is in modal
            const modal = this.closest('.fixed');
            if (modal) {
                modal.classList.add('hidden');
            }
        });
    });
    
    // Add smooth scrolling to anchor links
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
    
    // Initialize property cards hover effects
    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Search functionality
    const searchInputs = document.querySelectorAll('input[type="text"][placeholder*="Поиск"]');
    searchInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    });
});

// Carousel functionality
function initCarousels() {
    document.querySelectorAll('.carousel').forEach(carousel => {
        const inner = carousel.querySelector('.carousel-inner');
        const items = inner ? inner.querySelectorAll('.carousel-item') : [];
        const dots = carousel.querySelectorAll('.carousel-dot');
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');
        
        if (items.length === 0) return;
        
        let currentIndex = 0;
        
        function updateCarousel() {
            if (inner) {
                inner.style.transform = `translateX(-${currentIndex * 100}%)`;
            }
            
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentIndex);
            });
        }
        
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
        
        carousel.addEventListener('mouseenter', () => clearInterval(interval));
        carousel.addEventListener('mouseleave', () => {
            interval = setInterval(() => {
                currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                updateCarousel();
            }, 5000);
        });
        
        // Initialize
        updateCarousel();
    });
}

// Initialize carousels when DOM is loaded
document.addEventListener('DOMContentLoaded', initCarousels);

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// UNIFIED COMPARISON SYSTEM - Compatible with properties page
window.ComparisonManager = window.ComparisonManager || {
    // Get current comparison data
    getData: function() {
        return JSON.parse(localStorage.getItem('comparison-data') || '{"properties": [], "complexes": []}');
    },
    
    // Save comparison data
    saveData: function(data) {
        localStorage.setItem('comparison-data', JSON.stringify(data));
        this.updateCounters();
    },
    
    // Update all counters
    updateCounters: function() {
        const data = this.getData();
        const totalCount = data.properties.length + data.complexes.length;
        
        // Update global comparison counter in header
        const globalCounter = document.getElementById('comparison-count');
        if (globalCounter) {
            globalCounter.textContent = totalCount;
            globalCounter.style.display = totalCount > 0 ? 'flex' : 'none';
        }
        
        // Update dashboard counters if available
        const propertiesCount = document.getElementById('properties-tab-count');
        if (propertiesCount) {
            propertiesCount.textContent = data.properties.length;
        }
        
        const complexesCount = document.getElementById('complexes-tab-count');
        if (complexesCount) {
            complexesCount.textContent = data.complexes.length;
        }
    },
    
    // Show notification message
    showMessage: function(message, type = 'info') {
        if (typeof showNotification === 'function') {
            showNotification(message, type);
        } else {
            console.log(`[${type}] ${message}`);
        }
    }
};

// Legacy compatibility functions
let comparisonData = { properties: [], complexes: [] };

function loadComparisonFromStorage() {
    if (window.ComparisonManager) {
        comparisonData = window.ComparisonManager.getData();
        window.ComparisonManager.updateCounters();
    }
}

function saveComparisonToStorage() {
    if (window.ComparisonManager) {
        window.ComparisonManager.saveData(comparisonData);
    }
}

function updateComparisonCounts() {
    if (window.ComparisonManager) {
        window.ComparisonManager.updateCounters();
    }
}

// УДАЛЕНА СТАРАЯ ФУНКЦИЯ addToComparison - ТЕПЕРЬ ИСПОЛЬЗУЕТСЯ PostgreSQL РЕАЛИЗАЦИЯ ИЗ properties-comparison-fix.js

function removeFromComparison(type, id) {
    const data = window.ComparisonManager.getData();
    const idStr = id.toString();
    
    if (type === 'property') {
        data.properties = data.properties.filter(pid => pid !== idStr);
        window.ComparisonManager.showMessage('Квартира удалена из сравнения', 'info');
    } else if (type === 'complex') {
        data.complexes = data.complexes.filter(cid => cid !== idStr);
        window.ComparisonManager.showMessage('ЖК удален из сравнения', 'info');
    }
    
    window.ComparisonManager.saveData(data);
    comparisonData = data;
}

function isInComparison(type, id) {
    const data = window.ComparisonManager.getData();
    const idStr = id.toString();
    
    if (type === 'property') {
        return data.properties.includes(idStr);
    } else if (type === 'complex') {
        return data.complexes.includes(idStr);
    }
    return false;
}

function clearAllComparisons() {
    const emptyData = { properties: [], complexes: [] };
    window.ComparisonManager.saveData(emptyData);
    comparisonData = emptyData;
    
    if (typeof showNotification === 'function') {
        showNotification('Сравнение очищено', 'info');
    }
    
    // Refresh comparison page if we're on it
    if (window.location.pathname.includes('comparison') || 
        (document.getElementById('comparison') && !document.getElementById('comparison').classList.contains('content-section'))) {
        location.reload();
    }
}

function switchComparisonTab(tab) {
    // Update tab buttons
    document.querySelectorAll('.comparison-tab').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white');
        btn.classList.add('bg-gray-100', 'text-gray-600');
    });
    
    const activeTab = document.getElementById(`comparison-tab-${tab}`);
    if (activeTab) {
        activeTab.classList.remove('bg-gray-100', 'text-gray-600');
        activeTab.classList.add('bg-blue-600', 'text-white');
    }
    
    // Switch content
    document.querySelectorAll('.comparison-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    const activeContent = document.getElementById(`${tab}-comparison`);
    if (activeContent) {
        activeContent.classList.remove('hidden');
    }
}

// Initialize comparison data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadComparisonFromStorage();
});

// Simple notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 px-4 py-2 rounded-lg text-white transition-all duration-300 transform translate-x-full`;
    
    switch (type) {
        case 'success':
            notification.classList.add('bg-green-500');
            break;
        case 'error':
            notification.classList.add('bg-red-500');
            break;
        case 'warning':
            notification.classList.add('bg-yellow-500');
            break;
        default:
            notification.classList.add('bg-blue-500');
    }
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Animate out and remove
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

})(); // Close IIFE