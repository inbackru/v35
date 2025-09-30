/**
 * Супер-оптимизированный поиск недвижимости
 * Команда чемпионов по производительности 🏆
 */

class SuperSearch {
    constructor() {
        // Настройки производительности
        this.config = {
            DEBOUNCE_DELAY: 150,        // Уменьшенная задержка
            CACHE_TTL: 300000,          // 5 минут кэш
            MAX_CACHE_SIZE: 100,        // Максимум записей в кэше
            MIN_QUERY_LENGTH: 1,        // Минимальная длина запроса
            MAX_SUGGESTIONS: 8,         // Максимум подсказок
            PRELOAD_POPULAR: true       // Предзагрузка популярных запросов
        };
        
        // Кэши для ускорения
        this.cache = {
            suggestions: new Map(),
            searches: new Map(),
            popular: new Map()
        };
        
        // Состояние поиска
        this.state = {
            currentQuery: '',
            isLoading: false,
            abortController: null,
            lastSearchTime: 0
        };
        
        // Статистика производительности
        this.metrics = {
            searchCount: 0,
            cacheHits: 0,
            avgResponseTime: 0,
            totalResponseTime: 0
        };
        
        // Элементы DOM
        this.elements = {};
        
        this.init();
    }
    
    async init() {
        console.log('🚀 SuperSearch v2.0 - Initializing...');
        
        // Находим элементы поиска
        this.findSearchElements();
        
        // Предзагружаем популярные запросы
        if (this.config.PRELOAD_POPULAR) {
            await this.preloadPopularQueries();
        }
        
        // Инициализируем обработчики событий
        this.setupEventListeners();
        
        // Мониторинг производительности
        this.startPerformanceMonitoring();
        
        console.log('✅ SuperSearch initialized successfully');
    }
    
    findSearchElements() {
        // Ищем все элементы поиска на странице
        const searchInputs = [
            document.getElementById('hero-search'),
            document.getElementById('property-search'),
            document.querySelector('[data-search-input]')
        ].filter(Boolean);
        
        searchInputs.forEach((input, index) => {
            const key = input.id || `search-${index}`;
            this.elements[key] = {
                input: input,
                dropdown: this.createDropdown(input),
                debounceTimer: null
            };
        });
        
        console.log(`Found ${searchInputs.length} search inputs`);
    }
    
    createDropdown(input) {
        const existing = input.parentNode.querySelector('.super-search-dropdown');
        if (existing) return existing;
        
        const dropdown = document.createElement('div');
        dropdown.className = 'super-search-dropdown absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg mt-1 shadow-xl hidden z-50 max-h-80 overflow-y-auto';
        dropdown.style.animation = 'fadeIn 0.15s ease-out';
        
        // Добавляем стили для анимации
        if (!document.getElementById('super-search-styles')) {
            const styles = document.createElement('style');
            styles.id = 'super-search-styles';
            styles.textContent = `
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(-5px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .super-search-dropdown {
                    backdrop-filter: blur(10px);
                    background: rgba(255, 255, 255, 0.95);
                }
                .suggestion-item {
                    transition: background-color 0.1s ease;
                }
                .suggestion-item:hover {
                    background-color: #f8fafc;
                    transform: translateX(2px);
                }
                .suggestion-highlight {
                    background: linear-gradient(90deg, #3b82f6, #1e40af);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-weight: 600;
                }
            `;
            document.head.appendChild(styles);
        }
        
        input.parentNode.style.position = 'relative';
        input.parentNode.appendChild(dropdown);
        
        return dropdown;
    }
    
