/**
 * InBack.ru - Яндекс карты с границами районов и улицами
 * Интеграция полигонов и полилиний как на kayan.ru
 * Использует стабильный Yandex Maps API v2.1 с улучшениями из v3
 */

class InBackMaps {
    constructor() {
        this.map = null;
        this.districtPolygons = new Map();
        this.streetPolylines = new Map();
        this.isInitialized = false;
    }

    /**
     * Инициализация карты с улучшенными стилями
     */
    async initMap(containerId, centerCoords = [45.035180, 38.977414], zoom = 11) {
        return new Promise((resolve, reject) => {
            if (typeof ymaps === 'undefined') {
                reject(new Error('Яндекс.Карты API не загружен'));
                return;
            }

            ymaps.ready(() => {
                try {
                    // Создаем карту с улучшенными настройками
                    this.map = new ymaps.Map(containerId, {
                        center: centerCoords,
                        zoom: zoom,
                        controls: ['zoomControl', 'geolocationControl', 'typeSelector', 'fullscreenControl']
                    }, {
                        searchControlProvider: 'yandex#search',
                        suppressMapOpenBlock: true
                    });

                    this.isInitialized = true;
                    console.log('✅ InBack карта инициализирована (API v2.1)');
                    resolve(this.map);
                } catch (error) {
                    reject(error);
                }
            });
        });
    }

    /**
     * Загружает и отображает границы района с улучшенными стилями
     */
    async loadDistrictBoundaries(districtSlug) {
        if (!this.isInitialized) {
            console.error('❌ Карта не инициализирована');
            return false;
        }

        try {
            console.log(`🗺️ Загружаем границы района: ${districtSlug}`);
            
            const response = await fetch(`/api/district/boundaries/${districtSlug}`);
            const data = await response.json();
            
            if (data.success && data.boundaries) {
                const boundaries = data.boundaries;
                
                // Удаляем старые полигоны района если есть
                if (this.districtPolygons.has(districtSlug)) {
                    this.map.geoObjects.remove(this.districtPolygons.get(districtSlug));
                }
                
                // Создаем полигон из GeoJSON координат
                let coordinates;
                
                // Обрабатываем GeoJSON Feature
                if (boundaries.type === 'Feature') {
                    const geometry = boundaries.geometry;
                    if (geometry.type === 'Polygon') {
                        coordinates = geometry.coordinates;
                    } else if (geometry.type === 'MultiPolygon') {
                        coordinates = geometry.coordinates[0];
                    } else {
                        console.warn('⚠️ Неподдерживаемый тип геометрии в Feature:', geometry.type);
                        return false;
                    }
                } else if (boundaries.type === 'Polygon') {
                    coordinates = boundaries.coordinates;
                } else if (boundaries.type === 'MultiPolygon') {
                    // Для мультиполигонов берем первый полигон
                    coordinates = boundaries.coordinates[0];
                } else {
                    console.warn('⚠️ Неподдерживаемый тип геометрии:', boundaries.type);
                    return false;
                }
                
                // Конвертируем координаты из [lng, lat] в [lat, lng] для Яндекс карт
                const yandexCoords = coordinates.map(ring => 
                    ring.map(coord => [coord[1], coord[0]])
                );
                
                // Создаем полигон с красивыми стилями по примеру из документации
                const polygon = new ymaps.Polygon(yandexCoords, {
                    hintContent: `Границы района ${data.district_name}`,
                    balloonContent: `
                        <div style="padding: 10px;">
                            <strong style="font-size: 16px; color: #1E3A8A;">${data.district_name}</strong><br>
                            <span style="color: #666; font-size: 14px;">Границы района на карте</span><br>
                            <span style="color: #888; font-size: 12px;">Нажмите для подробностей</span>
                        </div>
                    `
                }, {
                    // Очень яркие и заметные стили границ района
                    fillColor: '#FF6B35',        // Яркий оранжевый
                    fillOpacity: 0.4,            // Увеличенная прозрачность заливки
                    strokeColor: '#DC2626',      // Яркий красный контур
                    strokeWidth: 6,              // Увеличенная толщина линии
                    strokeOpacity: 1.0,          // Полная непрозрачность
                    strokeStyle: 'solid'
                });
                
                // Добавляем на карту
                this.map.geoObjects.add(polygon);
                this.districtPolygons.set(districtSlug, polygon);
                
                console.log('✅ Полигон границ района добавлен на карту:', districtSlug);
                console.log('Координаты полигона:', coordinates);
                
                // Подгоняем вид карты под границы с увеличенными отступами
                this.map.setBounds(polygon.geometry.getBounds(), {
                    checkZoomRange: true,
                    margin: [80, 80, 80, 80]  // Больше отступы для лучшего обзора
                });
                
                // Дополнительно: устанавливаем минимальный зум для видимости полигона
                setTimeout(() => {
                    if (this.map.getZoom() > 14) {
                        this.map.setZoom(14);
                    }
                }, 500);
                
                console.log(`✅ Границы района ${data.district_name} загружены`);
                return true;
                
            } else {
                console.warn(`⚠️ Границы района ${districtSlug} не найдены:`, data.error);
                return false;
            }
            
        } catch (error) {
            console.error(`❌ Ошибка загрузки границ района ${districtSlug}:`, error);
            return false;
        }
    }

