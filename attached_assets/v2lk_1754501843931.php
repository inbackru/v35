<!DOCTYPE html>

<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>ClickBack | Личный кабинет</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>



<link href="css/styles.css" rel="stylesheet"/></head>
<body class="bg-ton-light">
<?php include 'header.php'; ?>

<div class="flex h-screen overflow-hidden">
<!-- Sidebar -->
<div class="hidden md:flex md:flex-shrink-0">
<div class="flex flex-col w-64 bg-white border-r border-gray-200">
<div class="flex items-center justify-center h-16 px-4 bg-ton-primary">
<div class="flex items-center">
<i class="fas fa-home text-white text-2xl mr-2"></i>
<span class="text-white font-bold text-xl">ClickBack</span>
</div>
</div>
<div class="flex flex-col flex-grow px-4 py-4 overflow-y-auto">
<!-- User Profile -->
<div class="flex items-center mb-8">
<div class="relative">
<img alt="User profile" class="w-12 h-12 rounded-full" src="https://randomuser.me/api/portraits/men/32.jpg"/>
<div class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
</div>
<div class="ml-3">
<p class="text-sm font-medium text-ton-dark">Иван Петров</p>
<p class="text-xs text-gray-500">ID: CB12345678</p>
</div>
</div>
<!-- Navigation -->
<nav class="flex-1 space-y-2">
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item active" href="#">
<i class="fas fa-tachometer-alt text-ton-primary mr-3 w-5 text-center"></i>
<span>Главная</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="manager" href="#">
<i class="fas fa-user-tie text-ton-primary mr-3 w-5 text-center"></i>
<span>Личный менеджер</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="cashback" href="#">
<i class="fas fa-coins text-ton-primary mr-3 w-5 text-center"></i>
<span>Кешбек</span>
<span class="ml-auto bg-ton-primary text-white text-xs px-2 py-1 rounded-full">3</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="applications" href="#">
<i class="fas fa-file-alt text-ton-primary mr-3 w-5 text-center"></i>
<span>Заявки</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="favorites" href="#">
<i class="fas fa-heart text-ton-primary mr-3 w-5 text-center"></i>
<span>Избранное</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="collections" href="#">
<i class="fas fa-list text-ton-primary mr-3 w-5 text-center"></i>
<span>Подборки</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="documents" href="#">
<i class="fas fa-file-alt text-ton-primary mr-3 w-5 text-center"></i>
<span>Документы</span>
<span class="ml-auto bg-red-500 text-white text-xs px-2 py-1 rounded-full">3</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="settings" href="#">
<i class="fas fa-cog text-ton-primary mr-3 w-5 text-center"></i>
<span>Настройки</span>
</a>
<a class="flex items-center px-4 py-2.5 text-sm font-medium sidebar-item" data-page="placeholder" href="#">
<i class="fas fa-question-circle text-ton-primary mr-3 w-5 text-center"></i>
<span>Заглушка</span>
</a>
</nav>
<!-- Support -->
<div class="mt-auto pt-4">
<div class="bg-ton-light rounded-lg p-4">
<div class="flex items-center">
<img alt="Manager profile" class="w-12 h-12 rounded-full" src="https://randomuser.me/api/portraits/women/44.jpg"/>
<div class="ml-3">
<p class="text-sm font-medium text-ton-dark">Анна Смирнова</p>
<p class="text-xs text-gray-500">Ваш персональный менеджер</p>
<p class="text-xs font-medium text-ton-primary mt-1">+7(999)-999-99-99</p>
</div>
</div>
<div class="grid grid-cols-4 gap-2 mt-3">
<a class="flex items-center justify-center bg-white hover:bg-green-100 text-green-600 py-2 px-2 rounded-lg transition duration-200 border border-gray-200 hover:border-green-300 shadow-sm hover:shadow-md" href="https://wa.me/79991234567" target="_blank">
<i class="fab fa-whatsapp"></i>
</a>
<a class="flex items-center justify-center bg-white hover:bg-blue-100 text-blue-500 py-2 px-2 rounded-lg transition duration-200 border border-gray-200 hover:border-blue-300 shadow-sm hover:shadow-md" href="https://t.me/clickback_manager" target="_blank">
<i class="fab fa-telegram-plane"></i>
</a>
<a class="flex items-center justify-center bg-white hover:bg-red-100 text-red-500 py-2 px-2 rounded-lg transition duration-200 border border-gray-200 hover:border-red-300 shadow-sm hover:shadow-md" href="mailto:manager@clickback.ru">
<i class="fas fa-envelope"></i>
</a>
<button class="flex items-center justify-center bg-ton-primary hover:bg-blue-700 text-white py-2 px-2 rounded-lg transition duration-200 shadow-md hover:shadow-lg">
<i class="fas fa-comment-dots"></i>
</button>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- Main Content -->
<div class="flex flex-col flex-1 overflow-hidden">
<!-- Mobile Header -->
<div class="md:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200">
<button class="text-ton-dark">
<i class="fas fa-bars text-xl"></i>
</button>
<div class="flex items-center">
<i class="fas fa-home text-ton-primary text-xl mr-2"></i>
<span class="text-ton-dark font-bold">ClickBack</span>
</div>
<div class="relative">
<button class="focus:outline-none" id="notification-button-mobile">
<i class="fas fa-bell text-xl text-ton-dark"></i>
<div class="notification-badge" id="notification-badge-mobile">5</div>
</button>
<div class="absolute right-0 mt-2 w-72 bg-white rounded-lg shadow-lg z-50 overflow-hidden" id="notification-dropdown-mobile" style="display: none;">
<div class="px-4 py-3 border-b border-gray-200">
<h3 class="text-sm font-medium text-ton-dark">Уведомления</h3>
</div>
<div class="divide-y divide-gray-100 max-h-96 overflow-y-auto">
<!-- Notification items -->
<a class="flex px-4 py-3 hover:bg-gray-50" href="#">
<div class="flex-shrink-0">
<div class="bg-blue-100 p-2 rounded-full">
<i class="fas fa-info-circle text-blue-600"></i>
</div>
</div>
<div class="ml-3">
<p class="text-sm font-medium text-gray-900">Новая заявка одобрена</p>
<p class="text-sm text-gray-500">Ваша заявка на ЖК "Солнечный" одобрена</p>
<p class="text-xs text-gray-400 mt-1">2 часа назад</p>
</div>
</a>
<a class="flex px-4 py-3 hover:bg-gray-50" href="#">
<div class="flex-shrink-0">
<div class="bg-green-100 p-2 rounded-full">
<i class="fas fa-check-circle text-green-600"></i>
</div>
</div>
<div class="ml-3">
<p class="text-sm font-medium text-gray-900">Выплата отправлена</p>
<p class="text-sm text-gray-500">Ваша выплата 75,000 ₽ обработана</p>
<p class="text-xs text-gray-400 mt-1">1 день назад</p>
</div>
</a>
<a class="flex px-4 py-3 hover:bg-gray-50" href="#">
<div class="flex-shrink-0">
<div class="bg-yellow-100 p-2 rounded-full">
<i class="fas fa-exclamation-circle text-yellow-600"></i>
</div>
</div>
<div class="ml-3">
<p class="text-sm font-medium text-gray-900">Требуются документы</p>
<p class="text-sm text-gray-500">Для ЖК "Лесная Гавань" нужны дополнительные документы</p>
<p class="text-xs text-gray-400 mt-1">2 дня назад</p>
</div>
</a>
</div>
<div class="px-4 py-2 bg-gray-50 text-center">
<a class="text-sm font-medium text-ton-primary hover:text-blue-700" href="#">Показать все</a>
</div>
</div>
</div>
</div>
<!-- Desktop Header -->
<div class="hidden md:flex items-center justify-between px-6 py-4 bg-white border-b border-gray-200">
<div class="flex items-center space-x-6">
<h1 class="text-xl font-semibold text-ton-dark">Добро пожаловать, Иван!</h1>
<a class="text-ton-primary hover:underline flex items-center text-sm" href="https://clickback.ru">
<i class="fas fa-arrow-left mr-1"></i> На главный сайт
                    </a>
