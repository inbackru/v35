<!DOCTYPE html>

<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Карточка квартиры</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>

<link href="css/styles.css" rel="stylesheet"/></head>
<body class="bg-gray-100 flex justify-center items-center p-4">
<?php include 'header.php'; ?>

<div class="no-print absolute top-4 right-4">
<button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition-colors" onclick="window.print()">
            Печать карточки
        </button>
</div>
<div class="print-area bg-white shadow-lg rounded-lg overflow-hidden">
<!-- Шапка документа -->
<div class="flex justify-between items-start border-b border-gray-200 pb-4 mb-6">
<div>
<h1 class="text-2xl font-bold text-gray-800">Карточка объекта недвижимости</h1>
<p class="text-gray-600">Дата формирования: 15.05.2023</p>
</div>
<div class="flex items-center gap-4">
<div class="qr-code">
                    QR-код<br/>объекта
                </div>
<div class="text-right">
<p class="text-gray-600 text-sm">ID объекта:</p>
<p class="font-semibold">14003425</p>
</div>
</div>
</div>
<!-- Основная информация -->
<div class="grid grid-cols-2 gap-8 mb-8">
<div>
<h2 class="text-xl font-semibold text-gray-800 mb-4">Основная информация</h2>
<div class="space-y-3">
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Номер помещения:</span>
<span class="font-medium">КВ-12-78</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Жилой комплекс:</span>
<span class="font-medium">TON Residence</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Тип объекта:</span>
<span class="font-medium">Квартира</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Статус:</span>
<span class="font-medium text-green-600">Свободна</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Адрес:</span>
<span class="font-medium text-right">г. Москва, р-н Хамовники, ул. Льва Толстого, д. 18</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Этаж:</span>
<span class="font-medium">12 из 25</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Площадь:</span>
<span class="font-medium">78.5 м²</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Комнат:</span>
<span class="font-medium">2</span>
</div>
</div>
</div>
<div>
<h2 class="text-xl font-semibold text-gray-800 mb-4">Финансовая информация</h2>
<div class="space-y-3">
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Цена:</span>
<span class="font-medium text-blue-600">25 750 000 ₽</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Кешбек:</span>
<span class="font-medium text-green-600">5%</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Цена с кешбеком:</span>
<span class="font-medium text-blue-600">24 462 500 ₽</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Цена за м²:</span>
<span class="font-medium">328 025 ₽</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Ипотека:</span>
<span class="font-medium">Доступна</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Рассрочка:</span>
<span class="font-medium">Не предусмотрена</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Комиссия:</span>
<span class="font-medium">Нет</span>
</div>
</div>
</div>
</div>
<!-- Описание ЖК -->
<div class="mb-8">
<h2 class="text-xl font-semibold text-gray-800 mb-4">Описание жилого комплекса</h2>
<div class="bg-blue-50 p-6 rounded-lg">
<p class="text-gray-700 mb-3"><span class="font-medium text-blue-800">TON Residence</span> - премиальный жилой комплекс бизнес-класса в историческом центре Москвы.</p>
<p class="text-gray-700 mb-3">Комплекс включает 3 корпуса с закрытой охраняемой территорией, подземным паркингом и собственной инфраструктурой.</p>
<p class="text-gray-700 mb-3">Инфраструктура: фитнес-клуб, SPA-центр, детский сад, ресторан, коворкинг и парковая зона.</p>
<p class="text-gray-700">Срок сдачи: 4 квартал 2024 года. Застройщик: ООО "Строительная компания ТОН".</p>
</div>
</div>
<!-- Фото ЖК -->
<div class="mb-8">
<h2 class="text-xl font-semibold text-gray-800 mb-4">Фото жилого комплекса</h2>
<div class="flex justify-center bg-gray-100 p-4 rounded-lg">
<div class="w-full h-64 bg-gray-200 flex items-center justify-center text-gray-500">
                    [Фото жилого комплекса]
                </div>
</div>
</div>
<!-- Дополнительная информация -->
<div class="mb-8">
<h2 class="text-xl font-semibold text-gray-800 mb-4">Дополнительная информация</h2>
<div class="grid grid-cols-3 gap-6">
<div class="space-y-3">
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Отделка:</span>
<span class="font-medium">Черновая</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Санузел:</span>
<span class="font-medium">Раздельный</span>
</div>
</div>
<div class="space-y-3">
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Балкон:</span>
<span class="font-medium">Есть</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Окна:</span>
<span class="font-medium">Пластиковые</span>
</div>
</div>
<div class="space-y-3">
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Лифты:</span>
<span class="font-medium">2 пассажирских</span>
</div>
<div class="flex justify-between border-b border-gray-100 pb-2">
<span class="text-gray-600">Парковка:</span>
<span class="font-medium">Подземная</span>
</div>
</div>
</div>
</div>
<!-- Планировка -->
<div class="mb-8">
<h2 class="text-xl font-semibold text-gray-800 mb-4">Планировка</h2>
<div class="flex justify-center bg-gray-100 p-4 rounded-lg">
<div class="w-full h-64 bg-gray-200 flex items-center justify-center text-gray-500">
                    [Изображение планировки]
                </div>
</div>
</div>
<!-- Контактная информация -->
<div>
<h2 class="text-xl font-semibold text-gray-800 mb-4">Контактная информация</h2>
<div class="grid grid-cols-4 gap-6 bg-blue-50 p-6 rounded-lg">
<div>
<h3 class="font-medium text-blue-800 mb-2">Застройщик</h3>
<p class="text-gray-700">ООО "Строительная компания ТОН"</p>
<p class="text-gray-700 text-sm mt-1">ИНН 7701234567</p>
</div>
<div>
<h3 class="font-medium text-blue-800 mb-2">Проектная декларация</h3>
<p class="text-gray-700">на сайте наш.дом.рф</p>
</div>
<div>
<h3 class="font-medium text-blue-800 mb-2">Телефон</h3>
<p class="text-gray-700">+7 (495) 123-45-67</p>
</div>
<div>
<h3 class="font-medium text-blue-800 mb-2">Сайт</h3>
<p class="text-gray-700">www.ton.org</p>
</div>
</div>
</div>
<!-- Подвал -->
<div class="mt-8 pt-4 border-t border-gray-200 text-center text-gray-500 text-sm">
<p>Данная карточка сгенерирована автоматически и действительна на дату формирования.</p>
<p class="mt-1">Официальный партнер застройщика. Проектная декларация на сайте наш.дом.рф</p>
<p class="mt-1">© 2023 ООО "Строительная компания ТОН". Все права защищены.</p>
</div>
</div>
<script src="js/main.js"></script>

<?php include 'footer.php'; ?>
</body>
</html>