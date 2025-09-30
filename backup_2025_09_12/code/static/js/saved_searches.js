/**
 * Saved Searches Manager
 * Handles saving, loading, and applying search parameters
 */

class SavedSearchesManager {
    constructor() {
        this.init();
    }

    init() {
        try {
            this.bindEvents();
            this.loadSavedSearches();
        } catch (error) {
            console.error('Error initializing saved searches:', error);
        }
    }

    bindEvents() {
        // Save search button
        document.addEventListener('click', (e) => {
            if (e.target && e.target.classList.contains('save-search-btn')) {
                this.openSaveSearchModal();
                e.preventDefault();
            }
        });

        // Apply saved search
        document.addEventListener('click', (e) => {
            if (e.target && e.target.classList.contains('apply-search-btn')) {
                const searchId = e.target.dataset.searchId;
                this.applySavedSearch(searchId);
                e.preventDefault();
            }
        });

        // Delete saved search
        document.addEventListener('click', (e) => {
            if (e.target && e.target.classList.contains('delete-search-btn')) {
                const searchId = e.target.dataset.searchId;
                this.deleteSavedSearch(searchId);
                e.preventDefault();
            }
        });
    }

    getCurrentSearchParams() {
        let params = {};

        // Get parameters from URL first - this is most reliable source
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.forEach((value, key) => {
            if (value && value.trim() !== '') {
                // Handle multiple values for same parameter (e.g., rooms)
                if (params[key]) {
                    if (Array.isArray(params[key])) {
                        params[key].push(value.trim());
                    } else {
                        params[key] = [params[key], value.trim()];
                    }
                } else {
                    params[key] = value.trim();
                }
            }
        });

        // If no URL params, try to extract from form and active UI elements
        if (Object.keys(params).length === 0) {
            // Check active filter buttons on properties page  
            try {
                const activeFilters = document.querySelectorAll('.active-filter-btn, .filter-btn.active, input[type="checkbox"]:checked');
                activeFilters.forEach(element => {
                    const filterType = element.dataset.filter || element.name;
                    const filterValue = element.dataset.value || element.value;
                    
                    if (filterType && filterValue) {
                        if (!params[filterType]) {
                            params[filterType] = [];
                        }
                    if (Array.isArray(params[filterType])) {
                        params[filterType].push(filterValue);
                    } else {
                        params[filterType] = [params[filterType], filterValue];
                    }
                }
                });
            } catch (error) {
                console.error('Error reading active filters:', error);
            }

            // Check price range inputs with error handling
            try {
            const priceFromInput = document.querySelector('#priceFrom, input[name="priceFrom"]');
            const priceToInput = document.querySelector('#priceTo, input[name="priceTo"]');
            if (priceFromInput && priceFromInput.value && priceFromInput.value !== '0') {
                params.priceFrom = priceFromInput.value;
            }
            if (priceToInput && priceToInput.value && priceToInput.value !== '0') {
                params.priceTo = priceToInput.value;
            }

            // Check area range inputs
            const areaFromInput = document.querySelector('#areaFrom, input[name="areaFrom"]');
            const areaToInput = document.querySelector('#areaTo, input[name="areaTo"]');
            if (areaFromInput && areaFromInput.value && areaFromInput.value !== '0') {
                params.areaFrom = areaFromInput.value;
            }
            if (areaToInput && areaToInput.value && areaToInput.value !== '0') {
                params.areaTo = areaToInput.value;
            }
            } catch (error) {
                console.error('Error reading input values:', error);
            }
        }

        // Clean up params - convert single-item arrays to strings
        for (const [key, value] of Object.entries(params)) {
            if (Array.isArray(value) && value.length === 1) {
                params[key] = value[0];
            }
        }

        console.log('Final search params:', params);
        return params;
    }