    setupEventListeners() {
        Object.entries(this.elements).forEach(([key, element]) => {
            const { input, dropdown } = element;
            
            // Оптимизированный input обработчик
            input.addEventListener('input', (e) => {
                this.handleInput(e, key);
            });
            
            // Focus - показываем кэшированные результаты если есть
            input.addEventListener('focus', (e) => {
                this.handleFocus(e, key);
            });
            
            // Blur с задержкой для кликов
            input.addEventListener('blur', (e) => {
                setTimeout(() => {
                    if (!dropdown.contains(document.activeElement)) {
                        this.hideDropdown(key);
                    }
                }, 150);
            });
            
            // Навигация клавиатурой
            input.addEventListener('keydown', (e) => {
                this.handleKeyDown(e, key);
            });
            
            // Enter для поиска
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.performSearch(input.value, key);
                }
            });
        });
        
        // Глобальные обработчики
        document.addEventListener('click', (e) => {
            this.handleGlobalClick(e);
        });
    }
    
    handleInput(event, elementKey) {
        const query = event.target.value.trim();
        const element = this.elements[elementKey];
        
        // Отменяем предыдущий запрос
        if (this.state.abortController) {
            this.state.abortController.abort();
        }
        
        // Очищаем предыдущий таймер
        if (element.debounceTimer) {
            clearTimeout(element.debounceTimer);
        }
        
        if (query.length < this.config.MIN_QUERY_LENGTH) {
            this.hideDropdown(elementKey);
            return;
        }
        
        // Проверяем кэш сначала
        const cacheKey = `suggestions_${query.toLowerCase()}`;
        if (this.cache.suggestions.has(cacheKey)) {
            const cached = this.cache.suggestions.get(cacheKey);
            if (Date.now() - cached.timestamp < this.config.CACHE_TTL) {
                this.metrics.cacheHits++;
                this.renderSuggestions(cached.data, elementKey);
                this.showDropdown(elementKey);
                return;
            }
        }
        
        // Debounced запрос к API
        element.debounceTimer = setTimeout(() => {
            this.fetchSuggestions(query, elementKey);
        }, this.config.DEBOUNCE_DELAY);
    }
    
    handleFocus(event, elementKey) {
        const query = event.target.value.trim();
        if (query && this.cache.suggestions.has(`suggestions_${query.toLowerCase()}`)) {
            this.showDropdown(elementKey);
        }
    }
    
    handleKeyDown(event, elementKey) {
        const dropdown = this.elements[elementKey].dropdown;
        const suggestions = dropdown.querySelectorAll('.suggestion-item');
        const active = dropdown.querySelector('.suggestion-item.active');
        
        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                this.navigateSuggestions(suggestions, active, 'down');
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.navigateSuggestions(suggestions, active, 'up');
                break;
            case 'Escape':
                this.hideDropdown(elementKey);
                break;
        }
    }
    
    navigateSuggestions(suggestions, active, direction) {
        if (!suggestions.length) return;
        
        if (active) active.classList.remove('active');
        
        let newIndex = 0;
        if (active) {
            const currentIndex = Array.from(suggestions).indexOf(active);
            newIndex = direction === 'down' 
                ? (currentIndex + 1) % suggestions.length
                : currentIndex === 0 ? suggestions.length - 1 : currentIndex - 1;
        }
        
        suggestions[newIndex].classList.add('active');
        suggestions[newIndex].scrollIntoView({ block: 'nearest' });
    }
    
    async fetchSuggestions(query, elementKey) {
        const startTime = performance.now();
        this.state.isLoading = true;
        
        try {
            // Создаем AbortController для отмены запросов
            this.state.abortController = new AbortController();
            
            const response = await fetch(`/api/search-suggestions?q=${encodeURIComponent(query)}`, {
                signal: this.state.abortController.signal,
                headers: {
                    'Accept': 'application/json',
                    'Cache-Control': 'max-age=300'
                }
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            const suggestions = Array.isArray(data) ? data : (data.suggestions || []);
            
            // Кэшируем результат
            this.cacheResult('suggestions', query, suggestions);
            
            // Рендерим подсказки
            this.renderSuggestions(suggestions, elementKey);
            this.showDropdown(elementKey);
            
            // Обновляем метрики
            const responseTime = performance.now() - startTime;
            this.updateMetrics(responseTime);
            
        } catch (error) {
            if (error.name !== 'AbortError') {
                console.warn('Search suggestions error:', error);
                this.showErrorMessage('Ошибка поиска', elementKey);
            }
        } finally {
            this.state.isLoading = false;
        }
    }
    
    renderSuggestions(suggestions, elementKey) {
        const dropdown = this.elements[elementKey].dropdown;
        
        if (!suggestions || suggestions.length === 0) {
            dropdown.innerHTML = '<div class="p-4 text-center text-gray-500">Ничего не найдено</div>';
            return;
        }
        
        const iconMap = {
            'complex': '🏢',
            'developer': '👔',
            'district': '📍',
            'street': '🛣️',
            'rooms': '🏠'
        };
        
        const typeNames = {
            'complex': 'ЖК',
            'developer': 'Застройщик',
            'district': 'Район',
            'street': 'Улица',
            'rooms': 'Тип квартиры'
        };
        
        const html = suggestions.map((suggestion, index) => `
            <div class="suggestion-item flex items-center justify-between px-4 py-3 cursor-pointer border-b border-gray-100 last:border-b-0 hover:bg-gray-50 transition-colors" 
                 data-url="${suggestion.url}" 
                 data-suggestion-index="${index}">
                <div class="flex items-center flex-1">
                    <i class="${suggestion.icon || 'fas fa-building'} text-[#0088CC] mr-3 text-lg"></i>
                    <div class="flex-1">
                        <div class="font-medium text-gray-900">${suggestion.text || suggestion.title}</div>
                        <div class="text-sm text-gray-600">${suggestion.subtitle || ''}</div>
                    </div>
                </div>
                <div class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded font-medium">
                    ${typeNames[suggestion.type] || suggestion.type}
                </div>
            </div>
        `).join('');
        
        dropdown.innerHTML = html;
        
        // ✅ ИСПРАВЛЕНО: Добавляем обработчики кликов через addEventListener для надёжности
        dropdown.querySelectorAll('.suggestion-item').forEach((item, index) => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const url = item.dataset.url;
                if (url) {
                    console.log('SuperSearch navigation:', url);
                    window.location.href = url;
                }
            });
        });
    }
    
    showDropdown(elementKey) {
        const dropdown = this.elements[elementKey].dropdown;
        dropdown.classList.remove('hidden');
    }
    
    hideDropdown(elementKey) {
        const dropdown = this.elements[elementKey].dropdown;
        dropdown.classList.add('hidden');
    }
    
    hideAllDropdowns() {
        Object.keys(this.elements).forEach(key => {
            this.hideDropdown(key);
        });
    }
    
    handleGlobalClick(event) {
        // Закрываем все дропдауны при клике вне их
        const isSearchClick = Object.values(this.elements).some(element => 
            element.input.contains(event.target) || element.dropdown.contains(event.target)
        );
        
        if (!isSearchClick) {
            this.hideAllDropdowns();
        }
    }
    
    cacheResult(type, query, data) {
        const cache = this.cache[type];
        const key = `${type}_${query.toLowerCase()}`;
        
        // Очищаем старый кэш если превышен лимит
        if (cache.size >= this.config.MAX_CACHE_SIZE) {
            const firstKey = cache.keys().next().value;
            cache.delete(firstKey);
        }
        
        cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }
    
    async preloadPopularQueries() {
        const popular = ['студия', 'новостройка', 'центр', 'неометрия', '1-комнатная'];
        
        for (const query of popular) {
            try {
                const response = await fetch(`/api/search-suggestions?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                this.cacheResult('suggestions', query, data || []);
            } catch (error) {
                console.warn(`Failed to preload query: ${query}`, error);
            }
        }
        
        console.log(`Preloaded ${popular.length} popular queries`);
    }
    
    updateMetrics(responseTime) {
        this.metrics.searchCount++;
        this.metrics.totalResponseTime += responseTime;
        this.metrics.avgResponseTime = this.metrics.totalResponseTime / this.metrics.searchCount;
    }
    
    startPerformanceMonitoring() {
        // Логируем метрики каждые 30 секунд
        setInterval(() => {
            if (this.metrics.searchCount > 0) {
                console.log('🚀 SuperSearch Performance:', {
                    searches: this.metrics.searchCount,
                    avgResponseTime: Math.round(this.metrics.avgResponseTime),
                    cacheHitRate: Math.round((this.metrics.cacheHits / this.metrics.searchCount) * 100),
                    cacheSize: this.cache.suggestions.size
                });
            }
        }, 30000);
    }
    
    performSearch(query, elementKey) {
        if (!query.trim()) return;
        
        this.hideDropdown(elementKey);
        
        // Переходим на страницу результатов
        const url = `/properties?q=${encodeURIComponent(query)}`;
        window.location.href = url;
    }
    
    showErrorMessage(message, elementKey) {
        const dropdown = this.elements[elementKey].dropdown;
        dropdown.innerHTML = `
            <div class="p-4 text-center text-red-500">
                <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div class="text-sm">${message}</div>
            </div>
        `;
        this.showDropdown(elementKey);
    }
    
    // Публичный API для интеграции
    getMetrics() {
        return { ...this.metrics };
    }
    
    clearCache() {
        Object.values(this.cache).forEach(cache => cache.clear());
        console.log('Cache cleared');
    }
    
    destroy() {
        // Очистка ресурсов
        Object.values(this.elements).forEach(element => {
            if (element.debounceTimer) {
                clearTimeout(element.debounceTimer);
            }
        });
        
        if (this.state.abortController) {
            this.state.abortController.abort();
        }
        
        console.log('SuperSearch destroyed');
    }
}

// Инициализация
let superSearchInstance;

document.addEventListener('DOMContentLoaded', () => {
    superSearchInstance = new SuperSearch();
    
    // Делаем доступным глобально для отладки
    window.superSearch = superSearchInstance;
});

// Экспорт для модулей
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SuperSearch;
}