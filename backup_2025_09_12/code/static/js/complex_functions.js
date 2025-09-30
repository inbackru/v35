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
    // Загрузить данные сравнения
    load: function() {
        try {
            const stored = localStorage.getItem('comparison-data');
            const data = stored ? JSON.parse(stored) : { properties: [], complexes: [] };
            return data.complexes || [];
        } catch (error) {
            console.error('Ошибка загрузки сравнения ЖК:', error);
            return [];
        }
    },
    
    // Сохранить данные сравнения
    save: function(complexes) {
        try {
            console.log('=== COMPLEX COMPARISON SAVE START ===');
            console.log('Complexes to save:', complexes);
            console.log('Type of complexes:', typeof complexes, Array.isArray(complexes));
            
            const currentData = localStorage.getItem('comparison-data');
            console.log('Current comparison-data before save:', currentData);
            
            const comparisonData = JSON.parse(currentData || '{"properties": [], "complexes": []}');
            console.log('Parsed current data:', comparisonData);
            
            comparisonData.complexes = complexes;
            const newData = JSON.stringify(comparisonData);
            console.log('New data to save:', newData);
            
            localStorage.setItem('comparison-data', newData);
            console.log('Data saved to localStorage');
            
            // Проверим что записалось
            const verification = localStorage.getItem('comparison-data');
            console.log('Verification - what was actually saved:', verification);
            
            // Парсим еще раз для проверки
            const verificationParsed = JSON.parse(verification);
            console.log('Verification parsed complexes:', verificationParsed.complexes);
            
            console.log('Сравнение ЖК сохранено:', complexes);
            console.log('=== COMPLEX COMPARISON SAVE END ===');
            
            // Обновить счетчики
            this.updateCounters();
        } catch (error) {
            console.error('Ошибка сохранения сравнения ЖК:', error);
            console.error('Error stack:', error.stack);
        }
    },
    
    // Добавить ЖК в сравнение
    add: function(complexId) {
        const complexes = this.load();
        const complexIdStr = String(complexId);
        
        console.log('=== ADDING COMPLEX TO COMPARISON ===');
        console.log('Complex ID to add:', complexIdStr);
        console.log('Current complexes in comparison:', complexes);
        
        if (complexes.includes(complexIdStr)) {
            this.showNotification('ЖК уже в сравнении', 'info');
            return false;
        }
        
        if (complexes.length >= 3) {
            this.showNotification('Можно сравнивать максимум 3 ЖК', 'warning');
            return false;
        }
        
        complexes.push(complexIdStr);
        console.log('Updated complexes list:', complexes);
        
        this.save(complexes);
        
        // Проверим что сохранилось
        const saved = this.load();
        console.log('Complexes after save:', saved);
        console.log('Raw localStorage after save:', localStorage.getItem('comparison-data'));
        
        // Обновить глобальные счетчики (безопасно)
        console.log('Trying to update dashboard counters...');
        if (typeof window.updateDashboardCounters === 'function') {
            console.log('Calling window.updateDashboardCounters');
            window.updateDashboardCounters();
        } else {
            console.log('updateDashboardCounters not available yet, will try later');
            // Попробуем позже, когда дашборд загрузится
            setTimeout(() => {
                if (typeof window.updateDashboardCounters === 'function') {
                    window.updateDashboardCounters();
                }
            }, 1000);
        }
        
        // Попробуем обновить счетчики через ComparisonManager
        if (window.ComparisonManager && window.ComparisonManager.updateCounters) {
            console.log('Calling ComparisonManager.updateCounters');
            window.ComparisonManager.updateCounters();
        } else {
            console.log('ComparisonManager not available');
        }
        
        this.showNotification('ЖК добавлен в сравнение!', 'success');
        console.log('=== COMPLEX ADDED SUCCESSFULLY ===');
        return true;
    },
    
    // Удалить ЖК из сравнения
    remove: function(complexId) {
        const complexes = this.load();
        const complexIdStr = String(complexId);
        const filtered = complexes.filter(id => id !== complexIdStr);
        
        this.save(filtered);
        this.showNotification('ЖК удален из сравнения', 'info');
    },
    
    // Обновить счетчики
    updateCounters: function() {
        const complexes = this.load();
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
    return window.ComplexFavorites.toggle(complexId);
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
    
    // Обновить UI избранного
    window.ComplexFavorites.updateAllUI();
    
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