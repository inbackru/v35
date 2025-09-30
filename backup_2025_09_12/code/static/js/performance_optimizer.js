/**
 * Система оптимизации производительности
 * Максимальная скорость для чемпионов 🏆
 */

class PerformanceOptimizer {
    constructor() {
        this.config = {
            IMAGE_LAZY_THRESHOLD: 100,      // Пикселей до изображения для загрузки
            PREFETCH_DELAY: 2000,           // Задержка перед предзагрузкой
            RESOURCE_CACHE_TTL: 3600000,    // 1 час кэш для ресурсов
            COMPRESS_IMAGES: true,          // Сжатие изображений
            ENABLE_SERVICE_WORKER: true     // Service Worker для кэширования
        };
        
        this.metrics = {
            pageLoadTime: 0,
            resourcesLoaded: 0,
            cacheHits: 0,
            totalRequests: 0
        };
        
        this.observers = new Map();
        this.resourceCache = new Map();
        
        this.init();
    }
    
    async init() {
        console.log('🚀 Performance Optimizer v2.0 - Starting...');
        
        // Измеряем время загрузки страницы
        this.measurePageLoad();
        
        // Инициализируем ленивую загрузку изображений
        this.initLazyLoading();
        
        // Предзагружаем критические ресурсы
        this.preloadCriticalResources();
        
        // Оптимизируем изображения
        if (this.config.COMPRESS_IMAGES) {
            this.optimizeImages();
        }
        
        // Регистрируем Service Worker
        if (this.config.ENABLE_SERVICE_WORKER) {
            await this.registerServiceWorker();
        }
        
        // Мониторинг производительности
        this.startPerformanceMonitoring();
        
        console.log('✅ Performance Optimizer initialized');
    }
    
