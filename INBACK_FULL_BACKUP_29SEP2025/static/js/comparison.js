
class ComparisonManager {
    constructor() {
        this.comparisons = this.loadComparisons();
        this.complexes = this.loadComplexes();
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateComparisonUI();
        this.updateComparisonCounter();
        
        // Show view button if there are items in comparison
        if (this.getTotalCount() > 0) {
            this.showViewComparisonButton();
        }
    }

    loadComparisons() {
        try {
            const saved = localStorage.getItem('comparisons');
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            console.error('Error loading comparisons:', e);
            return [];
        }
    }

    loadComplexes() {
        try {
            // Try new key first, fallback to old key for compatibility
            const saved = localStorage.getItem('comparison_complexes') || localStorage.getItem('complexes');
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            console.error('Error loading complexes:', e);
            return [];
        }
    }

    saveComparisons() {
        try {
            localStorage.setItem('comparisons', JSON.stringify(this.comparisons));
        } catch (e) {
            console.error('Error saving comparisons:', e);
        }
    }

    saveComplexes() {
        try {
            // Use unified key for both files
            localStorage.setItem('comparison_complexes', JSON.stringify(this.complexes));
            // Remove old key for cleanup
            localStorage.removeItem('complexes');
        } catch (e) {
            console.error('Error saving complexes:', e);
        }
    }

    bindEvents() {
        document.addEventListener('click', (e) => {
            let compareElement = null;
            
            if (e.target && e.target.classList && e.target.classList.contains('compare-btn')) {
                compareElement = e.target;
            } else if (e.target && e.target.closest) {
                compareElement = e.target.closest('.compare-btn');
            }
            
            if (compareElement) {
                // Handle property comparison
                if (compareElement.dataset.propertyId) {
                    const propertyId = compareElement.dataset.propertyId;
                    this.toggleComparison(propertyId, compareElement);
                    e.preventDefault();
                    e.stopPropagation();
                }
                // Handle complex comparison
                else if (compareElement.dataset.complexId) {
                    const complexId = compareElement.dataset.complexId;
                    this.toggleComplexComparison(complexId, compareElement);
                    e.preventDefault();
                    e.stopPropagation();
                }
            }
        });
    }

    toggleComparison(propertyId, element) {
        console.log('🔥 toggleComparison called with:', propertyId);
        console.log('🔥 Current comparisons before toggle:', this.comparisons);
        
        const index = this.comparisons.indexOf(String(propertyId));
        
        if (index > -1) {
            this.comparisons.splice(index, 1);
            this.updateCompareButton(element, false);
            this.showNotification('Удалено из сравнения', 'info');
            console.log('🔥 Removed from comparison, new list:', this.comparisons);
        } else {
            if (this.comparisons.length >= 4) {
                this.showNotification('Максимум 4 объекта для сравнения', 'info');
                return;
            }
            this.comparisons.push(String(propertyId));
            this.updateCompareButton(element, true);
            this.showNotification('Добавлено в сравнение', 'success');
            this.showViewComparisonButton();
            console.log('🔥 Added to comparison, new list:', this.comparisons);
        }
        
        this.saveComparisons();
        this.updateComparisonCounter();
    }

    toggleComplexComparison(complexId, element) {
        const index = this.complexes.indexOf(complexId);
        
        if (index > -1) {
            this.complexes.splice(index, 1);
            this.updateCompareButton(element, false);
            this.showNotification('ЖК удален из сравнения', 'info');
            console.log('Complex removed from comparison:', complexId);
        } else {
            if (this.complexes.length >= 4) {
                this.showNotification('Максимум 4 ЖК для сравнения', 'info');
                return;
            }
            this.complexes.push(complexId);
            this.updateCompareButton(element, true);
            this.showNotification('ЖК добавлен в сравнение', 'success');
            this.showViewComparisonButton();
            console.log('Complex added to comparison:', complexId);
        }
        
        this.saveComplexes();
        this.updateComparisonCounter();
    }

    updateCompareButton(element, isInComparison) {
        if (isInComparison) {
            element.classList.add('active');
            element.classList.remove('text-gray-600', 'hover:bg-blue-50', 'hover:border-blue-300', 'hover:text-blue-600');
            element.classList.add('bg-blue-500', 'border-blue-500', 'text-white');
            element.title = 'Удалить из сравнения';
        } else {
            element.classList.remove('active', 'bg-blue-500', 'border-blue-500', 'text-white');
            element.classList.add('text-gray-600', 'hover:bg-blue-50', 'hover:border-blue-300', 'hover:text-blue-600');
            element.title = 'Добавить к сравнению';
        }
    }

