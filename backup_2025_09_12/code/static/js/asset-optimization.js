// Asset optimization and HTTP/2 optimization
(function() {
    'use strict';

    // CSS and JS minification utilities
    function minifyCSS(css) {
        return css
            .replace(/\/\*[\s\S]*?\*\//g, '')
            .replace(/\s+/g, ' ')
            .replace(/;\s*}/g, '}')
            .replace(/\s*{\s*/g, '{')
            .replace(/:\s*/g, ':')
            .replace(/;\s*/g, ';')
            .trim();
    }

    function minifyJS(js) {
        // Basic JS minification (for inline scripts)
        return js
            .replace(/\/\*[\s\S]*?\*\//g, '')
            .replace(/\/\/.*$/gm, '')
            .replace(/\s+/g, ' ')
            .replace(/;\s*}/g, ';}')
            .replace(/\s*{\s*/g, '{')
            .replace(/,\s*/g, ',')
            .trim();
    }

    // Resource bundling for HTTP/2
    function bundleResources() {
        const criticalCSS = [];
        const criticalJS = [];

        // Collect critical CSS
        document.querySelectorAll('style').forEach(style => {
            if (style.dataset.critical === 'true') {
                criticalCSS.push(style.textContent);
            }
        });

        // Collect critical JS
        document.querySelectorAll('script[data-critical="true"]').forEach(script => {
            if (script.textContent) {
                criticalJS.push(script.textContent);
            }
        });

        // Create bundled critical resources
        if (criticalCSS.length > 0) {
            const bundledCSS = minifyCSS(criticalCSS.join('\n'));
            const styleEl = document.createElement('style');
            styleEl.textContent = bundledCSS;
            styleEl.dataset.bundled = 'true';
            document.head.appendChild(styleEl);
        }

        if (criticalJS.length > 0) {
            const bundledJS = minifyJS(criticalJS.join('\n'));
            const scriptEl = document.createElement('script');
            scriptEl.textContent = bundledJS;
            scriptEl.dataset.bundled = 'true';
            document.head.appendChild(scriptEl);
        }
    }

    // Advanced caching strategy
    function setupAdvancedCaching() {
        // Cache static resources with Service Worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw-advanced.js')
                .then(registration => {
                    console.log('Advanced SW registered');
                    
                    // Update cache when new version is available
                    registration.addEventListener('updatefound', () => {
                        const newWorker = registration.installing;
                        newWorker.addEventListener('statechange', () => {
                            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                // Show update available notification
                                showUpdateNotification();
                            }
                        });
                    });
                })
                .catch(error => {
                    console.log('Advanced SW registration failed:', error);
                });
        }

        // Browser cache optimization
        const cacheableResources = [
            '/static/css/style.css',
            '/static/js/main.js',
            '/static/js/performance.js',
            '/static/js/image-optimization.js',
            '/static/images/logo.png'
        ];

        cacheableResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = resource;
            document.head.appendChild(link);
        });
    }

    // HTTP/2 Push optimization
    function optimizeForHTTP2() {
        // Use link prefetch for HTTP/2 server push simulation
        const criticalResources = [
            { href: '/static/css/critical.css', as: 'style' },
            { href: '/static/js/critical.js', as: 'script' },
            { href: '/static/fonts/inter-var.woff2', as: 'font', crossorigin: 'anonymous' }
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource.href;
            link.as = resource.as;
            if (resource.crossorigin) {
                link.crossOrigin = resource.crossorigin;
            }
            document.head.appendChild(link);
        });
    }

    // Resource hints optimization
    function addResourceHints() {
        const hints = [
            { rel: 'dns-prefetch', href: '//fonts.googleapis.com' },
            { rel: 'dns-prefetch', href: '//cdn.jsdelivr.net' },
            { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: true },
            { rel: 'preconnect', href: 'https://cdnjs.cloudflare.com' }
        ];

        hints.forEach(hint => {
            const link = document.createElement('link');
            link.rel = hint.rel;
            link.href = hint.href;
            if (hint.crossorigin) {
                link.crossOrigin = 'anonymous';
            }
            document.head.appendChild(link);
        });
    }

    // Critical resource optimization
    function loadCriticalResources() {
        // Inline critical CSS
        const criticalCSS = `
            .hero-section { display: flex; align-items: center; min-height: 60vh; }
            .header { position: sticky; top: 0; z-index: 50; background: white; }
            .btn-primary { background: linear-gradient(135deg, #0088cc, #32a4fb); }
            .card { border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        `;

        const style = document.createElement('style');
        style.textContent = minifyCSS(criticalCSS);
        style.dataset.critical = 'true';
        document.head.insertBefore(style, document.head.firstChild);
    }

    // Async data loading optimization
    function optimizeDataLoading() {
        // Use RequestIdleCallback for non-critical data
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                loadNonCriticalData();
            });
        } else {
            // Fallback for older browsers
            setTimeout(loadNonCriticalData, 0);
        }
    }

    function loadNonCriticalData() {
        // Load analytics, social widgets, etc.
        const scripts = [
            '/static/js/analytics.js',
            '/static/js/social-widgets.js'
        ];

        scripts.forEach(src => {
            const script = document.createElement('script');
            script.src = src;
            script.async = true;
            script.defer = true;
            document.body.appendChild(script);
        });
    }

    // Update notification for new versions
    function showUpdateNotification() {
        const notification = document.createElement('div');
        notification.className = 'update-notification';
        notification.innerHTML = `
            <div class="update-content">
                <span>Доступно обновление сайта</span>
                <button onclick="location.reload()">Обновить</button>
                <button onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            .update-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #0088cc;
                color: white;
                padding: 12px 16px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 10000;
                font-size: 14px;
            }
            .update-content button {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                padding: 4px 8px;
                margin-left: 8px;
                border-radius: 4px;
                cursor: pointer;
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(notification);
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }

    // Initialize all optimizations
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        loadCriticalResources();
        addResourceHints();
        optimizeForHTTP2();
        bundleResources();
        setupAdvancedCaching();
        optimizeDataLoading();

        console.log('Asset optimization initialized');
    }

    init();
})();