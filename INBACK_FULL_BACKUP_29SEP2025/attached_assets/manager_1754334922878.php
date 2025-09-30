<!DOCTYPE html>

<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>ClickBack | Личный кабинет менеджера</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>

<link href="css/styles.css" rel="stylesheet"/></head>
<body class="bg-gray-50 font-sans">
<?php include 'header.php'; ?>

<div class="flex h-screen overflow-hidden">
<!-- Sidebar -->
<div class="hidden md:flex md:flex-shrink-0">
<div class="flex flex-col w-64 gradient-bg text-white">
<div class="flex items-center justify-center h-16 px-4 border-b border-blue-300">
<div class="flex items-center">
<i class="fas fa-home mr-2 text-xl"></i>
<span class="text-xl font-bold">ClickBack</span>
</div>
</div>
<div class="flex flex-col flex-grow px-4 py-4 overflow-y-auto">
<div class="flex items-center px-4 py-3 mt-2 rounded-lg bg-blue-700">
<i class="fas fa-user-circle mr-3 text-lg"></i>
<span class="font-medium">Иван Петров</span>
</div>
<nav class="mt-8">
<div class="sidebar-item flex items-center px-4 py-3 mt-1 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-tachometer-alt mr-3"></i>
<span>Главная</span>
</div>
<div class="sidebar-item flex items-center px-4 py-3 mt-1 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-users mr-3"></i>
<span>Клиенты</span>
</div>
<div class="sidebar-item flex items-center px-4 py-3 mt-1 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-building mr-3"></i>
<span>Новостройки</span>
</div>
<div class="sidebar-item flex items-center px-4 py-3 mt-1 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-hand-holding-usd mr-3"></i>
<span>Кешбек заявки</span>
<div class="notification-dot"></div>
</div>
<div class="sidebar-item flex items-center px-4 py-3 mt-1 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-envelope mr-3"></i>
<span>Подборки</span>
</div>
<div class="sidebar-item flex items-center px-4 py-3 mt-1 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-chart-line mr-3"></i>
<span>Аналитика</span>
</div>
<div class="sidebar-item flex items-center px-4 py-3 mt-1 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-cog mr-3"></i>
<span>Настройки</span>
</div>
</nav>
</div>
<div class="px-4 py-4 border-t border-blue-300">
<div class="sidebar-item flex items-center px-4 py-3 rounded-lg hover:bg-blue-600 cursor-pointer">
<i class="sidebar-icon fas fa-sign-out-alt mr-3"></i>
<span>Выйти</span>
</div>
</div>
</div>
</div>
<!-- Main content -->
<div class="flex flex-col flex-1 overflow-hidden">
<!-- Top navbar -->
<div class="flex items-center justify-between h-16 px-4 bg-white border-b border-gray-200">
<div class="flex items-center md:hidden">
<button class="text-gray-500 focus:outline-none">
<i class="fas fa-bars"></i>
</button>
</div>
<div class="flex items-center">
<div class="relative">
<button class="text-gray-500 focus:outline-none">
<i class="fas fa-bell text-xl"></i>
<div class="notification-dot"></div>
</button>
</div>
<div class="ml-4 relative">
<div class="flex items-center">
<div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
                                IP
                            </div>
