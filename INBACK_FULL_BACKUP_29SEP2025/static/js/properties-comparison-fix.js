// ОКОНЧАТЕЛЬНОЕ РЕШЕНИЕ для кнопок сравнения с PostgreSQL
console.log('🚀 ЗАГРУЖАЕТСЯ PostgreSQL РЕШЕНИЕ - ВЕРСИЯ с ЖК поддержкой');

// Создаем менеджер сравнения с поддержкой PostgreSQL
class SimpleComparisonManager {
    constructor() {
        this.comparisons = [];
        this.complexComparisons = [];
        this.isManager = this.checkIsManager();
        console.log('📦 PostgreSQL Comparison Manager инициализирован. Менеджер:', this.isManager);
        this.loadFromDatabase();
    }
    
    checkIsManager() {
        // ✅ ИСПРАВЛЕНО: Используем только официальную переменную
        // Убираем проверку несуществующей window.isManager
        const result = Boolean(window.manager_authenticated);
        console.log('🔍 Manager status check (FIXED):', {
            manager_authenticated: window.manager_authenticated,
            result: result
        });
        return result;
    }
    
    // Helper function to get CSRF token from meta tag
    getCSRFToken() {
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) {
            return csrfMeta.getAttribute('content');
        }
        
        // Fallback check for other possible CSRF token locations
        const csrfInput = document.querySelector('input[name="csrf_token"]');
        if (csrfInput) {
            return csrfInput.value;
        }
        
