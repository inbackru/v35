// Mobile Menu functionality - SIMPLIFIED
document.addEventListener('DOMContentLoaded', function() {
    console.log('Mobile menu script loaded');
    
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const hamburgerIcon = document.getElementById('hamburgerIcon');
    const closeIcon = document.getElementById('closeIcon');

    console.log('Mobile menu initialization:', {
        btn: !!mobileMenuBtn,
        menu: !!mobileMenu,
        hamburger: !!hamburgerIcon,
        close: !!closeIcon
    });

    if (mobileMenuBtn) {
        console.log('Adding click event to mobile menu button');
        
        mobileMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Mobile menu button clicked');
            
            if (mobileMenu) {
                // Toggle menu visibility
                const isHidden = mobileMenu.classList.contains('hidden');
                
                if (isHidden) {
                    console.log('Opening mobile menu');
                    mobileMenu.classList.remove('hidden');
                    hamburgerIcon?.classList.add('hidden');
                    closeIcon?.classList.remove('hidden');
                    // Prevent scrolling using unified system
                    if (typeof window.unifiedDisableScroll === 'function') {
                        window.unifiedDisableScroll();
                    } else if (document.body) {
                        document.body.style.overflow = 'hidden';
                    }
                } else {
                    console.log('Closing mobile menu');
                    mobileMenu.classList.add('hidden');
                    hamburgerIcon?.classList.remove('hidden');
                    closeIcon?.classList.add('hidden');
                    // Restore scrolling using unified system
                    if (typeof window.unifiedRestoreScroll === 'function') {
                        window.unifiedRestoreScroll();
                    } else if (document.body) {
                        if (typeof window.unifiedRestoreScroll === 'function') {
                window.unifiedRestoreScroll();
            } else {
                document.body.style.overflow = '';
            }
                    }
                }
            } else {
                console.log('Mobile menu element not found, creating it');
                createAndShowMobileMenu();
            }
        });
    } else {
        console.error('Mobile menu button not found');
    }

    // Close menu when clicking outside
    if (mobileMenu) {
        mobileMenu.addEventListener('click', function(e) {
            if (e.target === mobileMenu || e.target.closest('.mobile-dropdown-btn')) {
                return; // Don't close if clicking menu content or dropdowns
            }
            console.log('Closing mobile menu - outside click');
            mobileMenu.classList.add('hidden');
            if (typeof window.unifiedRestoreScroll === 'function') {
                window.unifiedRestoreScroll();
            } else {
                document.body.style.overflow = '';
            }
        });
    }

    // Close on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu && !mobileMenu.classList.contains('hidden')) {
            console.log('Closing mobile menu - escape key');
            mobileMenu.classList.add('hidden');
            if (typeof window.unifiedRestoreScroll === 'function') {
                window.unifiedRestoreScroll();
            } else {
                document.body.style.overflow = '';
            }
        }
    });

    // Mobile dropdown functionality for existing menu
    function initMobileDropdowns() {
        const dropdownBtns = document.querySelectorAll('.mobile-dropdown-btn');
        dropdownBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const content = this.nextElementSibling;
                const arrow = this.querySelector('svg');
                
                if (content && content.classList.contains('mobile-dropdown-content')) {
                    if (content.classList.contains('hidden')) {
                        content.classList.remove('hidden');
                        arrow?.classList.add('rotate-180');
                    } else {
                        content.classList.add('hidden');
                        arrow?.classList.remove('rotate-180');
                    }
                }
            });
        });
    }

    // Initialize dropdowns when DOM is ready
    initMobileDropdowns();

    // Function to create mobile menu if it doesn't exist
    function createAndShowMobileMenu() {
        console.log('Creating mobile menu dynamically');
        
        const existingMenu = document.getElementById('dynamic-mobile-menu');
        if (existingMenu) {
            existingMenu.remove();
        }
        
        const menu = document.createElement('div');
        menu.id = 'dynamic-mobile-menu';
        menu.className = 'fixed inset-0 z-50 lg:hidden bg-black bg-opacity-50';
        
        menu.innerHTML = `
            <div class="bg-white h-full w-3/4 max-w-sm shadow-lg overflow-y-auto">
                <div class="p-4 border-b border-gray-200 flex justify-between items-center">
                    <h2 class="text-lg font-semibold text-gray-900">Меню</h2>
                    <button id="close-dynamic-menu" class="text-gray-500 hover:text-gray-700">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <nav class="p-4 space-y-1">
                    <a href="/" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Главная</a>
                    <a href="/properties" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Квартиры</a>
                    <a href="/residential-complexes" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">ЖК</a>
                    <a href="/developers" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Застройщики</a>
                    <a href="/districts" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Районы</a>
                    <a href="/streets" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Улицы</a>
                    <a href="/ipoteka" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Ипотека</a>
                    <a href="/blog" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Блог</a>
                    <a href="/about" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">О нас</a>
                    <a href="/how-it-works" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Как это работает</a>
                    <a href="/contacts" class="block px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">Контакты</a>
                    <hr class="my-4 border-gray-200">
                    <a href="tel:+78001234567" class="block px-4 py-3 text-blue-600 hover:bg-blue-50 rounded-lg font-medium">📞 +7 (800) 123-45-67</a>
                </nav>
            </div>
        `;
        
        document.body.appendChild(menu);
        document.body.style.overflow = 'hidden';
        
        // Add close handlers
        menu.querySelector('#close-dynamic-menu').addEventListener('click', () => {
            menu.remove();
            if (typeof window.unifiedRestoreScroll === 'function') {
                window.unifiedRestoreScroll();
            } else {
                document.body.style.overflow = '';
            }
        });
        
        menu.addEventListener('click', (e) => {
            if (e.target === menu) {
                menu.remove();
                if (typeof window.unifiedRestoreScroll === 'function') {
                window.unifiedRestoreScroll();
            } else {
                document.body.style.overflow = '';
            }
            }
        });
    }
});