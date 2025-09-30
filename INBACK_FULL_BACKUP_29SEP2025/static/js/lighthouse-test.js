// Lighthouse performance test simulation
(function() {
    'use strict';
    
    // Performance metrics tracking
    let performanceData = {
        startTime: Date.now(),
        metrics: {},
        resources: [],
        errors: []
    };

    // Core Web Vitals tracking
    function trackCoreWebVitals() {
        // First Contentful Paint
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.name === 'first-contentful-paint') {
                        performanceData.metrics.FCP = entry.startTime;
                        console.log('First Contentful Paint:', entry.startTime + 'ms');
                    }
                }
            });
            observer.observe({ entryTypes: ['paint'] });
        }

        // Largest Contentful Paint
        if ('LargestContentfulPaint' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                performanceData.metrics.LCP = lastEntry.startTime;
                console.log('Largest Contentful Paint:', lastEntry.startTime + 'ms');
            });
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
        }

        // First Input Delay
        if ('PerformanceEventTiming' in window) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.processingStart && entry.startTime) {
                        const fid = entry.processingStart - entry.startTime;
                        performanceData.metrics.FID = fid;
                        console.log('First Input Delay:', fid + 'ms');
                    }
                }
            });
            observer.observe({ entryTypes: ['first-input'] });
        }

        // Cumulative Layout Shift
        if ('LayoutShift' in window) {
            let cumulativeScore = 0;
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        cumulativeScore += entry.value;
                    }
                }
                performanceData.metrics.CLS = cumulativeScore;
                console.log('Cumulative Layout Shift:', cumulativeScore);
            });
            observer.observe({ entryTypes: ['layout-shift'] });
        }
    }

    // Resource loading analysis
    function analyzeResources() {
        if ('performance' in window && 'getEntriesByType' in performance) {
            const resources = performance.getEntriesByType('resource');
            
            let totalSize = 0;
            let slowResources = [];
            
            resources.forEach(resource => {
                const size = resource.transferSize || 0;
                totalSize += size;
                
                if (resource.duration > 1000) {
                    slowResources.push({
                        url: resource.name,
                        duration: Math.round(resource.duration),
                        size: Math.round(size / 1024) + ' KB'
                    });
                }
            });
            
            performanceData.resources = {
                totalCount: resources.length,
                totalSize: Math.round(totalSize / 1024) + ' KB',
                slowResources: slowResources
            };
            
            console.log('Total resources:', resources.length);
            console.log('Total size:', Math.round(totalSize / 1024) + ' KB');
            
            if (slowResources.length > 0) {
                console.warn('Slow loading resources:', slowResources);
            }
        }
    }

    // Network Information API
    function analyzeNetwork() {
        if ('connection' in navigator) {
            const connection = navigator.connection;
            performanceData.network = {
                effectiveType: connection.effectiveType,
                downlink: connection.downlink + ' Mbps',
                rtt: connection.rtt + 'ms',
                saveData: connection.saveData
            };
            
            console.log('Network info:', performanceData.network);
        }
    }

    // Page visibility tracking
    function trackVisibility() {
        let visibilityStart = Date.now();
        
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                const visibleTime = Date.now() - visibilityStart;
                performanceData.metrics.visibleTime = visibleTime;
            } else {
                visibilityStart = Date.now();
            }
        });
    }

    // Error tracking
    function trackErrors() {
        window.addEventListener('error', (event) => {
            performanceData.errors.push({
                message: event.message,
                filename: event.filename,
                line: event.lineno,
                column: event.colno,
                timestamp: Date.now()
            });
            
            console.error('JavaScript error:', {
                message: event.message,
                filename: event.filename,
                line: event.lineno
            });
        });
        
        window.addEventListener('unhandledrejection', (event) => {
            performanceData.errors.push({
                message: 'Unhandled Promise Rejection: ' + event.reason,
                timestamp: Date.now()
            });
            
            console.error('Unhandled promise rejection:', event.reason);
        });
    }

    // Performance recommendations
    function generateRecommendations() {
        const recommendations = [];
        
        // FCP recommendations
        if (performanceData.metrics.FCP > 3000) {
            recommendations.push({
                metric: 'First Contentful Paint',
                issue: 'Slow FCP (' + Math.round(performanceData.metrics.FCP) + 'ms)',
                suggestion: 'Optimize critical CSS, reduce blocking resources'
            });
        }
        
        // LCP recommendations
        if (performanceData.metrics.LCP > 4000) {
            recommendations.push({
                metric: 'Largest Contentful Paint',
                issue: 'Slow LCP (' + Math.round(performanceData.metrics.LCP) + 'ms)',
                suggestion: 'Optimize images, improve server response times'
            });
        }
        
        // CLS recommendations
        if (performanceData.metrics.CLS > 0.1) {
            recommendations.push({
                metric: 'Cumulative Layout Shift',
                issue: 'High CLS (' + performanceData.metrics.CLS.toFixed(3) + ')',
                suggestion: 'Add size attributes to images, avoid dynamic content insertion'
            });
        }
        
        // Resource recommendations
        if (performanceData.resources && performanceData.resources.slowResources.length > 0) {
            recommendations.push({
                metric: 'Resource Loading',
                issue: performanceData.resources.slowResources.length + ' slow resources',
                suggestion: 'Optimize images, enable compression, use CDN'
            });
        }
        
        return recommendations;
    }

    // Generate Lighthouse-style report
    function generateReport() {
        const loadTime = Date.now() - performanceData.startTime;
        const recommendations = generateRecommendations();
        
        const report = {
            timestamp: new Date().toISOString(),
            url: window.location.href,
            loadTime: loadTime + 'ms',
            metrics: performanceData.metrics,
            resources: performanceData.resources,
            network: performanceData.network,
            errors: performanceData.errors,
            recommendations: recommendations,
            score: calculateScore()
        };
        
        console.log('Performance Report:', report);
        
        // Display report in console
        displayConsoleReport(report);
        
        return report;
    }

    // Calculate Lighthouse-style score
    function calculateScore() {
        let score = 100;
        
        // Deduct points for poor metrics
        if (performanceData.metrics.FCP > 3000) score -= 20;
        if (performanceData.metrics.LCP > 4000) score -= 25;
        if (performanceData.metrics.CLS > 0.1) score -= 15;
        if (performanceData.metrics.FID > 300) score -= 20;
        
        // Deduct points for slow resources
        if (performanceData.resources && performanceData.resources.slowResources.length > 0) {
            score -= performanceData.resources.slowResources.length * 5;
        }
        
        // Deduct points for errors
        score -= performanceData.errors.length * 10;
        
        return Math.max(0, Math.min(100, score));
    }

    // Display formatted report in console
    function displayConsoleReport(report) {
        console.log('\n🚀 PERFORMANCE REPORT');
        console.log('=====================');
        console.log('Score:', report.score + '/100');
        console.log('Load Time:', report.loadTime);
        
        if (report.metrics.FCP) {
            console.log('First Contentful Paint:', Math.round(report.metrics.FCP) + 'ms');
        }
        if (report.metrics.LCP) {
            console.log('Largest Contentful Paint:', Math.round(report.metrics.LCP) + 'ms');
        }
        if (report.metrics.CLS) {
            console.log('Cumulative Layout Shift:', report.metrics.CLS.toFixed(3));
        }
        if (report.metrics.FID) {
            console.log('First Input Delay:', Math.round(report.metrics.FID) + 'ms');
        }
        
        if (report.resources) {
            console.log('\n📦 Resources:', report.resources.totalCount, '(' + report.resources.totalSize + ')');
        }
        
        if (report.recommendations && report.recommendations.length > 0) {
            console.log('\n💡 Recommendations:');
            report.recommendations.forEach((rec, index) => {
                console.log((index + 1) + '.', rec.suggestion + ' (' + rec.issue + ')');
            });
        }
        
        if (report.errors && report.errors.length > 0) {
            console.warn('\n⚠️ Errors found:', report.errors.length);
        }
        
        console.log('\n');
    }

    // Initialize performance tracking
    function init() {
        trackCoreWebVitals();
        trackVisibility();
        trackErrors();
        analyzeNetwork();
        
        // Generate report when page is fully loaded
        window.addEventListener('load', () => {
            setTimeout(() => {
                analyzeResources();
                generateReport();
            }, 2000);
        });
        
        // Generate final report before page unload
        window.addEventListener('beforeunload', () => {
            generateReport();
        });
        
        console.log('Lighthouse performance tracking initialized');
    }

    // Export for manual testing
    window.performanceTest = {
        generateReport: generateReport,
        getMetrics: () => performanceData,
        analyze: () => {
            analyzeResources();
            return generateReport();
        }
    };

    init();
})();