    updateComparisonUI() {
        // Update property comparison buttons
        document.querySelectorAll('.compare-btn[data-property-id]').forEach(btn => {
            const propertyId = btn.dataset.propertyId;
            // Convert to string for comparison since localStorage stores strings
            const isInComparison = this.comparisons.includes(String(propertyId));
            this.updateCompareButton(btn, isInComparison);
        });
        
        // Update complex comparison buttons  
        document.querySelectorAll('.compare-btn[data-complex-id]').forEach(btn => {
            const complexId = btn.dataset.complexId;
            // Convert to string for comparison since localStorage stores strings
            const isInComparison = this.complexes.includes(String(complexId));
            this.updateCompareButton(btn, isInComparison);
        });
    }

    updateComparisonCounter() {
        const totalItems = this.comparisons.length + this.complexes.length;
        const counter = document.querySelector('.comparison-counter');
        if (counter) {
            counter.textContent = totalItems;
            counter.style.display = totalItems > 0 ? 'inline' : 'none';
        }
    }

    getComparisons() {
        return this.comparisons;
    }

    getComplexes() {
        return this.complexes;
    }

    getTotalCount() {
        return this.comparisons.length + this.complexes.length;
    }

    // Show notification similar to FavoritesManager
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-4 py-2 rounded-lg text-white text-sm font-medium z-50 transition-all duration-300 transform translate-x-full opacity-0`;
        
        if (type === 'success') {
            notification.classList.add('bg-green-500');
        } else if (type === 'info') {
            notification.classList.add('bg-blue-500');
        } else {
            notification.classList.add('bg-red-500');
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full', 'opacity-0');
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Show "Посмотреть сравнения" button
    showViewComparisonButton() {
        // Remove existing button first
        const existingButton = document.querySelector('.view-comparison-btn');
        if (existingButton) {
            existingButton.remove();
        }
        
        // Only show if there are items to compare
        if (this.getTotalCount() === 0) return;
        
        // Determine the correct URL based on user role
        const isManager = Boolean(window.manager_authenticated);
        const comparisonUrl = isManager ? '/manager/property-comparison' : '/comparison';
        
        const button = document.createElement('div');
        button.className = 'view-comparison-btn fixed bottom-6 right-6 z-50 transform transition-all duration-300 translate-y-full opacity-0';
        button.innerHTML = `
            <a href="${comparisonUrl}" 
               class="bg-[#0088CC] hover:bg-[#0077BB] text-white px-6 py-3 rounded-lg font-medium shadow-lg flex items-center gap-2 transform hover:scale-105 transition-all duration-200">
                <i class="fas fa-balance-scale"></i>
                <span>Посмотреть сравнения (${this.getTotalCount()})</span>
            </a>
        `;
        
        document.body.appendChild(button);
        
        // Animate in
        setTimeout(() => {
            button.classList.remove('translate-y-full', 'opacity-0');
        }, 100);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (button && button.parentNode) {
                button.classList.add('translate-y-full', 'opacity-0');
                setTimeout(() => {
                    if (button && button.parentNode) {
                        document.body.removeChild(button);
                    }
                }, 300);
            }
        }, 5000);
    }

    // Clear all comparisons
    clearAll() {
        console.log('🔥 clearAll() called');
        console.log('🔥 Before clear - comparisons:', this.comparisons);
        console.log('🔥 Before clear - complexes:', this.complexes);
        
        this.comparisons = [];
        this.complexes = [];
        
        // Explicitly clear localStorage
        localStorage.removeItem('property_comparisons');
        localStorage.removeItem('complex_comparisons');
        
        // Force save empty arrays
        this.saveComparisons();
        this.saveComplexes();
        
        console.log('🔥 After clear - comparisons:', this.comparisons);
        console.log('🔥 After clear - complexes:', this.complexes);
        console.log('🔥 localStorage check:', {
            properties: localStorage.getItem('property_comparisons'),
            complexes: localStorage.getItem('complex_comparisons')
        });
        
        this.updateComparisonUI();
        this.updateComparisonCounter();
        this.showNotification('Все сравнения очищены', 'info');
        
        // Remove all floating buttons (both new and legacy)
        const viewButton = document.querySelector('.view-comparison-btn');
        if (viewButton) {
            viewButton.remove();
        }
        const legacyButton = document.getElementById('comparison-floating-link');
        if (legacyButton) {
            legacyButton.remove();
        }
        
        console.log('🔥 clearAll() completed');
    }
}

// Initialize comparison manager
let comparisonManager;
document.addEventListener('DOMContentLoaded', function() {
    comparisonManager = new ComparisonManager();
    
    // Make clearComparison global function compatible
    window.clearComparison = function() {
        if (confirm('Вы уверены, что хотите очистить все объекты из сравнения?')) {
            comparisonManager.clearAll();
        }
    };
});
