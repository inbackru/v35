<!DOCTYPE html>

<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>ClickBack | Кешбек за новостройки</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>


<link href="css/styles.css" rel="stylesheet"/></head>
<body class="min-h-screen bg-ton-light">
<?php include 'header.php'; ?>

<div class="relative overflow-hidden">
<!-- Decorative elements -->
<div class="absolute top-0 left-0 w-full h-1 gradient-bg"></div>
<div class="absolute top-20 -left-20 w-40 h-40 rounded-full bg-ton-primary opacity-10"></div>
<div class="absolute bottom-20 -right-20 w-60 h-60 rounded-full bg-ton-secondary opacity-10"></div>
<div class="container mx-auto px-4 py-12">
<div class="flex flex-col lg:flex-row items-center justify-center min-h-screen">
<!-- Left side - Illustration and info -->
<div class="lg:w-1/2 lg:pr-12 mb-12 lg:mb-0 relative">
<div class="max-w-md mx-auto">
<div class="flex items-center mb-8">
<div class="w-12 h-12 rounded-lg gradient-bg flex items-center justify-center mr-4">
<i class="fas fa-home text-white text-2xl"></i>
</div>
<h1 class="text-3xl font-bold text-ton-dark">InBack</h1>
</div>
<h2 class="text-4xl font-bold text-ton-dark mb-6 leading-tight">
                            Получайте кешбэк <span class="text-ton-primary">до 5%</span> при покупке новостроек
                        </h2>
<p class="text-gray-600 mb-8 text-lg">
                            Зарегистрируйтесь и получайте возврат денег с каждой покупки недвижимости. Просто, надежно и выгодно.
                        </p>
<div class="bg-white rounded-xl shadow-lg p-6 mb-8 floating-card">
<div class="flex items-start">
<div class="bg-ton-primary bg-opacity-10 p-3 rounded-lg mr-4">
<i class="fas fa-coins text-ton-primary text-xl"></i>
</div>
<div>
<h3 class="font-bold text-ton-dark mb-2">Как это работает?</h3>
<p class="text-gray-600 text-sm">
                                        1. Зарегистрируйтесь в сервисе<br/>
                                        2. Получите подбору квартир и ЖК<br/>
										3. Посмотрите ЖК с менеджером сервиса<br/>
										4. Определитесь с квартирой<br/>
                                        5. Получите кешбэк за пользование сервисом
                                    </p>
</div>
</div>
</div>
<div class="flex flex-wrap gap-4">
<div class="flex items-center bg-white px-4 py-2 rounded-lg shadow-sm">
<i class="fas fa-check-circle text-ton-primary mr-2"></i>
<span class="text-sm">Без скрытых условий</span>
</div>
<div class="flex items-center bg-white px-4 py-2 rounded-lg shadow-sm">
<i class="fas fa-shield-alt text-ton-primary mr-2"></i>
<span class="text-sm">Защита данных</span>
</div>
<div class="flex items-center bg-white px-4 py-2 rounded-lg shadow-sm">
<i class="fas fa-bolt text-ton-primary mr-2"></i>
<span class="text-sm">Мгновенные выплаты</span>
</div>
</div>
</div>
</div>
<!-- Right side - Auth forms -->
<div class="lg:w-1/2">
<div class="bg-white rounded-2xl shadow-xl overflow-hidden max-w-md w-full mx-auto">
<!-- Tabs -->
<div class="flex border-b">
<button class="flex-1 py-4 px-6 text-center font-medium tab-active" id="login-tab">
                                Вход
                            </button>
<button class="flex-1 py-4 px-6 text-center font-medium text-gray-500" id="register-tab">
                                Регистрация
                            </button>
</div>
<!-- Login Form -->
<div class="p-8" id="login-form">
<h3 class="text-2xl font-bold text-ton-dark mb-2">Войдите в аккаунт</h3>
<p class="text-gray-500 mb-6">И начните получать кешбэк уже сегодня</p>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="login-email">
                                    Email или телефон
                                </label>
<div class="relative">
<i class="fas fa-user absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="login-email" placeholder="example@mail.com" type="text"/>
</div>
</div>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="login-password">
                                    Пароль
                                </label>
<div class="relative">
<i class="fas fa-lock absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="login-password" placeholder="••••••••" type="password"/>
<button class="absolute right-3 top-3 text-gray-400 hover:text-gray-600">
<i class="fas fa-eye"></i>
</button>
</div>
</div>
<div class="flex items-center justify-between mb-6">
<div class="flex items-center">
<input class="h-4 w-4 text-ton-primary focus:ring-ton-primary border-gray-300 rounded" id="remember-me" type="checkbox"/>
<label class="ml-2 block text-sm text-gray-700" for="remember-me">
                                        Запомнить меня
                                    </label>
</div>
<button class="text-sm text-ton-primary hover:text-ton-secondary font-medium" id="show-forgot">
                                    Забыли пароль?
                                </button>
</div>
<a href="/login.php">
<button class="btn-ton w-full py-3 px-4 rounded-lg text-white font-medium mb-6">
                                Войти
                            </button>
