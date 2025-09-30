// Cache Optimization System
(function() {
    'use strict';

    // Browser cache optimization
    function optimizeCache() {
        // Set aggressive caching for static resources
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw-cache.js', {
                scope: '/'
            }).then(reg => {
                console.log('Cache SW registered');
            }).catch(err => {
                console.log('Cache SW failed:', err);
            });
        }
    }

    // Memory cache for API responses
    const apiCache = new Map();
    const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

    window.getCachedAPI = function(url) {
        const cached = apiCache.get(url);
        if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
            return Promise.resolve(cached.data);
        }
        
        return fetch(url)
            .then(response => response.json())
            .then(data => {
                apiCache.set(url, {
                    data: data,
                    timestamp: Date.now()
                });
                return data;
            });
    };

    // Initialize cache optimization
    optimizeCache();
    console.log('Cache optimizer initialized');
})();