<span class="ml-2 text-gray-700 hidden md:block">Иван Петров</span>
</div>
</div>
</div>
</div>
<!-- Content -->
<div class="flex-1 overflow-auto p-4 md:p-6">
<div class="mb-6">
<h1 class="text-2xl font-bold text-gray-800">Добро пожаловать, Иван!</h1>
<p class="text-gray-600">Ваши последние действия и статистика</p>
</div>
<!-- Stats cards -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
<div class="card-hover bg-white rounded-lg shadow p-4">
<div class="flex items-center">
<div class="p-3 rounded-full bg-blue-100 text-blue-500">
<i class="fas fa-users text-lg"></i>
</div>
<div class="ml-4">
<p class="text-sm text-gray-500">Клиентов</p>
<p class="text-xl font-semibold">142</p>
</div>
</div>
</div>
<div class="card-hover bg-white rounded-lg shadow p-4">
<div class="flex items-center">
<div class="p-3 rounded-full bg-green-100 text-green-500">
<i class="fas fa-hand-holding-usd text-lg"></i>
</div>
<div class="ml-4">
<p class="text-sm text-gray-500">Заявки на кешбек</p>
<p class="text-xl font-semibold">24</p>
</div>
</div>
</div>
<div class="card-hover bg-white rounded-lg shadow p-4">
<div class="flex items-center">
<div class="p-3 rounded-full bg-purple-100 text-purple-500">
<i class="fas fa-building text-lg"></i>
</div>
<div class="ml-4">
<p class="text-sm text-gray-500">Новостроек</p>
<p class="text-xl font-semibold">18</p>
</div>
</div>
</div>
<div class="card-hover bg-white rounded-lg shadow p-4">
<div class="flex items-center">
<div class="p-3 rounded-full bg-yellow-100 text-yellow-500">
<i class="fas fa-ruble-sign text-lg"></i>
</div>
<div class="ml-4">
<p class="text-sm text-gray-500">Выплачено кешбека</p>
<p class="text-xl font-semibold">1,240,500 ₽</p>
</div>
</div>
</div>
</div>
<!-- Recent activity and quick actions -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<!-- Recent clients -->
<div class="lg:col-span-2">
<div class="bg-white rounded-lg shadow overflow-hidden">
<div class="px-4 py-3 border-b border-gray-200 flex justify-between items-center">
<h2 class="font-semibold text-gray-800">Последние клиенты</h2>
<button class="text-blue-500 text-sm font-medium">Смотреть всех</button>
</div>
<div class="divide-y divide-gray-200">
<div class="p-4 hover:bg-gray-50 cursor-pointer">
<div class="flex items-center">
<div class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
<i class="fas fa-user text-gray-500"></i>
</div>
<div class="ml-4">
<p class="font-medium">Александр Смирнов</p>
<p class="text-sm text-gray-500">+7 (912) 345-67-89</p>
</div>
<div class="ml-auto">
<span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Новая заявка</span>
</div>
</div>
</div>
<div class="p-4 hover:bg-gray-50 cursor-pointer">
<div class="flex items-center">
<div class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
<i class="fas fa-user text-gray-500"></i>
</div>
<div class="ml-4">
<p class="font-medium">Елена Козлова</p>
<p class="text-sm text-gray-500">+7 (912) 987-65-43</p>
</div>
<div class="ml-auto">
<span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">В процессе</span>
</div>
</div>
</div>
<div class="p-4 hover:bg-gray-50 cursor-pointer">
<div class="flex items-center">
<div class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
<i class="fas fa-user text-gray-500"></i>
</div>
<div class="ml-4">
<p class="font-medium">Дмитрий Иванов</p>
<p class="text-sm text-gray-500">+7 (912) 123-45-67</p>
</div>
<div class="ml-auto">
<span class="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800">Ожидает документы</span>
</div>
</div>
</div>
<div class="p-4 hover:bg-gray-50 cursor-pointer">
<div class="flex items-center">
<div class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
<i class="fas fa-user text-gray-500"></i>
</div>
<div class="ml-4">
<p class="font-medium">Ольга Петрова</p>
<p class="text-sm text-gray-500">+7 (912) 765-43-21</p>
</div>
<div class="ml-auto">
<span class="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800">Кешбек выплачен</span>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- Quick actions -->
<div>
<div class="bg-white rounded-lg shadow overflow-hidden mb-6">
<div class="px-4 py-3 border-b border-gray-200">
<h2 class="font-semibold text-gray-800">Быстрые действия</h2>
</div>
<div class="p-4">
<button class="w-full flex items-center justify-center px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 mb-3">
<i class="fas fa-plus mr-2"></i>
<span>Добавить клиента</span>
</button>
<button class="w-full flex items-center justify-center px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 mb-3">
<i class="fas fa-paper-plane mr-2"></i>
<span>Отправить подборку</span>
</button>
<button class="w-full flex items-center justify-center px-4 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600">
<i class="fas fa-file-alt mr-2"></i>
<span>Создать отчет</span>
</button>
</div>
</div>
<!-- Recent cashback requests -->
<div class="bg-white rounded-lg shadow overflow-hidden">
<div class="px-4 py-3 border-b border-gray-200 flex justify-between items-center">
<h2 class="font-semibold text-gray-800">Заявки на кешбек</h2>
<button class="text-blue-500 text-sm font-medium">Все заявки</button>
</div>
<div class="p-4">
<div class="flex items-start mb-4">
<div class="bg-blue-100 p-2 rounded-lg">
<i class="fas fa-home text-blue-500"></i>
</div>
<div class="ml-3">
<p class="font-medium">ЖК "Солнечный"</p>
<p class="text-sm text-gray-500">Александр С., 450 000 ₽</p>
<p class="text-xs text-gray-400 mt-1">Сегодня, 10:45</p>
</div>
</div>
<div class="flex items-start mb-4">
<div class="bg-green-100 p-2 rounded-lg">
<i class="fas fa-home text-green-500"></i>
</div>
<div class="ml-3">
<p class="font-medium">ЖК "Речной"</p>
<p class="text-sm text-gray-500">Елена К., 320 000 ₽</p>
<p class="text-xs text-gray-400 mt-1">Вчера, 15:30</p>
</div>
</div>
<div class="flex items-start">
<div class="bg-yellow-100 p-2 rounded-lg">
<i class="fas fa-home text-yellow-500"></i>
</div>
<div class="ml-3">
<p class="font-medium">ЖК "Лесной"</p>
<p class="text-sm text-gray-500">Дмитрий И., 280 000 ₽</p>
<p class="text-xs text-gray-400 mt-1">2 дня назад</p>
</div>
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