</div>
<div class="flex items-center space-x-4">
<div class="relative">
<button class="focus:outline-none" id="notification-button">
<i class="fas fa-bell text-xl text-ton-primary cursor-pointer"></i>
<div class="notification-badge" id="notification-badge">5</div>
</button>
<div class="hidden absolute right-0 mt-2 w-72 bg-white rounded-lg shadow-lg z-50 overflow-hidden" id="notification-dropdown">
<div class="px-4 py-3 border-b border-gray-200">
<h3 class="text-sm font-medium text-ton-dark">Уведомления</h3>
</div>
<div class="divide-y divide-gray-100 max-h-96 overflow-y-auto">
<!-- Notification items -->
<a class="flex px-4 py-3 hover:bg-gray-50" href="#">
<div class="flex-shrink-0">
<div class="bg-blue-100 p-2 rounded-full">
<i class="fas fa-info-circle text-blue-600"></i>
</div>
</div>
<div class="ml-3">
<p class="text-sm font-medium text-gray-900">Новая заявка одобрена</p>
<p class="text-sm text-gray-500">Ваша заявка на ЖК "Солнечный" одобрена</p>
<p class="text-xs text-gray-400 mt-1">2 часа назад</p>
</div>
</a>
<a class="flex px-4 py-3 hover:bg-gray-50" href="#">
<div class="flex-shrink-0">
<div class="bg-green-100 p-2 rounded-full">
<i class="fas fa-check-circle text-green-600"></i>
</div>
</div>
<div class="ml-3">
<p class="text-sm font-medium text-gray-900">Выплата отправлена</p>
<p class="text-sm text-gray-500">Ваша выплата 75,000 ₽ обработана</p>
<p class="text-xs text-gray-400 mt-1">1 день назад</p>
</div>
</a>
<a class="flex px-4 py-3 hover:bg-gray-50" href="#">
<div class="flex-shrink-0">
<div class="bg-yellow-100 p-2 rounded-full">
<i class="fas fa-exclamation-circle text-yellow-600"></i>
</div>
</div>
<div class="ml-3">
<p class="text-sm font-medium text-gray-900">Требуются документы</p>
<p class="text-sm text-gray-500">Для ЖК "Лесная Гавань" нужны дополнительные документы</p>
<p class="text-xs text-gray-400 mt-1">2 дня назад</p>
</div>
</a>
</div>
<div class="px-4 py-2 bg-gray-50 text-center">
<a class="text-sm font-medium text-ton-primary hover:text-blue-700" href="#">Показать все</a>
</div>
</div>
</div>
<div class="relative">
<button class="flex items-center focus:outline-none" id="user-menu-button">
<img alt="User profile" class="w-8 h-8 rounded-full" src="https://randomuser.me/api/portraits/men/32.jpg"/>
<span class="ml-2 text-sm font-medium text-ton-dark">Иван Петров</span>
<i class="fas fa-chevron-down ml-1 text-xs text-gray-500"></i>
</button>
<div class="hidden absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg py-2 z-50 overflow-hidden" id="user-menu">
<a class="flex items-center px-4 py-3 text-sm font-medium text-gray-700 hover:bg-ton-primary hover:text-white transition duration-150 ease-in-out" href="#">
<i class="fas fa-user-circle w-5 mr-3 text-gray-400 group-hover:text-white"></i>
<span>Личный кабинет</span>
</a>
<a class="flex items-center px-4 py-3 text-sm font-medium text-gray-700 hover:bg-ton-primary hover:text-white transition duration-150 ease-in-out" href="#settings">
<i class="fas fa-cog w-5 mr-3 text-gray-400 group-hover:text-white"></i>
<span>Профиль</span>
</a>
<div class="border-t border-gray-100 my-1"></div>
<a class="flex items-center px-4 py-3 text-sm font-medium text-red-600 hover:bg-red-50 transition duration-150 ease-in-out" href="#">
<i class="fas fa-sign-out-alt w-5 mr-3 text-red-400"></i>
<span>Выйти</span>
</a>
</div>
</div>
</div>
</div>
<!-- Content -->
<div class="flex-1 overflow-auto p-4 md:p-6">
<!-- Cashback Section -->
<div class="hidden" id="cashback">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6">
<h1 class="text-2xl font-bold text-ton-dark mb-6">Ваш кешбек</h1>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
<div class="bg-ton-light rounded-lg p-5">
<div class="flex justify-between items-center mb-4">
<h3 class="text-lg font-semibold text-ton-dark">Доступный кешбек</h3>
<span class="text-xl font-bold text-ton-primary">125,000  ₽</span>
</div>
<button class="w-full bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition duration-200">
                                    Запросить выплату
                                </button>
</div>
<div class="bg-ton-light rounded-lg p-5">
<div class="flex justify-between items-center mb-4">
<h3 class="text-lg font-semibold text-ton-dark">Всего накоплено</h3>
<span class="text-xl font-bold text-ton-dark">250,000 ₽</span>
</div>
<div class="progress-bar">
<div class="progress-fill" style="width: 50%"></div>
</div>
</div>
</div>
<h2 class="text-xl font-semibold text-ton-dark mb-4">История операций</h2>
<div class="overflow-x-auto">
<table class="min-w-full bg-white">
<thead>
<tr class="border-b border-gray-200">
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Дата</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Операция</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Сумма</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Статус</th>
</tr>
</thead>
<tbody>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">12.05.2023</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Солнечный"</td>
<td class="py-3 px-4 text-sm font-medium text-green-600">+75,000  ₽</td>
<td class="py-3 px-4 text-sm text-gray-700"><span class="bg-green-100 text-green-800 py-1 px-2 rounded-full text-xs">Выплачено</span></td>
</tr>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">28.05.2023</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Лесная Гавань"</td>
<td class="py-3 px-4 text-sm font-medium text-blue-600">+50,000  ₽</td>
<td class="py-3 px-4 text-sm text-gray-700"><span class="bg-blue-100 text-blue-800 py-1 px-2 rounded-full text-xs">В обработке</span></td>
</tr>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">03.06.2023</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Центральный"</td>
<td class="py-3 px-4 text-sm font-medium text-yellow-600">+50,000 ₽</td>
<td class="py-3 px-4 text-sm text-gray-700"><span class="bg-yellow-100 text-yellow-800 py-1 px-2 rounded-full text-xs">Требуются документы</span></td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
<!-- Cashback Page -->
<div class="hidden" id="cashback-page">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6">
<h1 class="text-2xl font-bold text-ton-dark mb-6">Ваш кешбек</h1>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
<div class="bg-ton-light rounded-lg p-5">
<div class="flex justify-between items-center mb-4">
<h3 class="text-lg font-semibold text-ton-dark">Доступный кешбек</h3>
<span class="text-xl font-bold text-ton-primary">125,000 ₽</span>
</div>
<button class="w-full bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition duration-200">
                                    Запросить выплату
                                </button>
</div>
<div class="bg-ton-light rounded-lg p-5">
<div class="flex justify-between items-center mb-4">
<h3 class="text-lg font-semibold text-ton-dark">Всего накоплено</h3>
<span class="text-xl font-bold text-ton-dark">250,000 ₽</span>
</div>
<div class="progress-bar">
<div class="progress-fill" style="width: 50%"></div>
</div>
</div>
</div>
<div class="bg-white rounded-lg p-5 mb-8">
<h2 class="text-xl font-semibold text-ton-dark mb-4">Калькулятор кешбека</h2>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Стоимость объекта</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="1,000,000 ₽" type="number"/>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Процент кешбека</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg" placeholder="5%" type="number"/>
</div>
<div class="bg-ton-light p-4 rounded-lg">
<p class="text-sm text-gray-500">Ваш кешбек составит</p>
<p class="text-2xl font-bold text-ton-primary">50,000 ₽</p>
</div>
</div>
</div>
<h2 class="text-xl font-semibold text-ton-dark mb-4">История операций</h2>
<div class="overflow-x-auto">
<table class="min-w-full bg-white">
<thead>
<tr class="border-b border-gray-200">
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Дата</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Операция</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Сумма</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Статус</th>
</tr>
</thead>
<tbody>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">12.05.2023</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Солнечный"</td>
<td class="py-3 px-4 text-sm font-medium text-green-600">+75,000 ₽</td>
<td class="py-3 px-4 text-sm text-gray-700"><span class="bg-green-100 text-green-800 py-1 px-2 rounded-full text-xs">Выплачено</span></td>
</tr>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">28.05.2023</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Лесная Гавань"</td>
<td class="py-3 px-4 text-sm font-medium text-blue-600">+50,000 ₽</td>
<td class="py-3 px-4 text-sm text-gray-700"><span class="bg-blue-100 text-blue-800 py-1 px-2 rounded-full text-xs">В обработке</span></td>
</tr>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">03.06.2023</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Центральный"</td>
<td class="py-3 px-4 text-sm font-medium text-yellow-600">+50,000 ₽</td>
<td class="py-3 px-4 text-sm text-gray-700"><span class="bg-yellow-100 text-yellow-800 py-1 px-2 rounded-full text-xs">Требуются документы</span></td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
<!-- Collections Page -->
<div class="hidden" id="collections-page">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6">
<div class="flex items-center mb-6">
<a class="text-ton-primary hover:underline flex items-center" href="#">
<i class="fas fa-home mr-2"></i>
                                Главная
                            </a>
<span class="mx-2 text-gray-400">/</span>
<span class="text-gray-600">Подборки квартир</span>
</div>
<h1 class="text-2xl font-bold text-ton-dark mb-6">Подборки квартир</h1>
<div class="mb-6">
<div class="relative">
<input class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-ton-primary focus:border-transparent transition duration-200 pl-10" placeholder="Поиск подборок..." type="text"/>
<i class="fas fa-search absolute left-3 top-3.5 text-gray-400"></i>
</div>
</div>
<div class="flex justify-end mb-6">
<button class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition duration-200 flex items-center">
<i class="fas fa-plus mr-2"></i> Создать подборку
                            </button>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
<!-- Collection 1 -->
<div class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition duration-200 card-hover border border-gray-100">
<div class="relative">
<img alt="Новостройки у метро" class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="absolute top-3 right-3 bg-white bg-opacity-90 rounded-full p-2 shadow-sm">
<i class="fas fa-bookmark text-ton-primary"></i>
</div>
</div>
<div class="p-5">
<div class="flex justify-between items-start">
<h3 class="text-lg font-semibold text-ton-dark mb-2">Новостройки у метро</h3>
<span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">Новые</span>
</div>
<p class="text-sm text-gray-500 mb-4">12 объектов в пешей доступности от станций метро</p>
<div class="flex justify-between items-center">
<div>
<span class="text-sm text-gray-500">Кешбек до</span>
<span class="text-ton-primary font-bold ml-1">5%</span>
</div>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg text-sm transition duration-200">
                                            Показать <i class="fas fa-chevron-right ml-1"></i>
