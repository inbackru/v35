// Smart Search Integration for Header and Hero sections
class SmartSearch {
    constructor() {
        // Header search removed per user request
        
        // Initialize hero search
        this.heroSearchInput = document.getElementById('hero-search');
        this.heroDropdown = document.getElementById('hero-searchSuggestions');
        this.heroSearchBtn = document.getElementById('hero-search-btn');
        
        // Initialize properties page search
        this.propertySearchInput = document.getElementById('property-search');
        this.propertyDropdown = document.getElementById('property-searchSuggestions');
        
        this.debounceTimer = null;
        this.isVisible = false;
        
        // Initialize available search inputs (header search disabled)
        this.initHeroSearch();
        this.initPropertySearch();
    }
    
    // Header search removed per user request
    
    initHeroSearch() {
        if (this.heroSearchInput) {
            console.log('Hero search initialized');
            if (this.heroDropdown) {
                this.initSearchInput(this.heroSearchInput, this.heroDropdown);
            }
            
            // Hero search button
            if (this.heroSearchBtn) {
                this.heroSearchBtn.addEventListener('click', () => {
                    this.executeSearch(this.heroSearchInput.value.trim());
                });
            }
        }
    }
    
    initPropertySearch() {
        if (this.propertySearchInput && this.propertyDropdown) {
            console.log('Property search initialized with smart search');
            this.initSearchInput(this.propertySearchInput, this.propertyDropdown);
            
            // Disable the old property search script
            this.disableOldPropertySearch();
        }
    }
    
    disableOldPropertySearch() {
        // Remove old event listeners by cloning the element
        const oldInput = this.propertySearchInput;
        const newInput = oldInput.cloneNode(true);
        oldInput.parentNode.replaceChild(newInput, oldInput);
        this.propertySearchInput = newInput;
        
        // Re-initialize with smart search
        this.initSearchInput(this.propertySearchInput, this.propertyDropdown);
        console.log('Old property search disabled, smart search enabled');
    }
    
