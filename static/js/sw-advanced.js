// Advanced Service Worker with HTTP/2 optimization and intelligent caching
const CACHE_NAME = 'inback-optimized-v2';
const CACHE_DYNAMIC = 'inback-dynamic-v2';

// Cache strategies for different resource types
const CACHE_STRATEGIES = {
    images: 'cache-first',
    styles: 'stale-while-revalidate',
    scripts: 'stale-while-revalidate',
    pages: 'network-first',
    api: 'network-first'
};

// Static resources to cache immediately
const STATIC_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/mobile_menu.js',
    '/static/js/performance.js',
    '/static/js/image-optimization.js',
    '/static/js/asset-optimization.js',
    '/static/css/performance.css'
];

// Install event - precache critical resources
self.addEventListener('install', event => {
    event.waitUntil(
        Promise.all([
            caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_CACHE)),
            caches.open(CACHE_DYNAMIC)
        ]).then(() => {
            console.log('Advanced SW: Cache populated');
            self.skipWaiting();
        })
    );
});

// Activate event - cleanup old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(name => 
                        name !== CACHE_NAME && 
                        name !== CACHE_DYNAMIC &&
                        name.startsWith('inback-')
                    )
                    .map(name => {
                        console.log('Advanced SW: Deleting old cache', name);
                        return caches.delete(name);
                    })
            );
        }).then(() => {
            console.log('Advanced SW: Activated');
            self.clients.claim();
        })
    );
});

// Fetch event - intelligent caching strategy
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip admin and API requests from caching
    if (url.pathname.includes('/admin/') || 
        url.pathname.includes('/api/') ||
        url.pathname.includes('/manager/')) {
        return;
    }

    // Determine resource type and apply appropriate strategy
    const resourceType = getResourceType(request);
    const strategy = CACHE_STRATEGIES[resourceType] || 'network-first';

    event.respondWith(
        executeStrategy(request, strategy, resourceType)
    );
});

// Determine resource type based on request
function getResourceType(request) {
    const url = new URL(request.url);
    const pathname = url.pathname;
    
    if (pathname.match(/\.(jpg|jpeg|png|gif|webp|avif|svg|ico)$/i)) {
        return 'images';
    } else if (pathname.match(/\.(css)$/i)) {
        return 'styles';
    } else if (pathname.match(/\.(js)$/i)) {
        return 'scripts';
    } else if (pathname.includes('/api/') || pathname.includes('.json')) {
        return 'api';
    } else {
        return 'pages';
    }
}

// Execute caching strategy
async function executeStrategy(request, strategy, resourceType) {
    const cacheName = resourceType === 'images' ? CACHE_DYNAMIC : CACHE_NAME;
    
    switch (strategy) {
        case 'cache-first':
            return cacheFirstStrategy(request, cacheName);
        
        case 'network-first':
            return networkFirstStrategy(request, cacheName);
        
        case 'stale-while-revalidate':
            return staleWhileRevalidateStrategy(request, cacheName);
        
        default:
            return networkFirstStrategy(request, cacheName);
    }
}

// Cache-first strategy (good for images)
async function cacheFirstStrategy(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    
    if (cached) {
        return cached;
    }
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.log('Network failed, no cache available');
        return new Response('Offline', { status: 503 });
    }
}

// Network-first strategy (good for pages and API)
async function networkFirstStrategy(request, cacheName) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cache = await caches.open(cacheName);
        const cached = await cache.match(request);
        
        if (cached) {
            return cached;
        }
        
        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match('/') || new Response('Offline', { status: 503 });
        }
        
        return new Response('Offline', { status: 503 });
    }
}

// Stale-while-revalidate strategy (good for CSS/JS)
async function staleWhileRevalidateStrategy(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    
    // Update cache in background
    const networkResponse = fetch(request).then(response => {
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    }).catch(() => {
        console.log('Background update failed');
    });
    
    // Return cached version immediately if available
    if (cached) {
        return cached;
    }
    
    // Otherwise wait for network
    return networkResponse;
}

// Background sync for failed requests
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(
            // Retry failed requests
            retryFailedRequests()
        );
    }
});

// Retry failed requests when back online
async function retryFailedRequests() {
    // Implementation for retrying failed form submissions, etc.
    console.log('Retrying failed requests...');
}

// Push notification handling
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        
        const options = {
            body: data.body,
            icon: '/static/images/icon-192.png',
            badge: '/static/images/badge-72.png',
            tag: data.tag || 'default',
            requireInteraction: data.requireInteraction || false,
            data: data.data || {}
        };

        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    event.waitUntil(
        clients.openWindow(event.notification.data.url || '/')
    );
});

// Message handling for cache updates
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => caches.delete(cacheName))
                );
            })
        );
    }
});

// Periodic background sync for cache cleanup
self.addEventListener('periodicsync', event => {
    if (event.tag === 'cache-cleanup') {
        event.waitUntil(
            cleanupOldCacheEntries()
        );
    }
});

// Clean up old cache entries
async function cleanupOldCacheEntries() {
    const cache = await caches.open(CACHE_DYNAMIC);
    const requests = await cache.keys();
    const now = Date.now();
    const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days
    
    for (const request of requests) {
        const response = await cache.match(request);
        const dateHeader = response.headers.get('date');
        
        if (dateHeader) {
            const responseDate = new Date(dateHeader).getTime();
            if (now - responseDate > maxAge) {
                await cache.delete(request);
                console.log('Cleaned up old cache entry:', request.url);
            }
        }
    }
}

console.log('Advanced Service Worker loaded');