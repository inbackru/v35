// Advanced image optimization system
(function() {
    'use strict';

    // WebP and AVIF support detection
    function supportsWebP() {
        const canvas = document.createElement('canvas');
        canvas.width = canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }

    function supportsAVIF() {
        const canvas = document.createElement('canvas');
        canvas.width = canvas.height = 1;
        return canvas.toDataURL('image/avif').indexOf('data:image/avif') === 0;
    }

    // Adaptive image format selection
    function getOptimalImageUrl(originalUrl) {
        if (!originalUrl) return originalUrl;
        
        const extension = originalUrl.split('.').pop().toLowerCase();
        const basePath = originalUrl.replace(`.${extension}`, '');
        
        if (supportsAVIF()) {
            return `${basePath}.avif`;
        } else if (supportsWebP()) {
            return `${basePath}.webp`;
        }
        
        return originalUrl;
    }

    // Advanced lazy loading with Intersection Observer
    function initAdvancedLazyLoading() {
        if (!('IntersectionObserver' in window)) {
            // Fallback for older browsers
            document.querySelectorAll('img[data-src]').forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
            });
            return;
        }

        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Start loading image
                    const tempImg = new Image();
                    
                    tempImg.onload = function() {
                        img.src = getOptimalImageUrl(img.dataset.src);
                        img.classList.remove('lazy');
                        img.classList.add('lazy-loaded');
                        
                        // Fade in animation
                        img.style.opacity = '0';
                        img.style.transition = 'opacity 0.3s ease';
                        setTimeout(() => { img.style.opacity = '1'; }, 50);
                        
                        console.log('Image lazy loaded:', img.src);
                    };
                    
                    tempImg.onerror = function() {
                        // Fallback to original if optimized format fails
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('lazy-loaded');
                    };
                    
                    tempImg.src = getOptimalImageUrl(img.dataset.src);
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });

        // Apply to all lazy images
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });

        // Apply to dynamically added images
        const contentObserver = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        const lazyImages = node.querySelectorAll ? 
                            node.querySelectorAll('img[data-src]') : 
                            (node.tagName === 'IMG' && node.dataset.src ? [node] : []);
                        
                        lazyImages.forEach(img => imageObserver.observe(img));
                    }
                });
            });
        });

        contentObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Responsive image srcset generator
    function generateSrcSet(basePath, sizes = [320, 640, 1024, 1280, 1920]) {
        const extension = basePath.split('.').pop();
        const basePathWithoutExt = basePath.replace(`.${extension}`, '');
        
        return sizes.map(size => {
            let format = extension;
            if (supportsAVIF()) format = 'avif';
            else if (supportsWebP()) format = 'webp';
            
            return `${basePathWithoutExt}-${size}w.${format} ${size}w`;
        }).join(', ');
    }

    // Apply responsive images to existing img elements
    function enhanceImages() {
        document.querySelectorAll('img:not([srcset])').forEach(img => {
            if (img.src && !img.dataset.enhanced) {
                const srcset = generateSrcSet(img.src);
                if (srcset) {
                    img.srcset = srcset;
                    img.sizes = '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw';
                    img.dataset.enhanced = 'true';
                }
            }
        });
    }

    // Image compression quality detection
    function detectConnectionSpeed() {
        if ('connection' in navigator) {
            const connection = navigator.connection;
            if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
                return 'low';
            } else if (connection.effectiveType === '3g') {
                return 'medium';
            }
        }
        return 'high';
    }

    // Adjust image quality based on connection
    function adjustImageQuality() {
        const quality = detectConnectionSpeed();
        const qualityMap = {
            'low': 'q_30',
            'medium': 'q_60',
            'high': 'q_80'
        };
        
        document.querySelectorAll('img').forEach(img => {
            if (img.src && img.src.includes('cloudinary') && !img.dataset.qualityAdjusted) {
                const qualityParam = qualityMap[quality];
                img.src = img.src.replace(/\/upload\//, `/upload/${qualityParam}/`);
                img.dataset.qualityAdjusted = 'true';
            }
        });
    }

    // Progressive image loading
    function loadProgressiveImages() {
        document.querySelectorAll('img[data-progressive]').forEach(img => {
            const lowRes = img.dataset.lowRes;
            const highRes = img.dataset.src;
            
            if (lowRes) {
                img.src = lowRes;
                img.classList.add('progressive-loading');
                
                const highResImg = new Image();
                highResImg.onload = function() {
                    img.src = highRes;
                    img.classList.remove('progressive-loading');
                    img.classList.add('progressive-loaded');
                };
                highResImg.src = highRes;
            }
        });
    }

    // Initialize all image optimizations
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        initAdvancedLazyLoading();
        enhanceImages();
        adjustImageQuality();
        loadProgressiveImages();

        // Recheck images periodically for dynamic content
        setInterval(enhanceImages, 5000);

        console.log('Advanced image optimization initialized');
        console.log('WebP support:', supportsWebP());
        console.log('AVIF support:', supportsAVIF());
        console.log('Connection speed:', detectConnectionSpeed());
    }

    init();
})();