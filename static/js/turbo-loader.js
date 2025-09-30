// Turbo Loading System
(function() {
    'use strict';

    // Preload critical pages on hover
    const preloadedPages = new Set();
    
    function preloadPage(url) {
        if (preloadedPages.has(url)) return;
        preloadedPages.add(url);
        
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        document.head.appendChild(link);
    }

    // Instant page loading on hover
    function initHoverPreload() {
        document.addEventListener('mouseover', (e) => {
            const link = e.target.closest('a');
            if (link && link.href && link.hostname === location.hostname) {
                preloadPage(link.href);
            }
        });
    }

    // Resource bundling
    function bundleCSS() {
        const styles = document.querySelectorAll('link[rel="stylesheet"]');
        if (styles.length > 3) {
            console.log('CSS optimization: Found', styles.length, 'stylesheets');
        }
    }

    // Initialize turbo features
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initHoverPreload();
            bundleCSS();
            console.log('Turbo loader initialized');
        });
    } else {
        initHoverPreload();
        bundleCSS();
        console.log('Turbo loader initialized');
    }
})();