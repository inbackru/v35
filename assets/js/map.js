// Map functionality for property search
class PropertyMap {
    constructor(mapId, options = {}) {
        this.mapId = mapId;
        this.map = null;
        this.markers = {};
        this.markerCluster = null;
        this.properties = [];
        this.filters = {
            rooms: 'all',
            priceMin: null,
            priceMax: null,
            developer: null
        };
        
        this.defaultOptions = {
            center: [45.0355, 38.9753], // Krasnodar coordinates
            zoom: 12,
            maxZoom: 18,
            ...options
        };
        
        this.init();
    }
    
    init() {
        if (!document.getElementById(this.mapId)) {
            console.error(`Map container with ID "${this.mapId}" not found`);
            return;
        }
        
        this.initMap();
        this.bindEvents();
    }
    
    initMap() {
        // Initialize Leaflet map
        this.map = L.map(this.mapId).setView(this.defaultOptions.center, this.defaultOptions.zoom);
        
        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: this.defaultOptions.maxZoom
        }).addTo(this.map);
        
        // Add custom controls
        this.addCustomControls();
    }
    
    addCustomControls() {
        // Add fullscreen control
        const fullscreenControl = L.control({position: 'topleft'});
        fullscreenControl.onAdd = function(map) {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
            container.innerHTML = '<a href="#" title="Полный экран"><i class="fas fa-expand"></i></a>';
            container.style.backgroundColor = 'white';
            container.style.width = '30px';
            container.style.height = '30px';
            container.style.lineHeight = '30px';
            container.style.textAlign = 'center';
            
            container.onclick = function(e) {
                e.preventDefault();
                toggleFullscreen(map.getContainer());
            };
            
            return container;
        };
        fullscreenControl.addTo(this.map);
        
        // Add location control
        const locationControl = L.control({position: 'topleft'});
        locationControl.onAdd = function(map) {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
            container.innerHTML = '<a href="#" title="Моё местоположение"><i class="fas fa-location-arrow"></i></a>';
            container.style.backgroundColor = 'white';
            container.style.width = '30px';
            container.style.height = '30px';
            container.style.lineHeight = '30px';
            container.style.textAlign = 'center';
            
            container.onclick = function(e) {
                e.preventDefault();
                getCurrentLocation(map);
            };
            
            return container;
        };
        locationControl.addTo(this.map);
    }
    
    loadProperties(properties) {
        this.properties = properties;
        this.clearMarkers();
        this.addMarkers(properties);
    }
    
    addMarkers(properties) {
        properties.forEach(property => {
            if (property.coordinates && property.coordinates.length === 2) {
                const marker = this.createPropertyMarker(property);
                this.markers[property.id] = marker;
                marker.addTo(this.map);
            }
        });
    }
    
    createPropertyMarker(property) {
        const [lat, lng] = property.coordinates;
        
        // Create custom marker icon
        const markerIcon = L.divIcon({
            html: this.createMarkerHTML(property),
            className: 'custom-property-marker',
            iconSize: [40, 40],
            iconAnchor: [20, 40],
            popupAnchor: [0, -40]
        });
        
        const marker = L.marker([lat, lng], { icon: markerIcon });
        
        // Create popup content
        const popupContent = this.createPopupContent(property);
        marker.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'property-popup'
        });
        
        // Add click event
        marker.on('click', () => {
            this.onMarkerClick(property);
        });
        
        return marker;
    }
    
    createMarkerHTML(property) {
        const priceShort = this.formatPriceShort(property.price);
        const statusColor = this.getStatusColor(property.status);
        
        return `
            <div class="marker-container">
                <div class="marker-pulse" style="background-color: ${statusColor}"></div>
                <div class="marker-content" style="background-color: ${statusColor}">
                    <span class="marker-text">${property.rooms}</span>
                </div>
                <div class="marker-price">${priceShort}</div>
            </div>
        `;
    }
    
    createPopupContent(property) {
        const cashbackFormatted = new Intl.NumberFormat('ru-RU').format(property.cashback);
        const priceFormatted = new Intl.NumberFormat('ru-RU').format(property.price);
        
        return `
            <div class="property-popup-content">
                ${property.images && property.images[0] ? 
                    `<div class="popup-image">
                        <img src="${property.images[0]}" alt="${property.title}" loading="lazy">
                    </div>` : ''
                }
                
                <div class="popup-body">
                    <h3 class="popup-title">${property.title}</h3>
                    <div class="popup-price">${priceFormatted} ₽</div>
                    
                    <div class="popup-details">
                        <div class="detail-item">
                            <span class="detail-label">Комнат:</span>
                            <span class="detail-value">${property.rooms}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Площадь:</span>
                            <span class="detail-value">${property.area} м²</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Этаж:</span>
                            <span class="detail-value">${property.floor}/${property.total_floors}</span>
                        </div>
                    </div>
                    
                    <div class="popup-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${property.district}
                    </div>
                    
                    <div class="popup-cashback">
                        Кэшбек: ${cashbackFormatted} ₽
                    </div>
                    
                    <div class="popup-actions">
                        <a href="object.php?id=${property.id}" class="btn-primary">Подробнее</a>
                        <button onclick="propertyMap.addToFavorites(${property.id})" class="btn-secondary">
                            <i class="far fa-heart"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    clearMarkers() {
        Object.values(this.markers).forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.markers = {};
    }
    
    filterMarkers(filters) {
        this.filters = { ...this.filters, ...filters };
        
        Object.keys(this.markers).forEach(propertyId => {
            const property = this.properties.find(p => p.id == propertyId);
            const marker = this.markers[propertyId];
            
            if (this.shouldShowProperty(property)) {
                if (!this.map.hasLayer(marker)) {
                    marker.addTo(this.map);
                }
            } else {
                if (this.map.hasLayer(marker)) {
                    this.map.removeLayer(marker);
                }
            }
        });
    }
    
    shouldShowProperty(property) {
        // Room filter
        if (this.filters.rooms !== 'all') {
            if (this.filters.rooms === '4+') {
                if (property.rooms < 4) return false;
            } else {
                if (property.rooms != this.filters.rooms) return false;
            }
        }
        
        // Price filters
        if (this.filters.priceMin && property.price < this.filters.priceMin) {
            return false;
        }
        
        if (this.filters.priceMax && property.price > this.filters.priceMax) {
            return false;
        }
        
        // Developer filter
        if (this.filters.developer && property.developer !== this.filters.developer) {
            return false;
        }
        
        return true;
    }
    
    focusOnProperty(propertyId) {
        const marker = this.markers[propertyId];
        if (marker) {
            this.map.setView(marker.getLatLng(), 16);
            marker.openPopup();
        }
    }
    
    fitBounds() {
        const visibleMarkers = Object.values(this.markers).filter(marker => 
            this.map.hasLayer(marker)
        );
        
        if (visibleMarkers.length > 0) {
            const group = new L.featureGroup(visibleMarkers);
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }
    
    // Event handlers
    onMarkerClick(property) {
        // Trigger custom event
        const event = new CustomEvent('propertyMarkerClick', {
            detail: { property }
        });
        document.dispatchEvent(event);
    }
    
    addToFavorites(propertyId) {
        // Get current favorites from localStorage
        let favorites = JSON.parse(localStorage.getItem('property_favorites') || '[]');
        
        if (!favorites.includes(propertyId.toString())) {
            favorites.push(propertyId.toString());
            localStorage.setItem('property_favorites', JSON.stringify(favorites));
            this.showNotification('Добавлено в избранное');
        } else {
            this.showNotification('Уже в избранном');
        }
    }
    
    showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'map-notification';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    bindEvents() {
        // Listen for property list item clicks
        document.addEventListener('click', (e) => {
            const propertyItem = e.target.closest('[data-property-id]');
            if (propertyItem) {
                const propertyId = propertyItem.dataset.propertyId;
                this.focusOnProperty(propertyId);
            }
        });
        
        // Listen for filter changes
        document.addEventListener('filterChange', (e) => {
            this.filterMarkers(e.detail);
        });
    }
    
    // Utility methods
    formatPriceShort(price) {
        if (price >= 1000000) {
            return (price / 1000000).toFixed(1) + 'М';
        } else if (price >= 1000) {
            return (price / 1000).toFixed(0) + 'К';
        }
        return price.toString();
    }
    
    getStatusColor(status) {
        const colors = {
            'new': '#10B981',
            'available': '#0088CC',
            'reserved': '#F59E0B',
            'sold': '#EF4444'
        };
        return colors[status] || colors['available'];
    }
}

// Map utility functions
function toggleFullscreen(element) {
    if (!document.fullscreenElement) {
        element.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

function getCurrentLocation(map) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                map.setView([lat, lng], 15);
                
                // Add user location marker
                L.marker([lat, lng])
                    .addTo(map)
                    .bindPopup('Ваше местоположение')
                    .openPopup();
            },
            function(error) {
                console.warn('Geolocation error:', error);
                alert('Не удалось определить ваше местоположение');
            }
        );
    } else {
        alert('Геолокация не поддерживается в вашем браузере');
    }
}

// Initialize map when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if map container exists
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        // Initialize property map
        window.propertyMap = new PropertyMap('map');
        
        // Load properties if available
        if (typeof window.mapProperties !== 'undefined') {
            propertyMap.loadProperties(window.mapProperties);
        }
        
        // Setup sidebar toggle for mobile
        const toggleButton = document.querySelector('.toggle-sidebar');
        const sidebar = document.getElementById('sidebar');
        
        if (toggleButton && sidebar) {
            window.toggleSidebar = function() {
                sidebar.classList.toggle('hidden');
            };
        }
        
        // Setup filter buttons
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Update active state
                filterButtons.forEach(btn => {
                    btn.classList.remove('active', 'bg-ton-blue', 'text-white');
                    btn.classList.add('text-gray-600');
                });
                
                this.classList.add('active', 'bg-ton-blue', 'text-white');
                this.classList.remove('text-gray-600');
                
                // Apply filter
                const filterType = this.textContent.trim();
                let rooms = 'all';
                
                if (filterType.includes('1 комн')) rooms = '1';
                else if (filterType.includes('2 комн')) rooms = '2';
                else if (filterType.includes('3 комн')) rooms = '3';
                else if (filterType.includes('4+ комн')) rooms = '4+';
                
                propertyMap.filterMarkers({ rooms });
                
                // Filter sidebar items
                filterSidebarItems(rooms);
            });
        });
    }
});

// Filter sidebar property items
function filterSidebarItems(rooms) {
    const propertyItems = document.querySelectorAll('.property-item');
    
    propertyItems.forEach(item => {
        const itemRooms = item.dataset.rooms;
        const show = rooms === 'all' || 
                    (rooms === '4+' && parseInt(itemRooms) >= 4) || 
                    itemRooms === rooms;
        
        item.style.display = show ? 'block' : 'none';
    });
}

// Focus on property from sidebar
window.focusOnProperty = function(propertyId) {
    if (window.propertyMap) {
        window.propertyMap.focusOnProperty(propertyId);
    }
};

// Export for use in other files
window.PropertyMap = PropertyMap;