</button>
</div>
</div>
</div>
<!-- Collection 2 -->
<div class="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition duration-200 card-hover">
<img alt="Студии в центре" class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="p-4">
<h3 class="text-lg font-semibold text-ton-dark mb-2">Студии в центре</h3>
<p class="text-sm text-gray-500 mb-4">8 компактных квартир в центре города</p>
<div class="flex justify-between items-center">
<span class="text-sm text-gray-500">Кешбек до 7%</span>
<button class="text-ton-primary hover:underline text-sm">Показать</button>
</div>
</div>
</div>
<!-- Collection 3 -->
<div class="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition duration-200 card-hover">
<img alt="Семейные квартиры" class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="p-4">
<h3 class="text-lg font-semibold text-ton-dark mb-2">Семейные квартиры</h3>
<p class="text-sm text-gray-500 mb-4">15 просторных вариантов для семей</p>
<div class="flex justify-between items-center">
<span class="text-sm text-gray-500">Кешбек до 6%</span>
<button class="text-ton-primary hover:underline text-sm">Показать</button>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- Favorites Page -->
<div class="hidden" id="favorites-page">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6">
<h1 class="text-2xl font-bold text-ton-dark mb-6">Избранные объекты</h1>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<!-- Favorite Item 1 -->
<div class="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition duration-200">
<img alt="ЖК Речной" class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="p-4">
<div class="flex justify-between items-start">
<h3 class="text-lg font-semibold text-ton-dark">ЖК "Речной"</h3>
<button class="text-red-500 hover:text-red-700">
<i class="fas fa-heart"></i>
</button>
</div>
<p class="text-sm text-gray-500 mt-1">2-комн. квартира, 56 м²</p>
<div class="flex justify-between items-center mt-4">
<span class="text-lg font-bold text-ton-primary">8,500,000 ₽</span>
<button class="text-ton-primary hover:underline text-sm">Подробнее</button>
</div>
</div>
</div>
<!-- Favorite Item 2 -->
<div class="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition duration-200">
<img alt="ЖК Парковый" class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="p-4">
<div class="flex justify-between items-start">
<h3 class="text-lg font-semibold text-ton-dark">ЖК "Парковый"</h3>
<button class="text-red-500 hover:text-red-700">
<i class="fas fa-heart"></i>
</button>
</div>
<p class="text-sm text-gray-500 mt-1">3-комн. квартира, 78 м²</p>
<div class="flex justify-between items-center mt-4">
<span class="text-lg font-bold text-ton-primary">12,300,000  ₽</span>
<button class="text-ton-primary hover:underline text-sm">Подробнее</button>
</div>
</div>
</div>
<!-- Favorite Item 3 -->
<div class="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition duration-200">
<img alt="ЖК Солнечный" class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="p-4">
<div class="flex justify-between items-start">
<h3 class="text-lg font-semibold text-ton-dark">ЖК "Солнечный"</h3>
<button class="text-red-500 hover:text-red-700">
<i class="fas fa-heart"></i>
</button>
</div>
<p class="text-sm text-gray-500 mt-1">1-комн. квартира, 42 м²</p>
<div class="flex justify-between items-center mt-4">
<span class="text-lg font-bold text-ton-primary">6,200,000  ₽</span>
<button class="text-ton-primary hover:underline text-sm">Подробнее</button>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- Manager Placeholder Page -->
<div class="hidden" id="manager-page">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6 overflow-hidden relative">
<div class="absolute top-0 right-0 w-64 h-64 bg-ton-primary opacity-5 rounded-full -mr-32 -mt-32"></div>
<div class="text-center py-8 relative z-10">
<div class="mx-auto w-32 h-32 rounded-full bg-gradient-to-br from-ton-primary to-blue-300 flex items-center justify-center mb-6 shadow-lg">
<i class="fas fa-user-tie text-4xl text-white"></i>
</div>
<h2 class="text-3xl font-bold text-ton-dark mb-2">Личный менеджер</h2>
<p class="text-gray-500 mb-8 max-w-lg mx-auto">Ваш персональный менеджер поможет с любыми вопросами и подберет лучшие варианты</p>
<div class="max-w-md mx-auto bg-gradient-to-br from-white to-blue-50 rounded-xl p-8 border border-blue-100 shadow-sm">
<div class="flex items-center mb-8 p-4 bg-white rounded-lg shadow-sm">
<img alt="Manager" class="w-16 h-16 rounded-full border-2 border-white shadow-md" src="https://randomuser.me/api/portraits/women/44.jpg"/>
<div class="ml-4 text-left">
<h3 class="font-bold text-ton-dark">Анна Смирнова</h3>
<p class="text-sm text-gray-500">Ваш персональный менеджер</p>
<div class="flex items-center mt-1">
<i class="fas fa-star text-yellow-400 text-xs"></i>
<span class="text-xs text-gray-500 ml-1">4.9 рейтинг</span>
</div>
</div>
</div>
<h3 class="text-xl font-semibold text-ton-dark mb-6">Свяжитесь удобным способом</h3>
<div class="space-y-4">
<a class="flex items-center justify-between bg-white hover:bg-ton-primary hover:text-white text-ton-dark py-4 px-6 rounded-xl transition duration-200 shadow-sm border border-gray-100 hover:border-ton-primary" href="tel:+74951234567">
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-4">
<i class="fas fa-phone-alt text-blue-600"></i>
</div>
<span>+7 (495) 123-45-67</span>
</div>
<i class="fas fa-chevron-right text-sm opacity-70"></i>
</a>
<a class="flex items-center justify-between bg-white hover:bg-ton-primary hover:text-white text-ton-dark py-4 px-6 rounded-xl transition duration-200 shadow-sm border border-gray-100 hover:border-ton-primary" href="https://t.me/clickback_support">
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-4">
<i class="fab fa-telegram text-blue-600"></i>
</div>
<span>@clickback_support</span>
</div>
<i class="fas fa-chevron-right text-sm opacity-70"></i>
</a>
<a class="flex items-center justify-between bg-white hover:bg-ton-primary hover:text-white text-ton-dark py-4 px-6 rounded-xl transition duration-200 shadow-sm border border-gray-100 hover:border-ton-primary" href="mailto:support@clickback.ru">
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-4">
<i class="fas fa-envelope text-blue-600"></i>
</div>
<span>support@clickback.ru</span>
</div>
<i class="fas fa-chevron-right text-sm opacity-70"></i>
</a>
</div>
</div>
</div>
</div>
</div>
<!-- Applications Page -->
<div class="hidden" id="applications-page">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6">
<h1 class="text-2xl font-bold text-ton-dark mb-6">Ваши заявки на кешбек</h1>
<div class="mb-8">
<div class="bg-white rounded-xl shadow-sm p-6 mb-8 border border-dashed border-ton-primary">
<h2 class="text-xl font-semibold text-ton-dark mb-6">Новая заявка на кешбек</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div class="relative">
<label class="block text-sm font-medium text-gray-700 mb-1">Жилой комплекс</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary" placeholder="Название ЖК" type="text"/>
</div>
<div class="relative">
<label class="block text-sm font-medium text-gray-700 mb-1">Тип недвижимости</label>
<select class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary">
<option>Квартира</option>
<option>Апартаменты</option>
<option>Коммерческая</option>
</select>
</div>
<div class="relative">
<label class="block text-sm font-medium text-gray-700 mb-1">Стоимость объекта</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary" placeholder="₽" type="number"/>
</div>
<div class="relative">
<label class="block text-sm font-medium text-gray-700 mb-1">Ожидаемый кешбек %</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary" placeholder="%" type="number"/>
</div>
<div class="md:col-span-2">
<label class="block text-sm font-medium text-gray-700 mb-1">Дополнительные пожелания</label>
<textarea class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary" rows="3"></textarea>
</div>
</div>
<div class="mt-6 flex justify-end space-x-4">
<button class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
                                        Отмена
                                    </button>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-6 rounded-lg transition duration-200">
<i class="fas fa-check-circle mr-2"></i>Отправить заявку
                                    </button>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