    measurePageLoad() {
        const startTime = performance.mark('page-start');
        
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            this.metrics.pageLoadTime = loadTime;
            
            console.log(`📊 Page Load Time: ${Math.round(loadTime)}ms`);
            
            // Отправляем метрики
            this.sendMetrics({
                type: 'page_load',
                duration: loadTime,
                url: window.location.pathname
            });
        });
        
        // Измеряем первый contentful paint
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (entry.name === 'first-contentful-paint') {
                        console.log(`🎨 First Contentful Paint: ${Math.round(entry.startTime)}ms`);
                    }
                });
            });
            observer.observe({ entryTypes: ['paint'] });
        }
    }
    
    initLazyLoading() {
        // Intersection Observer для ленивой загрузки
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    this.loadImage(img);
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: `${this.config.IMAGE_LAZY_THRESHOLD}px`
        });
        
        // Находим все изображения с data-src
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
        
        this.observers.set('images', imageObserver);
        
        console.log(`🖼️ Lazy loading initialized for ${lazyImages.length} images`);
    }
    
    async loadImage(img) {
        const src = img.dataset.src;
        if (!src) return;
        
        try {
            // Предзагружаем изображение
            const image = new Image();
            image.onload = () => {
                img.src = src;
                img.classList.add('loaded');
                img.removeAttribute('data-src');
                this.metrics.resourcesLoaded++;
            };
            image.onerror = () => {
                img.classList.add('error');
                console.warn(`Failed to load image: ${src}`);
            };
            image.src = src;
            
        } catch (error) {
            console.warn('Image loading error:', error);
        }
    }
    
    preloadCriticalResources() {
        // Предзагружаем критические ресурсы
        const criticalResources = [
            '/static/css/styles.css',
            '/static/js/super_search.js',
            '/static/js/main.js'
        ];
        
        setTimeout(() => {
            criticalResources.forEach(url => {
                this.preloadResource(url);
            });
        }, this.config.PREFETCH_DELAY);
    }
    
    preloadResource(url) {
        // Проверяем кэш
        if (this.resourceCache.has(url)) {
            this.metrics.cacheHits++;
            return Promise.resolve(this.resourceCache.get(url));
        }
        
        return fetch(url, {
            method: 'GET',
            cache: 'force-cache'
        }).then(response => {
            if (response.ok) {
                this.resourceCache.set(url, response.clone());
                console.log(`📦 Preloaded: ${url}`);
                return response;
            }
        }).catch(error => {
            console.warn(`Failed to preload: ${url}`, error);
        });
    }
    
    optimizeImages() {
        // WebP поддержка
        const supportsWebP = this.checkWebPSupport();
        
        if (supportsWebP) {
            // Заменяем расширения на WebP где возможно
            const images = document.querySelectorAll('img[src*=".jpg"], img[src*=".png"], img[data-src*=".jpg"], img[data-src*=".png"]');
            images.forEach(img => {
                const src = img.src || img.dataset.src;
                if (src) {
                    const webpSrc = src.replace(/\.(jpg|png)$/, '.webp');
                    // Проверяем существование WebP версии
                    this.checkImageExists(webpSrc).then(exists => {
                        if (exists) {
                            if (img.dataset.src) {
                                img.dataset.src = webpSrc;
                            } else {
                                img.src = webpSrc;
                            }
                        }
                    });
                }
            });
        }
    }
    
    checkWebPSupport() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 1;
            canvas.height = 1;
            return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
        } catch (error) {
            return false;
        }
    }
    
    async checkImageExists(url) {
        try {
            const response = await fetch(url, { method: 'HEAD' });
            return response.ok;
        } catch {
            return false;
        }
    }
    
    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/js/sw-cache.js');
                console.log('🔧 Service Worker registered successfully');
                
                // Обновляем SW при изменениях
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            console.log('🔄 New Service Worker available');
                        }
                    });
                });
                
            } catch (error) {
                console.warn('Service Worker registration failed:', error);
            }
        }
    }
    
    startPerformanceMonitoring() {
        // Мониторим производительность каждые 10 секунд
        setInterval(() => {
            this.collectMetrics();
        }, 10000);
        
        // Отправляем метрики при уходе со страницы
        window.addEventListener('beforeunload', () => {
            this.sendMetrics({
                type: 'session_end',
                metrics: this.metrics,
                duration: performance.now()
            });
        });
    }
    
    collectMetrics() {
        const metrics = {
            timestamp: Date.now(),
            memory: this.getMemoryUsage(),
            connectionType: this.getConnectionType(),
            resources: this.metrics.resourcesLoaded,
            cacheHitRate: this.metrics.totalRequests > 0 
                ? (this.metrics.cacheHits / this.metrics.totalRequests) * 100 
                : 0
        };
        
        // Логируем важные метрики
        if (metrics.memory.used > 50) {
            console.warn(`⚠️ High memory usage: ${metrics.memory.used}MB`);
        }
        
        return metrics;
    }
    
    getMemoryUsage() {
        if ('memory' in performance) {
            const memory = performance.memory;
            return {
                used: Math.round(memory.usedJSHeapSize / 1024 / 1024),
                total: Math.round(memory.totalJSHeapSize / 1024 / 1024),
                limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024)
            };
        }
        return { used: 0, total: 0, limit: 0 };
    }
    
    getConnectionType() {
        if ('connection' in navigator) {
            return navigator.connection.effectiveType || 'unknown';
        }
        return 'unknown';
    }
    
    sendMetrics(data) {
        // Отправляем метрики на сервер для анализа
        if (navigator.sendBeacon) {
            navigator.sendBeacon('/api/metrics', JSON.stringify(data));
        } else {
            // Fallback для старых браузеров
            fetch('/api/metrics', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: { 'Content-Type': 'application/json' },
                keepalive: true
            }).catch(() => {}); // Игнорируем ошибки
        }
    }
    
    // Публичные методы для управления
    prefetchPage(url) {
        // Предзагружаем страницу для мгновенного перехода
        this.preloadResource(url);
        
        // Также можем предзагрузить ресурсы страницы
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        document.head.appendChild(link);
    }
    
    optimizePage() {
        // Полная оптимизация текущей страницы
        this.initLazyLoading();
        this.preloadCriticalResources();
        this.optimizeImages();
    }
    
    getPerformanceReport() {
        return {
            pageLoadTime: this.metrics.pageLoadTime,
            resourcesLoaded: this.metrics.resourcesLoaded,
            cacheHitRate: this.metrics.totalRequests > 0 
                ? Math.round((this.metrics.cacheHits / this.metrics.totalRequests) * 100)
                : 0,
            memoryUsage: this.getMemoryUsage(),
            connectionType: this.getConnectionType()
        };
    }
}

// Инициализация оптимизатора
let performanceOptimizer;

document.addEventListener('DOMContentLoaded', () => {
    performanceOptimizer = new PerformanceOptimizer();
    
    // Делаем доступным глобально
    window.performanceOptimizer = performanceOptimizer;
});

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceOptimizer;
}