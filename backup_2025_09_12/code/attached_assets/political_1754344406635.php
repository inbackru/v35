<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Согласие на обработку данных | ClickBack</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        .ton-gradient {
            background: linear-gradient(135deg, #0088cc, #00aadd);
        }
        .ton-btn {
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0, 170, 255, 0.3);
        }
        .ton-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 170, 255, 0.4);
        }
        .wave-bg {
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%2300aadd' fill-opacity='0.1' d='M0,256L48,261.3C96,267,192,277,288,256C384,235,480,181,576,181.3C672,181,768,235,864,250.7C960,267,1056,245,1152,224C1248,203,1344,181,1392,170.7L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E") no-repeat bottom;
            background-size: 100% auto;
        }
        .card-animation {
            animation: float 4s ease-in-out infinite;
        }
        .checkbox-custom {
            width: 20px;
            height: 20px;
            background-color: white;
            border: 2px solid #0088cc;
            border-radius: 4px;
            transition: all 0.2s;
        }
        input[type="checkbox"]:checked + .checkbox-custom {
            background-color: #0088cc;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='white'%3E%3Cpath fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'/%3E%3C/svg%3E");
            background-position: center;
            background-repeat: no-repeat;
        }
    </style>
</head>
<body class="font-['Inter'] bg-gray-50 text-gray-800 min-h-screen flex flex-col">
    <header class="ton-gradient text-white shadow-lg">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0088cc" class="w-6 h-6">
                        <path d="M5.566 4.657A4.505 4.505 0 016.75 4.5h10.5c.41 0 .806.055 1.183.157A3 3 0 0015.75 3h-7.5a3 3 0 00-2.684 1.657zM2.25 12a3 3 0 013-3h13.5a3 3 0 013 3v6a3 3 0 01-3 3H5.25a3 3 0 01-3-3v-6zM5.25 7.5c-.41 0-.806.055-1.184.157A3 3 0 016.75 6h10.5a3 3 0 012.683 1.657A4.505 4.505 0 0018.75 7.5H5.25z" />
                    </svg>
                </div>
                <h1 class="text-xl font-bold">ClickBack</h1>
            </div>
        </div>
    </header>

    <main class="flex-grow container mx-auto px-4 py-8 wave-bg">
        <div class="max-w-4xl mx-auto lg:flex items-center gap-12">
            <div class="lg:w-1/2 mb-10 lg:mb-0">
                <div class="relative card-animation">
                    <div class="absolute -inset-2 rounded-xl bg-blue-200 opacity-75 blur-lg"></div>
                    <div class="relative bg-white rounded-xl shadow-xl p-8">
                        <div class="text-center mb-6">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0088cc" class="w-16 h-16 mx-auto">
                                <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <h2 class="text-2xl font-bold text-center text-blue-900 mb-4">Ваш кэшбек защищён</h2>
                        <p class="text-center text-gray-600 mb-6">Мы используем самые современные методы шифрования для защиты ваших персональных данных.</p>
                        <div class="flex justify-center space-x-3">
                            <div class="w-3 h-3 rounded-full bg-blue-400"></div>
                            <div class="w-3 h-3 rounded-full bg-blue-300"></div>
                            <div class="w-3 h-3 rounded-full bg-blue-200"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="lg:w-1/2 bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="ton-gradient p-6 text-white">
                    <h2 class="text-2xl font-bold">Согласие на обработку персональных данных</h2>
                    <p class="opacity-90 mt-2">Для получения кэшбека необходимо ваше подтверждение</p>
                </div>
                
                <div class="p-6">
                    <div class="bg-blue-50 rounded-lg p-4 mb-6">
                        <p class="text-sm text-blue-800">Мы обязуемся использовать ваши данные исключительно для обработки возврата кэшбека за покупку недвижимости и не передавать их третьим лицам.</p>
                    </div>
                    
                    <form id="consentForm" class="space-y-6">
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">ФИО</label>
                            <input type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="Иванов Иван Иванович" required>
                        </div>
                        
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">Email</label>
                            <input type="email" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="example@mail.com" required>
                        </div>
                        
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">Телефон</label>
                            <input type="tel" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="+7 (999) 123-45-67" required>
                        </div>
                        
                        <div class="space-y-4">
                            <label class="flex items-start space-x-3">
                                <input type="checkbox" class="hidden" id="consentCheckbox" required>
                                <div class="checkbox-custom mt-0.5"></div>
                                <span class="text-sm leading-tight text-gray-700">Я даю согласие на обработку моих персональных данных в соответствии с <a href="#" class="text-blue-600 hover:underline">Политикой конфиденциальности</a> и согласен с условиями возврата кэшбека.</span>
                            </label>
                            
                            <label class="flex items-start space-x-3">
                                <input type="checkbox" class="hidden" id="marketingCheckbox">
                                <div class="checkbox-custom mt-0.5"></div>
                                <span class="text-sm leading-tight text-gray-700">Я согласен получать информацию о специальных предложениях и акциях от ClickBack (не обязательно).</span>
                            </label>
                        </div>
                        
                        <button type="submit" class="w-full ton-gradient text-white font-bold py-3 px-4 rounded-lg ton-btn hover:bg-blue-600 transition-colors">
                            Подтвердить и получить кэшбек
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 inline ml-1">
                                <path fill-rule="evenodd" d="M5 10a.75.75 0 01.75-.75h6.638L10.23 7.29a.75.75 0 111.04-1.08l3.5 3.25a.75.75 0 010 1.08l-3.5 3.25a.75.75 0 11-1.04-1.08l2.158-1.96H5.75A.75.75 0 015 10z" clip-rule="evenodd" />
                            </svg>
                        </button>
                    </form>
                    
                    <div class="mt-6 text-xs text-gray-500">
                        <p>Нажимая кнопку, вы подтверждаете, что ознакомились с условиями оферты и политикой конфиденциальности.</p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <section id="privacy-policy" class="py-12 bg-gray-50">
        <div class="container mx-auto px-4 max-w-4xl">
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="ton-gradient p-6 text-white">
                    <h2 class="text-2xl font-bold">Политика конфиденциальности</h2>
                    <p class="opacity-90 mt-2">Последнее обновление: 1 января 2023 года</p>
                </div>
                
                <div class="p-6 space-y-6">
                    <div>
                        <h3 class="text-xl font-semibold text-blue-900 mb-3">1. Какие данные мы собираем</h3>
                        <p class="text-gray-700">При оформлении заявки на кэшбек мы собираем следующие персональные данные:</p>
                        <ul class="list-disc pl-5 mt-2 space-y-1 text-gray-700">
                            <li>Фамилия, имя и отчество</li>
                            <li>Контактный телефон</li>
                            <li>Адрес электронной почты</li>
                            <li>Данные о покупке недвижимости</li>
                        </ul>
                    </div>

                    <div>
                        <h3 class="text-xl font-semibold text-blue-900 mb-3">2. Как мы используем данные</h3>
                        <p class="text-gray-700">Мы используем ваши персональные данные для:</p>
                        <ul class="list-disc pl-5 mt-2 space-y-1 text-gray-700">
                            <li>Оформления и выплаты кэшбека</li>
                            <li>Связи с вами по вопросам выплаты</li>
                            <li>Улучшения качества нашего сервиса</li>
                            <li>Отправки информации о специальных предложениях (только с вашего согласия)</li>
                        </ul>
                    </div>

                    <div>
                        <h3 class="text-xl font-semibold text-blue-900 mb-3">3. Защита данных</h3>
                        <p class="text-gray-700">Мы используем современные методы защиты данных:</p>
                        <ul class="list-disc pl-5 mt-2 space-y-1 text-gray-700">
                            <li>Шифрование передаваемых данных</li>
                            <li>Регулярное обновление систем безопасности</li>
                            <li>Ограниченный доступ к персональным данным</li>
                        </ul>
                    </div>

                    <div>
                        <h3 class="text-xl font-semibold text-blue-900 mb-3">4. Ваши права</h3>
                        <p class="text-gray-700">Вы имеете право:</p>
                        <ul class="list-disc pl-5 mt-2 space-y-1 text-gray-700">
                            <li>Запросить доступ к вашим данным</li>
                            <li>Исправить неточности в данных</li>
                            <li>Удалить ваши данные</li>
                            <li>Отозвать согласие на обработку</li>
                        </ul>
                    </div>

                    <div class="bg-blue-50 rounded-lg p-4">
                        <p class="text-sm text-blue-800">Если у вас есть вопросы о нашей политике конфиденциальности, пожалуйста, свяжитесь с нами по адресу: privacy@clickback.ru</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <footer class="bg-white shadow-inner py-6">
        <div class="container mx-auto px-4">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="mb-4 md:mb-0">
                    <p class="text-sm text-gray-600">© 2023 ClickBack. Все права защищены.</p>
                </div>
                <div class="flex space-x-6">
                    <a href="#" class="text-sm text-gray-600 hover:text-blue-600">Политика конфиденциальности</a>
                    <a href="#" class="text-sm text-gray-600 hover:text-blue-600">Условия использования</a>
                    <a href="#" class="text-sm text-gray-600 hover:text-blue-600">Контакты</a>
                </div>
            </div>
        </div>
    </footer>

    <div id="successModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-xl max-w-md w-full p-6 transform transition-all duration-300 scale-95">
            <div class="flex justify-center mb-4">
                <div class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#10B981" class="w-8 h-8">
                        <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
                    </svg>
                </div>
            </div>
            <h3 class="text-xl font-bold text-center mb-2">Спасибо за ваше доверие!</h3>
            <p class="text-center text-gray-600 mb-6">Ваше согласие успешно отправлено. Наш менеджер свяжется с вами в ближайшее время для оформления кэшбека.</p>
            <button onclick="closeModal()" class="w-full ton-gradient text-white font-bold py-2 px-4 rounded-lg ton-btn">
                Понятно
            </button>
        </div>
    </div>

    <script>
        document.getElementById('consentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('successModal').classList.remove('hidden');
            document.getElementById('consentForm').reset();
        });

        function closeModal() {
            document.getElementById('successModal').classList.add('hidden');
        }

        // Анимация чекбоксов
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if(this.checked) {
                    this.nextElementSibling.classList.add('animate-pulse');
                    setTimeout(() => {
                        this.nextElementSibling.classList.remove('animate-pulse');
                    }, 300);
                }
            });
        });
    </script>
</body>
</html>