<div class="bg-ton-light rounded-lg p-4">
<h3 class="text-lg font-semibold text-ton-dark mb-2">Всего заявок</h3>
<p class="text-2xl font-bold">7</p>
</div>
<div class="bg-ton-light rounded-lg p-4">
<h3 class="text-lg font-semibold text-ton-dark mb-2">На проверке</h3>
<p class="text-2xl font-bold text-blue-600">3</p>
</div>
<div class="bg-ton-light rounded-lg p-4">
<h3 class="text-lg font-semibold text-ton-dark mb-2">Одобрено</h3>
<p class="text-2xl font-bold text-green-600">4</p>
</div>
</div>
</div>
<div class="overflow-x-auto">
<table class="min-w-full bg-white">
<thead>
<tr class="border-b border-gray-200">
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">ID заявки</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Жилой комплекс</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Дата подачи</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Сумма кешбека</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Статус</th>
<th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Действия</th>
</tr>
</thead>
<tbody>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">CB-2023-045</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Речной"</td>
<td class="py-3 px-4 text-sm text-gray-700">15.06.2023</td>
<td class="py-3 px-4 text-sm font-medium text-ton-dark">85,000  ₽</td>
<td class="py-3 px-4 text-sm text-gray-700">
<span class="bg-green-100 text-green-800 py-1 px-2 rounded-full text-xs">Одобрено</span>
</td>
<td class="py-3 px-4 text-sm text-gray-700">
<button class="text-ton-primary hover:underline">Подробнее</button>
</td>
</tr>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">CB-2023-044</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Парковый"</td>
<td class="py-3 px-4 text-sm text-gray-700">10.06.2023</td>
<td class="py-3 px-4 text-sm font-medium text-ton-dark">120,000 ₽</td>
<td class="py-3 px-4 text-sm text-gray-700">
<span class="bg-blue-100 text-blue-800 py-1 px-2 rounded-full text-xs">На проверке</span>
</td>
<td class="py-3 px-4 text-sm text-gray-700">
<button class="text-ton-primary hover:underline">Подробнее</button>
</td>
</tr>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">CB-2023-043</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Солнечный"</td>
<td class="py-3 px-4 text-sm text-gray-700">05.06.2023</td>
<td class="py-3 px-4 text-sm font-medium text-ton-dark">75,000  ₽</td>
<td class="py-3 px-4 text-sm text-gray-700">
<span class="bg-yellow-100 text-yellow-800 py-1 px-2 rounded-full text-xs">Требуются документы</span>
</td>
<td class="py-3 px-4 text-sm text-gray-700">
<button class="text-ton-primary hover:underline">Загрузить</button>
</td>
</tr>
<tr class="border-b border-gray-100 hover:bg-gray-50">
<td class="py-3 px-4 text-sm text-gray-700">CB-2023-042</td>
<td class="py-3 px-4 text-sm text-gray-700">ЖК "Лесная Гавань"</td>
<td class="py-3 px-4 text-sm text-gray-700">01.06.2023</td>
<td class="py-3 px-4 text-sm font-medium text-ton-dark">95,000 ₽</td>
<td class="py-3 px-4 text-sm text-gray-700">
<span class="bg-green-100 text-green-800 py-1 px-2 rounded-full text-xs">Одобрено</span>
</td>
<td class="py-3 px-4 text-sm text-gray-700">
<button class="text-ton-primary hover:underline">Подробнее</button>
</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
<!-- Stats Cards -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
<div class="bg-white rounded-xl shadow-sm p-5 card-hover transition duration-200">
<div class="flex items-center justify-between">
<div>
<p class="text-sm text-gray-500">Доступный кешбек</p>
<p class="text-2xl font-bold text-ton-dark mt-1">125,000 ₽</p>
</div>
<div class="bg-ton-primary bg-opacity-10 p-3 rounded-full">
<i class="fas fa-wallet text-ton-primary text-xl"></i>
</div>
</div>
<div class="mt-4">
<div class="flex justify-between text-xs text-gray-500 mb-1">
<span>Всего накоплено</span>
<span>250,000 ₽</span>
</div>
<div class="progress-bar">
<div class="progress-fill" style="width: 50%"></div>
</div>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm p-5 card-hover transition duration-200">
<div class="flex items-center justify-between">
<div>
<p class="text-sm text-gray-500">Активные заявки</p>
<p class="text-2xl font-bold text-ton-dark mt-1">3</p>
</div>
<div class="bg-green-100 p-3 rounded-full">
<i class="fas fa-file-alt text-green-600 text-xl"></i>
</div>
</div>
<div class="mt-4">
<div class="flex justify-between text-xs text-gray-500 mb-1">
<span>Всего заявок</span>
<span>7</span>
</div>
<div class="progress-bar">
<div class="progress-fill" style="width: 42%"></div>
</div>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm p-5 card-hover transition duration-200">
<div class="flex items-center justify-between">
<div>
<p class="text-sm text-gray-500">Избранные объекты</p>
<p class="text-2xl font-bold text-ton-dark mt-1">12</p>
</div>
<div class="bg-red-100 p-3 rounded-full">
<i class="fas fa-heart text-red-600 text-xl"></i>
</div>
</div>
<div class="mt-4">
<div class="flex justify-between text-xs text-gray-500 mb-1">
<span>Просмотрено за месяц</span>
<span>28</span>
</div>
<div class="progress-bar">
<div class="progress-fill" style="width: 75%"></div>
</div>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm p-5 card-hover transition duration-200">
<div class="flex items-center justify-between">
<div>
<p class="text-sm text-gray-500">Персональные подборки</p>
<p class="text-2xl font-bold text-ton-dark mt-1">5</p>
</div>
<div class="bg-purple-100 p-3 rounded-full">
<i class="fas fa-list text-purple-600 text-xl"></i>
</div>
</div>
<div class="mt-4">
<div class="flex justify-between text-xs text-gray-500 mb-1">
<span>Рекомендовано</span>
<span>15</span>
</div>
<div class="progress-bar">
<div class="progress-fill" style="width: 33%"></div>
</div>
</div>
</div>
</div>
<!-- Main Sections -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<!-- Left Column -->
<div class="lg:col-span-2 space-y-6">
<!-- Documents Block -->
<div class="bg-white rounded-xl shadow-lg p-6 mb-6">
<div class="flex justify-between items-center mb-8">
<div>
<h2 class="text-2xl font-bold text-ton-dark">
<i class="fas fa-file-alt text-ton-primary mr-3"></i>
                                        Мои документы
                                    </h2>
<p class="text-gray-500 mt-1">3/8 документов загружено</p>
</div>
<span class="bg-red-500 text-white text-sm px-3 py-1 rounded-full">Требуются документы</span>
</div>
<!-- Upload Section -->
<div class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center mb-6 hover:border-ton-primary transition duration-200 cursor-pointer">
<div class="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
<i class="fas fa-cloud-upload-alt text-2xl text-ton-primary"></i>
</div>
<h3 class="text-lg font-medium text-ton-dark mb-2">Перетащите файлы сюда</h3>
<p class="text-gray-500 mb-4">или</p>
<label class="cursor-pointer">
<span class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition duration-200 inline-flex items-center">
<i class="fas fa-folder-open mr-2"></i> Выбрать файлы
                                        <input class="hidden" multiple="" type="file"/>
</span>
</label>
<p class="text-xs text-gray-400 mt-4">PDF, JPG, PNG, DOC до 25MB</p>
</div>
<!-- Documents List -->
<div class="space-y-4">
<div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-ton-primary transition duration-200">
<div class="flex items-center">
<div class="bg-red-50 p-2 rounded-lg mr-4">
<i class="fas fa-file-pdf text-xl text-red-500"></i>
</div>
<div>
<h3 class="font-medium text-ton-dark">Паспорт.pdf</h3>
<p class="text-xs text-gray-500">Загружен: 12.05.2023</p>
</div>
</div>
<span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">Проверен</span>
</div>
<div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-ton-primary transition duration-200">
<div class="flex items-center">
<div class="bg-blue-50 p-2 rounded-lg mr-4">
<i class="fas fa-file-contract text-xl text-blue-500"></i>
</div>
<div>
<h3 class="font-medium text-ton-dark">Ипотечный договор.pdf</h3>
<p class="text-xs text-gray-500">Загружен: 15.05.2023</p>
</div>
</div>
<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">На проверке</span>
</div>
<div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-ton-primary transition duration-200">
<div class="flex items-center">
<div class="bg-yellow-50 p-2 rounded-lg mr-4">
<i class="fas fa-exclamation-circle text-xl text-yellow-500"></i>
</div>
<div>
<h3 class="font-medium text-ton-dark">Выписка из ЕГРН</h3>
<p class="text-xs text-gray-500">Требуется срочно</p>
</div>
</div>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-1 px-3 rounded-lg text-xs">
                                        Загрузить
                                    </button>
</div>
</div>
<div class="pt-4 mt-4 border-t border-gray-200 text-right">
<a class="text-ton-primary hover:underline font-medium inline-flex items-center" href="#documents">
                                    Все документы <i class="fas fa-chevron-right ml-2"></i>
