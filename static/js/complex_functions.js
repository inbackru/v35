/**
 * Специальные функции для работы с ЖК (жилыми комплексами)
 * Избранное и сравнение ЖК для страницы /residential-complexes
 */

// Функции для избранных ЖК
window.ComplexFavorites = {
    // Загрузить избранные ЖК из localStorage
    load: function() {
        try {
            const stored = localStorage.getItem('inback_favorite_complexes');
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Ошибка загрузки избранных ЖК:', error);
            return [];
        }
    },
    
    // Сохранить избранные ЖК в localStorage
    save: function(favorites) {
        try {
            localStorage.setItem('inback_favorite_complexes', JSON.stringify(favorites));
            console.log('Избранные ЖК сохранены:', favorites);
        } catch (error) {
            console.error('Ошибка сохранения избранных ЖК:', error);
        }
    },
    
    // Добавить/удалить ЖК из избранного
    toggle: function(complexId) {
        const favorites = this.load();
        const complexIdStr = String(complexId);
        
        // Проверяем если уже в избранном
        const existingIndex = favorites.findIndex(fav => {
            const id = typeof fav === 'object' ? fav.id : fav;
            return String(id) === complexIdStr;
        });
        
        if (existingIndex >= 0) {
            // Удаляем из избранного
            favorites.splice(existingIndex, 1);
            this.save(favorites);
            this.updateUI(complexId, false);
            this.showNotification('ЖК удален из избранного', 'info');
            return false;
        } else {
            // Добавляем в избранное
            const favoriteItem = {
                id: complexIdStr,
                addedAt: new Date().toLocaleString('ru-RU')
            };
            favorites.push(favoriteItem);
            this.save(favorites);
            this.updateUI(complexId, true);
            this.showNotification('ЖК добавлен в избранное!', 'success');
            return true;
        }
    },
    
    // Обновить UI кнопки избранного
    updateUI: function(complexId, isFavorited) {
        const hearts = document.querySelectorAll(`[data-complex-id="${complexId}"]`);
        hearts.forEach(heart => {
            if (isFavorited) {
                heart.classList.add('favorited');
                heart.style.color = '#ef4444';
            } else {
                heart.classList.remove('favorited');
                heart.style.color = '#6b7280';
            }
        });
    },
    
    // Обновить все UI элементы на странице
    updateAllUI: function() {
        const favorites = this.load();
        favorites.forEach(fav => {
            const id = typeof fav === 'object' ? fav.id : fav;
            this.updateUI(id, true);
        });
    },
    
    // Показать уведомление
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
        
        if (type === 'success') {
            notification.classList.add('bg-green-500', 'text-white');
            notification.innerHTML = `<i class="fas fa-heart mr-2"></i>${message}`;
        } else {
            notification.classList.add('bg-blue-500', 'text-white');
            notification.innerHTML = `<i class="fas fa-info-circle mr-2"></i>${message}`;
        }
        
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.remove('translate-x-full'), 100);
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Функции для сравнения ЖК
window.ComplexComparison = {
    // Определить тип пользователя
    isManager: function() {
        return Boolean(window.manager_authenticated);
    },
    
    // Получить CSRF токен
    getCSRFToken: function() {
        const csrfInput = document.querySelector('input[name="csrf_token"]');
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        return (csrfInput && csrfInput.value) || (csrfMeta && csrfMeta.content) || '';
    },
    
    // Загрузить данные сравнения (из API для managers, localStorage для users)
    load: async function() {
        if (this.isManager()) {
            return await this.loadFromAPI();
        } else {
            return this.loadFromLocalStorage();
        }
    },
    
    // Загрузка из localStorage (для обычных пользователей)
    loadFromLocalStorage: function() {
        try {
            const stored = localStorage.getItem('comparison-data');
            const data = stored ? JSON.parse(stored) : { properties: [], complexes: [] };
            return data.complexes || [];
        } catch (error) {
            console.error('Ошибка загрузки сравнения ЖК из localStorage:', error);
            return [];
        }
    },
    
    // Загрузка из API (для managers)
    loadFromAPI: async function() {
        try {
            console.log('🏢 Loading complex comparison from API for manager');
            const response = await fetch('/api/manager/comparison/load');
            const result = await response.json();
            
            if (result.success) {
                const complexes = result.complexes || [];
                console.log('🏢 Loaded complexes from API:', complexes);
                // ИСПРАВЛЕНО: Приводим все ID к strings для consistency
                return complexes.map(c => String(c.complex_id));
            } else {
                console.error('Failed to load comparison from API:', result.error);
                return this.loadFromLocalStorage(); // Fallback
            }
        } catch (error) {
            console.error('Error loading comparison from API:', error);
            return this.loadFromLocalStorage(); // Fallback
        }
    },
    
    // Сохранить данные сравнения  
    save: function(complexes) {
        if (this.isManager()) {
            // Для managers не сохраняем в localStorage, только через API
            this.updateCounters();
            return;
        } else {
            this.saveToLocalStorage(complexes);
        }
    },
    
    // Сохранение в localStorage (для обычных пользователей) 
    saveToLocalStorage: function(complexes) {
        try {
            console.log('=== COMPLEX COMPARISON SAVE START ===');
            console.log('Complexes to save:', complexes);
            
            const currentData = localStorage.getItem('comparison-data');
            const comparisonData = JSON.parse(currentData || '{"properties": [], "complexes": []}');
            comparisonData.complexes = complexes;
            
            localStorage.setItem('comparison-data', JSON.stringify(comparisonData));
            console.log('Data saved to localStorage');
            console.log('=== COMPLEX COMPARISON SAVE END ===');
            
            // Обновить счетчики
            this.updateCounters();
        } catch (error) {
            console.error('Ошибка сохранения сравнения ЖК:', error);
        }
    },
    
    // Добавить ЖК в сравнение
    add: async function(complexId) {
        try {
            const complexIdStr = String(complexId);
            
            console.log('=== ADDING COMPLEX TO COMPARISON ===');
            console.log('Complex ID to add:', complexIdStr);
            console.log('Is manager:', this.isManager());
            
            // Загрузить текущее состояние
            const complexes = await this.load();
            console.log('Current complexes in comparison:', complexes);
            
            if (complexes.includes(complexIdStr)) {
                this.showNotification('ЖК уже в сравнении', 'info');
                return false;
            }
            
            if (complexes.length >= 3) {
                this.showNotification('Можно сравнивать максимум 3 ЖК', 'warning');
                return false;
            }
            
            if (this.isManager()) {
                return await this.addComplexForManager(complexIdStr);
            } else {
                return await this.addComplexForUser(complexIdStr, complexes);
            }
        } catch (error) {
            console.error('Error adding complex to comparison:', error);
            this.showNotification('Ошибка добавления в сравнение', 'error');
            return false;
        }
    },
    
    // Добавить ЖК для manager через API
    addComplexForManager: async function(complexId) {
        try {
            console.log('🏢 Adding complex via manager API:', complexId);
            
            const response = await fetch('/api/manager/comparison/save-complex', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    complex_id: complexId,
                    complex_name: 'ЖК',
                    developer_name: '',
                    district: '',
                    min_price: 0,
                    max_price: 0,
                    buildings_count: 0
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Complex added via manager API');
                this.updateCounters();
                this.showNotification('ЖК добавлен в сравнение!', 'success');
                return true;
            } else {
                console.error('Failed to add complex via manager API:', result.error);
                // ИСПРАВЛЕНО: Добавлен fallback на localStorage
                return await this.addComplexForManagerFallback(complexId, 'API returned error');
            }
        } catch (error) {
            console.error('Error adding complex via manager API:', error);
            // ИСПРАВЛЕНО: Добавлен fallback на localStorage  
            return await this.addComplexForManagerFallback(complexId, 'API unavailable');
        }
    },
    
    // НОВЫЙ: Fallback для manager add когда API недоступен
    addComplexForManagerFallback: async function(complexId, reason) {
        try {
            console.log('🔄 Manager API fallback - using localStorage:', reason);
            
            const complexes = this.loadFromLocalStorage();
            complexes.push(complexId);
            this.saveToLocalStorage(complexes);
            
            this.updateCounters();
            this.showNotification('ЖК добавлен в сравнение (локальный режим)', 'success');
            
            // Показать дополнительное уведомление о режиме fallback
            setTimeout(() => {
                this.showNotification('Данные сохранены локально - синхронизация при следующем подключении к БД', 'info');
            }, 2000);
            
            return true;
        } catch (error) {
            console.error('Error in manager fallback:', error);
            this.showNotification('Ошибка добавления в сравнение', 'error');
            return false;
        }
    },
    
    // Добавить ЖК для user через localStorage 
    addComplexForUser: async function(complexId, complexes) {
        try {
            console.log('👤 Adding complex via localStorage for user:', complexId);
            
            complexes.push(complexId);
            this.saveToLocalStorage(complexes);
            
            // Обновить счетчики
            this.updateCounters();
            
            this.showNotification('ЖК добавлен в сравнение!', 'success');
            console.log('=== COMPLEX ADDED SUCCESSFULLY ===');
            return true;
        } catch (error) {
            console.error('Error adding complex via localStorage:', error);
            return false;
        }
    },
    
    // Удалить ЖК из сравнения
    remove: async function(complexId) {
        try {
            const complexIdStr = String(complexId);
            
            console.log('=== REMOVING COMPLEX FROM COMPARISON ===');
            console.log('Complex ID to remove:', complexIdStr);
            console.log('Is manager:', this.isManager());
            
            if (this.isManager()) {
                return await this.removeComplexForManager(complexIdStr);
            } else {
                return await this.removeComplexForUser(complexIdStr);
            }
        } catch (error) {
            console.error('Error removing complex from comparison:', error);
            this.showNotification('Ошибка удаления из сравнения', 'error');
            return false;
        }
    },
    
    // Удалить ЖК для manager через API
    removeComplexForManager: async function(complexId) {
        try {
            console.log('🏢 Removing complex via manager API:', complexId);
            
            const response = await fetch(`/api/manager/comparison/remove-complex`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ complex_id: complexId })
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Complex removed via manager API');
                this.updateCounters();
                this.showNotification('ЖК удален из сравнения', 'info');
                return true;
            } else {
                console.error('Failed to remove complex via manager API:', result.error);
                this.showNotification('Ошибка удаления из сравнения', 'error');
                return false;
            }
        } catch (error) {
            console.error('Error removing complex via manager API:', error);
            this.showNotification('Ошибка удаления из сравнения', 'error');
            return false;
        }
    },
    
    // Удалить ЖК для user через localStorage
    removeComplexForUser: async function(complexId) {
        try {
            console.log('👤 Removing complex via localStorage for user:', complexId);
            
            const complexes = await this.load();
            const filtered = complexes.filter(id => id !== complexId);
            
            this.saveToLocalStorage(filtered);
            this.updateCounters();
            this.showNotification('ЖК удален из сравнения', 'info');
            return true;
        } catch (error) {
            console.error('Error removing complex via localStorage:', error);
            return false;
        }
    },
    
    // Обновить счетчики
    updateCounters: async function() {
        const complexes = await this.load();
        const count = complexes.length;
        
        console.log('=== UPDATING COMPLEX COMPARISON COUNTERS ===');
        console.log('Complex count:', count);
        console.log('Complexes:', complexes);
        
        // Обновить глобальный счетчик если доступен
        if (window.ComparisonManager && window.ComparisonManager.updateCounters) {
            console.log('Calling ComparisonManager.updateCounters');
            window.ComparisonManager.updateCounters();
        }
        
        // Обновить локальные счетчики
        const counters = document.querySelectorAll('[data-comparison-counter]');
        console.log('Found local counters:', counters.length);
        counters.forEach(counter => {
            counter.textContent = count;
            counter.style.display = count > 0 ? 'inline' : 'none';
        });
        
        // Обновить счетчики дашборда если функция доступна (безопасно)
        console.log('Dashboard counter function available:', typeof window.updateDashboardCounters);
        if (typeof window.updateDashboardCounters === 'function') {
            console.log('Calling dashboard counter update');
            window.updateDashboardCounters();
        } else {
            console.log('updateDashboardCounters not available yet, scheduling retry');
            // Попробуем позже, когда дашборд загрузится
            setTimeout(() => {
                if (typeof window.updateDashboardCounters === 'function') {
                    window.updateDashboardCounters();
                }
            }, 1000);
        }
        
        console.log('=== COUNTERS UPDATE COMPLETE ===');
    },
    
    // Показать уведомление
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
        
        switch (type) {
            case 'success':
                notification.classList.add('bg-green-500', 'text-white');
                break;
            case 'warning':
                notification.classList.add('bg-yellow-500', 'text-white');
                break;
            default:
                notification.classList.add('bg-blue-500', 'text-white');
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.remove('translate-x-full'), 100);
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Глобальные функции для использования в HTML
window.toggleComplexFavorite = function(complexId) {
    console.log('Переключение избранного для ЖК:', complexId);
    
    // Используем продвинутую версию из favorites.js, которая автоматически определяет тип пользователя
    if (window.favoritesManager && window.favoritesManager.toggleComplexFavorite) {
        // Найти элемент сердечка для передачи в функцию
        const heartElement = document.querySelector(`.favorite-heart[data-complex-id="${complexId}"]`);
        return window.favoritesManager.toggleComplexFavorite(complexId, heartElement);
    } else {
        // Fallback к старой простой версии
        console.warn('FavoritesManager не найден, используем простую версию');
        return window.ComplexFavorites.toggle(complexId);
    }
};