        console.warn('CSRF token not found in page');
        return null;
    }
    
    // ✅ НОВЫЙ МЕТОД: Попробовать БД сначала, независимо от isManager флага
    async tryDatabaseFirst() {
        try {
            // Use appropriate endpoint based on user type
            const endpoint = this.isManager ? '/api/manager/comparison/load' : '/api/comparison/load';
            const testResponse = await fetch(endpoint);
            if (testResponse.ok) {
                const data = await testResponse.json();
                if (data.success) {
                    console.log('✅ БД доступна для пользователя');
                    return true;
                }
            }
        } catch (error) {
            console.log('ℹ️ БД недоступна, используем localStorage');
        }
        return false;
    }
    
    async loadFromDatabase() {
        try {
            console.log('🔍 Загружаем сравнение из PostgreSQL...');
            // Use appropriate endpoint based on user type
            const endpoint = this.isManager ? '/api/manager/comparison/load' : '/api/comparison/load';
            const response = await fetch(endpoint);
            const data = await response.json();
            
            if (data.success) {
                // ✅ ИСПРАВЛЕНО: Получаем данные API
                const apiProperties = data.properties.map(p => String(p.property_id)) || [];
                const apiComplexes = data.complexes.map(c => String(c.complex_id)) || [];
                
                console.log('✅ Загружено из API - квартиры:', apiProperties.length, 'ЖК:', apiComplexes.length);
                
                // ✅ НОВОЕ: Проверяем конфликт с localStorage и очищаем при необходимости
                await this.syncWithLocalStorage(apiProperties, apiComplexes);
                
                // Устанавливаем данные API как приоритетные
                this.comparisons = apiProperties;
                this.complexComparisons = apiComplexes;
                
            } else {
                console.log('ℹ️ БД недоступна, используем localStorage fallback');
                this.loadFromStorage();
            }
        } catch (error) {
            console.error('❌ Ошибка загрузки из БД:', error);
            console.log('🔄 Fallback на localStorage');
            this.loadFromStorage(); // Fallback на localStorage
        }
        this.updateCounter();
        // ✅ ИСПРАВЛЕНО: Обновляем UI кнопок после загрузки данных из БД
        this.updateComparisonUI();
    }
    
    // ✅ НОВЫЙ МЕТОД: Синхронизация API данных с localStorage
    async syncWithLocalStorage(apiProperties, apiComplexes) {
        try {
            // Загружаем текущие данные localStorage
            const localProperties = JSON.parse(localStorage.getItem('comparisons') || '[]');
            const localComplexes = JSON.parse(localStorage.getItem('comparison_complexes') || '[]');
            
            // Проверяем конфликты
            const propertiesConflict = JSON.stringify(localProperties.sort()) !== JSON.stringify(apiProperties.sort());
            const complexesConflict = JSON.stringify(localComplexes.sort()) !== JSON.stringify(apiComplexes.sort());
            
            if (propertiesConflict || complexesConflict) {
                console.log('🔄 КОНФЛИКТ ОБНАРУЖЕН! API имеет приоритет над localStorage');
                console.log('📊 localStorage квартиры:', localProperties.length, '→ API квартиры:', apiProperties.length);
                console.log('📊 localStorage ЖК:', localComplexes.length, '→ API ЖК:', apiComplexes.length);
                
                // ✅ ИСПРАВЛЕНИЕ: Принудительно обновляем localStorage данными API
                localStorage.setItem('comparisons', JSON.stringify(apiProperties));
                localStorage.setItem('comparison_complexes', JSON.stringify(apiComplexes));
                
                // Очищаем старые ключи
                localStorage.removeItem('comparison_properties');
                localStorage.removeItem('comparison-data');
                
                console.log('✅ localStorage синхронизирован с API данными');
            } else {
                console.log('✅ localStorage и API данные синхронизированы');
            }
        } catch (error) {
            console.error('❌ Ошибка синхронизации localStorage:', error);
        }
    }
    
    loadFromStorage() {
        try {
            const saved = localStorage.getItem('comparisons');
            this.comparisons = saved ? JSON.parse(saved) : [];
            
            const savedComplexes = localStorage.getItem('comparison_complexes');
            this.complexComparisons = savedComplexes ? JSON.parse(savedComplexes) : [];
            
            console.log('📦 Загружено из localStorage - квартиры:', this.comparisons.length, 'ЖК:', this.complexComparisons.length);
        } catch (e) {
            this.comparisons = [];
            this.complexComparisons = [];
        }
    }
    
    saveToStorage() {
        try {
            localStorage.setItem('comparisons', JSON.stringify(this.comparisons));
            localStorage.setItem('comparison_complexes', JSON.stringify(this.complexComparisons));
        } catch (e) {
            console.error('Ошибка сохранения в localStorage:', e);
        }
    }
    
    async toggleComparison(propertyId, button) {
        const id = String(propertyId);
        const index = this.comparisons.indexOf(id);
        
        try {
            if (index > -1) {
                // Удаляем из сравнения
                let dbSuccess = false;
                try {
                    await this.removePropertyFromDatabase(id);
                    dbSuccess = true;
                    console.log('✅ Квартира удалена из PostgreSQL БД:', id);
                } catch (dbError) {
                    console.log('ℹ️ БД недоступна для удаления, используем localStorage:', dbError.message);
                }
                
                this.comparisons.splice(index, 1);
                console.log('➖ Удален из сравнения:', id);
                this.showNotification(dbSuccess ? 'Объект удален из сравнения (БД)' : 'Объект удален из сравнения (локально)');
                this.updateButtonState(button, false);
            } else {
                // Добавляем в сравнение
                let dbSuccess = false;
                try {
                    await this.addPropertyToDatabase(id);
                    dbSuccess = true;
                    console.log('✅ Квартира добавлена в PostgreSQL БД:', id);
                } catch (dbError) {
                    console.log('ℹ️ БД недоступна для добавления, используем localStorage:', dbError.message);
                }
                
                this.comparisons.push(id);
                console.log('➕ Добавлен в сравнение:', id);
                this.showNotification(dbSuccess ? 'Объект добавлен в сравнение (БД)' : 'Объект добавлен в сравнение (локально)');
                this.updateButtonState(button, true);
            }
        } catch (error) {
            console.error('❌ Критическая ошибка операции:', error);
            this.showNotification('Ошибка! Попробуйте позже');
            return; // Не обновляем состояние при ошибке
        }
        
        this.saveToStorage(); // Дублируем в localStorage как backup
        this.updateCounter();
    }
    
    async addPropertyToDatabase(propertyId) {
        // Use appropriate endpoint based on user type
        const endpoint = this.isManager ? '/api/manager/comparison/save-property' : '/api/comparison/save-property';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                property_id: propertyId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Database error');
        }
        
        console.log('✅ Квартира добавлена в БД:', propertyId);
    }
    
    async removePropertyFromDatabase(propertyId) {
        // Use appropriate endpoint based on user type
        const endpoint = this.isManager ? '/api/manager/comparison/remove-property' : '/api/comparison/remove-property';
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                property_id: propertyId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Database error');
        }
        
        console.log('✅ Квартира удалена из БД:', propertyId);
    }
    
    getCSRFToken() {
        // Пытаемся найти CSRF токен на странице
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) {
            return csrfMeta.getAttribute('content');
        }
        
        const csrfInput = document.querySelector('input[name="csrf_token"]');
        if (csrfInput) {
            return csrfInput.value;
        }
        
        // Генерируем простой токен если не найден (для compatibility)
        return 'simple-token-' + Date.now();
    }
    
    updateButtonState(button, isActive) {
        if (isActive) {
            button.style.backgroundColor = '#2563eb';
            button.style.borderColor = '#2563eb';
            button.style.color = 'white';
        } else {
            button.style.backgroundColor = 'white';
            button.style.borderColor = '#d1d5db';
            button.style.color = '#6b7280';
        }
    }
    
    async toggleComplexComparison(complexId, button) {
        const id = String(complexId);
        const index = this.complexComparisons.indexOf(id);
        
        try {
            if (index > -1) {
                // Удаляем ЖК из сравнения
                let dbSuccess = false;
                try {
                    await this.removeComplexFromDatabase(id);
                    dbSuccess = true;
                    console.log('✅ ЖК удален из PostgreSQL БД:', id);
                } catch (dbError) {
                    console.log('ℹ️ БД недоступна для удаления, используем localStorage:', dbError.message);
                }
                
                this.complexComparisons.splice(index, 1);
                console.log('➖ ЖК удален из сравнения:', id);
                this.showNotification(dbSuccess ? 'ЖК удален из сравнения (БД)' : 'ЖК удален из сравнения (локально)');
                // ✅ ЗАЩИТА: Обновляем кнопку только если она существует
                if (button) {
                    this.updateButtonState(button, false);
                } else {
                    console.log('ℹ️ Кнопка не найдена, обновление визуального состояния пропущено');
                }
            } else {
                // Добавляем ЖК в сравнение
                let dbSuccess = false;
                try {
                    await this.addComplexToDatabase(id);
                    dbSuccess = true;
                    console.log('✅ ЖК добавлен в PostgreSQL БД:', id);
                } catch (dbError) {
                    console.log('ℹ️ БД недоступна для добавления, используем localStorage:', dbError.message);
                }
                
                this.complexComparisons.push(id);
                console.log('➕ ЖК добавлен в сравнение:', id);
                this.showNotification(dbSuccess ? 'ЖК добавлен в сравнение (БД)' : 'ЖК добавлен в сравнение (локально)');
                // ✅ ЗАЩИТА: Обновляем кнопку только если она существует
                if (button) {
                    this.updateButtonState(button, true);
                } else {
                    console.log('ℹ️ Кнопка не найдена, обновление визуального состояния пропущено');
                }
            }
        } catch (error) {
            console.error('❌ Критическая ошибка операции с ЖК:', error);
            this.showNotification('Ошибка! Попробуйте позже');
            return;
        }
        
        this.saveToStorage();
        this.updateCounter();
    }
    
    async addComplexToDatabase(complexId) {
        // ✅ ПОЛУЧАЕМ ПОЛНЫЕ ДАННЫЕ ЖК ИЗ DOM
        const complexData = this.getComplexDataFromDOM(complexId);
        
        // Use appropriate endpoint based on user type
        const endpoint = this.isManager ? '/api/manager/comparison/save-complex' : '/api/comparison/save-complex';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                complex_id: complexId,
                complex_name: complexData.name || '',
                developer_name: complexData.developer_name || '',
                district: complexData.district || '',
                min_price: complexData.min_price || 0,
                max_price: complexData.max_price || 0,
                photo: complexData.photo || '',
                buildings_count: complexData.buildings_count || 0,
                apartments_count: complexData.apartments_count || 0,
                completion_date: complexData.completion_date || '',
                status: complexData.status || '',
                complex_class: complexData.complex_class || ''
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Database error');
        }
        
        console.log('✅ ЖК добавлен в БД с данными:', complexId, complexData);
    }
    
    // ✅ ИСПРАВЛЕННЫЙ МЕТОД: Извлекает данные ЖК из DOM элемента
    getComplexDataFromDOM(complexId) {
        console.log('🔍 === ВХОД В getComplexDataFromDOM ===', complexId);
        try {
            // Робастный поиск карточки ЖК
            let complexCard = document.querySelector(`[data-complex-id="${complexId}"]`) || 
                             document.querySelector(`[data-id="${complexId}"]`);
            
            if (!complexCard) {
                console.log('⚠️ Карточка ЖК не найдена для ID:', complexId);
                console.log('🔍 Попробуем поиск по всем карточкам...');
                // Поиск среди всех комплексных карточек
                const allCards = document.querySelectorAll('.complex-card, [class*="complex"]');
                console.log('📦 Найдено карточек:', allCards.length);
                return {};
            }
            
            // Поднимаемся к корневой карточке ЖК
            const card = complexCard.closest('.bg-white') || complexCard.closest('.shadow-lg') || 
                        complexCard.closest('div[class*="rounded"]') || complexCard.parentElement?.parentElement;
            
            if (!card) {
                console.log('⚠️ Корневая карточка не найдена для ID:', complexId);
                return {};
            }
            
            console.log('🔍 Найдена карточка ЖК для анализа:', complexId);
            
            const extractText = (selector) => {
                const element = card.querySelector(selector);
                const text = element ? element.textContent.trim() : '';
                console.log(`📝 Селектор "${selector}": "${text}"`);
                return text;
            };
            
            // ✅ ИСПРАВЛЕННЫЕ СЕЛЕКТОРЫ ПО РЕКОМЕНДАЦИЯМ АРХИТЕКТОРА
            
            // Название ЖК: <h3 class="text-lg font-bold text-gray-900 mb-1">
            const name = extractText('h3.text-lg.font-bold') || 
                         extractText('h3') || 
                         extractText('.text-lg.font-bold') || '';
                         
            // Застройщик: ИСПРАВЛЕНО - сначала по href, потом по цвету
            const developer = extractText('a[href*="/developer/"]') || 
                             extractText('p.text-gray-500.text-sm') || 
                             extractText('a[class*="text-[#0088CC]"]') || '';
                            
            // Район: ИСПРАВЛЕНО - робастные fallbacks для разных HTML структур
            const locationSelectors = [
                'i.fa-map-marker-alt', 'i.fa-location-dot', 
                'i[class*="map"]', 'i[class*="location"]',
                '[class*="location"]', '[class*="map"]'
            ];
            let district = '';
            for (const selector of locationSelectors) {
                const element = card.querySelector(selector);
                if (element) {
                    // Множественные fallback стратегии:
                    // 1. Текст из соседнего span
                    const siblingSpan = element.parentElement?.querySelector('span');
                    if (siblingSpan) district = siblingSpan.textContent.trim();
                    
                    // 2. Текст из родительского элемента (убираем иконку)
                    if (!district && element.parentElement) {
                        const parentText = element.parentElement.textContent.trim();
                        const iconText = element.textContent.trim();
                        district = parentText.replace(iconText, '').trim();
                    }
                    
                    // 3. Следующий текстовый узел
                    if (!district && element.nextSibling) {
                        district = element.nextSibling.textContent?.trim() || '';
                    }
                    
                    if (district) {
                        console.log(`🏠 Найден район с селектором "${selector}": "${district}"`);
                        break;
                    }
                }
            }
            
            // Цены: ИСПРАВЛЕНО - более надежный парсинг
            let min_price = 0, max_price = 0;
            const allPrices = [];
            
            // 1. Основная цена из ценника
            const mainPriceText = extractText('.bg-orange-50') || extractText('[class*="bg-orange"]') || '';
            console.log('💰 Основная цена:', mainPriceText);
            
            // 2. Цены из кнопок квартир
            const roomButtons = card.querySelectorAll('button[data-room-type]');
            roomButtons.forEach(button => {
                const priceText = button.querySelector('.text-\\[\\#0088CC\\]')?.textContent || 
                                 button.querySelector('[class*="text-blue"]')?.textContent || '';
                if (priceText) console.log('💰 Текст кнопки:', priceText);
            });
            
            // 3. ИСПРАВЛЕНО - корректная нормализация цен
            
            // Помощник для нормализации цен
            const normalizePrice = (text, unit) => {
                if (!text) return 0;
                
                // Убираем все кроме цифр, коммы и точек
                let cleanText = text.replace(/[^\d.,]/g, '');
                
                // Если есть единица (млн/тыс), обрабатываем как десятичное число
                if (unit) {
                    // Заменяем комму на точку для десятичного числа
                    cleanText = cleanText.replace(',', '.');
                    let price = parseFloat(cleanText);
                    
                    if (unit === 'млн') price *= 1000000;
                    else if (unit === 'тыс') price *= 1000;
                    
                    return price || 0;
                } else {
                    // Нет единицы - считаем что это рубли, убираем все кроме цифр
                    cleanText = cleanText.replace(/[^\d]/g, '');
                    return parseInt(cleanText) || 0;
                }
            };
            
            // Парсим основную цену
            const mainPriceMatch = mainPriceText.match(/от\s*([\d.,\s]+)\s*(млн|тыс)?/i);
            if (mainPriceMatch) {
                const price = normalizePrice(mainPriceMatch[1], mainPriceMatch[2]);
                if (price > 0) {
                    allPrices.push(price);
                    console.log('💰 Основная цена:', price);
                }
            }
            
            // Парсим цены из кнопок
            roomButtons.forEach(button => {
                const priceText = button.querySelector('.text-\\[\\#0088CC\\]')?.textContent || 
                                 button.querySelector('[class*="text-blue"]')?.textContent || '';
                const priceMatch = priceText.match(/от\s*([\d.,\s]+)\s*(млн|тыс)?/i);
                if (priceMatch) {
                    const price = normalizePrice(priceMatch[1], priceMatch[2]);
                    if (price > 0) {
                        allPrices.push(price);
                        console.log('💰 Цена из кнопки:', price);
                    }
                }
            });
            
            // Fallback: поиск по всему тексту только если ничего не нашли
            if (allPrices.length === 0) {
                const fullCardText = card.textContent || '';
                const priceMatches = fullCardText.match(/от\s*([\d\s]+)\s*(млн|тыс|₽)?/gi) || [];
                
                priceMatches.forEach(match => {
                    const numMatch = match.match(/от\s*([\d\s]+)\s*(млн|тыс|₽)?/i);
                    if (numMatch) {
                        const price = normalizePrice(numMatch[1], numMatch[2]);
                        if (price > 0) {
                            allPrices.push(price);
                            console.log('💰 Fallback цена:', price, 'из', match);
                        }
                    }
                });
            }
            
            if (allPrices.length > 0) {
                min_price = Math.min(...allPrices);
                max_price = Math.max(...allPrices);
            }
            
            // ✅ ДОБАВЛЕНО: Извлечение дополнительных полей ЖК
            
            // Фото: первое изображение из слайдера
            const photoElement = card.querySelector('.complex-slider img') || card.querySelector('img');
            const photo = photoElement ? photoElement.src : '';
            
            // Количество корпусов: из сетки статистики
            let buildings_count = 0;
            const buildingsText = extractText('.grid .font-medium') || card.textContent;
            const buildingsMatch = buildingsText.match(/корпусов?[^\d]*(\d+)/i);
            if (buildingsMatch) {
                buildings_count = parseInt(buildingsMatch[1]) || 0;
            }
            
            // Количество квартир: из сетки статистики  
            let apartments_count = 0;
            const apartmentsText = extractText('.grid .font-medium') || card.textContent;
            const apartmentsMatch = apartmentsText.match(/квартир?[^\d]*(\d+)/i);
            if (apartmentsMatch) {
                apartments_count = parseInt(apartmentsMatch[1]) || 0;
            }
            
            // Срок сдачи: ищем элемент с календарем
            let completion_date = '';
            const calendarSelectors = [
                'i.fa-calendar', 
                'i[class*="calendar"]', 
                '[class*="completion"]'
            ];
            for (const selector of calendarSelectors) {
                const element = card.querySelector(selector);
                if (element) {
                    const parentText = element.parentElement?.textContent.trim() || '';
                    const iconText = element.textContent.trim();
                    completion_date = parentText.replace(iconText, '').trim();
                    if (completion_date) break;
                }
            }
            
            // Статус: из цветных span элементов
            let status = '';
            const statusElement = card.querySelector('.bg-green-50') || 
                                 card.querySelector('.bg-orange-50') ||
                                 card.querySelector('[class*="bg-green"]') ||
                                 card.querySelector('[class*="bg-orange"]');
            if (statusElement) {
                status = statusElement.textContent.trim();
                // Нормализация статуса
                if (status.includes('Готов') || status.includes('Сдан')) {
                    status = 'Сдан';
                } else {
                    status = 'Строится';
                }
            }
            
            // Класс ЖК: из текста карточки
            let complex_class = '';
            // Поиск класса в тексте карточки
            const cardText = card.textContent.toLowerCase();
            if (cardText.includes('бизнес')) {
                complex_class = 'Бизнес';
            } else if (cardText.includes('эконом')) {
                complex_class = 'Эконом';
            } else {
                complex_class = 'Комфорт';  // По умолчанию
            }
            
            // ✅ ИСПРАВЛЕНО: поле developer_name вместо developer для совместимости с ComparisonComplex API
            const result = {
                name: name,
                developer_name: developer,
                district: district,
                min_price: min_price,
                max_price: max_price,
                photo: photo,
                buildings_count: buildings_count,
                apartments_count: apartments_count,
                completion_date: completion_date,
                status: status,
                complex_class: complex_class
            };
            
            console.log('✅ ФИНАЛЬНЫЕ данные ЖК (РАСШИРЕННЫЕ):', complexId, result);
            return result;
            
        } catch (error) {
            console.error('❌ Ошибка извлечения данных ЖК:', error);
            return {};
        }
    }
    
    async removeComplexFromDatabase(complexId) {
        // Use appropriate endpoint based on user type
        const endpoint = this.isManager ? '/api/manager/comparison/remove-complex' : '/api/comparison/remove-complex';
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                complex_id: complexId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Database error');
        }
        
        console.log('✅ ЖК удален из БД:', complexId);
    }
    
    updateCounter() {
        // Обновляем счетчик в верхнем меню
        const counter = document.querySelector('#comparison-counter');
        const totalCount = this.comparisons.length + this.complexComparisons.length;
        if (counter) {
            counter.textContent = totalCount;
            counter.style.display = totalCount > 0 ? 'inline' : 'none';
        }
        console.log('🔢 Счетчик обновлен:', totalCount, '(квартиры:', this.comparisons.length, 'ЖК:', this.complexComparisons.length, ')');
    }
    
    showNotification(message) {
        // Простое уведомление
        const notification = document.createElement('div');
        notification.innerHTML = `
            <div style="position: fixed; top: 20px; right: 20px; background: #10b981; color: white; padding: 12px 20px; border-radius: 8px; font-weight: 500; z-index: 10000; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                ✅ ${message}
            </div>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// Инициализация НЕМЕДЛЕННО при загрузке скрипта
console.log('🔧 НЕМЕДЛЕННАЯ инициализация кнопок сравнения');

// Функция безопасной инициализации
function safeInit() {
    if (document.readyState === 'loading') {
        // DOM еще загружается
        document.addEventListener('DOMContentLoaded', actualInit);
    } else {
        // DOM уже загружен
        actualInit();
    }
}

function actualInit() {
    console.log('🔧 Инициализируем кнопки сравнения...');
    
    // Создаем простой менеджер
    window.simpleComparisonManager = new SimpleComparisonManager();
    
    // Инициализируем кнопки
    setTimeout(() => {
        initAllComparisonButtons();
        console.log('✅ Система сравнения полностью готова к работе');
    }, 100);
}

// Запускаем инициализацию
safeInit();

function initAllComparisonButtons() {
    // ОЧИЩАЕМ ВСЕ СТАРЫЕ ОБРАБОТЧИКИ (property buttons)
    document.querySelectorAll('.compare-btn').forEach(btn => {
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
    });
    
    // ОЧИЩАЕМ ВСЕ СТАРЫЕ ОБРАБОТЧИКИ (complex buttons)
    document.querySelectorAll('.compare-btn[data-complex-id]').forEach(btn => {
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
    });
    
    // ДОБАВЛЯЕМ НОВЫЕ ЧИСТЫЕ ОБРАБОТЧИКИ ДЛЯ КВАРТИР
    const propertyButtons = document.querySelectorAll('.compare-btn');
    console.log(`🏠 Инициализируем ${propertyButtons.length} кнопок сравнения квартир`);
    
    propertyButtons.forEach((btn, index) => {
        const propertyId = btn.getAttribute('data-property-id');
        
        if (propertyId) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                
                console.log(`🚀 КЛИК по кнопке квартиры: ${propertyId}`);
                
                if (window.simpleComparisonManager) {
                    window.simpleComparisonManager.toggleComparison(propertyId, btn);
                }
            });
            
            // Проверяем состояние кнопки
            const isInComparison = window.simpleComparisonManager?.comparisons.includes(String(propertyId));
            if (isInComparison) {
                window.simpleComparisonManager.updateButtonState(btn, true);
            }
            
            console.log(`✅ Кнопка квартиры ${index + 1} готова: ${propertyId}`);
        }
    });
    
    // ДОБАВЛЯЕМ НОВЫЕ ЧИСТЫЕ ОБРАБОТЧИКИ ДЛЯ ЖК
    const complexButtons = document.querySelectorAll('.compare-btn[data-complex-id]');
    console.log(`🏢 Инициализируем ${complexButtons.length} кнопок сравнения ЖК`);
    
    complexButtons.forEach((btn, index) => {
        const complexId = btn.getAttribute('data-complex-id');
        
        if (complexId) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                
                console.log(`🚀 КЛИК по кнопке ЖК: ${complexId}`);
                
                if (window.simpleComparisonManager) {
                    window.simpleComparisonManager.toggleComplexComparison(complexId, btn);
                }
            });
            
            // Проверяем состояние кнопки ЖК
            const isInComparison = window.simpleComparisonManager?.complexComparisons.includes(String(complexId));
            if (isInComparison) {
                window.simpleComparisonManager.updateButtonState(btn, true);
            }
            
            console.log(`✅ Кнопка ЖК ${index + 1} готова: ${complexId}`);
        }
    });
}

// Функция для реинициализации после пагинации  
window.reinitComparisonButtons = function() {
    console.log('🔄 Переинициализация после пагинации');
    setTimeout(() => {
        initAllComparisonButtons();
    }, 200);
};

// ФУНКЦИЯ ДЛЯ ЖК КНОПОК (используется в onclick="addToComplexCompare(id)")
window.addToComplexCompare = function(complexId, button = null) {
    console.log('🏢 ЖК кнопка нажата:', complexId, 'button:', !!button);
    if (!window.simpleComparisonManager) {
        console.error('❌ Менеджер сравнения не готов');
        return;
    }
    
    // ✅ ЗАЩИТА: Ищем кнопку если не передана или undefined
    if (!button) {
        console.log('🔍 Ищем кнопку через querySelector для ID:', complexId);
        button = document.querySelector(`[data-complex-id="${complexId}"]`);
    }
    
    if (button) {
        console.log('🚀 Вызываем PostgreSQL функцию для ЖК:', complexId);
        window.simpleComparisonManager.toggleComplexComparison(complexId, button);
    } else {
        console.error('❌ Кнопка ЖК не найдена для ID:', complexId);
        // ✅ FALLBACK: Попробуем без кнопки
        window.simpleComparisonManager.toggleComplexComparison(complexId, null);
    }
};

// АЛЬТЕРНАТИВНОЕ ИМЯ ДЛЯ СОВМЕСТИМОСТИ
window.addToComplexComparison = window.addToComplexCompare;

// ✅ КРИТИЧНО: Добавляем delegated click handler для ВСЕХ кликов
document.addEventListener('click', (e) => {
    // Ищем кнопку сравнения ЖК в любом виде
    const btn = e.target.closest('[data-complex-id][class*="compare"], .complex-compare-btn, .compare-btn[data-complex-id]');
    if (!btn) return;
    
    console.log('🎯 DELEGATED CLICK перехвачен:', btn);
    
    const complexId = btn.dataset.complexId || btn.getAttribute('data-complex-id') || btn.getAttribute('data-id');
    if (complexId && window.simpleComparisonManager) {
        console.log('🚀 Перенаправляем на PostgreSQL систему:', complexId);
        e.preventDefault();
        e.stopImmediatePropagation();
        
        window.simpleComparisonManager.toggleComplexComparison(complexId, btn);
    }
}, true); // true = capture phase, срабатывает РАНЬШЕ других

// ✅ Убедимся что глобальные функции правильно привязаны
window.addToComplexCompare = function(complexId, button = null) {
    console.log('🏢 ГЛОБАЛЬНАЯ ФУНКЦИЯ вызвана:', complexId);
    if (window.simpleComparisonManager) {
        return window.simpleComparisonManager.toggleComplexComparison(complexId, button);
    }
};

window.addToComplexComparison = window.addToComplexCompare;

// ✅ КРИТИЧНО: Добавляем ГЛОБАЛЬНУЮ ФУНКЦИЮ addToComparison для КВАРТИР
window.addToComparison = function(type, id) {
    console.log('🚀 ГЛОБАЛЬНАЯ addToComparison вызвана:', type, id);
    if (!window.simpleComparisonManager) {
        console.error('❌ Менеджер сравнения не готов');
        return;
    }
    
    if (type === 'property') {
        console.log('🏠 Добавляем квартиру в PostgreSQL сравнение:', id);
        return window.simpleComparisonManager.toggleComparison(id, null);
    } else if (type === 'complex') {
        console.log('🏢 Добавляем ЖК в PostgreSQL сравнение:', id);
        return window.simpleComparisonManager.toggleComplexComparison(id, null);
    } else {
        console.error('❌ Неизвестный тип сравнения:', type);
    }
};

// ✅ НОВАЯ ФУНКЦИЯ: Обновляем визуальное состояние кнопок сравнения
SimpleComparisonManager.prototype.updateComparisonUI = function() {
    console.log('🔄 Обновляем UI кнопок сравнения...');
    
    // Обновляем кнопки квартир
    document.querySelectorAll('.compare-btn[data-property-id], [data-property-id][class*="compare"]').forEach(btn => {
        const propertyId = btn.dataset.propertyId || btn.getAttribute('data-property-id');
        if (propertyId) {
            const isInComparison = this.comparisons.includes(String(propertyId));
            this.updateButtonState(btn, isInComparison);
        }
    });
    
    // Обновляем кнопки ЖК 
    document.querySelectorAll('.compare-btn[data-complex-id], [data-complex-id][class*="compare"]').forEach(btn => {
        const complexId = btn.dataset.complexId || btn.getAttribute('data-complex-id');
        if (complexId) {
            const isInComparison = this.complexComparisons.includes(String(complexId));
            this.updateButtonState(btn, isInComparison);
        }
    });
    
    console.log('✅ UI кнопок обновлено:', this.comparisons.length, 'квартир +', this.complexComparisons.length, 'ЖК');
};

console.log('🎉 ПРОСТОЕ РЕШЕНИЕ + ГЛОБАЛЬНАЯ addToComparison ЗАГРУЖЕНО УСПЕШНО');