</a>
</div>
</div>
<!-- Personal Manager -->
<div class="bg-white rounded-xl shadow-sm p-5 relative overflow-hidden">
<div class="absolute top-0 right-0 w-32 h-32 bg-ton-primary opacity-5 rounded-full -mr-10 -mt-10"></div>
<div class="flex items-center justify-between mb-4">
<h2 class="text-lg font-semibold text-ton-dark">Ваш личный менеджер</h2>
<button class="text-ton-primary text-sm font-medium hover:underline">Написать сообщение</button>
</div>
<div class="flex items-center p-4 bg-gradient-to-r from-ton-light to-blue-50 rounded-lg border border-blue-100">
<div class="relative floating">
<img alt="Manager profile" class="w-16 h-16 rounded-full border-2 border-white shadow-md" src="https://randomuser.me/api/portraits/women/44.jpg"/>
<div class="absolute -bottom-1 -right-1 bg-green-500 w-4 h-4 rounded-full border-2 border-white"></div>
</div>
<div class="ml-4">
<p class="font-medium text-ton-dark">Анна Смирнова</p>
<p class="text-sm text-gray-500">Персональный менеджер ClickBack</p>
<p class="text-xs font-medium text-ton-primary mt-1">+7(999)-999-99-99</p>
<p class="text-xs font-medium text-ton-primary mt-1">+7(999)-999-99-99</p>
<div class="flex items-center mt-1">
<div class="flex">
<i class="fas fa-star text-yellow-400 text-sm"></i>
<i class="fas fa-star text-yellow-400 text-sm"></i>
<i class="fas fa-star text-yellow-400 text-sm"></i>
<i class="fas fa-star text-yellow-400 text-sm"></i>
<i class="fas fa-star text-yellow-400 text-sm"></i>
</div>
<span class="text-xs text-gray-500 ml-1">4.9 (87 отзывов)</span>
</div>
</div>
</div>
<div class="mt-4 grid grid-cols-4 gap-2">
<a class="flex items-center justify-center bg-white hover:bg-green-100 text-green-600 py-2 px-2 rounded-lg transition duration-200 border border-gray-200 hover:border-green-300 shadow-sm hover:shadow-md" href="https://wa.me/79991234567" target="_blank">
<i class="fab fa-whatsapp"></i>
</a>
<a class="flex items-center justify-center bg-white hover:bg-blue-100 text-blue-500 py-2 px-2 rounded-lg transition duration-200 border border-gray-200 hover:border-blue-300 shadow-sm hover:shadow-md" href="https://t.me/clickback_manager" target="_blank">
<i class="fab fa-telegram-plane"></i>
</a>
<a class="flex items-center justify-center bg-white hover:bg-red-100 text-red-500 py-2 px-2 rounded-lg transition duration-200 border border-gray-200 hover:border-red-300 shadow-sm hover:shadow-md" href="mailto:manager@clickback.ru">
<i class="fas fa-envelope"></i>
</a>
<button class="flex items-center justify-center bg-ton-primary hover:bg-blue-700 text-white py-2 px-2 rounded-lg transition duration-200 shadow-md hover:shadow-lg">
<i class="fas fa-comment-dots"></i>
</button>
</div>
</div>
<!-- Cashback Applications -->
<div class="bg-white rounded-xl shadow-sm p-5">
<div class="flex items-center justify-between mb-4">
<h2 class="text-lg font-semibold text-ton-dark">Заявки на кешбек</h2>
<button class="text-ton-primary text-sm font-medium">Все заявки</button>
</div>
<div class="space-y-4">
<div class="flex items-center p-3 bg-ton-light rounded-lg">
<div class="bg-green-100 p-2 rounded-lg">
<i class="fas fa-check-circle text-green-600"></i>
</div>
<div class="ml-3 flex-1">
<p class="font-medium text-ton-dark">ЖК "Солнечный"</p>
<p class="text-sm text-gray-500">Одобрено: 75,000 ₽</p>
</div>
<div class="text-right">
<p class="text-xs text-gray-500">12.05.2023</p>
<button class="text-ton-primary text-xs font-medium mt-1">Подробнее</button>
</div>
</div>
<div class="flex items-center p-3 bg-ton-light rounded-lg">
<div class="bg-blue-100 p-2 rounded-lg">
<i class="fas fa-clock text-blue-600"></i>
</div>
<div class="ml-3 flex-1">
<p class="font-medium text-ton-dark">ЖК "Лесная Гавань"</p>
<p class="text-sm text-gray-500">На проверке: 50,000 ₽</p>
</div>
<div class="text-right">
<p class="text-xs text-gray-500">28.05.2023</p>
<button class="text-ton-primary text-xs font-medium mt-1">Подробнее</button>
</div>
</div>
<div class="flex items-center p-3 bg-ton-light rounded-lg">
<div class="bg-yellow-100 p-2 rounded-lg">
<i class="fas fa-exclamation-circle text-yellow-600"></i>
</div>
<div class="ml-3 flex-1">
<p class="font-medium text-ton-dark">ЖК "Центральный"</p>
<p class="text-sm text-gray-500">Требуются документы</p>
</div>
<div class="text-right">
<p class="text-xs text-gray-500">03.06.2023</p>
<button class="text-ton-primary text-xs font-medium mt-1">Подробнее</button>
</div>
</div>
</div>
</div>
</div>
<!-- Right Column -->
<div class="space-y-6">
<!-- Quick Actions -->
<div class="bg-white rounded-xl shadow-sm p-5">
<h2 class="text-lg font-semibold text-ton-dark mb-4">Быстрые действия</h2>
<div class="grid grid-cols-2 gap-3">
<button class="flex flex-col items-center justify-center bg-ton-light hover:bg-ton-primary hover:text-white text-ton-dark py-4 px-2 rounded-lg transition duration-200" id="new-application-btn">
<i class="fas fa-plus-circle text-2xl mb-2"></i>
<span class="text-sm">Новая заявка</span>
</button>
<button class="flex flex-col items-center justify-center bg-ton-light hover:bg-ton-primary hover:text-white text-ton-dark py-4 px-2 rounded-lg transition duration-200">
<i class="fas fa-search-dollar text-2xl mb-2"></i>
<span class="text-sm">Найти объект</span>
</button>
<a class="flex flex-col items-center justify-center bg-ton-light hover:bg-ton-primary hover:text-white text-ton-dark py-4 px-2 rounded-lg transition duration-200" href="#documents">
<i class="fas fa-file-invoice-dollar text-2xl mb-2"></i>
<span class="text-sm">Документы</span>
</a>
<button class="flex flex-col items-center justify-center bg-ton-light hover:bg-ton-primary hover:text-white text-ton-dark py-4 px-2 rounded-lg transition duration-200">
<i class="fas fa-headset text-2xl mb-2"></i>
<span class="text-sm">Поддержка</span>
</button>
</div>
</div>
<!-- Favorites -->
<div class="bg-white rounded-xl shadow-sm p-5">
<div class="flex items-center justify-between mb-4">
<h2 class="text-lg font-semibold text-ton-dark">Избранное</h2>
<button class="text-ton-primary text-sm font-medium">Все объекты</button>
</div>
<div class="space-y-3">
<div class="flex items-center p-3 hover:bg-ton-light rounded-lg transition duration-200 cursor-pointer">
<img alt="Property" class="w-12 h-12 rounded-lg object-cover" src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="ml-3 flex-1">
<p class="font-medium text-ton-dark text-sm">ЖК "Речной"</p>
<p class="text-xs text-gray-500">2-комн. квартира, 56 м²</p>
</div>
<i class="fas fa-heart text-red-500"></i>
</div>
<div class="flex items-center p-3 hover:bg-ton-light rounded-lg transition duration-200 cursor-pointer">
<img alt="Property" class="w-12 h-12 rounded-lg object-cover" src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="ml-3 flex-1">
<p class="font-medium text-ton-dark text-sm">ЖК "Парковый"</p>
<p class="text-xs text-gray-500">3-комн. квартира, 78 м²</p>
</div>
<i class="fas fa-heart text-red-500"></i>
</div>
<div class="flex items-center p-3 hover:bg-ton-light rounded-lg transition duration-200 cursor-pointer">
<img alt="Property" class="w-12 h-12 rounded-lg object-cover" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"/>
<div class="ml-3 flex-1">
<p class="font-medium text-ton-dark text-sm">ЖК "Солнечный"</p>
<p class="text-xs text-gray-500">1-комн. квартира, 42 м²</p>
</div>
<i class="fas fa-heart text-red-500"></i>
</div>
</div>
</div>
<!-- Recommended Collections -->
<div class="bg-white rounded-xl shadow-sm p-5">
<div class="flex items-center justify-between mb-4">
<h2 class="text-lg font-semibold text-ton-dark">Рекомендуемые подборки</h2>
<button class="text-ton-primary text-sm font-medium">Все подборки</button>
</div>
<div class="space-y-3">
<div class="p-3 bg-ton-light rounded-lg cursor-pointer hover:bg-ton-primary hover:text-white transition duration-200">
<p class="font-medium">Новостройки у метро</p>
<p class="text-xs mt-1">12 объектов</p>
</div>
<div class="p-3 bg-ton-light rounded-lg cursor-pointer hover:bg-ton-primary hover:text-white transition duration-200">
<p class="font-medium">Студии в центре</p>
<p class="text-xs mt-1">8 объектов</p>
</div>
<div class="p-3 bg-ton-light rounded-lg cursor-pointer hover:bg-ton-primary hover:text-white transition duration-200">
<p class="font-medium">Семейные квартиры</p>
<p class="text-xs mt-1">15 объектов</p>
</div>
</div>
</div>
</div>
</div>
<!-- Documents Page -->
<div class="hidden" id="documents-page">
<div class="bg-white rounded-xl shadow-lg p-6">
<div class="flex justify-between items-center mb-8">
<div>
<h1 class="text-3xl font-bold text-ton-dark">
<i class="fas fa-folder-open text-ton-primary mr-3"></i>
                                    Мои документы
                                </h1>