    generateSearchName(params) {
        let parts = [];

        // Add room types
        if (params.rooms && params.rooms.length > 0) {
            const roomTypes = Array.isArray(params.rooms) ? params.rooms : [params.rooms];
            const roomNames = roomTypes.map(room => {
                if (room.includes('студия')) return 'Студия';
                if (room.includes('комн')) return room;
                return room + '-комн';
            });
            parts.push(roomNames.join(', '));
        }

        // Add districts
        if (params.districts && params.districts.length > 0) {
            const districts = Array.isArray(params.districts) ? params.districts : [params.districts];
            parts.push('р-н ' + districts.join(', '));
        }

        // Add developers
        if (params.developers && params.developers.length > 0) {
            const developers = Array.isArray(params.developers) ? params.developers : [params.developers];
            parts.push('от ' + developers.join(', '));
        }

        // Add price range
        if (params.priceFrom || params.priceTo) {
            let priceText = '';
            if (params.priceFrom && params.priceTo) {
                priceText = `${params.priceFrom}-${params.priceTo} млн`;
            } else if (params.priceFrom) {
                priceText = `от ${params.priceFrom} млн`;
            } else if (params.priceTo) {
                priceText = `до ${params.priceTo} млн`;
            }
            parts.push(priceText);
        }

        // Add area range
        if (params.areaFrom || params.areaTo) {
            let areaText = '';
            if (params.areaFrom && params.areaTo) {
                areaText = `${params.areaFrom}-${params.areaTo} м²`;
            } else if (params.areaFrom) {
                areaText = `от ${params.areaFrom} м²`;
            } else if (params.areaTo) {
                areaText = `до ${params.areaTo} м²`;
            }
            parts.push(areaText);
        }

        return parts.length > 0 ? parts.join(', ') : 'Поиск недвижимости';
    }

    openSaveSearchModal() {
        const params = this.getCurrentSearchParams();
        
        // Check if user is authenticated (support both users and managers)
        const userAuthElement = document.querySelector('a[href*="dashboard"]') || document.querySelector('.user-authenticated');
        const managerAuthElement = document.querySelector('a[href*="manager/dashboard"]') || document.querySelector('.manager-authenticated');
        const isAuthenticated = userAuthElement !== null || managerAuthElement !== null || 
                              document.querySelector('a[href*="logout"]') !== null ||
                              window.user_authenticated === true || window.manager_authenticated === true;
        
        if (!isAuthenticated) {
            this.showNotification('Войдите в аккаунт для сохранения поисков', 'warning');
            return;
        }

        if (Object.keys(params).length === 0) {
            this.showNotification('Задайте параметры поиска для сохранения', 'warning');
            return;
        }

        // Generate suggested search name based on current filters
        const suggestedName = this.generateSearchName(params);

        // Create modal HTML
        const modalHTML = `
            <div id="save-search-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
                    <h3 class="text-lg font-semibold mb-4">Сохранить поиск</h3>
                    <form id="save-search-form">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Название поиска
                            </label>
                            <input type="text" id="search-name" name="name" required
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                   placeholder="Например: 2-комн в центре до 10млн"
                                   value="${suggestedName}">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Описание (необязательно)
                            </label>
                            <textarea id="search-description" name="description" rows="2"
                                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                      placeholder="Дополнительные заметки о поиске"></textarea>
                        </div>
                        <div class="mb-4">
                            <label class="flex items-center">
                                <input type="checkbox" id="notify-matches" name="notify_new_matches" checked
                                       class="mr-2 rounded">
                                <span class="text-sm text-gray-700">Уведомлять о новых подходящих объектах</span>
                            </label>
                        </div>
                        <div class="flex justify-end space-x-3">
                            <button type="button" class="cancel-save-search px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50">
                                Отмена
                            </button>
                            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                                Сохранить
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        `;

        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Bind modal events
        document.querySelector('.cancel-save-search').addEventListener('click', () => {
            this.closeSaveSearchModal();
        });

        document.querySelector('#save-search-modal').addEventListener('click', (e) => {
            if (e.target.id === 'save-search-modal') {
                this.closeSaveSearchModal();
            }
        });

        document.querySelector('#save-search-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitSaveSearch();
        });

