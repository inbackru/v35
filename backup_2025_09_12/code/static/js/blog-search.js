/**
 * Blog Search and Category Navigation
 * Instant search and fast category switching
 */

(function() {
    'use strict';
    
    let searchTimeout;
    let articlesCache = new Map();
    let currentQuery = '';
    let currentCategory = '';
    
    function initBlogSearch() {
        const searchInput = document.getElementById('blog-search');
        const searchBtn = document.getElementById('search-btn');
        const categoryFilters = document.querySelectorAll('.category-filter'); // Исправлено
        const sortSelect = document.getElementById('sort-articles');
        const quickSearchTags = document.querySelectorAll('.quick-search-tag');
        const suggestionsContainer = document.getElementById('search-suggestions');
        const articlesContainer = document.getElementById('articles-container');
        
        // Initialize current state from URL
        const urlParams = new URLSearchParams(window.location.search);
        currentQuery = urlParams.get('search') || '';
        currentCategory = urlParams.get('category') || '';
        
        // Instant search functionality
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const searchValue = this.value.trim();
                currentQuery = searchValue;
                
                if (searchValue.length >= 2) {
                    showSearchSuggestions(searchValue);
                } else {
                    hideSuggestions();
                }
                
                // Instant search with minimal debounce
                searchTimeout = setTimeout(() => {
                    if (searchValue !== this.value.trim()) return;
                    performInstantSearch(searchValue);
                }, 200); // 200ms debounce for instant feel
            });
            
            // Hide suggestions when clicking outside
            document.addEventListener('click', function(e) {
                if (!searchInput.contains(e.target) && !suggestionsContainer?.contains(e.target)) {
                    hideSuggestions();
                }
            });
            
            // Focus handling
            searchInput.addEventListener('focus', function() {
                if (this.value.trim().length >= 2) {
                    showSearchSuggestions(this.value.trim());
                }
            });
            
            // Enter key search
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    clearTimeout(searchTimeout);
                    hideSuggestions();
                    performInstantSearch(this.value.trim());
                }
            });
            
            // Search button click
            if (searchBtn) {
                searchBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    performInstantSearch(searchInput.value.trim());
                });
            }
        }
        
        // Quick search tags
        quickSearchTags.forEach(tag => {
            tag.addEventListener('click', function(e) {
                e.preventDefault();
                const query = this.dataset.query;
                if (searchInput) {
                    searchInput.value = query;
                    currentQuery = query;
                    performInstantSearch(query);
                }
            });
        });
        
        // Instant category navigation
        categoryFilters.forEach(category => {
            category.addEventListener('click', function(e) {
                e.preventDefault(); // Prevent page reload
                
                const categoryName = this.dataset.category;
                currentCategory = categoryName === 'all' ? '' : categoryName;
                
                // Update active state
                updateActiveCategory(this);
                
                // Instant category switch
                performInstantCategorySwitch(currentCategory);
            });
        });
        
        // Sorting functionality
        if (sortSelect) {
            sortSelect.addEventListener('change', function() {
                // For now just trigger a new search with current filters
                performInstantSearch(currentQuery, currentCategory);
            });
        }
        
        console.log('Blog search and navigation initialized');
    }
    
    function showSearchSuggestions(query) {
        const suggestionsContainer = document.getElementById('search-suggestions');
        if (!suggestionsContainer) return;
        
        // Fetch real suggestions from API
        fetch(`/api/blog/search?q=${encodeURIComponent(query)}&suggestions=true`)
            .then(response => response.json())
            .then(data => {
                const suggestions = data.suggestions || [];
                
                if (suggestions.length === 0) {
                    hideSuggestions();
                    return;
                }
                
                const suggestionsHTML = suggestions.map(item => `
                    <div class="suggestion-item px-4 py-2 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0" 
                         data-query="${item.title}" data-slug="${item.slug}">
                        <div class="text-sm font-medium text-gray-900">${item.title}</div>
                        <div class="text-xs text-gray-500">${item.category}</div>
                    </div>
                `).join('');
                
                suggestionsContainer.innerHTML = suggestionsHTML;
                suggestionsContainer.classList.remove('hidden');
                
                // Add click handlers to suggestions
                suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
                    item.addEventListener('click', function() {
                        const suggestionQuery = this.dataset.query;
                        document.getElementById('blog-search').value = suggestionQuery;
                        hideSuggestions();
                        performInstantSearch(suggestionQuery);
                    });
                });
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
                hideSuggestions();
            });
    }
    
    function hideSuggestions() {
        const suggestionsContainer = document.getElementById('search-suggestions');
        if (suggestionsContainer) {
            suggestionsContainer.classList.add('hidden');
        }
    }
    
    function performInstantSearch(searchValue) {
        const searchBtn = document.getElementById('search-btn');
        const articlesContainer = document.getElementById('articles-container');
        
        if (!articlesContainer) return;
        
        try {
            // Show loading state
            if (searchBtn) {
                searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            }
            
            // Use AJAX for instant search
            const params = new URLSearchParams();
            if (searchValue) params.set('q', searchValue);
            if (currentCategory) params.set('category', currentCategory);
            
            fetch(`/api/blog/search?${params}`, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    renderArticles(data.articles);
                    updateURL(searchValue, currentCategory);
                })
                .catch(error => {
                    console.error('Search error:', error);
                })
                .finally(() => {
                    if (searchBtn) {
                        searchBtn.innerHTML = '<i class="fas fa-search"></i>';
                    }
                });
            
        } catch (error) {
            console.error('Search error:', error);
            if (searchBtn) {
                searchBtn.innerHTML = '<i class="fas fa-search"></i>';
            }
        }
    }
    
    function performInstantCategorySwitch(category) {
        const articlesContainer = document.getElementById('articles-container');
        if (!articlesContainer) return;
        
        // Show loading animation
        articlesContainer.style.opacity = '0.6';
        
        const params = new URLSearchParams();
        if (currentQuery) params.set('q', currentQuery);
        if (category) params.set('category', category);
        
        console.log('Category switch request:', category, params.toString());
        
        fetch(`/api/blog/search?${params}`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Category switch response:', data);
                renderArticles(data.articles || []);
                updateURL(currentQuery, category);
            })
            .catch(error => {
                console.error('Category switch error:', error);
                // Show error message to user
                articlesContainer.innerHTML = `
                    <div class="col-span-full text-center py-12">
                        <i class="fas fa-exclamation-triangle text-red-400 text-5xl mb-4"></i>
                        <h3 class="text-lg font-medium text-gray-900 mb-2">Ошибка загрузки</h3>
                        <p class="text-gray-600">Попробуйте обновить страницу или выберите другую категорию.</p>
                    </div>
                `;
            })
            .finally(() => {
                articlesContainer.style.opacity = '1';
            });
    }
    
    function renderArticles(articles) {
        const articlesContainer = document.getElementById('articles-container');
        if (!articlesContainer) {
            console.error('Articles container not found');
            return;
        }
        
        console.log('Rendering articles:', articles.length);
        
        if (articles.length === 0) {
            articlesContainer.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <i class="fas fa-newspaper text-gray-400 text-5xl mb-4"></i>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">Статьи не найдены</h3>
                    <p class="text-gray-600">Попробуйте изменить критерии поиска или выберите другую категорию.</p>
                </div>
            `;
            return;
        }
        
        const articlesHTML = articles.map(article => `
            <article class="article-card bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow">
                ${article.featured_image ? `
                    <div class="aspect-video bg-gray-200 overflow-hidden">
                        <img src="${article.featured_image}" alt="${article.title}" class="w-full h-full object-cover">
                    </div>
                ` : ''}
                
                <div class="p-6">
                    <div class="flex items-center mb-3">
                        <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-700 rounded-full">
                            ${article.category || 'Общее'}
                        </span>
                        <span class="text-sm text-gray-500 ml-auto">
                            ${article.date}
                        </span>
                    </div>
                    
                    <h3 class="text-lg font-semibold mb-2 line-clamp-2">
                        <a href="/blog/${article.slug}" class="text-gray-900 hover:text-blue-600 transition-colors">
                            ${article.title}
                        </a>
                    </h3>
                    
                    ${article.excerpt ? `
                        <p class="text-gray-600 text-sm mb-4 line-clamp-3">${article.excerpt}</p>
                    ` : ''}
                    
                    <div class="flex items-center justify-between text-sm text-gray-500">
                        <div class="flex items-center space-x-4">
                            <span><i class="fas fa-clock mr-1"></i>${article.reading_time || 5} мин</span>
                            <span><i class="fas fa-eye mr-1"></i>${article.views || 0}</span>
                        </div>
                        <a href="/blog/${article.slug}" class="text-blue-600 hover:text-blue-700 font-medium">
                            Читать →
                        </a>
                    </div>
                </div>
            </article>
        `).join('');
        
        articlesContainer.innerHTML = articlesHTML;
        
        // Add fade-in animation
        articlesContainer.style.opacity = '0';
        setTimeout(() => {
            articlesContainer.style.transition = 'opacity 0.3s ease';
            articlesContainer.style.opacity = '1';
        }, 50);
    }
    
    function updateActiveCategory(activeElement) {
        // Remove active state from all categories
        document.querySelectorAll('.quick-category').forEach(cat => {
            cat.classList.remove('bg-blue-50', 'text-blue-700', 'border-blue-200');
            cat.classList.add('text-gray-700');
        });
        
        // Add active state to selected category
        activeElement.classList.remove('text-gray-700');
        activeElement.classList.add('bg-blue-50', 'text-blue-700', 'border-blue-200');
    }
    
    function updateURL(query, category) {
        const url = new URL(window.location);
        
        if (query) {
            url.searchParams.set('search', query);
        } else {
            url.searchParams.delete('search');
        }
        
        if (category) {
            url.searchParams.set('category', category);
        } else {
            url.searchParams.delete('category');
        }
        
        url.searchParams.delete('page'); // Reset pagination
        
        // Update URL without reloading page
        window.history.replaceState({}, '', url.toString());
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initBlogSearch);
    } else {
        initBlogSearch();
    }
    
})();