<p class="text-gray-500 mt-1">Все загруженные и требуемые документы</p>
</div>
<span class="bg-ton-primary text-white text-sm px-3 py-1 rounded-full">8 документов</span>
</div>
<!-- Document Categories -->
<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
<button class="flex flex-col items-center justify-center bg-gray-50 hover:bg-ton-primary hover:text-white text-ton-dark p-3 rounded-lg transition duration-200 border border-gray-200">
<i class="fas fa-user-tie text-2xl mb-2"></i>
<span class="text-sm">Личные</span>
</button>
<button class="flex flex-col items-center justify-center bg-gray-50 hover:bg-ton-primary hover:text-white text-ton-dark p-3 rounded-lg transition duration-200 border border-gray-200">
<i class="fas fa-home text-2xl mb-2"></i>
<span class="text-sm">Недвижимость</span>
</button>
<button class="flex flex-col items-center justify-center bg-gray-50 hover:bg-ton-primary hover:text-white text-ton-dark p-3 rounded-lg transition duration-200 border border-gray-200">
<i class="fas fa-file-signature text-2xl mb-2"></i>
<span class="text-sm">Ипотека</span>
</button>
<button class="flex flex-col items-center justify-center bg-gray-50 hover:bg-ton-primary hover:text-white text-ton-dark p-3 rounded-lg transition duration-200 border border-gray-200">
<i class="fas fa-coins text-2xl mb-2"></i>
<span class="text-sm">Кешбек</span>
</button>
</div>
<!-- Upload Section -->
<div class="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-200">
<h2 class="text-xl font-semibold text-ton-dark mb-6">Загрузка документов</h2>
<!-- Drag & Drop Area -->
<div class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center mb-6 hover:border-ton-primary transition duration-200 cursor-pointer">
<div class="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
<i class="fas fa-cloud-upload-alt text-3xl text-ton-primary"></i>
</div>
<h3 class="text-lg font-medium text-ton-dark mb-2">Перетащите файлы сюда</h3>
<p class="text-gray-500 mb-4">или</p>
<label class="cursor-pointer">
<span class="bg-ton-primary hover:bg-blue-700 text-white py-3 px-6 rounded-lg font-medium transition duration-200 shadow-md hover:shadow-lg inline-flex items-center">
<i class="fas fa-folder-open mr-2"></i> Выбрать файлы на компьютере 
                                        <input accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" class="hidden" multiple="" type="file"/>
</span>
</label>
<p class="text-xs text-gray-400 mt-4">Поддерживаемые форматы: PDF, JPG, PNG, DOC, DOCX (до 25MB каждый)</p>
</div>
<!-- Upload Progress -->
<div class="space-y-4">
<div class="flex items-center p-3 bg-blue-50 rounded-lg">
<div class="w-10 h-10 bg-white rounded-full flex items-center justify-center mr-3">
<i class="fas fa-file-pdf text-red-500"></i>
</div>
<div class="flex-1">
<div class="flex justify-between text-sm mb-1">
<span class="font-medium">Паспорт.pdf</span>
<span>1.2 MB</span>
</div>
<div class="w-full bg-gray-200 rounded-full h-1.5">
<div class="bg-green-600 h-1.5 rounded-full" style="width: 45%"></div>
</div>
</div>
<button class="ml-4 text-gray-400 hover:text-red-500">
<i class="fas fa-times"></i>
</button>
</div>
<div class="flex items-center p-3 bg-blue-50 rounded-lg">
<div class="w-10 h-10 bg-white rounded-full flex items-center justify-center mr-3">
<i class="fas fa-file-image text-blue-500"></i>
</div>
<div class="flex-1">
<div class="flex justify-between text-sm mb-1">
<span class="font-medium">Договор.jpg</span>
<span>2.5 MB</span>
</div>
<div class="w-full bg-gray-200 rounded-full h-1.5">
<div class="bg-green-600 h-1.5 rounded-full" style="width: 75%"></div>
</div>
</div>
<button class="ml-4 text-gray-400 hover:text-red-500">
<i class="fas fa-times"></i>
</button>
</div>
</div>
<!-- Requirements -->
<div class="mt-6 pt-6 border-t border-gray-200">
<h3 class="text-sm font-medium text-ton-dark mb-3">Требования к документам:</h3>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div>
<h4 class="font-medium text-ton-dark mb-2">Общие требования</h4>
<ul class="text-sm text-gray-600 space-y-2">
<li class="flex items-start">
<i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
<span>Четкое изображение всех страниц документа</span>
</li>
<li class="flex items-start">
<i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
<span>Документы должны быть действительны на момент проверки</span>
</li>
<li class="flex items-start">
<i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
<span>Подписи и печати должны быть читаемы</span>
</li>
</ul>
</div>
<div>
<h4 class="font-medium text-ton-dark mb-2">Ипотечные документы</h4>
<ul class="text-sm text-gray-600 space-y-2">
<li class="flex items-start">
<i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
<span>Все страницы договора (включая приложения)</span>
</li>
<li class="flex items-start">
<i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
<span>График платежей (если отдельно)</span>
</li>
<li class="flex items-start">
<i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
<span>Справки о доходах по форме банка</span>
</li>
</ul>
</div>
</div>
</div>
</div>
<!-- Documents List with Tabs -->
<div class="mb-8">
<div class="border-b border-gray-200">
<nav class="flex -mb-px space-x-8">
<button class="border-b-2 border-ton-primary text-ton-primary whitespace-nowrap py-4 px-1 font-medium text-sm">Все документы</button>
<button class="border-b-2 border-transparent text-gray-500 hover:text-gray-700 whitespace-nowrap py-4 px-1 font-medium text-sm hover:border-gray-300">Личные</button>
<button class="border-b-2 border-transparent text-gray-500 hover:text-gray-700 whitespace-nowrap py-4 px-1 font-medium text-sm hover:border-gray-300">Ипотека</button>
<button class="border-b-2 border-transparent text-gray-500 hover:text-gray-700 whitespace-nowrap py-4 px-1 font-medium text-sm hover:border-gray-300">Недвижимость</button>
<button class="border-b-2 border-transparent text-gray-500 hover:text-gray-700 whitespace-nowrap py-4 px-1 font-medium text-sm hover:border-gray-300">Кешбек</button>
</nav>
</div>
</div>
<!-- Documents List -->
<div class="space-y-4">
<!-- Personal Documents -->
<h3 class="text-lg font-semibold text-ton-dark mb-4">Личные документы</h3>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 hover:border-ton-primary transition duration-200 group">
<div class="flex items-center p-4">
<div class="bg-red-50 p-3 rounded-lg mr-4">
<i class="fas fa-file-pdf text-2xl text-red-500"></i>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-lg font-semibold text-ton-dark truncate">Паспорт.pdf</h3>
<div class="flex items-center text-sm text-gray-500 mt-1">
<span class="mr-4">1.2 MB</span>
<span class="mr-4">•</span>
<span class="mr-4">Загружен: 12.05.2023</span>
<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">Обязательный</span>
</div>
</div>
<div class="flex space-x-3 opacity-0 group-hover:opacity-100 transition-opacity">
<button class="text-gray-400 hover:text-blue-500 p-2" title="Скачать">
<i class="fas fa-download"></i>
</button>
<button class="text-gray-400 hover:text-green-500 p-2" title="Просмотреть">
<i class="fas fa-eye"></i>
</button>
<button class="text-gray-400 hover:text-red-500 p-2" title="Удалить">
<i class="fas fa-trash"></i>
</button>
</div>
</div>
</div>
<!-- Mortgage Documents -->
<h3 class="text-lg font-semibold text-ton-dark mb-4 mt-8">Ипотечные документы</h3>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 hover:border-ton-primary transition duration-200 group">
<div class="flex items-center p-4">
<div class="bg-blue-50 p-3 rounded-lg mr-4">
<i class="fas fa-file-contract text-2xl text-blue-500"></i>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-lg font-semibold text-ton-dark truncate">Ипотечный договор.pdf</h3>
<div class="flex items-center text-sm text-gray-500 mt-1">
<span class="mr-4">3.1 MB</span>
<span class="mr-4">•</span>
<span class="mr-4">Загружен: 15.05.2023</span>
<span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">Подтверждён</span>
</div>
</div>
<div class="flex space-x-3 opacity-0 group-hover:opacity-100 transition-opacity">
<button class="text-gray-400 hover:text-blue-500 p-2" title="Скачать">
<i class="fas fa-download"></i>
</button>
<button class="text-gray-400 hover:text-green-500 p-2" title="Просмотреть">
<i class="fas fa-eye"></i>
</button>
<button class="text-gray-400 hover:text-red-500 p-2" title="Удалить">
<i class="fas fa-trash"></i>
</button>
</div>
</div>
</div>
<!-- Property Documents -->
<h3 class="text-lg font-semibold text-ton-dark mb-4 mt-8">Документы по недвижимости</h3>
<div class="bg-white rounded-xl shadow-sm border border-gray-100 hover:border-ton-primary transition duration-200 group">
<div class="flex items-center p-4">
<div class="bg-blue-50 p-3 rounded-lg mr-4">
<i class="fas fa-file-image text-2xl text-blue-500"></i>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-lg font-semibold text-ton-dark truncate">Договор купли-продажи.jpg</h3>
<div class="flex items-center text-sm text-gray-500 mt-1">
<span class="mr-4">2.5 MB</span>
<span class="mr-4">•</span>
<span class="mr-4">Загружен: 28.05.2023</span>
<span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">Подтверждён</span>
</div>
</div>
<div class="flex space-x-3 opacity-0 group-hover:opacity-100 transition-opacity">
<button class="text-gray-400 hover:text-blue-500 p-2" title="Скачать">
<i class="fas fa-download"></i>
</button>
<button class="text-gray-400 hover:text-green-500 p-2" title="Просмотреть">
<i class="fas fa-eye"></i>
</button>
<button class="text-gray-400 hover:text-red-500 p-2" title="Удалить">
<i class="fas fa-trash"></i>
</button>
</div>
</div>
</div>
<!-- Missing Documents -->
<h3 class="text-lg font-semibold text-ton-dark mb-4 mt-8">Необходимо загрузить</h3>
<div class="bg-white rounded-xl shadow-sm border border-gray-200 border-dashed">
<div class="flex items-center p-4">
<div class="bg-yellow-50 p-3 rounded-lg mr-4">
<i class="fas fa-exclamation-circle text-2xl text-yellow-500"></i>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-lg font-semibold text-ton-dark truncate">Выписка из ЕГРН</h3>
<p class="text-sm text-gray-500 mt-1">Требуется для подтверждения сделки</p>
</div>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg text-sm transition duration-200">
                                        Загрузить
                                    </button>