        // Auto-generate search name suggestion
        this.generateSearchName(params);
    }

    generateSearchName(params) {
        let name = '';
        
        if (params.property_type) {
            name += params.property_type + ' ';
        }
        
        if (params.location) {
            name += 'в ' + params.location + ' ';
        }
        
        if (params.price_max) {
            name += 'до ' + this.formatPrice(params.price_max) + ' ';
        }
        
        if (params.developer) {
            name += 'от ' + params.developer + ' ';
        }

        if (name.trim() === '') {
            name = 'Мой поиск';
        }

        document.querySelector('#search-name').value = name.trim();
    }

    formatPrice(price) {
        if (price >= 1000000) {
            return (price / 1000000).toFixed(1) + 'млн';
        }
        return price.toLocaleString() + 'р';
    }

    closeSaveSearchModal() {
        const modal = document.querySelector('#save-search-modal');
        if (modal) {
            modal.remove();
        }
    }

    async submitSaveSearch() {
        const form = document.querySelector('#save-search-form');
        const formData = new FormData(form);
        const params = this.getCurrentSearchParams();

        // Determine if user is a manager
        const managerAuthElement = document.querySelector('a[href*="manager/dashboard"]') || document.querySelector('.manager-authenticated');
        const isManager = managerAuthElement !== null || window.manager_authenticated === true;
        
        console.log('Manager detection debug:', {
            managerAuthElement: managerAuthElement,
            window_manager_authenticated: window.manager_authenticated,
            isManager: isManager
        });
        
        // Choose appropriate endpoint and data format
        let endpoint, requestData;
        
        if (isManager) {
            // Manager endpoint expects filters object
            endpoint = '/api/manager/saved-searches';
            requestData = {
                name: formData.get('name'),
                filters: params
            };
        } else {
            // User endpoint expects flat data structure
            endpoint = '/api/searches';
            requestData = {
                name: formData.get('name'),
                description: formData.get('description'),
                notify_new_matches: formData.has('notify_new_matches'),
                search_type: 'properties',
                ...params
            };
        }

        console.log('Saving search with data:', requestData);
        console.log('Request data:', { name: requestData.name, filters: requestData.filters || requestData });

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin',
                body: JSON.stringify(requestData)
            });

            const result = await response.json();

            if (result.success) {
                this.showNotification('Поиск сохранен успешно', 'success');
                this.closeSaveSearchModal();
                this.loadSavedSearches(); // Refresh saved searches list
            } else {
                this.showNotification('Ошибка при сохранении поиска: ' + result.error, 'error');
            }
        } catch (error) {
            console.error('Error saving search:', error);
            this.showNotification('Ошибка при сохранении поиска', 'error');
        }
    }

    async loadSavedSearches() {
        try {
            const response = await fetch('/api/searches', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();

            if (result.success) {
                this.displaySavedSearches(result.searches);
            } else {
                console.error('Server error loading saved searches:', result.error);
            }
        } catch (error) {
            console.error('Error loading saved searches:', error);
        }
    }

    displaySavedSearches(searches) {
        const container = window.safeQuery ? window.safeQuery('#saved-searches-container') : document.querySelector('#saved-searches-container');
        if (!container) return;

        if (searches.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-center py-4">Сохраненных поисков нет</p>';
            return;
        }

        const searchesHTML = searches.map(search => `
            <div class="saved-search-item border rounded-lg p-4 mb-3 bg-white">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <h4 class="font-semibold text-lg">${search.name}</h4>
                        ${search.description ? `<p class="text-gray-600 text-sm mt-1">${search.description}</p>` : ''}
                        <div class="mt-2 text-xs text-gray-500">
                            Создан: ${new Date(search.created_at).toLocaleDateString('ru-RU')}
                            ${search.last_used ? ` • Использован: ${new Date(search.last_used).toLocaleDateString('ru-RU')}` : ''}
                        </div>
                        ${this.getSearchSummary(search)}
                    </div>
                    <div class="flex space-x-2 ml-4">
                        <button class="apply-search-btn px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700" 
                                data-search-id="${search.id}">
                            Применить
                        </button>
                        <button class="delete-search-btn px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700" 
                                data-search-id="${search.id}">
                            Удалить
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = searchesHTML;
    }

    getSearchSummary(search) {
        const parts = [];
        
        if (search.property_type) parts.push(search.property_type);
        if (search.location) parts.push('в ' + search.location);
        if (search.price_min || search.price_max) {
            let priceRange = '';
            if (search.price_min) priceRange += `от ${this.formatPrice(search.price_min)}`;
            if (search.price_max) priceRange += ` до ${this.formatPrice(search.price_max)}`;
            parts.push(priceRange);
        }
        if (search.developer) parts.push('от ' + search.developer);
        if (search.complex_name) parts.push('ЖК ' + search.complex_name);

        if (parts.length === 0) return '';

        return `<div class="mt-2 text-sm text-gray-600">${parts.join(', ')}</div>`;
    }

    async applySavedSearch(searchId) {
        try {
            console.log('Applying saved search:', searchId);
            const response = await fetch(`/api/searches/${searchId}/apply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            console.log('Response status:', response.status);
            
            // Check if response is HTML (error page) instead of JSON
            const contentType = response.headers.get('content-type');
            console.log('Response content-type:', contentType);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Apply result:', result);

            if (result.success) {
                console.log('Applying search with result:', result);
                
                // Apply filters and redirect to properties page
                const filters = result.filters || {};
                console.log('Filters to apply:', filters);
                
                // Build URL with filter parameters, converting arrays to multiple params
                const params = new URLSearchParams();
                
                for (const [key, value] of Object.entries(filters)) {
                    if (value && value !== '' && value !== '0') {
                        if (Array.isArray(value) && value.length > 0) {
                            // For arrays, add each value as separate parameter
                            value.forEach(v => {
                                if (v && v !== '' && v !== '0') {
                                    // URLSearchParams automatically handles encoding
                                    params.append(key, v);
                                }
                            });
                        } else if (!Array.isArray(value)) {
                            // URLSearchParams automatically handles encoding
                            params.set(key, value);
                        }
                    }
                }

                const url = `/properties${params.toString() ? '?' + params.toString() : ''}`;
                console.log('Redirecting to URL:', url);
                window.location.href = url;
            } else {
                console.error('Server error:', result.error);
                this.showNotification('Ошибка при применении поиска: ' + (result.error || 'Unknown error'), 'error');
            }
        } catch (error) {
            console.error('Error applying search:', error);
            this.showNotification('Ошибка при применении поиска', 'error');
        }
    }

    applySearchParams(search) {
        // Apply search parameters to current form
        const form = document.querySelector('#property-search-form') || document.querySelector('.search-form');
        if (!form) {
            // Redirect to search page with parameters
            const params = new URLSearchParams();
            Object.keys(search).forEach(key => {
                if (search[key] && key !== 'id' && key !== 'name' && key !== 'description') {
                    params.set(key, search[key]);
                }
            });
            window.location.href = '/properties?' + params.toString();
            return;
        }

        // Fill form fields
        Object.keys(search).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field && search[key]) {
                field.value = search[key];
            }
        });

        // Trigger search
        if (typeof window.searchProperties === 'function') {
            window.searchProperties();
        } else {
            form.submit();
        }
    }

    applyFilters(filters) {
        console.log('Applying filters:', filters);
        
        // Check if we're on properties page
        if (window.location.pathname === '/properties') {
            // Apply filters directly to the properties page
            if (typeof window.applySearchFilters === 'function') {
                window.applySearchFilters(filters);
            } else {
                console.warn('applySearchFilters function not found, redirecting...');
                this.redirectWithFilters(filters);
            }
        } else {
            // Redirect to properties page with filters
            this.redirectWithFilters(filters);
        }
    }

    redirectWithFilters(filters) {
        const params = new URLSearchParams();
        
        // Convert filters to URL parameters
        Object.keys(filters).forEach(key => {
            const value = filters[key];
            if (value && value !== '' && !(Array.isArray(value) && value.length === 0)) {
                if (Array.isArray(value)) {
                    value.forEach(item => {
                        if (item && item !== '') {
                            params.append(key, item);
                        }
                    });
                } else {
                    params.set(key, value);
                }
            }
        });
        
        console.log('Redirecting to:', '/properties?' + params.toString());
        window.location.href = '/properties?' + params.toString();
    }

    async deleteSavedSearch(searchId) {
        if (!confirm('Удалить сохраненный поиск?')) {
            return;
        }

        try {
            const response = await fetch(`/api/searches/${searchId}`, {
                method: 'DELETE',
            });

            const result = await response.json();

            if (result.success) {
                this.showNotification('Поиск удален', 'success');
                this.loadSavedSearches(); // Refresh list
            } else {
                this.showNotification('Ошибка при удалении поиска', 'error');
            }
        } catch (error) {
            console.error('Error deleting search:', error);
            this.showNotification('Ошибка при удалении поиска', 'error');
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 px-4 py-2 rounded-md text-white ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 
            type === 'warning' ? 'bg-yellow-500' : 
            'bg-blue-500'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// Initialize when DOM is ready with safety checks
function initSavedSearches() {
    try {
        // Check if DOM helpers are available
        if (typeof window.safeQuery === 'undefined') {
            setTimeout(initSavedSearches, 100);
            return;
        }
        
        window.savedSearchManager = new SavedSearchesManager();
        console.log('Saved Searches Manager initialized safely');
    } catch (error) {
        console.error('Error loading saved searches:', error);
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSavedSearches);
} else {
    initSavedSearches();
}