    /**
     * Загружает и отображает подсветку улицы с улучшенными стилями
     */
    async loadStreetHighlight(streetSlug) {
        if (!this.isInitialized) {
            console.error('❌ Карта не инициализирована');
            return false;
        }

        try {
            console.log(`🛣️ Загружаем координаты улицы: ${streetSlug}`);
            
            const response = await fetch(`/api/street/coordinates/${streetSlug}`);
            const data = await response.json();
            
            if (data.success && data.coordinates) {
                const coordinates = data.coordinates;
                
                // Удаляем старые полилинии улицы если есть
                if (this.streetPolylines.has(streetSlug)) {
                    this.map.geoObjects.remove(this.streetPolylines.get(streetSlug));
                }
                
                // Создаем полилинию из GeoJSON координат
                let lineCoords;
                
                if (coordinates.type === 'LineString') {
                    lineCoords = coordinates.coordinates;
                } else if (coordinates.type === 'MultiLineString') {
                    // Для мультилиний берем первую линию
                    lineCoords = coordinates.coordinates[0];
                } else {
                    console.warn('⚠️ Неподдерживаемый тип геометрии для улицы:', coordinates.type);
                    return false;
                }
                
                // Конвертируем координаты из [lng, lat] в [lat, lng] для Яндекс карт
                const yandexCoords = lineCoords.map(coord => [coord[1], coord[0]]);
                
                // Создаем полилинию с красивыми стилями по примеру из документации
                const polyline = new ymaps.Polyline(yandexCoords, {
                    hintContent: `Улица ${data.street_name}`,
                    balloonContent: `
                        <div style="padding: 10px;">
                            <strong style="font-size: 16px; color: #DC2626;">${data.street_name}</strong><br>
                            <span style="color: #666; font-size: 14px;">Выделенная улица на карте</span><br>
                            <span style="color: #888; font-size: 12px;">Маршрут подсвечен красным</span>
                        </div>
                    `
                }, {
                    // Красивые стили для улиц по примеру из документации
                    strokeColor: '#DC2626',
                    strokeWidth: 6,
                    strokeOpacity: 0.8,
                    strokeStyle: 'solid'
                });
                
                // Добавляем обводку для лучшей видимости
                const polylineOutline = new ymaps.Polyline(yandexCoords, {}, {
                    strokeColor: '#FFFFFF',
                    strokeWidth: 8,
                    strokeOpacity: 0.6,
                    strokeStyle: 'solid'
                });
                
                // Добавляем сначала обводку, потом основную линию
                this.map.geoObjects.add(polylineOutline);
                this.map.geoObjects.add(polyline);
                
                // Сохраняем обе линии для удаления
                this.streetPolylines.set(streetSlug, {
                    main: polyline,
                    outline: polylineOutline
                });
                
                // Подгоняем вид карты под улицу
                this.map.setBounds(polyline.geometry.getBounds(), {
                    checkZoomRange: true,
                    margin: [100, 100, 100, 100]
                });
                
                console.log(`✅ Улица ${data.street_name} подсвечена`);
                return true;
                
            } else {
                console.warn(`⚠️ Координаты улицы ${streetSlug} не найдены:`, data.error);
                return false;
            }
            
        } catch (error) {
            console.error(`❌ Ошибка загрузки координат улицы ${streetSlug}:`, error);
            return false;
        }
    }

    /**
     * Очищает все полигоны и полилинии
     */
    clearAll() {
        // Удаляем все полигоны районов
        this.districtPolygons.forEach(polygon => {
            this.map.geoObjects.remove(polygon);
        });
        this.districtPolygons.clear();
        
        // Удаляем все полилинии улиц (включая обводки)
        this.streetPolylines.forEach(lines => {
            if (lines.main) {
                this.map.geoObjects.remove(lines.main);
            }
            if (lines.outline) {
                this.map.geoObjects.remove(lines.outline);
            }
        });
        this.streetPolylines.clear();
        
        console.log('🧹 Карта очищена от всех полигонов и полилиний');
    }

    /**
     * Добавляет маркер на карту с улучшенными стилями
     */
    addMarker(coords, title, content, iconColor = 'blue') {
        if (!this.isInitialized) {
            console.error('❌ Карта не инициализирована');
            return null;
        }

        const placemark = new ymaps.Placemark(coords, {
            hintContent: title,
            balloonContent: `
                <div style="padding: 10px; max-width: 250px;">
                    <strong style="font-size: 16px; color: #1E3A8A;">${title}</strong><br>
                    <span style="color: #666; font-size: 14px;">${content}</span>
                </div>
            `
        }, {
            preset: `islands#${iconColor}DotIcon`,
            iconImageSize: [30, 42],
            iconImageOffset: [-15, -42]
        });

        this.map.geoObjects.add(placemark);
        return placemark;
    }

    /**
     * Устанавливает центр карты
     */
    setCenter(coords, zoom = null) {
        if (!this.isInitialized) {
            console.error('❌ Карта не инициализирована');
            return;
        }

        if (zoom) {
            this.map.setCenter(coords, zoom);
        } else {
            this.map.setCenter(coords);
        }
    }

    /**
     * Получает экземпляр карты
     */
    getMap() {
        return this.map;
    }
}

// Глобальная переменная для доступа к картам
window.InBackMaps = InBackMaps;

// Автоматическая инициализация если есть контейнер карты
document.addEventListener('DOMContentLoaded', function() {
    const mapContainer = document.getElementById('yandex-map');
    if (mapContainer) {
        console.log('🗺️ Обнаружен контейнер карты, готовим к инициализации...');
    }
});