</div>
</div>
<div class="bg-white rounded-xl shadow-sm border border-gray-200 border-dashed">
<div class="flex items-center p-4">
<div class="bg-yellow-50 p-3 rounded-lg mr-4">
<i class="fas fa-exclamation-circle text-2xl text-yellow-500"></i>
</div>
<div class="flex-1 min-w-0">
<h3 class="text-lg font-semibold text-ton-dark truncate">Справка о доходах (2-НДФЛ)</h3>
<p class="text-sm text-gray-500 mt-1">Необходима для ипотечной заявки</p>
</div>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg text-sm transition duration-200">
                                        Загрузить
                                    </button>
</div>
</div>
</div>
<!-- Help Section -->
<div class="bg-ton-light rounded-xl p-6 mt-8 border border-gray-200">
<div class="flex items-start">
<div class="bg-white p-3 rounded-full shadow-md mr-4">
<i class="fas fa-question-circle text-ton-primary text-xl"></i>
</div>
<div>
<h3 class="text-xl font-semibold text-ton-dark mb-2">Нужна помощь с документами?</h3>
<p class="text-gray-600 mb-4">Наш менеджер поможет с загрузкой и проверкой всех необходимых документов</p>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition duration-200 inline-flex items-center">
<i class="fas fa-headset mr-2"></i> Связаться с поддержкой
                                    </button>
</div>
</div>
</div>
</div>
</div>
<!-- Placeholder Page -->
<div class="hidden" id="placeholder-page">
<div class="bg-white rounded-xl shadow-lg p-6">
<div class="text-center py-12">
<div class="mx-auto w-24 h-24 bg-ton-light rounded-full flex items-center justify-center mb-6">
<i class="fas fa-file-alt text-3xl text-ton-primary"></i>
</div>
<h2 class="text-2xl font-bold text-ton-dark mb-4">Извините, у вас нет активных заявок</h2>
<p class="text-gray-500 mb-8 max-w-md mx-auto">Как только у вас появятся активные заявки, они отобразятся здесь.</p>
<div class="max-w-md mx-auto bg-ton-light rounded-xl p-6">
<h3 class="text-lg font-semibold text-ton-dark mb-4">Контакты компании</h3>
<div class="space-y-3">
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-3">
<i class="fas fa-phone-alt text-blue-600"></i>
</div>
<span>+7 (495) 123-45-67</span>
</div>
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-3">
<i class="fab fa-telegram text-blue-600"></i>
</div>
<span>@clickback_support</span>
</div>
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-3">
<i class="fas fa-envelope text-blue-600"></i>
</div>
<span>support@clickback.ru</span>
</div>
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-3">
<i class="fas fa-map-marker-alt text-blue-600"></i>
</div>
<span>Москва, ул. Примерная, д. 123</span>
</div>
<div class="flex items-center">
<div class="bg-blue-100 p-2 rounded-lg mr-3">
<i class="fas fa-clock text-blue-600"></i>
</div>
<span>Пн-Пт: 9:00 - 18:00</span>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- Settings Page -->
<div class="hidden" id="settings-page">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6">
<h1 class="text-2xl font-bold text-ton-dark mb-6">Настройки профиля</h1>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<!-- Profile Settings -->
<div class="md:col-span-2">
<div class="bg-white rounded-xl shadow-sm p-6 mb-6 border border-gray-100">
<h2 class="text-xl font-bold text-ton-dark mb-6 pb-4 border-b border-gray-100">Личные данные</h2>
<div class="space-y-6">
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="relative">
<label class="absolute -top-2 left-3 bg-white px-1 text-sm font-medium text-gray-500">Имя</label>
<input class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-ton-primary focus:border-transparent transition duration-200" type="text" value="Иван"/>
</div>
<div class="relative">
<label class="absolute -top-2 left-3 bg-white px-1 text-sm font-medium text-gray-500">Фамилия</label>
<input class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-ton-primary focus:border-transparent transition duration-200" type="text" value="Петров"/>
</div>
<div class="relative">
<label class="absolute -top-2 left-3 bg-white px-1 text-sm font-medium text-gray-500">Отчество</label>
<input class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-ton-primary focus:border-transparent transition duration-200" placeholder="Иванович" type="text"/>
</div>
</div>
<div class="relative">
<label class="absolute -top-2 left-3 bg-white px-1 text-sm font-medium text-gray-500">Email</label>
<div class="flex items-center">
<input class="flex-1 px-4 py-3 border border-gray-200 rounded-l-lg focus:ring-2 focus:ring-ton-primary focus:border-transparent transition duration-200" type="email" value="ivan.petrov@example.com"/>
<button class="bg-green-100 text-green-700 px-4 py-3 rounded-r-lg text-sm font-medium hover:bg-green-200 transition duration-200">
<i class="fas fa-check-circle mr-1"></i> Подтвержден
                                                </button>
</div>
</div>
<div class="relative">
<label class="absolute -top-2 left-3 bg-white px-1 text-sm font-medium text-gray-500">Телефон</label>
<div class="flex items-center">
<input class="flex-1 px-4 py-3 border border-gray-200 rounded-l-lg focus:ring-2 focus:ring-ton-primary focus:border-transparent transition duration-200" type="tel" value="+7 (999) 123-45-67"/>
<button class="bg-yellow-100 text-yellow-700 px-4 py-3 rounded-r-lg text-sm font-medium hover:bg-yellow-200 transition duration-200">
<i class="fas fa-exclamation-circle mr-1"></i> Подтвердить
                                                </button>
</div>
<p class="mt-1 text-xs text-gray-500">Мы отправим SMS с кодом подтверждения</p>
</div>
<div class="pt-4 border-t border-gray-100">
<button class="bg-ton-primary hover:bg-blue-700 text-white py-3 px-6 rounded-lg font-medium transition duration-200 shadow-md hover:shadow-lg">
                                                Сохранить изменения
                                            </button>
</div>
</div>
</div>
<div class="bg-white rounded-lg shadow-sm p-5">
<h2 class="text-lg font-semibold text-ton-dark mb-4">Безопасность</h2>
<div class="space-y-4">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Текущий пароль</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg" type="password"/>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Новый пароль</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg" type="password"/>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Подтвердите пароль</label>
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg" type="password"/>
</div>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition duration-200">
                                            Сохранить изменения
                                        </button>
</div>
</div>
</div>
<!-- Profile Picture -->
<div>
<div class="bg-white rounded-lg shadow-sm p-5 sticky top-6">
<h2 class="text-lg font-semibold text-ton-dark mb-4">Фото профиля</h2>
<div class="flex flex-col items-center">
<div class="relative mb-4">
<img alt="User profile" class="w-32 h-32 rounded-full" src="https://randomuser.me/api/portraits/men/32.jpg"/>
<div class="absolute bottom-0 right-0 w-8 h-8 bg-ton-primary rounded-full border-2 border-white flex items-center justify-center">
<i class="fas fa-camera text-white text-sm"></i>
</div>
</div>
<button class="text-ton-primary hover:underline text-sm mb-6">
                                            Загрузить новое фото
                                        </button>