</a>
<div class="flex items-center mb-6">
<div class="flex-1 border-t border-gray-200"></div>
<span class="px-3 text-gray-500 text-sm">Или войдите через</span>
<div class="flex-1 border-t border-gray-200"></div>
</div>
<div class="flex justify-center gap-4 mb-6">
<button class="w-12 h-12 rounded-full border flex items-center justify-center text-gray-600 hover:bg-gray-50">
<i class="fab fa-google text-xl"></i>
</button>
<button class="w-12 h-12 rounded-full border flex items-center justify-center text-gray-600 hover:bg-gray-50">
<i class="fab fa-apple text-xl"></i>
</button>
<button class="w-12 h-12 rounded-full border flex items-center justify-center text-gray-600 hover:bg-gray-50">
<i class="fab fa-facebook-f text-xl"></i>
</button>
</div>
<p class="text-center text-gray-500 text-sm">
                                Нет аккаунта? <button class="text-ton-primary hover:text-ton-secondary font-medium" id="show-register">Зарегистрируйтесь</button>
</p>
</div>
<!-- Register Form (hidden by default) -->
<div class="p-8 hidden" id="register-form">
<h3 class="text-2xl font-bold text-ton-dark mb-2">Создайте аккаунт</h3>
<p class="text-gray-500 mb-6">И получите бонус 500₽ на первый кешбэк</p>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="register-name">
                                    Ваше имя
                                </label>
<div class="relative">
<i class="fas fa-user absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="register-name" placeholder="Иван Иванов" type="text"/>
</div>
</div>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="register-email">
                                    Email
                                </label>
<div class="relative">
<i class="fas fa-envelope absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="register-email" placeholder="example@mail.com" type="email"/>
</div>
</div>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="register-phone">
                                    Телефон
                                </label>
<div class="relative">
<i class="fas fa-phone absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="register-phone" placeholder="+7 (999) 123-45-67" type="tel"/>
</div>
</div>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="register-password">
                                    Пароль
                                </label>
<div class="relative">
<i class="fas fa-lock absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="register-password" placeholder="••••••••" type="password"/>
<button class="absolute right-3 top-3 text-gray-400 hover:text-gray-600">
<i class="fas fa-eye"></i>
</button>
</div>
<p class="text-xs text-gray-500 mt-1">Минимум 8 символов, включая цифры</p>
</div>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="register-confirm">
                                    Подтвердите пароль
                                </label>
<div class="relative">
<i class="fas fa-lock absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="register-confirm" placeholder="••••••••" type="password"/>
<button class="absolute right-3 top-3 text-gray-400 hover:text-gray-600">
<i class="fas fa-eye"></i>
</button>
</div>
</div>
<div class="mb-6">
<div class="flex items-start">
<input class="h-4 w-4 text-ton-primary focus:ring-ton-primary border-gray-300 rounded mt-1" id="register-terms" type="checkbox"/>
<label class="ml-2 block text-sm text-gray-700" for="register-terms">
                                        Я согласен с <a class="text-ton-primary hover:underline" href="#">Условиями использования</a> и <a class="text-ton-primary hover:underline" href="#">Политикой конфиденциальности</a>
</label>
</div>
</div>
<button class="btn-ton w-full py-3 px-4 rounded-lg text-white font-medium mb-6">
                                Зарегистрироваться
                            </button>
<p class="text-center text-gray-500 text-sm">
                                Уже есть аккаунт? <button class="text-ton-primary hover:text-ton-secondary font-medium" id="show-login">Войдите</button>
</p>
</div>
<!-- Forgot Password Form (hidden by default) -->
<div class="p-8 hidden" id="forgot-form">
<div class="text-center mb-6">
<div class="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mx-auto mb-4 pulse">
<i class="fas fa-key text-white text-2xl"></i>
</div>
<h3 class="text-2xl font-bold text-ton-dark mb-2">Восстановление пароля</h3>
<p class="text-gray-500">Введите email, указанный при регистрации</p>
</div>
<div class="mb-6">
<label class="block text-gray-700 text-sm font-medium mb-2" for="forgot-email">
                                    Email
                                </label>
<div class="relative">
<i class="fas fa-envelope absolute left-3 top-3 text-gray-400"></i>
<input class="input-ton w-full pl-10 pr-4 py-3 rounded-lg border focus:outline-none" id="forgot-email" placeholder="example@mail.com" type="email"/>
</div>
</div>
<button class="btn-ton w-full py-3 px-4 rounded-lg text-white font-medium mb-6">
                                Отправить инструкции
                            </button>
<p class="text-center text-gray-500 text-sm">
<button class="text-ton-primary hover:text-ton-secondary font-medium" id="back-to-login">Вернуться к входу</button>
</p>
</div>
</div>
<!-- Success message (hidden by default) -->
<div class="bg-green-50 border border-green-200 rounded-lg p-4 mt-6 max-w-md mx-auto hidden" id="success-message">
<div class="flex items-center">
<div class="flex-shrink-0">
<i class="fas fa-check-circle text-green-500 text-xl"></i>
</div>
<div class="ml-3">
<h3 class="text-sm font-medium text-green-800">Письмо отправлено!</h3>
<p class="text-sm text-green-600 mt-1">Проверьте ваш email для дальнейших инструкций.</p>
</div>
</div>
</div>
</div>
</div>
</div>
</div>

<script src="js/main.js"></script>

<?php include 'footer.php'; ?>
</body>
</html>