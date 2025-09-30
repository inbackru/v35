// Lightweight performance optimization
(function() {
    'use strict';

    // Simple lazy loading for images
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            imageObserver.unobserve(img);
                        }
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // Memory monitoring (lightweight)
    function monitorMemory() {
        if ('memory' in performance) {
            setInterval(() => {
                const mem = performance.memory;
                const used = Math.round(mem.usedJSHeapSize / 1024 / 1024);
                const total = Math.round(mem.totalJSHeapSize / 1024 / 1024);
                const limit = Math.round(mem.jsHeapSizeLimit / 1024 / 1024);
                console.log('Memory usage:', {
                    used: `${used} MB`,
                    total: `${total} MB`, 
                    limit: `${limit} MB`
                });
            }, 5000);
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initLazyLoading();
            monitorMemory();
            console.log('Performance optimizations initialized');
        });
    } else {
        initLazyLoading();
        monitorMemory();
        console.log('Performance optimizations initialized');
    }
})();