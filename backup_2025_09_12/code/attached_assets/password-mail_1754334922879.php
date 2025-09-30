<!DOCTYPE html>

<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>TON Property - Email</title>
<script src="https://cdn.tailwindcss.com"></script>
<script crossorigin="anonymous" src="https://kit.fontawesome.com/4a9fa069dc.js"></script>

<link href="css/styles.css" rel="stylesheet"/></head>
<body class="bg-gray-50">
<?php include 'header.php'; ?>

<!-- Main Container -->
<div class="max-w-2xl mx-auto my-8 bg-white rounded-xl shadow-md overflow-hidden">
<!-- Header -->
<div class="ton-gradient p-6 text-white">
<div class="flex items-center justify-between">
<div class="flex items-center space-x-2">
<svg class="h-8 w-8" fill="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M12 2L1 7l11 5 10-5-10-5zm0 7L1 14l11 5 10-5-10-5z"></path>
</svg>
<span class="text-xl font-bold">TON Property</span>
</div>
<span class="text-sm opacity-80">Сервис новостроек с кешбеком</span>
</div>
</div>
<!-- Dynamic Content -->
<!-- Registration Email -->
<div class="text-center mb-6">
<img alt="TON Property Welcome" class="w-full max-w-xs mx-auto rounded-lg" src="https://static.openbb.co/hub/login-light.png"/>
</div>
<div class="p-6" id="registration-email">
<h2 class="text-2xl font-bold mb-4">Добро пожаловать в TON Property!</h2>
<p class="mb-4">Благодарим вас за регистрацию в нашем сервисе по продаже новостроек с кешбеком до 10% от стоимости.</p>
<div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
<p class="font-medium text-blue-800">Ваш аккаунт успешно создан!</p>
<p class="text-sm text-blue-700 mt-1">Теперь вы можете получать кешбек за каждую покупку недвижимости через наш сервис.</p>
</div>
<div class="mb-6">
<h3 class="font-bold text-lg mb-2">Что дальше?</h3>
<ul class="list-disc pl-5 space-y-2">
<li>Выбирайте новостройки из нашей проверенной базы</li>
<li>Получайте консультации от экспертов рынка</li>
<li>Оформляйте покупку через наш сервис</li>
<li>Получайте до 10% кешбека в TON криптовалюте</li>
</ul>
</div>
<div class="text-center mb-6 flex flex-col items-center">
<a class="btn-primary inline-block px-6 py-3 rounded-lg text-white font-medium mb-4" href="#">
                    Начать поиск квартиры
                </a>
<img alt="TON Coin" class="h-8" src="https://cryptologos.cc/logos/toncoin-ton-logo.png"/>
<p class="text-sm text-gray-600 mt-2">Кешбек выплачивается в TON</p>
</div>
<div class="border-t pt-4 text-sm text-gray-500">
<p>Если вы не регистрировались на нашем сервисе, пожалуйста, проигнорируйте это письмо.</p>
</div>
</div>
<!-- Password Reset Email (hidden by default) -->
<div class="p-6 hidden" id="password-reset-email">
<h2 class="text-2xl font-bold mb-4">Восстановление доступа</h2>
<p class="mb-4">Мы получили запрос на сброс пароля для вашего аккаунта в TON Property.</p>
<div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
<p class="font-medium text-blue-800">Для завершения процесса восстановления пароля нажмите на кнопку ниже:</p>
</div>
<div class="text-center mb-6">
<img alt="Password Reset" class="w-full max-w-xs mx-auto mb-4" src="https://ton.org/assets/img/password.svg"/>
<a class="btn-primary inline-block px-6 py-3 rounded-lg text-white font-medium mb-2" href="#">
                    Сбросить пароль
                </a>
<p class="text-xs text-gray-500">Ссылка действительна в течение 24 часов</p>
<div class="mt-4 p-4 bg-blue-50 rounded-lg">
<img alt="Security" class="h-8 mx-auto mb-2" src="https://ton.org/assets/img/shield.svg"/>
<p class="text-sm text-gray-700">Для вашей безопасности ссылка одноразовая и зашифрована</p>
</div>
</div>
<div class="mb-4 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r flex items-start">
<img alt="Warning" class="h-5 mr-3" src="https://ton.org/assets/img/warning.svg"/>
<p class="text-yellow-800 text-sm">Если вы не запрашивали сброс пароля, немедленно измените пароль в настройках безопасности вашего аккаунта.</p>
</div>
<div class="text-sm text-gray-500">
<p>Это письмо было отправлено автоматически. Пожалуйста, не отвечайте на него.</p>
</div>
</div>
<!-- Footer -->
<div class="bg-gray-50 p-6 border-t">
<div class="flex flex-col md:flex-row justify-between items-center">
<div class="flex items-center space-x-2 mb-4 md:mb-0">
<svg class="h-6 w-6 text-blue-600" fill="currentColor" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M12 2L1 7l11 5 10-5-10-5z"></path>
</svg>
<span class="font-medium">TON Property</span>
</div>
<div class="flex space-x-4">
<a class="text-gray-500 hover:text-blue-600" href="#">
<i class="fab fa-telegram"></i>
</a>
<a class="text-gray-500 hover:text-blue-600" href="#">
<i class="fab fa-twitter"></i>
</a>
<a class="text-gray-500 hover:text-blue-600" href="#">
<i class="fab fa-instagram"></i>
</a>
</div>
</div>
<div class="mt-4 text-center md:text-left text-xs text-gray-400">
<p>© 2023 TON Property. Все права защищены.</p>
<p class="mt-1">Это письмо было отправлено вам, потому что вы зарегистрированы в сервисе TON Property.</p>
</div>
</div>
</div>

<script src="js/main.js"></script>

<?php include 'footer.php'; ?>
</body>
</html>