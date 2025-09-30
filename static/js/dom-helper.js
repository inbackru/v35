/**
 * DOM Helper - Safe DOM Operations
 * Prevents JavaScript errors from null/undefined elements
 */

(function() {
    'use strict';
    
    // Safe element selection
    window.safeQuery = function(selector, context) {
        try {
            const element = (context || document).querySelector(selector);
            return element || null;
        } catch (error) {
            console.warn('Error selecting element:', selector, error);
            return null;
        }
    };

    window.safeQueryAll = function(selector, context) {
        try {
            const elements = (context || document).querySelectorAll(selector);
            return elements || [];
        } catch (error) {
            console.warn('Error selecting elements:', selector, error);
            return [];
        }
    };

    // Safe event binding
    window.safeAddEventListener = function(element, event, handler, options) {
        if (!element || typeof element.addEventListener !== 'function') {
            console.warn('Cannot add event listener to:', element);
            return false;
        }
        
        try {
            element.addEventListener(event, handler, options);
            return true;
        } catch (error) {
            console.warn('Error adding event listener:', error);
            return false;
        }
    };

    // Safe property access
    window.safeGetProperty = function(obj, path, defaultValue) {
        try {
            return path.split('.').reduce((current, prop) => current && current[prop], obj) ?? defaultValue;
        } catch (error) {
            console.warn('Error accessing property:', path, error);
            return defaultValue;
        }
    };

    // Initialize DOM safety helpers
    console.log('DOM Helper initialized - safe DOM operations available');
})();