<div class="w-full">
<h3 class="text-md font-medium text-ton-dark mb-2">Предпочтения</h3>
<div class="space-y-2">
<label class="flex items-center">
<input checked="" class="rounded text-ton-primary" type="checkbox"/>
<span class="ml-2 text-sm">Получать уведомления</span>
</label>
<label class="flex items-center">
<input checked="" class="rounded text-ton-primary" type="checkbox"/>
<span class="ml-2 text-sm">Получать рекомендации</span>
</label>
<label class="flex items-center">
<input class="rounded text-ton-primary" type="checkbox"/>
<span class="ml-2 text-sm">Показывать в рейтинге</span>
</label>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- New Application Modal -->
<div class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center p-4" id="new-application-modal">
<div class="bg-white rounded-xl max-w-5xl w-full max-h-[90vh] overflow-y-auto">
<div class="p-8">
<!-- Progress Tracker -->
<div class="mb-8">
<div class="flex items-center">
<div class="flex items-center text-ton-primary relative">
<div class="rounded-full transition duration-500 ease-in-out h-12 w-12 border-2 bg-ton-primary border-ton-primary flex items-center justify-center">
<span class="text-white font-bold">1</span>
</div>
<div class="hidden absolute top-0 -ml-10 text-center mt-16 w-32 text-xs font-medium uppercase text-ton-primary">Основные параметры</div>
</div>
<div class="flex-auto border-t-2 transition duration-500 ease-in-out border-gray-300"></div>
<div class="flex items-center text-gray-500 relative">
<div class="rounded-full transition duration-500 ease-in-out h-12 w-12 border-2 border-gray-300 flex items-center justify-center">
<span class="text-gray-600 font-bold">2</span>
</div>
<div class="hidden absolute top-0 -ml-10 text-center mt-16 w-32 text-xs font-medium uppercase text-gray-500">Дополнительно</div>
</div>
<div class="flex-auto border-t-2 transition duration-500 ease-in-out border-gray-300"></div>
<div class="flex items-center text-gray-500 relative">
<div class="rounded-full transition duration-500 ease-in-out h-12 w-12 border-2 border-gray-300 flex items-center justify-center">
<span class="text-gray-600 font-bold">3</span>
</div>
<div class="hidden absolute top-0 -ml-10 text-center mt-16 w-32 text-xs font-medium uppercase text-gray-500">Подтверждение</div>
</div>
</div>
</div>
<div class="flex justify-between items-center mb-8">
<div>
<h3 class="text-2xl font-bold text-ton-dark">Персональный подбор новостройки</h3>
<p class="text-gray-500 mt-1">Заполните форму и получите эксклюзивные варианты</p>
</div>
<button class="text-gray-500 hover:text-gray-700 text-2xl" id="close-application-modal">
<i class="fas fa-times"></i>
</button>
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
<div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Город*</label>
<input class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition" placeholder="Москва, Санкт-Петербург..." type="text"/>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Район (опционально)</label>
<input class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition" placeholder="Предпочтительный район" type="text"/>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Тип недвижимости*</label>
<select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition">
<option>Квартира</option>
<option>Апартаменты</option>
<option>Таймшер</option>
<option>Паркинг</option>
</select>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Количество комнат*</label>
<select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition">
<option>Студия</option>
<option>1</option>
<option>2</option>
<option>3</option>
<option>4+</option>
</select>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Отделка</label>
<select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition">
<option>Не важна</option>
<option>Без отделки</option>
<option>Предчистовая</option>
<option>Чистовая</option>
<option>Под ключ</option>
</select>
</div>
<div>
<label class="block text-sm font-medium text-gray-700 mb-1">Этаж</label>
<select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition">
<option>Не важен</option>
<option>Только первый</option>
<option>Средние этажи</option>
<option>Последний</option>
</select>
</div>
<div class="md:col-span-2">
<label class="block text-sm font-medium text-gray-700 mb-1">Бюджет (₽)*</label>
<div class="relative">
<input class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition pl-12" placeholder="От 2 000 000 ₽" type="text"/>
<span class="absolute left-3 top-3.5 text-gray-500">₽</span>
</div>
</div>
<div class="md:col-span-2">
<label class="block text-sm font-medium text-gray-700 mb-1">Площадь (м²)</label>
<div class="grid grid-cols-2 gap-4">
<div class="relative">
<input class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition pl-12" placeholder="От" type="text"/>
<span class="absolute left-3 top-3.5 text-gray-500">от</span>
</div>
<div class="relative">
<input class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition pl-12" placeholder="До" type="text"/>
<span class="absolute left-3 top-3.5 text-gray-500">до</span>
</div>
</div>
</div>
<div class="md:col-span-2">
<label class="block text-sm font-medium text-gray-700 mb-1">Желаемые сроки сдачи</label>
<select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition">
<option>Не важно</option>
<option>Уже сдан</option>
<option>В этом году</option>
<option>В течение 1-2 лет</option>
<option>В течение 2-5 лет</option>
</select>
</div>
<div class="md:col-span-2">
<label class="block text-sm font-medium text-gray-700 mb-1">Дополнительные пожелания</label>
<textarea class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-ton-primary focus:border-ton-primary transition" placeholder="Хорошая транспортная доступность, развитая инфраструктура, парковка..." rows="3"></textarea>
</div>
</div>
<!-- Cashback Calculator -->
<div class="bg-ton-light rounded-lg p-5 mb-6">
<h4 class="text-lg font-semibold text-ton-dark mb-4 flex items-center">
<i class="fas fa-calculator text-ton-primary mr-2"></i> Калькулятор кешбека
                            </h4>
<div class="grid grid-cols-3 gap-4">
<div>
<label class="block text-xs font-medium text-gray-500 mb-1">Стоимость (₽)</label>
<input class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg" placeholder="5 000 000" type="number"/>
</div>
<div>
<label class="block text-xs font-medium text-gray-500 mb-1">% кешбека</label>
<input class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg" placeholder="5" type="number"/>
</div>
<div class="bg-white p-2 rounded-lg shadow-sm">
<p class="text-xs text-gray-500 mb-1">Ваш кешбек</p>
<p class="text-lg font-bold text-ton-primary">250 000 ₽</p>
</div>
</div>
</div>
<div class="flex justify-between space-x-4 pt-4 border-t border-gray-200">
<button class="px-6 py-3 text-gray-700 hover:bg-gray-100 rounded-lg font-medium transition">
<i class="fas fa-arrow-left mr-2"></i> Назад
                            </button>
<button class="bg-ton-primary hover:bg-blue-700 text-white py-3 px-8 rounded-lg font-medium transition shadow-md hover:shadow-lg flex items-center">
                                Далее <i class="fas fa-arrow-right ml-2"></i>
</button>
</div>
</div>
<!-- Sales Elements -->
<div class="bg-ton-light rounded-xl p-6">
<div class="mb-6">
<h4 class="text-lg font-semibold text-ton-dark mb-3">Какие объекты мы для вас подберем?</h4>
<div class="grid grid-cols-2 gap-3 mb-4">
<div class="bg-white rounded-lg overflow-hidden shadow-sm">
<img alt="Новостройка" class="w-full h-24 object-cover" src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=300&amp;q=80"/>
<div class="p-2">
<p class="text-xs font-medium text-ton-dark truncate">ЖК "Речной"</p>
<p class="text-xs text-gray-500">от 5 200 000 ₽</p>
</div>
</div>
<div class="bg-white rounded-lg overflow-hidden shadow-sm">
<img alt="Новостройка" class="w-full h-24 object-cover" src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=300&amp;q=80"/>
<div class="p-2">
<p class="text-xs font-medium text-ton-dark truncate">ЖК "Парковый"</p>
<p class="text-xs text-gray-500">от 6 800 000 ₽</p>
</div>
</div>
<div class="bg-white rounded-lg overflow-hidden shadow-sm">
<img alt="Новостройка" class="w-full h-24 object-cover" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=300&amp;q=80"/>
<div class="p-2">
<p class="text-xs font-medium text-ton-dark truncate">ЖК "Солнечный"</p>
<p class="text-xs text-gray-500">от 4 500 000 ₽</p>
</div>
</div>
<div class="bg-white rounded-lg overflow-hidden shadow-sm">
<img alt="Новостройка" class="w-full h-24 object-cover" src="https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=300&amp;q=80"/>
<div class="p-2">
<p class="text-xs font-medium text-ton-dark truncate">ЖК "Центральный"</p>
<p class="text-xs text-gray-500">от 7 200 000 ₽</p>
</div>
</div>
</div>
<p class="text-sm text-gray-600">Мы подберем варианты, соответствующие вашим критериям, с максимальным кешбеком</p>
</div>
<!-- Benefits -->
<div class="mb-6">
<h4 class="text-lg font-semibold text-ton-dark mb-3">Почему стоит оставить заявку?</h4>
<div class="space-y-3">
<div class="flex items-start">
<div class="bg-white p-2 rounded-full mr-3 shadow">
<i class="fas fa-percentage text-ton-primary"></i>
</div>
<div>
<p class="font-medium text-ton-dark">До 7% кешбека</p>
<p class="text-sm text-gray-600">Максимальный возврат от стоимости объекта</p>
</div>
</div>
<div class="flex items-start">
<div class="bg-white p-2 rounded-full mr-3 shadow">
<i class="fas fa-check-circle text-green-500"></i>
</div>
<div>
<p class="font-medium text-ton-dark">Проверенные ЖК</p>
<p class="text-sm text-gray-600">Только надежные застройщики с хорошей репутацией</p>
</div>
</div>
<div class="flex items-start">
<div class="bg-white p-2 rounded-full mr-3 shadow">
<i class="fas fa-clock text-yellow-500"></i>
</div>
<div>
<p class="font-medium text-ton-dark">Быстрый подбор</p>
<p class="text-sm text-gray-600">Персональные варианты в течение 24 часов</p>
</div>
</div>
</div>
</div>
<!-- Testimonials -->
<div class="bg-white rounded-lg p-4 shadow-sm">
<h4 class="text-sm font-semibold text-ton-dark mb-3">Отзывы клиентов</h4>
<div class="space-y-3">
<div>
<div class="flex items-center mb-1">
<div class="flex">
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
</div>
<span class="text-xs text-gray-500 ml-2">2 недели назад</span>
</div>
<p class="text-sm text-gray-700">"Спасибо за отличный подбор! Нашли именно то, что хотели, плюс получили кешбек 350 000 рублей!"</p>
<p class="text-xs font-medium text-ton-dark mt-1">— Михаил, Москва</p>
</div>
<div class="border-t border-gray-100 pt-3">
<div class="flex items-center mb-1">
<div class="flex">
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
<i class="fas fa-star text-yellow-400 text-xs"></i>
</div>
<span class="text-xs text-gray-500 ml-2">1 месяц назад</span>
</div>
<p class="text-sm text-gray-700">"Менеджер учла все наши пожелания. Нашли квартиру рядом с метро с отличной отделкой."</p>
<p class="text-xs font-medium text-ton-dark mt-1">— Анна, Санкт-Петербург</p>
</div>
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