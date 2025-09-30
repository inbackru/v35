// Service Worker for aggressive caching
const CACHE_NAME = 'inback-cache-v1';
const STATIC_CACHE = [
    '/static/css/styles.css',
    '/static/js/main.js',
    '/static/js/header_search.js',
    '/static/js/blog-search.js'
];

// Install event
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_CACHE))
    );
});

// Fetch event - cache first strategy for static resources
self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('/static/')) {
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    return response || fetch(event.request);
                })
        );
    }
});