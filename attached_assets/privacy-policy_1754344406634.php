<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Политика конфиденциальности | clickback</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        ton: {
                            primary: '#0088cc',
                            dark: '#17212b',
                            light: '#f5f5f5',
                            accent: '#32a4fb',
                            secondary: '#2b5278'
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .gradient-bg {
            background: linear-gradient(135deg, #0088cc 0%, #32a4fb 100%);
        }
        
        .privacy-content {
            counter-reset: section;
        }
        
        .privacy-section h3::before {
            counter-increment: section;
            content: counter(section) ". ";
            color: #0088cc;
            font-weight: bold;
        }
        
        .highlight {
            position: relative;
        }
        
        .highlight::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 2px;
            width: 100%;
            height: 8px;
            background-color: rgba(0, 136, 204, 0.2);
            z-index: -1;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="gradient-bg text-white shadow-lg">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-2">
                    <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-sm">
                        <i class="fas fa-home text-ton-primary text-xl"></i>
                    </div>
                    <h1 class="text-2xl font-bold">clickback</h1>
                </div>
                <a href="/" class="text-white hover:underline">← Вернуться на главную</a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
        <div class="max-w-4xl mx-auto">
            <div class="bg-white rounded-xl shadow-md overflow-hidden mb-8">
                <div class="gradient-bg p-6">
                    <h1 class="text-3xl font-bold text-white mb-2">Политика конфиденциальности clickback</h1>
                    <p class="text-ton-light text-opacity-90">Последнее обновление: 1 ноября 2023 года</p>
                </div>
                
                <div class="p-6 md:p-8 privacy-content">
                    <div class="mb-8">
                        <p class="mb-4">Добро пожаловать в <span class="font-semibold text-ton-primary">clickback</span> — сервис кешбека при покупке недвижимости в новостройках.</p>
                        <p>Настоящая Политика конфиденциальности объясняет, как мы собираем, используем, раскрываем и защищаем вашу информацию при использовании нашего сервиса.</p>
                    </div>
                    
                    <div class="space-y-8 privacy-section">
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Согласие на обработку данных</h3>
                            <p class="mb-4">Используя сервис clickback, вы соглашаетесь с условиями данной Политики конфиденциальности. Если вы не согласны с этими условиями, пожалуйста, не используйте наш сервис.</p>
                            <p>Мы можем периодически обновлять эту Политику. Продолжая использование сервиса после внесения изменений, вы соглашаетесь с обновленной версией Политики.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Собираемая информация</h3>
                            <p class="mb-4">Для предоставления услуг кешбека мы можем собирать следующие виды информации:</p>
                            <ul class="list-disc pl-6 space-y-2 mb-4">
                                <li><span class="font-medium">Персональные данные:</span> имя, фамилия, отчество, контактные данные (телефон, email), паспортные данные (при необходимости для оформления кешбека)</li>
                                <li><span class="font-medium">Информация о сделке:</span> данные о выбранном ЖК, договоре долевого участия или ином договоре купли-продажи</li>
                                <li><span class="font-medium">Техническая информация:</span> IP-адрес, данные cookies, информация о браузере и устройстве</li>
                                <li><span class="font-medium">Финансовая информация:</span> реквизиты для перевода кешбека (не хранятся на наших серверах)</li>
                            </ul>
                            <p>Мы собираем только ту информацию, которая необходима для предоставления наших услуг и исполнения обязательств перед вами.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Как мы используем информацию</h3>
                            <p class="mb-4">Собранная информация используется для следующих целей:</p>
                            <ul class="list-disc pl-6 space-y-2 mb-4">
                                <li>Предоставление и персонализация услуг кешбека</li>
                                <li>Верификация вашей личности и сделки</li>
                                <li>Обратная связь и уведомления о статусе кешбека</li>
                                <li>Улучшение качества сервиса и разработка новых функций</li>
                                <li>Профилактика мошенничества и обеспечение безопасности</li>
                                <li>Выполнение юридических обязательств</li>
                            </ul>
                            <p>Мы не продаем и не передаем ваши персональные данные третьим лицам для маркетинговых целей без вашего явного согласия.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Передача данных третьим лицам</h3>
                            <p class="mb-4">В определенных случаях мы можем передавать ваши данные:</p>
                            <ul class="list-disc pl-6 space-y-2 mb-4">
                                <li><span class="font-medium">Партнерам-застройщикам:</span> для подтверждения факта покупки и расчета кешбека</li>
                                <li><span class="font-medium">Платежным системам:</span> исключительно для перевода вам кешбека</li>
                                <li><span class="font-medium">Государственным органам:</span> при наличии законного требования</li>
                                <li><span class="font-medium">Юридическим консультантам:</span> при необходимости защиты наших законных интересов</li>
                            </ul>
                            <p>Все третьи лица, получающие доступ к вашим данным, обязаны соблюдать конфиденциальность и использовать информацию только в целях, для которых она была предоставлена.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Безопасность данных</h3>
                            <p class="mb-4">Мы применяем комплексные меры безопасности для защиты ваших данных:</p>
                            <ul class="list-disc pl-6 space-y-2 mb-4">
                                <li>Шифрование передаваемых данных по протоколу TLS</li>
                                <li>Регулярное тестирование систем на уязвимости</li>
                                <li>Ограниченный доступ к персональным данным сотрудников</li>
                                <li>Регулярное резервное копирование данных</li>
                            </ul>
                            <p>Несмотря на наши усилия, ни один метод передачи или хранения данных в интернете не является абсолютно безопасным. Если у нас есть основания полагать, что произошла утечка данных, мы незамедлительно уведомим вас и соответствующие органы.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Cookies и аналогичные технологии</h3>
                            <p class="mb-4">Мы используем cookies и аналогичные технологии для:</p>
                            <ul class="list-disc pl-6 space-y-2 mb-4">
                                <li>Авторизации и аутентификации пользователей</li>
                                <li>Персонализации контента</li>
                                <li>Анализа трафика и поведения пользователей</li>
                                <li>Защиты от спама и мошенничества</li>
                            </ul>
                            <p>Вы можете управлять настройками cookies в своем браузере, но это может повлиять на функциональность сервиса.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Хранение данных</h3>
                            <p class="mb-4">Мы храним ваши персональные данные до тех пор, пока это необходимо для:</p>
                            <ul class="list-disc pl-6 space-y-2 mb-4">
                                <li>Предоставления услуг кешбека</li>
                                <li>Выполнения наших договорных обязательств</li>
                                <li>Соблюдения требований законодательства</li>
                                <li>Разрешения споров и защиты законных интересов</li>
                            </ul>
                            <p>После истечения сроков хранения ваши данные будут надежно удалены или анонимизированы.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Ваши права</h3>
                            <p class="mb-4">В соответствии с действующим законодательством, вы имеете право:</p>
                            <ul class="list-disc pl-6 space-y-2 mb-4">
                                <li>Получать информацию о том, какие ваши персональные данные мы обрабатываем</li>
                                <li>Запрашивать исправление неточных данных</li>
                                <li>Требовать удаления ваших данных при отсутствии законных оснований для их обработки</li>
                                <li>Ограничивать обработку данных в определенных случаях</li>
                                <li>Получать данные в структурированном формате для передачи другому оператору</li>
                                <li>Отозвать согласие на обработку данных</li>
                            </ul>
                            <p>Для реализации ваших прав или по любым вопросам, связанным с защитой персональных данных, вы можете обратиться к нам по контактам, указанным ниже.</p>
                        </div>
                        
                        <div>
                            <h3 class="text-xl font-semibold mb-4 text-ton-secondary">Контакты</h3>
                            <p class="mb-4">Если у вас есть вопросы о нашей Политике конфиденциальности или обработке ваших данных, пожалуйста, свяжитесь с нами:</p>
                            <div class="bg-ton-light rounded-lg p-4 mb-4">
                                <div class="flex items-center mb-2">
                                    <i class="fas fa-envelope text-ton-primary mr-2"></i>
                                    <span>Электронная почта: <a href="mailto:privacy@clickback.ru" class="text-ton-primary hover:underline">privacy@clickback.ru</a></span>
                                </div>
                                <div class="flex items-center mb-2">
                                    <i class="fas fa-phone-alt text-ton-primary mr-2"></i>
                                    <span>Телефон: <a href="tel:+78001234567" class="text-ton-primary hover:underline">8 (800) 123-45-67</a></span>
                                </div>
                                <div class="flex items-center">
                                    <i class="fas fa-map-marker-alt text-ton-primary mr-2"></i>
                                    <span>Почтовый адрес: 123456, г. Москва, ул. Строителей, д. 1, офис 101</span>
                                </div>
                            </div>
                            <p>Мы обязуемся оперативно реагировать на все обращения и разрешать возможные недоразумения в кратчайшие сроки.</p>
                        </div>
                    </div>
                    
                    <div class="mt-12 border-t pt-8">
                        <p class="text-center text-ton-secondary">© 2023 clickback. Все права защищены.</p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-ton-dark text-white py-4 text-center">
        <a href="/" class="hover:underline">← Вернуться на главную</a>
    </footer>
</body>
</html>