    initSearchInput(searchInput, dropdown) {
        console.log('Initializing search input:', searchInput.id);
        
        // Event listeners
        searchInput.addEventListener('input', (e) => this.handleInput(e, dropdown));
        searchInput.addEventListener('focus', () => this.handleFocus(searchInput, dropdown));
        searchInput.addEventListener('blur', (e) => this.handleBlur(e, dropdown));
        searchInput.addEventListener('keydown', (e) => this.handleKeydown(e, searchInput, dropdown));
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
                this.hideDropdown(dropdown);
            }
        });
    }
    
    handleInput(e, dropdown) {
        const query = e.target.value.trim();
        
        // Clear previous timer
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        if (query.length < 2) {
            this.hideDropdown(dropdown);
            return;
        }
        
        // Debounce search requests - use new fast API
        this.debounceTimer = setTimeout(() => {
            this.fetchFastSuggestions(query, dropdown);
        }, 200);
    }
    
    handleFocus(searchInput, dropdown) {
        const query = searchInput.value.trim();
        if (query.length >= 2) {
            this.fetchFastSuggestions(query, dropdown);
        }
    }
    
    handleBlur(e, dropdown) {
        // Delay hiding to allow click on suggestions
        setTimeout(() => {
            if (!dropdown.contains(document.activeElement)) {
                this.hideDropdown(dropdown);
            }
        }, 150);
    }
    
    handleKeydown(e, searchInput, dropdown) {
        const suggestions = dropdown.querySelectorAll('.suggestion-item');
        const activeItem = dropdown.querySelector('.suggestion-item.active');
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.navigateDropdown(suggestions, activeItem, 'down');
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.navigateDropdown(suggestions, activeItem, 'up');
                break;
            case 'Enter':
                e.preventDefault();
                if (activeItem) {
                    this.selectSuggestion(activeItem);
                } else {
                    this.executeSearch(searchInput.value.trim());
                }
                break;
            case 'Escape':
                this.hideDropdown(dropdown);
                searchInput.blur();
                break;
        }
    }
    
    navigateDropdown(suggestions, activeItem, direction) {
        if (suggestions.length === 0) return;
        
        // Remove current active
        if (activeItem) {
            activeItem.classList.remove('active');
        }
        
        let newIndex = 0;
        if (activeItem) {
            const currentIndex = Array.from(suggestions).indexOf(activeItem);
            if (direction === 'down') {
                newIndex = (currentIndex + 1) % suggestions.length;
            } else {
                newIndex = currentIndex === 0 ? suggestions.length - 1 : currentIndex - 1;
            }
        }
        
        suggestions[newIndex].classList.add('active');
        suggestions[newIndex].scrollIntoView({ block: 'nearest' });
    }
    
    async fetchFastSuggestions(query, dropdown) {
        try {
            console.log('Fetching fast suggestions for:', query);
            
            const response = await fetch(`/api/search/suggestions?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data && data.length > 0) {
                this.renderModernSuggestions(data, dropdown);
                this.showDropdown(dropdown);
            } else {
                this.hideDropdown(dropdown);
            }
            
        } catch (error) {
            console.error('Fast suggestions error:', error);
            this.hideDropdown(dropdown);
        }
    }

    async performSearch(query, dropdown) {
        try {
            console.log('Performing search for:', query);
            
            // First try the new fast search suggestions API
            const fastResponse = await fetch(`/api/search/suggestions?query=${encodeURIComponent(query)}`);
            const fastData = await fastResponse.json();
            
            if (fastData && fastData.length > 0) {
                this.renderModernSuggestions(fastData, dropdown);
                this.showDropdown(dropdown);
                return;
            }
            
            // Fallback to old smart search
            const suggestionsResponse = await fetch(`/api/smart-suggestions?q=${encodeURIComponent(query)}`);
            const suggestionsData = await suggestionsResponse.json();
            
            // Get search results preview
            const searchResponse = await fetch(`/api/smart-search?q=${encodeURIComponent(query)}`);
            const searchData = await searchResponse.json();
            
            this.showSuggestions(query, suggestionsData.suggestions || [], searchData.results || [], dropdown);
            
        } catch (error) {
            console.error('Search error:', error);
            this.showErrorMessage('Ошибка поиска', dropdown);
        }
    }
    
    showSuggestions(query, suggestions, results, dropdown) {
        let html = '';
        
        // Add search suggestions
        if (suggestions.length > 0) {
            html += '<div class="p-2 border-b border-gray-100">';
            html += '<div class="text-xs font-medium text-gray-500 mb-2">Подсказки</div>';
            
            suggestions.forEach(suggestion => {
                html += `
                    <div class="suggestion-item flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer rounded" data-suggestion="${suggestion}">
                        <svg class="w-4 h-4 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                        <span class="text-sm">${suggestion}</span>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        // Add quick results preview
        if (results.length > 0) {
            html += '<div class="p-2">';
            html += '<div class="text-xs font-medium text-gray-500 mb-2">Быстрые результаты</div>';
            
            results.slice(0, 3).forEach(result => {
                html += `
                    <div class="suggestion-item flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer rounded" data-url="${result.url}">
                        <div class="w-8 h-8 bg-gradient-to-r from-[#0088CC] to-[#006699] rounded mr-3 flex items-center justify-center">
                            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                            </svg>
                        </div>
                        <div class="flex-1">
                            <div class="text-sm font-medium text-gray-900">${result.title}</div>
                            <div class="text-xs text-gray-500">${result.subtitle}</div>
                            <div class="text-xs font-medium text-[#0088CC]">${this.formatPrice(result.price)}</div>
                        </div>
                    </div>
                `;
            });
            
            if (results.length > 3) {
                html += `
                    <div class="suggestion-item flex items-center px-3 py-2 hover:bg-blue-50 cursor-pointer rounded border-t border-gray-100 mt-2" data-search="${query}">
                        <span class="text-sm text-[#0088CC] font-medium">Показать все ${results.length} результатов</span>
                    </div>
                `;
            }
            html += '</div>';
        }
        
        // Show "no results" message
        if (suggestions.length === 0 && results.length === 0) {
            html = `
                <div class="p-4 text-center text-gray-500">
                    <svg class="w-8 h-8 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    <div class="text-sm">Ничего не найдено</div>
                    <div class="text-xs text-gray-400 mt-1">Попробуйте изменить запрос</div>
                </div>
            `;
        }
        
        dropdown.innerHTML = html;
        this.showDropdown(dropdown);
        
        // Add click handlers to suggestions
        dropdown.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => this.selectSuggestion(item));
        });
    }
    
    selectSuggestion(item) {
        const suggestion = item.dataset.suggestion;
        const url = item.dataset.url;
        const search = item.dataset.search;
        
        if (suggestion) {
            // Replace search input with suggestion and perform smart search
            if (this.propertySearchInput && window.location.pathname === '/properties') {
                this.propertySearchInput.value = suggestion;
                this.hideDropdown(this.propertyDropdown);
                this.executeSearch(suggestion);
            } else if (this.heroSearchInput) {
                this.heroSearchInput.value = suggestion;
                this.hideDropdown(this.heroDropdown);
                this.executeSearch(suggestion);
            } else if (this.headerSearchInput) {
                this.headerSearchInput.value = suggestion;
                this.hideDropdown(this.headerDropdown);
                this.executeSearch(suggestion);
            }
        } else if (url) {
            // Navigate to specific property
            window.location.href = url;
        } else if (search) {
            // Navigate to full search results
            window.location.href = `/properties?search=${encodeURIComponent(search)}`;
        }
    }
    
    executeSearch(query) {
        if (query) {
            // If we're on properties page and have property search input, apply smart filters
            if (window.location.pathname === '/properties' && this.propertySearchInput) {
                this.performSmartSearchOnPage(query);
            } else {
                // Redirect to properties page
                window.location.href = `/properties?search=${encodeURIComponent(query)}`;
            }
        }
    }
    
    async performSmartSearchOnPage(query) {
        try {
            console.log('Performing smart search on page for:', query);
            
            const response = await fetch(`/api/smart-search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            console.log('Smart search API response:', data);
            
            if (data.criteria && Object.keys(data.criteria).length > 0) {
                // Apply smart filters based on criteria
                this.applySmartFiltersToPage(data.criteria, query);
            }
            
        } catch (error) {
            console.error('Smart search error:', error);
            // Fallback to normal search
            window.location.href = `/properties?search=${encodeURIComponent(query)}`;
        }
    }
    
    applySmartFiltersToPage(criteria, originalQuery) {
        console.log('Applying smart filters:', criteria);
        
        // Update search input to show current query
        if (this.propertySearchInput) {
            this.propertySearchInput.value = originalQuery;
        }
        
        // Build URL with smart search parameters
        const url = new URL(window.location);
        url.searchParams.set('search', originalQuery);
        
        // Apply room filter
        if (criteria.rooms && criteria.rooms.length > 0) {
            url.searchParams.set('rooms', criteria.rooms[0]);
            
            // Update rooms dropdown if it exists
            const roomsSelect = document.querySelector('select[name="rooms"]');
            if (roomsSelect) {
                roomsSelect.value = criteria.rooms[0];
            }
        }
        
        // Apply district filter
        if (criteria.district) {
            url.searchParams.set('district', criteria.district);
            
            // Update district dropdown if it exists
            const districtSelect = document.querySelector('select[name="district"]');
            if (districtSelect) {
                districtSelect.value = criteria.district;
            }
        }
        
        // Update URL without reload
        window.history.replaceState({}, '', url.toString());
        
        // Trigger the existing filter system
        const form = document.querySelector('.filter-form');
        if (form) {
            console.log('Triggering existing filter system');
            
            // Create and dispatch a custom event to trigger filtering
            const filterEvent = new CustomEvent('smartFilter', {
                detail: { criteria: criteria, query: originalQuery }
            });
            form.dispatchEvent(filterEvent);
            
            // Or manually submit the form if event doesn't work
            setTimeout(() => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                }
            }, 100);
        } else {
            // Reload page with new parameters if no form found
            window.location.reload();
        }
    }
    
    showDropdown(dropdown) {
        dropdown.classList.remove('hidden');
        this.isVisible = true;
    }
    
    hideDropdown(dropdown) {
        dropdown.classList.add('hidden');
        this.isVisible = false;
        
        // Remove active states
        dropdown.querySelectorAll('.suggestion-item.active').forEach(item => {
            item.classList.remove('active');
        });
    }
    
    showErrorMessage(message, dropdown) {
        dropdown.innerHTML = `
            <div class="p-4 text-center text-red-500">
                <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div class="text-sm">${message}</div>
            </div>
        `;
        this.showDropdown(dropdown);
    }
    
    formatPrice(price) {
        if (!price) return '';
        return new Intl.NumberFormat('ru-RU', {
            style: 'currency',
            currency: 'RUB',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(price);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing smart search...');
    new SmartSearch();
});

// Enhanced search suggestions for faster search
SmartSearch.prototype.renderModernSuggestions = function(suggestions, dropdown) {
    const iconMap = {
        'complex': 'fas fa-building',
        'developer': 'fas fa-user-tie', 
        'district': 'fas fa-map-marker-alt',
        'street': 'fas fa-road',
        'rooms': 'fas fa-home'
    };
    
    const typeNames = {
        'complex': 'ЖК',
        'developer': 'Застройщик',
        'district': 'Район', 
        'street': 'Улица',
        'rooms': 'Тип квартиры'
    };
    
    let html = '<div class="p-2">';
    html += '<div class="text-xs font-medium text-gray-500 mb-2">Быстрый поиск</div>';
    
    suggestions.forEach(suggestion => {
        html += `
            <div class="suggestion-item flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer rounded transition-colors" 
                 data-url="${suggestion.url}">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mr-3">
                    <i class="${iconMap[suggestion.type] || 'fas fa-search'} text-sm"></i>
                </div>
                <div class="flex-1">
                    <div class="font-medium text-gray-900 text-sm">${suggestion.text || suggestion.title}</div>
                    <div class="text-xs text-gray-500">
                        <span class="inline-block bg-gray-100 px-2 py-0.5 rounded text-xs mr-2">
                            ${typeNames[suggestion.type] || suggestion.type}
                        </span>
                        ${suggestion.subtitle || ''}
                    </div>
                </div>
                <div class="text-gray-400">
                    <i class="fas fa-arrow-right text-xs"></i>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    dropdown.innerHTML = html;
    
    // Add click handlers
    dropdown.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', () => {
            const url = item.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
};