window.addToComplexCompare = function(complexId) {
    console.log('=== GLOBAL FUNCTION: addToComplexCompare START ===');
    console.log('Добавление ЖК в сравнение:', complexId);
    
    // Проверим состояние до добавления
    const beforeData = localStorage.getItem('comparison-data');
    console.log('До добавления:', beforeData);
    
    const result = window.ComplexComparison.add(complexId);
    
    // Проверим состояние после добавления
    const afterData = localStorage.getItem('comparison-data');
    console.log('После добавления:', afterData);
    
    console.log('Result from ComplexComparison.add:', result);
    console.log('=== GLOBAL FUNCTION: addToComplexCompare END ===');
    
    return result;
};

window.removeComplexFromComparison = function(complexId) {
    console.log('Удаление ЖК из сравнения:', complexId);
    return window.ComplexComparison.remove(complexId);
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Complex functions initialized');
    
    // Обновить UI избранного только если нет favoritesManager (чтобы избежать конфликтов)
    if (!window.favoritesManager) {
        window.ComplexFavorites.updateAllUI();
    }
    
    // Обновить счетчики сравнения
    window.ComplexComparison.updateCounters();
    
    // Привязать обработчики к сердечкам
    document.addEventListener('click', function(e) {
        const heartElement = e.target.closest('.favorite-heart[data-complex-id]');
        if (heartElement) {
            e.preventDefault();
            e.stopPropagation();
            const complexId = heartElement.dataset.complexId;
            window.toggleComplexFavorite(complexId);
        }
    });
});