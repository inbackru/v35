// Advanced Image Compression System
(function() {
    'use strict';

    // WebP support detection
    const supportsWebP = (function() {
        const canvas = document.createElement('canvas');
        canvas.width = canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    })();

    // Auto-convert images to WebP if supported
    function optimizeImages() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (supportsWebP && img.src && !img.src.includes('.webp')) {
                const originalSrc = img.src;
                // Try WebP version first
                const webpSrc = originalSrc.replace(/\.(jpg|jpeg|png)$/i, '.webp');
                
                const testImg = new Image();
                testImg.onload = () => {
                    img.src = webpSrc;
                };
                testImg.onerror = () => {
                    // Keep original if WebP fails
                };
                testImg.src = webpSrc;
            }
        });
    }

    // Responsive image loading
    function setupResponsiveImages() {
        const images = document.querySelectorAll('img[data-sizes]');
        images.forEach(img => {
            const sizes = JSON.parse(img.dataset.sizes || '{}');
            const screenWidth = window.innerWidth;
            
            let optimalSrc = img.src;
            if (screenWidth <= 480 && sizes.small) {
                optimalSrc = sizes.small;
            } else if (screenWidth <= 768 && sizes.medium) {
                optimalSrc = sizes.medium;
            } else if (sizes.large) {
                optimalSrc = sizes.large;
            }
            
            if (optimalSrc !== img.src) {
                img.src = optimalSrc;
            }
        });
    }

    // Initialize image optimization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            optimizeImages();
            setupResponsiveImages();
            console.log('Image compressor initialized - WebP support:', supportsWebP);
        });
    } else {
        optimizeImages();
        setupResponsiveImages();
        console.log('Image compressor initialized - WebP support:', supportsWebP);
    }

    // Re-optimize on window resize
    window.addEventListener('resize', setupResponsiveImages);
})();