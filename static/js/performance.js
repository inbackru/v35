// Performance optimization and lazy loading system
(function() {
    'use strict';

    // Lazy loading for images
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('lazy-loaded');
                        imageObserver.unobserve(img);
                        
                        // Log performance metrics
                        console.log('Image lazy loaded:', img.src);
                    }
                });
            });

            // Apply lazy loading to all images with data-src attribute
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for older browsers
            document.querySelectorAll('img[data-src]').forEach(img => {
                img.src = img.dataset.src;
            });
        }
    }

    // Preload critical resources
    function preloadCriticalResources() {
        const criticalResources = [
            '/static/css/style.css',
            '/static/js/main.js'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            link.href = resource;
            document.head.appendChild(link);
        });
    }

    // Service Worker registration for caching
    function initServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('SW registered successfully');
                })
                .catch(error => {
                    console.log('SW registration failed:', error);
                });
        }
    }

    // Performance metrics monitoring
    function logPerformanceMetrics() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    const metrics = {
                        dns: Math.round(perfData.domainLookupEnd - perfData.domainLookupStart),
                        connection: Math.round(perfData.connectEnd - perfData.connectStart),
                        response: Math.round(perfData.responseEnd - perfData.responseStart),
                        domComplete: Math.round(perfData.domComplete - perfData.navigationStart),
                        loadComplete: Math.round(perfData.loadEventEnd - perfData.navigationStart)
                    };
                    
                    console.log('Page Performance Metrics:', metrics);
                    
                    // Log slow loading resources
                    const resources = performance.getEntriesByType('resource');
                    const slowResources = resources.filter(resource => resource.duration > 1000);
                    if (slowResources.length > 0) {
                        console.warn('Slow loading resources:', slowResources);
                    }
                }, 1000);
            });
        }
    }

    // Memory usage monitoring
    function monitorMemoryUsage() {
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                const memoryInfo = {
                    used: Math.round(memory.usedJSHeapSize / 1024 / 1024) + ' MB',
                    total: Math.round(memory.totalJSHeapSize / 1024 / 1024) + ' MB',
                    limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024) + ' MB'
                };
                console.log('Memory usage:', memoryInfo);
            }, 30000); // Check every 30 seconds
        }
    }

    // Font optimization
    function optimizeFonts() {
        // Add font-display: swap to improve loading performance
        const fontLinks = document.querySelectorAll('link[rel="stylesheet"][href*="fonts.googleapis.com"]');
        fontLinks.forEach(link => {
            link.href += '&display=swap';
        });
    }

    // Initialize performance optimizations
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        preloadCriticalResources();
        initLazyLoading();
        initServiceWorker();
        logPerformanceMetrics();
        monitorMemoryUsage();
        optimizeFonts();

        console.log('Performance optimizations initialized');
    }

    // Start initialization
    init();

})();