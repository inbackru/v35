/**
 * InBack.ru - Enhanced District Maps with Boundaries
 * Интеграция нашей системы полигонов в страницы районов
 */

class DistrictMapsEnhanced {
    constructor() {
        this.primaryMap = null;
        this.secondaryMap = null;
        this.inBackMaps = null;
        this.districtSlug = null;
        this.isInitialized = false;
    }

    /**
     * Инициализация улучшенных карт района
     */
    async initializeEnhancedMaps(districtSlug, coordinates) {
        try {
            console.log('🚀 Инициализируем улучшенные карты для района:', districtSlug);
            
            this.districtSlug = districtSlug;
            
            // Инициализируем основную карту с полигонами
            await this.initializePrimaryMapWithBoundaries(coordinates);
            
            // Заменяем вторую карту на нашу систему или убираем её
            this.replaceSecondaryMap();
            
            console.log('✅ Улучшенные карты района инициализированы');
            this.isInitialized = true;
            
        } catch (error) {
            console.error('❌ Ошибка инициализации улучшенных карт:', error);
        }
    }

    /**
     * Инициализация основной карты с полигонами границ
     */
    async initializePrimaryMapWithBoundaries(coordinates) {
        try {
            // Создаем экземпляр нашей системы карт
            this.inBackMaps = new InBackMaps();
            
            // Инициализируем карту в контейнере основной карты
            await this.inBackMaps.initMap('district-map', 
                [coordinates.latitude, coordinates.longitude], 
                coordinates.zoom_level
            );
            
            console.log('✅ Основная карта инициализирована');
            
            // Загружаем границы района
            const success = await this.inBackMaps.loadDistrictBoundaries(this.districtSlug);
            
            if (success) {
                console.log('✅ Границы района загружены на основную карту');
            } else {
                console.log('⚠️ Границы района не найдены, добавляем маркер');
                // Добавляем маркер района если нет границ
                this.inBackMaps.addMarker(
                    [coordinates.latitude, coordinates.longitude],
                    coordinates.name || 'Район',
                    'Район Краснодара с новостройками'
                );
            }
            
            // Загружаем POI инфраструктуру
            await this.loadInfrastructurePOI(coordinates);
            
        } catch (error) {
            console.error('❌ Ошибка инициализации основной карты:', error);
        }
    }

    /**
     * Загружает POI инфраструктуры на карту
     */
    async loadInfrastructurePOI(coordinates) {
        try {
            console.log('🏢 Загружаем POI инфраструктуры...');
            
            const response = await fetch(`/api/infrastructure?lat=${coordinates.latitude}&lng=${coordinates.longitude}&radius=2000`);
            const poiData = await response.json();
            
            console.log('📍 POI данные получены:', Object.keys(poiData));
            
            // Добавляем POI маркеры на карту
            Object.keys(poiData).forEach(category => {
                const items = poiData[category];
                if (!items || items.length === 0) return;
                
                // Ограничиваем количество для производительности
                const limitedItems = items.slice(0, 6);
                
                limitedItems.forEach(poi => {
                    if (!poi.lat || !poi.lng) return;
                    
                    const iconColor = this.getPoiIconColor(category);
                    
                    this.inBackMaps.addMarker(
                        [poi.lat, poi.lng],
                        poi.name || 'POI',
                        this.getCategoryLabel(category),
                        iconColor
                    );
                });
            });
            
            console.log('✅ POI инфраструктура добавлена на карту');
            
        } catch (error) {
            console.error('❌ Ошибка загрузки POI:', error);
        }
    }

    /**
     * НЕ скрывает вторую карту, оставляем обе для полигонов
     */
    replaceSecondaryMap() {
        try {
            console.log('ℹ️ Оставляем обе карты активными для полигонов');
            
        } catch (error) {
            console.error('❌ Ошибка замены второй карты:', error);
        }
    }

    /**
     * Загружает и отображает подсветку улиц района
     */
    async loadDistrictStreets() {
        if (!this.inBackMaps || !this.districtSlug) {
            console.log('⚠️ Карта или район не инициализированы');
            return;
        }

        try {
            console.log('🛣️ Загружаем улицы района...');
            
            // Пробуем загрузить основные улицы района
            const mainStreets = ['krasnaya', 'severnaya', 'stavropol-skaya'];
            
            for (const streetSlug of mainStreets) {
                await this.inBackMaps.loadStreetHighlight(streetSlug);
            }
            
        } catch (error) {
            console.error('❌ Ошибка загрузки улиц:', error);
        }
    }

    /**
     * Получает цвет иконки по категории POI
     */
    getPoiIconColor(category) {
        const colors = {
            'education': 'green',
            'medical': 'red', 
            'shopping': 'orange',
            'transport': 'blue',
            'leisure': 'violet',
            'finance': 'yellow',
            'sports': 'pink'
        };
        return colors[category] || 'gray';
    }

    /**
     * Получает читаемое название категории
     */
    getCategoryLabel(category) {
        const labels = {
            'education': 'Образование',
            'medical': 'Медицина',
            'shopping': 'Торговля',
            'transport': 'Транспорт',
            'leisure': 'Досуг',
            'finance': 'Финансы',
            'sports': 'Спорт'
        };
        return labels[category] || category;
    }

    /**
     * Очищает все карты
     */
    clearAllMaps() {
        if (this.inBackMaps) {
            this.inBackMaps.clearAll();
        }
    }

    /**
     * Переключает отображение категории POI
     */
    togglePOICategory(category, show) {
        // Логика фильтрации POI по категориям
        console.log('🔄 Переключение категории POI:', category, show);
    }
}

// Глобальная переменная для доступа
window.DistrictMapsEnhanced = DistrictMapsEnhanced;

// Автоматическая инициализация когда загружается страница района
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем что мы на странице района
    if (document.getElementById('district-map') && window.districtCoords) {
        console.log('🗺️ Обнаружена страница района, инициализируем улучшенные карты...');
        
        // Ждем загрузки InBackMaps класса
        function waitForInBackMaps() {
            if (typeof InBackMaps === 'undefined') {
                setTimeout(waitForInBackMaps, 100);
                return;
            }
            
            // Инициализируем улучшенные карты
            const enhancedMaps = new DistrictMapsEnhanced();
            const districtSlug = window.location.pathname.split('/').pop();
            
            enhancedMaps.initializeEnhancedMaps(districtSlug, window.districtCoords);
            
            // Сохраняем в глобальной переменной для доступа
            window.enhancedDistrictMaps = enhancedMaps;
        }
        
        waitForInBackMaps();
    }
});