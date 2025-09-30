/**
 * Secondary District Map Initializer
 * InBack.ru - отдельный инициализатор для второй карты района
 * Исправляет проблемы с блокировкой inline JavaScript
 */

// ✅ IMMEDIATE DEBUG LOG
console.log('📦 district_secondary_map.js FILE LOADED!');

window.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Secondary district map DOMContentLoaded event fired!');
    
    const mapElement = document.getElementById('secondary-district-map');
    console.log('🔍 Looking for element #secondary-district-map:', mapElement);
    
    if (!mapElement) {
        console.log('❌ Secondary map element NOT FOUND - exiting');
        return;
    }
    
    console.log('✅ Secondary map element found');
    
    // Polling для ожидания загрузки Yandex Maps API
    function waitForYandexMaps() {
        if (!window.ymaps) {
            console.log('⏳ Waiting for Yandex Maps API...');
            setTimeout(waitForYandexMaps, 200);
            return;
        }
        
        console.log('✅ Yandex Maps API loaded');
        initializeSecondaryMap();
    }
    
    function initializeSecondaryMap() {
        ymaps.ready(function() {
            try {
                console.log('🗺️ Initializing secondary district map');
                
                // Получаем координаты из глобальной переменной или используем дефолтные
                const coords = window.districtCoords || {
                    latitude: 45.0355,
                    longitude: 38.9753,
                    zoom_level: 13
                };
                
                console.log('📍 Using coordinates:', coords);
                
                // Создаём карту
                const secondaryMap = new ymaps.Map('secondary-district-map', {
                    center: [coords.latitude, coords.longitude],
                    zoom: coords.zoom_level,
                    controls: ['zoomControl', 'typeSelector', 'fullscreenControl']
                });
                
                console.log('✅ Secondary map created successfully');
                
                // Добавляем маркер района
                const districtName = window.districtName || 'Район';
                const placemark = new ymaps.Placemark([coords.latitude, coords.longitude], {
                    balloonContentHeader: '<strong style="color: #0088CC;">' + districtName + '</strong>',
                    balloonContentBody: '<span style="font-size: 12px; color: #666;">Район Краснодара</span><br><div style="margin-top: 8px;"><strong style="color: #0088CC; font-size: 14px;">Новостройки с кешбеком</strong></div>',
                    hintContent: districtName
                }, {
                    preset: 'islands#blueIcon',
                    iconColor: '#0088CC'
                });
                
                secondaryMap.geoObjects.add(placemark);
                console.log('✅ District marker added to secondary map');
                
                // ✅ ДОБАВЛЯЕМ ЗАГРУЗКУ И ОТОБРАЖЕНИЕ POI ИНФРАСТРУКТУРЫ
                loadAndDisplayPOI(secondaryMap, coords);
                
                // Инициализация фильтра инфраструктуры для второй карты
                initializeSecondaryInfrastructureFilter(secondaryMap);
                
            } catch (error) {
                console.error('❌ Secondary map initialization error:', error);
            }
        });
    }
    
    // ✅ ФУНКЦИЯ ЗАГРУЗКИ И ОТОБРАЖЕНИЯ POI 
    function loadAndDisplayPOI(map, coords) {
        console.log('🔄 Loading POI data for secondary map...');
        
        // Загружаем инфраструктуру с API
        fetch('/api/infrastructure?lat=' + coords.latitude + '&lng=' + coords.longitude + '&radius=2000')
            .then(response => response.json())
            .then(poiData => {
                console.log('📍 Secondary map POI data received:', poiData);
                
                // Создаем глобальные переменные для POI (как на первой карте)
                window.allSecondaryPoiPlacemarks = [];
                window.secondaryPoiDataByCategory = poiData;
                
                // Добавляем POI на карту
                Object.keys(poiData).forEach(category => {
                    const items = poiData[category];
                    if (!items || items.length === 0) return;
                    
                    // Ограничиваем количество маркеров для производительности
                    const limitedItems = items.slice(0, 8);
                    
                    limitedItems.forEach(poi => {
                        if (!poi.lat || !poi.lng) return;
                        
                        // Определяем иконку по категории
                        const iconConfig = getPoiIconConfig(category);
                        
                        const placemark = new ymaps.Placemark([poi.lat, poi.lng], {
                            balloonContentHeader: '<strong>' + (poi.name || 'POI') + '</strong>',
                            balloonContentBody: getCategoryLabel(category),
                            hintContent: poi.name || category
                        }, {
                            preset: iconConfig.preset,
                            iconColor: iconConfig.color
                        });
                        
                        // Добавляем категорию к плейсмарку для фильтрации
                        placemark.options.set('category', category);
                        
                        map.geoObjects.add(placemark);
                        window.allSecondaryPoiPlacemarks.push(placemark);
                    });
                    
                    // Показываем количество найденных объектов
                    if (items.length > 8) {
                        console.log(`${category}: показано ${limitedItems.length} из ${items.length} объектов на второй карте`);
                    }
                });
                
                console.log('✅ Secondary map POI loaded successfully');
                
            })
            .catch(error => {
                console.error('❌ Error loading secondary map POI:', error);
            });
    }
    
    // ✅ КОНФИГУРАЦИЯ ИКОНОК POI ПО КАТЕГОРИЯМ
    function getPoiIconConfig(category) {
        const configs = {
            'education': { preset: 'islands#greenIcon', color: '#4CAF50' },
            'medical': { preset: 'islands#redIcon', color: '#f44336' },
            'shopping': { preset: 'islands#orangeIcon', color: '#FF9800' },
            'transport': { preset: 'islands#blueIcon', color: '#2196F3' },
            'leisure': { preset: 'islands#violetIcon', color: '#9C27B0' },
            'finance': { preset: 'islands#yellowIcon', color: '#FFEB3B' },
            'sports': { preset: 'islands#pinkIcon', color: '#E91E63' }
        };
        return configs[category] || { preset: 'islands#grayIcon', color: '#9E9E9E' };
    }
    
    // ✅ ПОЛУЧЕНИЕ ЧИТАЕМЫХ НАЗВАНИЙ КАТЕГОРИЙ
    function getCategoryLabel(category) {
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

    function initializeSecondaryInfrastructureFilter(map) {
        try {
            const toggleBtn = document.getElementById('secondary-infrastructure-toggle');
            const panel = document.getElementById('secondary-infrastructure-panel');
            
            if (!toggleBtn || !panel) {
                console.log('⚠️ Secondary infrastructure filter elements not found');
                return;
            }
            
            console.log('✅ Secondary infrastructure filter elements found');
            
            // Добавляем обработчик клика для кнопки toggle
            toggleBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleBtn.classList.toggle('active');
                panel.classList.toggle('active');
                console.log('🔘 Secondary infrastructure filter toggled');
            });
            
            // ✅ ДОБАВЛЯЕМ ФУНКЦИОНАЛЬНОСТЬ ФИЛЬТРАЦИИ POI МАРКЕРОВ
            setupSecondaryPoiFiltering(map, panel);
            
            // Закрытие при клике вне панели
            document.addEventListener('click', function(event) {
                if (!event.target.closest('.infrastructure-filter')) {
                    toggleBtn.classList.remove('active');
                    panel.classList.remove('active');
                }
            });
            
            console.log('✅ Secondary infrastructure filter initialized');
            
        } catch (error) {
            console.error('❌ Secondary infrastructure filter error:', error);
        }
    }
    
    // ✅ ФУНКЦИЯ НАСТРОЙКИ ФИЛЬТРАЦИИ POI МАРКЕРОВ
    function setupSecondaryPoiFiltering(map, panel) {
        try {
            // Находим все чекбоксы фильтров в панели
            const filterCheckboxes = panel.querySelectorAll('input[type="checkbox"]');
            console.log('🔍 Found filter checkboxes:', filterCheckboxes.length);
            
            // Добавляем обработчики на каждый чекбокс
            filterCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    console.log('📋 Filter checkbox changed:', checkbox.id, checkbox.checked);
                    updateSecondaryPoiVisibility(map);
                });
            });
            
            // Инициализируем видимость POI согласно текущим фильтрам
            updateSecondaryPoiVisibility(map);
            
            console.log('✅ Secondary POI filtering setup complete');
            
        } catch (error) {
            console.error('❌ Error setting up secondary POI filtering:', error);
        }
    }
    
    // ✅ ФУНКЦИЯ ОБНОВЛЕНИЯ ВИДИМОСТИ POI МАРКЕРОВ
    function updateSecondaryPoiVisibility(map) {
        if (!window.allSecondaryPoiPlacemarks || !map) {
            console.log('⚠️ Secondary POI placemarks or map not available yet');
            return;
        }
        
        try {
            // Получаем активные фильтры из чекбоксов
            const activeFilters = [];
            const checkboxes = document.querySelectorAll('#secondary-infrastructure-panel input[type="checkbox"]:checked');
            
            checkboxes.forEach(checkbox => {
                // Извлекаем категорию из ID чекбокса (например, medical-filter -> medical)
                const category = checkbox.id.replace('-filter', '');
                activeFilters.push(category);
            });
            
            console.log('🎯 Active secondary filters:', activeFilters);
            
            // Обновляем видимость каждого POI маркера
            window.allSecondaryPoiPlacemarks.forEach(placemark => {
                const category = placemark.options.get('category');
                if (activeFilters.length === 0 || activeFilters.includes(category)) {
                    // Показываем маркер
                    if (map.geoObjects.indexOf(placemark) < 0) {
                        map.geoObjects.add(placemark);
                    }
                } else {
                    // Скрываем маркер
                    map.geoObjects.remove(placemark);
                }
            });
            
            console.log(`✅ Updated visibility for ${window.allSecondaryPoiPlacemarks.length} secondary POI markers`);
            
        } catch (error) {
            console.error('❌ Error updating secondary POI visibility:', error);
        }
    }

    // Запуск инициализации
    waitForYandexMaps();
});