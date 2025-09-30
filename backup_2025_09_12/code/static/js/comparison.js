
class ComparisonManager {
    constructor() {
        this.comparisons = this.loadComparisons();
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateComparisonUI();
        this.updateComparisonCounter();
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

    saveComparisons() {
        try {
            localStorage.setItem('comparisons', JSON.stringify(this.comparisons));
        } catch (e) {
            console.error('Error saving comparisons:', e);
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
            
            if (compareElement && compareElement.dataset.propertyId) {
                const propertyId = compareElement.dataset.propertyId;
                this.toggleComparison(propertyId, compareElement);
                e.preventDefault();
                e.stopPropagation();
            }
        });
    }

    toggleComparison(propertyId, element) {
        const index = this.comparisons.indexOf(propertyId);
        
        if (index > -1) {
            this.comparisons.splice(index, 1);
            this.updateCompareButton(element, false);
        } else {
            if (this.comparisons.length >= 4) {
                alert('Максимум 4 объекта для сравнения');
                return;
            }
            this.comparisons.push(propertyId);
            this.updateCompareButton(element, true);
        }
        
        this.saveComparisons();
        this.updateComparisonCounter();
    }

    updateCompareButton(element, isInComparison) {
        if (isInComparison) {
            element.classList.add('active');
            element.textContent = 'В сравнении';
        } else {
            element.classList.remove('active');
            element.textContent = 'Сравнить';
        }
    }

    updateComparisonUI() {
        document.querySelectorAll('.compare-btn').forEach(btn => {
            const propertyId = btn.dataset.propertyId;
            const isInComparison = this.comparisons.includes(propertyId);
            this.updateCompareButton(btn, isInComparison);
        });
    }

    updateComparisonCounter() {
        const counter = document.querySelector('.comparison-counter');
        if (counter) {
            counter.textContent = this.comparisons.length;
            counter.style.display = this.comparisons.length > 0 ? 'inline' : 'none';
        }
    }

    getComparisons() {
        return this.comparisons;
    }
}

// Initialize comparison manager
let comparisonManager;
document.addEventListener('DOMContentLoaded', function() {
    comparisonManager = new ComparisonManager();
});
