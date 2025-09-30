<!-- Footer -->
    <footer class="bg-gray-900 border-t border-gray-700">
        <div class="container mx-auto px-4">
            <!-- Logo and social -->
            <div class="flex flex-col md:flex-row justify-between items-center py-4 border-b border-gray-700">
                <div class="flex items-center mb-4 md:mb-0">
                    <div class="flex items-center gap-2">
                        <div class="w-8 h-8 rounded-full bg-[rgb(0_136_204)] flex items-center justify-center text-white font-bold text-lg">C</div>
                        <span class="text-lg font-bold gradient-text">inback</span>
                    </div>
                </div>
                <div class="flex space-x-6">
                    <a href="#" class="text-gray-400 hover:text-white transition">
                        <i class="fab fa-vk text-xl"></i>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white transition">
                        <i class="fab fa-telegram text-xl"></i>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white transition">
                        <i class="fab fa-youtube text-xl"></i>
                    </a>
                </div>
            </div>

            <!-- Main footer menu -->
            <div class="py-8">
                <nav class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8">
                    <div class="footer-menu-group">
                        <h4 class="text-gray-300 font-medium mb-3 cursor-pointer flex items-center justify-between md:justify-start" onclick="toggleFooterMenu(this)">
                            О сервисе
                            <svg class="md:hidden w-4 h-4 ml-2 transform transition-transform" viewBox="0 0 20 20">
                                <path fill="currentColor" d="M7 10l5 5 5-5H7z"></path>
                            </svg>
                        </h4>
                        <ul class="footer-submenu hidden md:block space-y-2">
                            <li><a href="/about.php" class="text-gray-400 hover:text-white transition">О нас</a></li>
                            <li><a href="/how-it-works.php" class="text-gray-400 hover:text-white transition">Как это работает</a></li>
                            <li><a href="/partners.php" class="text-gray-400 hover:text-white transition">Партнеры</a></li>
                            <li><a href="/careers.php" class="text-gray-400 hover:text-white transition">Вакансии</a></li>
                            <li><a href="/reviews.php" class="text-gray-400 hover:text-white transition">Отзывы</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-menu-group">
                        <h4 class="text-gray-300 font-medium mb-3 cursor-pointer flex items-center justify-between md:justify-start" onclick="toggleFooterMenu(this)">
                            Помощь
                            <svg class="md:hidden w-4 h-4 ml-2 transform transition-transform" viewBox="0 0 20 20">
                                <path fill="currentColor" d="M7 10l5 5 5-5H7z"></path>
                            </svg>
                        </h4>
                        <ul class="footer-submenu hidden md:block space-y-2">
                            <li><a href="/legal-help.php" class="text-gray-400 hover:text-white transition">Юридическая помощь</a></li>
                            <li><a href="/contacts.php" class="text-gray-400 hover:text-white transition">Контакты</a></li>
                            <li><a href="/blog.php" class="text-gray-400 hover:text-white transition">Блог</a></li>
                        </ul>
                    </div>

                    <div class="footer-menu-group">
                        <h4 class="text-gray-300 font-medium mb-3 cursor-pointer flex items-center justify-between md:justify-start" onclick="toggleFooterMenu(this)">
                            Поиск по городу
                            <svg class="md:hidden w-4 h-4 ml-2 transform transition-transform" viewBox="0 0 20 20">
                                <path fill="currentColor" d="M7 10l5 5 5-5H7z"></path>
                            </svg>
                        </h4>
                        <ul class="footer-submenu hidden md:block space-y-2">
                            <li><a href="/location.php" class="text-gray-400 hover:text-white transition">Районы</a></li>
                            <li><a href="/streets.php" class="text-gray-400 hover:text-white transition">Улицы</a></li>
                            <li><a href="/map.php" class="text-gray-400 hover:text-white transition">Поиск по карте</a></li>
                            <li><a href="/developers.php" class="text-gray-400 hover:text-white transition">Застройщики</a></li>
                        </ul>
                    </div>

                    <div class="footer-menu-group">
                        <h4 class="text-gray-300 font-medium mb-3 cursor-pointer flex items-center justify-between md:justify-start" onclick="toggleFooterMenu(this)">
                            Ипотека
                            <svg class="md:hidden w-4 h-4 ml-2 transform transition-transform" viewBox="0 0 20 20">
                                <path fill="currentColor" d="M7 10l5 5 5-5H7z"></path>
                            </svg>
                        </h4>
                        <ul class="footer-submenu hidden md:block space-y-2">
                            <li><a href="/ipoteka.php" class="text-gray-400 hover:text-white transition">Ипотека</a></li>
                            <li><a href="/maternal-capital.php" class="text-gray-400 hover:text-white transition">Материнский капитал</a></li>
                            <li><a href="/military-mortgage.php" class="text-gray-400 hover:text-white transition">Военная ипотека</a></li>
                            <li><a href="/family-mortgage.php" class="text-gray-400 hover:text-white transition">Семейная ипотека</a></li>
                            <li><a href="/rassrochka.php" class="text-gray-400 hover:text-white transition">Рассрочка</a></li>
                            <li><a href="/rural-mortgage.php" class="text-gray-400 hover:text-white transition">Сельская ипотека</a></li>
                             <li><a href="/developer-mortgage.php" class="text-gray-400 hover:text-white transition">Ипотека от застройщика</a></li>
                              <li><a href="/it-mortgage.php" class="text-gray-400 hover:text-white transition">IT ипотека</a></li>
                        </ul>
                    </div>

                    <div class="footer-menu-group">
                        <h4 class="text-gray-300 font-medium mb-3">Документы</h4>
                        <ul class="space-y-2">
                            <li><a href="/privacy-policy.php" class="text-gray-400 hover:text-white transition">Политика конфиденциальности</a></li>
                             <li><a href="/security.php" class="text-gray-400 hover:text-white transition">Безопасность</a></li>
                        </ul>
                    </div>
                </nav>
            </div>

            <!-- Info and contacts -->
            <div class="py-8 grid grid-cols-1 md:grid-cols-3 gap-8">
                <div itemscope itemtype="https://schema.org/RealEstateAgent">
                    <h4 class="text-white font-medium mb-4" itemprop="name">О компании Inback</h4>
                    <meta itemprop="priceRange" content="2.5%-10%">
                    <div itemprop="address" itemscope itemtype="https://schema.org/PostalAddress" style="display:none;">
                        <span itemprop="streetAddress">ул. Красная, 32</span>
                        <span itemprop="addressLocality">Краснодар</span>
                        <span itemprop="addressRegion">Краснодарский край</span>
                    </div>
                    <p class="text-gray-400 mb-4">Inback - ведущий сервис кэшбека за новостройки в Краснодаре. Вернём до 10% от стоимости квартиры при покупке у наших партнеров-застройщиков.</p>
                    <p class="text-gray-400">Официальный партнер 30+ проверенных застройщиков Краснодара и Краснодарского края. Работаем с 2020 года, вернули клиентам более 150 миллионов рублей.</p>
                    <p class="text-gray-400">Лицензия на деятельность №123456789 от 01.01.2023</p>
                </div>
                
                <div>
                    <h4 class="text-white font-medium mb-4">Контакты</h4>
                    <div class="space-y-3 text-gray-400">
                        <div class="flex items-start gap-3">
                            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                            </svg>
                            <a href="tel:+78001231212" class="hover:text-white">8 800 123-12-12</a>
                        </div>
                        <div class="flex items-start gap-3">
                            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                            </svg>
                            <a href="mailto:info@inback.ru" class="hover:text-white">info@inback.ru</a>
                        </div>
                        <div class="flex items-start gap-3">
                            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                            <span>г. Краснодар, ул. Красная, 32</span>
                        </div>
                        <div class="flex items-start gap-3">
                            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                            <span>Пн-Пт: 9:00-19:00<br>Сб-Вс: 10:00-17:00</span>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h4 class="text-white font-medium mb-4">Подписаться на новости</h4>
                    <div class="flex">
                        <input type="email" placeholder="Ваш email" class="bg-gray-800 text-white px-4 py-2 rounded-l-md focus:outline-none focus:ring-1 focus:ring-[#0088CC] w-full">
                        <button class="bg-[#0088CC] text-white px-4 py-2 rounded-r-md hover:bg-[#006699] transition">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                            </svg>
                        </button>
                    </div>
                    <p class="text-xs text-gray-500 mt-2">Подписываясь, вы соглашаетесь с политикой конфиденциальности</p>
                </div>
            </div>
            
            <!-- Copyright -->
            <div class="py-6 text-center border-t border-gray-700 text-gray-400">
                © 2025 Inback. ООО "Инбэк". Официальный партнер застройщиков Краснодара. Все права защищены.
            </div>
        </div>
    </footer>