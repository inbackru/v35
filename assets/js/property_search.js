// Property Search JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize dropdowns
    initializeDropdowns();
    
    // Initialize mobile menu
    initializeMobileMenu();
    
    // Initialize favorites
    initializeFavorites();
    
    // Initialize property comparison
    initializeComparison();
    
    // Initialize search filters
    initializeSearchFilters();
    
});

// Dropdown functionality
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const button = dropdown.querySelector('.dropdown-btn');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (button && menu) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Close other dropdowns
                dropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.querySelector('.dropdown-menu')?.classList.remove('open');
                        otherDropdown.querySelector('.dropdown-btn')?.classList.remove('open');
                    }
                });
                
                // Toggle current dropdown
                menu.classList.toggle('open');
                button.classList.toggle('open');
            });
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            dropdowns.forEach(dropdown => {
                dropdown.querySelector('.dropdown-menu')?.classList.remove('open');
                dropdown.querySelector('.dropdown-btn')?.classList.remove('open');
            });
        }
    });
}

// Mobile menu functionality
function initializeMobileMenu() {
    window.toggleMobileMenu = function() {
        const menu = document.getElementById('mobileMenu');
        if (menu) {
            menu.classList.toggle('hidden');
        }
    };
}

// Favorites functionality
function initializeFavorites() {
    const favoriteButtons = document.querySelectorAll('[data-favorite]');
    const favorites = JSON.parse(localStorage.getItem('property_favorites') || '[]');
    
    favoriteButtons.forEach(button => {
        const propertyId = button.dataset.favorite;
        
        // Set initial state
        if (favorites.includes(propertyId)) {
            button.innerHTML = '<i class="fas fa-heart text-red-500"></i>';
            button.classList.add('favorited');
        }
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            toggleFavorite(propertyId, button);
        });
    });
}

function toggleFavorite(propertyId, button) {
    let favorites = JSON.parse(localStorage.getItem('property_favorites') || '[]');
    
    if (favorites.includes(propertyId)) {
        // Remove from favorites
        favorites = favorites.filter(id => id !== propertyId);
        button.innerHTML = '<i class="far fa-heart text-gray-600"></i>';
        button.classList.remove('favorited');
    } else {
        // Add to favorites
        favorites.push(propertyId);
        button.innerHTML = '<i class="fas fa-heart text-red-500"></i>';
        button.classList.add('favorited');
    }
    
    localStorage.setItem('property_favorites', JSON.stringify(favorites));
    
    // Show notification
    showNotification(favorites.includes(propertyId) ? 'Добавлено в избранное' : 'Удалено из избранного');
}

// Property comparison functionality
function initializeComparison() {
    window.addToComparison = function(propertyId) {
        let comparison = JSON.parse(localStorage.getItem('property_comparison') || '[]');
        
        if (comparison.includes(propertyId)) {
            showNotification('Объект уже добавлен к сравнению');
            return;
        }
        
        if (comparison.length >= 3) {
            showNotification('Можно сравнивать не более 3 объектов');
            return;
        }
        
        comparison.push(propertyId);
        localStorage.setItem('property_comparison', JSON.stringify(comparison));
        
        showNotification('Добавлено к сравнению');
        updateComparisonCounter();
    };
    
    updateComparisonCounter();
}

function updateComparisonCounter() {
    const comparison = JSON.parse(localStorage.getItem('property_comparison') || '[]');
    const counter = document.getElementById('comparisonCounter');
    
    if (counter) {
        if (comparison.length > 0) {
            counter.textContent = comparison.length;
            counter.classList.remove('hidden');
        } else {
            counter.classList.add('hidden');
        }
    }
}

// Search filters functionality
function initializeSearchFilters() {
    const searchForm = document.querySelector('form[method="GET"]');
    const searchInput = document.querySelector('input[name="search"]');
    
    if (searchInput) {
        // Add search suggestions
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                showSearchSuggestions(this.value);
            }, 300);
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.search-container')) {
                hideSearchSuggestions();
            }
        });
    }
    
    // Price range inputs
    const priceInputs = document.querySelectorAll('input[name="min_price"], input[name="max_price"]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPriceInput(this);
        });
    });
}

function formatPriceInput(input) {
    let value = input.value.replace(/\D/g, '');
    if (value) {
        value = parseInt(value).toLocaleString('ru-RU');
        input.setAttribute('data-value', input.value.replace(/\D/g, ''));
    }
}

function showSearchSuggestions(query) {
    if (!query || query.length < 2) {
        hideSearchSuggestions();
        return;
    }
    
    // This would typically make an AJAX request to get suggestions
    // For now, we'll show a simple loading state
    const container = document.querySelector('.search-container');
    if (!container) return;
    
    let suggestions = container.querySelector('.search-suggestions');
    if (!suggestions) {
        suggestions = document.createElement('div');
        suggestions.className = 'search-suggestions absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-b-lg shadow-lg z-50';
        container.appendChild(suggestions);
    }
    
    suggestions.innerHTML = '<div class="p-3 text-gray-500 text-sm">Поиск...</div>';
    suggestions.classList.remove('hidden');
}

function hideSearchSuggestions() {
    const suggestions = document.querySelector('.search-suggestions');
    if (suggestions) {
        suggestions.classList.add('hidden');
    }
}

// Utility functions
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification fixed top-4 right-4 px-4 py-3 rounded-lg shadow-lg z-50 transition-all duration-300 ${getNotificationClasses(type)}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('opacity-100', 'translate-y-0');
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('opacity-0', 'translate-y-full');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationClasses(type) {
    const classes = {
        'info': 'bg-blue-500 text-white',
        'success': 'bg-green-500 text-white',
        'warning': 'bg-yellow-500 text-white',
        'error': 'bg-red-500 text-white'
    };
    
    return classes[type] || classes['info'];
}

// Property card interactions
function initializePropertyCards() {
    const propertyCards = document.querySelectorAll('.property-card');
    
    propertyCards.forEach(card => {
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-xl', 'transform', 'scale-105');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-xl', 'transform', 'scale-105');
        });
        
        // Add click tracking
        card.addEventListener('click', function(e) {
            if (e.target.closest('a, button')) return;
            
            const propertyLink = this.querySelector('a[href*="object.php"]');
            if (propertyLink) {
                window.location.href = propertyLink.href;
            }
        });
    });
}

// Initialize property cards when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializePropertyCards();
});

// Scroll to top functionality
function addScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollButton.className = 'fixed bottom-6 right-6 bg-ton-blue text-white p-3 rounded-full shadow-lg hover:bg-opacity-90 transition-all duration-300 opacity-0 pointer-events-none z-50';
    scrollButton.id = 'scrollToTop';
    
    document.body.appendChild(scrollButton);
    
    // Show/hide on scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.classList.remove('opacity-0', 'pointer-events-none');
        } else {
            scrollButton.classList.add('opacity-0', 'pointer-events-none');
        }
    });
    
    // Scroll to top on click
    scrollButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize scroll to top
document.addEventListener('DOMContentLoaded', function() {
    addScrollToTop();
});

// Filter persistence
function saveFilterState() {
    const form = document.querySelector('form[method="GET"]');
    if (!form) return;
    
    const formData = new FormData(form);
    const filterState = {};
    
    for (let [key, value] of formData.entries()) {
        if (value) {
            filterState[key] = value;
        }
    }
    
    localStorage.setItem('property_filters', JSON.stringify(filterState));
}

function loadFilterState() {
    const savedFilters = localStorage.getItem('property_filters');
    if (!savedFilters) return;
    
    try {
        const filters = JSON.parse(savedFilters);
        
        Object.keys(filters).forEach(key => {
            const input = document.querySelector(`input[name="${key}"], select[name="${key}"]`);
            if (input) {
                input.value = filters[key];
            }
        });
    } catch (e) {
        console.warn('Failed to load saved filters:', e);
    }
}

// Auto-save filters on change
document.addEventListener('DOMContentLoaded', function() {
    const filterInputs = document.querySelectorAll('input[name], select[name]');
    
    filterInputs.forEach(input => {
        input.addEventListener('change', saveFilterState);
    });
    
    // Load saved filters on page load
    if (!window.location.search) {
        loadFilterState();
    }
});
