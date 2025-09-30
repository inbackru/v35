
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "HowTo",
      "name": "Как получить кэшбек за новостройку",
      "description": "Пошаговая инструкция получения кэшбека при покупке квартиры в новостройке",
      "totalTime": "P60D",
      "step": [
        {
          "@type": "HowToStep",
          "text": "Зарегистрируйтесь на сайте или оставьте заявку",
          "name": "Регистрация на сайте"
        },
        {
          "@type": "HowToStep",
          "text": "Выберите новостройку из каталога или укажите уже выбранную",
          "name": "Выбор новостройки"
        },
        {
          "@type": "HowToStep",
          "text": "Мы регистрируем вас как нашего клиента у застройщика перед покупкой",
          "name": "Оформление сделки"
        },
        {
          "@type": "HowToStep",
          "text": "После оформления собственности деньги поступают на ваш счет",
          "name": "Получение кэшбека"
        }
      ]
    }
    </script>


    <script type="application/ld+json">
    { 
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 1,
        "name": "Главная",
        "item": "https://inback.ru/"
      },{
        "@type": "ListItem",
        "position": 2,
        "name": "Как это работает",
        "item": "https://inback.ru/kak-eto-rabotaet"
      }]
    }
    </script>


<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Social Meta Tags -->
    <meta property="og:title" content="Кэшбек за новостройки в Краснодаре до 500 000 ₽ | inback">
    <meta property="og:description" content="Вернём до 10% стоимости квартиры при покупке новостройки в Краснодаре. Бесплатная юридическая поддержка.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://inback.ru/">
    <meta property="og:image" content="https://inback.ru/social-preview.jpg">
    <meta property="og:site_name" content="inback">
    <meta name="twitter:card" content="summary_large_image">
    <title>Кэшбек за новостройки в Краснодаре до 500 000 ₽ | inback</title>
    <meta name="description" content="Как получить кэшбек 2,5-10% за новостройку? Пошаговая инструкция работы сервиса Inback. Официальный возврат денег от застройщика при покупке квартиры в Краснодаре">
    <meta name="keywords" content="как получить кэшбек за квартиру, кэшбек за новостройку, возврат денег за квартиру, система кэшбека inback, оформление кэшбека, этапы получения кэшбека">
    <meta property="og:title" content="Как получить кэшбек 2,5-10% за новостройку? | Пошаговая инструкция">
    <meta property="og:description" content="Узнайте, как работает система кэшбека Inback при покупке квартиры в новостройке. 4 простых шага для получения возврата денег от застройщика">
    <link rel="canonical" href="https://inback.ru/kak-eto-rabotaet" />
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://inback.ru/" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Карта -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        /* TON Marker Styles */
        .custom-marker {
            background: transparent !important;
            border: none !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s ease;
        }
        
        .custom-marker:hover {
            transform: scale(1.2);
        }
        
        .ton-gradient {
            background: linear-gradient(135deg, #0087F5, #00A3FF);
        }
        
        .leaflet-popup-content-wrapper {
            border-radius: 12px !important;
            box-shadow: 0 6px 16px rgba(0,0,0,0.2) !important;
            border: none;
            padding: 0;
            overflow: hidden;
        }
        
        .leaflet-popup-content {
            margin: 0 !important;
            width: auto !important;
        }
        
        .marker-pulse {
            position: absolute;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            opacity: 0.3;
            animation: pulse 2s infinite;
            transform: translate(1px, 1px);
        }
        
        .marker-content {
            position: relative;
            width: 24px;
            height: 24px;
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 1;
        }
        
        .marker-content span {
            transform: rotate(45deg);
            color: white;
            font-weight: bold;
            font-size: 12px;
        }
        
        @keyframes pulse {
            0% { transform: translate(1px, 1px) scale(1); opacity: 0.3; }
            70% { transform: translate(1px, 1px) scale(1.5); opacity: 0.1; }
            100% { transform: translate(1px, 1px) scale(1); opacity: 0.3; }
        }
        
        /* Popup styling */
        .popup-content {
            font-family: 'Inter', sans-serif;
        }
        
        .leaflet-popup-content-wrapper {
            border-radius: 8px !important;
            box-shadow: 0 3px 14px rgba(0,0,0,0.15) !important;
        }
        
        .leaflet-popup-tip {
            width: 12px !important;
            height: 12px !important;
        }
        
        .marker-cluster-custom {
            background-clip: padding-box;
            border-radius: 50%;
            background: rgba(0, 135, 245, 0.8);
            color: white;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .marker-cluster-custom div {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-size: 14px;
        }
        
        .leaflet-popup-content-wrapper {
            border-radius: 8px;
        }
        
        .leaflet-popup-content {
            margin: 6px 12px !important;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f5f5f5;
        }
        .ton-gradient {
            background: linear-gradient(90deg, #0087F5 0%, #00A3FF 100%);
        }
        .ton-text-gradient {
            background: linear-gradient(90deg, #0087F5 0%, #00A3FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .map-container {
            transition: all 0.3s ease;
        }
        .object-card:hover {
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            transform: translateY(-2px);
        }
        .modal {
            transition: opacity 0.3s ease;
        }
        .modal-content {
            transform: translateY(20px);
            transition: transform 0.3s ease;
        }
        .modal.open {
            opacity: 1;
            pointer-events: auto;
        }
        .modal.open .modal-content {
            transform: translateY(0);
        }
        /* Cluster markers */
        .marker-cluster-custom {
            background: transparent !important;
        }
        #map {
            height: 100%;
            width: 100%;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 0;
            background: #f5f5f5;
        }
        .map-container {
            position: relative;
            height: 100%;
            width: 100%;
            overflow: hidden;
        }
        .leaflet-container {
            background: #f5f5f5;
        }
        
        /* Custom markers */
        .custom-marker {
            background: transparent;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .marker-cluster-custom {
            background-clip: padding-box;
            border-radius: 50%;
            background: rgba(0, 135, 245, 0.8);
            color: white;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        /* Popup styling */
        .leaflet-popup {
            bottom: 70px !important;
        }
        .leaflet-popup-content-wrapper {
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            padding: 8px;
        }
        .leaflet-popup-content {
            margin: 0;
            font-size: 13px;
        }
        .leaflet-popup-tip-container {
            display: none;
        }
    </style>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "RealEstateAgent",
      "name": "Inback",
      "image": "https://inback.ru/logo.jpg",
      "description": "Официальный сервис возврата кэшбека при покупке недвижимости в Краснодаре и других городах России",
      "priceRange": "$",
      "areaServed": {
        "@type": "AdministrativeArea",
        "name": "Краснодар и Краснодарский край"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "ул. Красная, 32",
        "addressLocality": "Краснодар",
        "addressRegion": "Краснодарский край" 
      },
      "telephone": "+78001231212",
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday"
        ],
        "opens": "09:00",
        "closes": "19:00"
      }
    }
    </script>
      <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        ton: {
                            blue: '#0088cc',
                            dark: '#222426',
                            light: '#f5f5f5',
                            accent: '#00a3e0',
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                }
            }
        }
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            scroll-behavior: smooth;
        }
        
        .gradient-bg {
            background: linear-gradient(135deg, #0088CC 0%, #006699 100%);
        }

        .hero-gradient {
            background: linear-gradient(135deg, rgba(0,136,204,0.08) 0%, rgba(0,163,224,0.08) 100%), #ffffff;
        }

        .btn-primary {
            background: linear-gradient(135deg, #0088CC 0%, #006699 100%);
            color: white;
            transition: all 0.3s ease;
        }

        .btn-primary:hover {
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 104, 155, 0.3);
        }

        .btn-secondary {
            background: white;
            color: #0088CC;
            border: 1px solid #0088CC;
            transition: all 0.3s ease;
        }

        .btn-secondary:hover {
            background: rgba(0, 136, 204, 0.05);
        }
        
        .card-hover:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 136, 204, 0.15);
            transition: all 0.3s ease;
        }
        
        .transition-all {
            transition: all 0.3s ease;
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #0088CC 0%, #006699 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        body {
            font-family: 'Inter', sans-serif;
            scroll-behavior: smooth;
            background-color: #f9fafb;
            color: #111827;
        }



        .shadow-sm {
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }

        .transition-all {
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .typewriter {
            display: inline-block;
            position: relative;
        }
        
        .typewriter-text {
            background: linear-gradient(135deg, #006699 0%, #0088CC 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            display: inline-block;
        }
        
        .typewriter::after {
            content: "|";
            position: absolute;
            right: -8px;
            animation: blink 0.7s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        .property-card {
            transition: all 0.3s ease;
        }
        
        .property-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        
        .search-box {
            box-shadow: 0 10px 25px rgba(0, 136, 204, 0.2);
        }
        
        .loading-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0088CC;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: fadeOut 0.5s 2s forwards;
        }
        
        @keyframes fadeOut {
            to {
                opacity: 0;
                visibility: hidden;
            }
        }
        
        @keyframes ping {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(1.5); opacity: 0; }
        }
        
        .animate-ping {
            animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
        }
        
        .animate-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .animation-delay-200 {
            animation-delay: 0.2s;
        }
        
        .animation-delay-400 {
            animation-delay: 0.4s;
        }
        
        .modal {
            transition: opacity 0.3s ease;
        }
        
        .step-item:not(:last-child):after {
            content: '';
            position: absolute;
            right: -2rem;
            top: 50%;
            transform: translateY(-50%);
            width: 4rem;
            height: 2px;
            background: rgb(0 136 204 / var(--tw-bg-opacity, 1));
        }

        /* Carousel dots */
        .carousel-dot {
            transition: all 0.3s ease;
        }
        .carousel-dot.active {
            opacity: 1;
            transform: scale(1.3);
        }

        /* Modern Filters */
        .dropdown-toggle {
            transition: all 0.2s ease;
        }
        
        .dropdown-toggle svg {
            transition: transform 0.2s ease;
        }
        
        .dropdown.active .dropdown-toggle svg {
            transform: rotate(180deg);
        }
        
        .dropdown.active .dropdown-toggle {
            border-color: #0088CC;
            box-shadow: 0 0 0 1px #0088CC;
        }
        
        .dropdown-menu {
            opacity: 0;
            transform: translateY(5px);
            transition: all 0.2s ease;
            pointer-events: none;
        }
        
        .dropdown.active .dropdown-menu {
            opacity: 1;
            transform: translateY(0);
            pointer-events: all;
        }
        /* Compact dropdown menu */
        .dropdown {
            position: relative;
            display: inline-block;
        }
        
        .dropdown-btn {
            background: transparent;
            border: none;
            color: #141A24;
            font-weight: 500;
            padding: 0.5rem 0.75rem;
            border-radius: 0.5rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .dropdown-btn:hover {
            background: rgba(0, 136, 204, 0.1);
        }
        
        .dropdown-btn svg {
            width: 16px;
            height: 16px;
            transition: transform 0.2s;
        }
        
        .dropdown-btn.open svg {
            transform: rotate(180deg);
        }
        
        .dropdown-menu {
            position: absolute;
            top: calc(100% + 8px);
            left: 0;
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            padding: 0.5rem 0;
            min-width: 200px;
            z-index: 50;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.2s ease-out;
            pointer-events: none;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .dropdown-menu.open,
        .group:hover .dropdown-menu {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
            pointer-events: auto;
        }

        .dropdown-item {
            padding: 0.5rem 1.5rem;
            display: flex;
            align-items: center;
            white-space: nowrap;
        }

        .dropdown-item:hover {
            background-color: rgba(0, 136, 204, 0.05);
        }

        input[type="checkbox"]:checked {
            background-color: rgb(0, 136, 204);
            border-color: rgb(0, 136, 204);
        }
        
        .dropdown-item {
            padding: 0.5rem 1rem;
            color: #141A24;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
            font-size: 0.9rem;
        }
        
        .dropdown-item:hover {
            background: rgba(0, 136, 204, 0.1);
            color: #0088CC;
        }
        
        .dropdown-item svg {
            width: 14px;
            height: 14px;
        }

        /* Selected filters */
        .selected-filter {
            background-color: #f5f3ff;
            color: #6d28d9;
            padding: 0.375rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            display: inline-flex;
            align-items: center;
        }
        
        /* Filter badge */
        .filter-badge {
            position: absolute;
            top: -6px;
            right: -6px;
            background-color: #0088CC;
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        /* Footer menu styles */
        .footer-menu-group {
            margin-bottom: 1.5rem;
        }
        
        .footer-submenu {
            transition: all 0.3s ease;
        }
        
        @media (min-width: 768px) {
            .footer-submenu {
                display: block !important;
            }
        }
        
        @media (max-width: 768px) {
            .step-item:not(:last-child):after {
                display: none;
            }
        }

        .ton-bg {
            background: linear-gradient(145deg, #0088cc, #7e5bef);
        }
        .ton-text-gradient {
            background: linear-gradient(90deg, #0088cc, #7e5bef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .scroll-hidden::-webkit-scrollbar {
            display: none;
        }
        .amenity-icon {
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 136, 204, 0.1);
            border-radius: 6px;
            color: #0088cc;
        }
        .swiper-button-prev, .swiper-button-next {
            color: white;
            background: rgba(0,0,0,0.5);
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }
        .swiper-button-prev:after, .swiper-button-next:after {
            font-size: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body class="bg-white">
    <!-- Loading Animation -->
    <div class="loading-animation bg-gradient-to-b from-[#006699] to-[#0088CC]">
        <div class="relative w-32 h-32">
            <div class="absolute inset-0 rounded-full border-[10px] border-white/20 animate-ping"></div>
            <div class="absolute inset-[15px] rounded-full border-[10px] border-white/30 animate-ping animation-delay-200"></div>
            <div class="absolute inset-[30px] rounded-full border-[10px] border-white/40 animate-ping animation-delay-400"></div>
            <div class="absolute inset-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 rounded-full bg-white flex items-center justify-center">
                <div class="w-8 h-8 rounded-full gradient-bg"></div>
            </div>
        </div>
        <div class="mt-8 text-white text-xl font-semibold">Загружаем лучшие предложения...</div>
    </div>

   

   <?php include 'header.php'; ?>
 <!-- Search Section -->
    <div class="bg-white shadow-sm sticky top-0 z-30">
        <div class="container mx-auto px-4 py-3">
            <div class="flex flex-col md:flex-row md:items-center space-y-3 md:space-y-0 md:space-x-3">
                <div class="relative flex-grow">
                    <input type="text" placeholder="Краснодар, район, метро, улица" 
                        class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm">
                    <div class="absolute left-3 top-3 text-gray-400">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                        </svg>
                    </div>
                </div>
                <button onclick="searchProperties()" class="ton-gradient text-white px-4 py-3 rounded-xl font-medium hover:opacity-90 transition text-sm">
                    Найти
                </button>
                <button onclick="document.getElementById('advancedFilters').classList.toggle('hidden')" 
                    class="flex items-center text-gray-600 hover:text-blue-500 px-3 py-1 rounded-lg text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z" />
                    </svg>
                    Фильтры
                </button>
            </div>

            <!-- Advanced Filters (hidden by default) -->
            <div id="advancedFilters" class="hidden mt-4 bg-gray-50 p-4 rounded-xl">
                <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    <!-- Price Range -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">Цена, ₽</label>
                        <div class="grid grid-cols-2 gap-2">
                            <input type="number" placeholder="От" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                            <input type="number" placeholder="До" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                        </div>
                    </div>

                    <!-- Property Type -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">Тип</label>
                        <select class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                            <option value="">Любой</option>
                            <option>Квартира</option>
                            <option>Новостройка</option>
                            <option>Дом</option>
                            <option>Коммерческая</option>
                        </select>
                    </div>

                    <!-- Rooms -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">Комнат</label>
                        <div class="flex space-x-1">
                            <button class="filter-pill">1</button>
                            <button class="filter-pill">2</button>
                            <button class="filter-pill">3</button>
                            <button class="filter-pill">4+</button>
                            <button class="filter-pill">Студия</button>
                        </div>
                    </div>

                    <!-- Area -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">Площадь, м²</label>
                        <div class="grid grid-cols-2 gap-2">
                            <input type="number" placeholder="От" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                            <input type="number" placeholder="До" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                        </div>
                    </div>

                    <!-- Floor -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">Этаж</label>
                        <div class="grid grid-cols-2 gap-2">
                            <input type="number" placeholder="От" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                            <input type="number" placeholder="До" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                        </div>
                    </div>

                    <!-- House Type -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">Дом</label>
                        <select class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
                            <option value="">Любой</option>
                            <option>Панельный</option>
                            <option>Кирпичный</option>
                            <option>Монолитный</option>
                            <option>Блочный</option>
                        </select>
                    </div>

                    <!-- Additional Options -->
                    <div>
                        <label class="block mb-2 text-sm font-medium text-gray-700">Опции</label>
                        <div class="space-y-2">
                            <label class="flex items-center text-sm">
                                <input type="checkbox" class="rounded border-gray-300 text-blue-500 mr-2">
                                Только с кешбеком
                            </label>
                            <label class="flex items-center text-sm">
                                <input type="checkbox" class="rounded border-gray-300 text-blue-500 mr-2">
                                С фото
                            </label>
                            <label class="flex items-center text-sm">
                                <input type="checkbox" class="rounded border-gray-300 text-blue-500 mr-2">
                                С балконом
                            </label>
                        </div>
                    </div>
                </div>

                <div class="mt-4 flex justify-between">
                    <button class="text-sm text-blue-500 hover:text-blue-700">
                        Очистить фильтры
                    </button>
                    <button class="ton-gradient text-white px-4 py-2 rounded-lg text-sm font-medium">
                        Показать 184 объекта
                    </button>
                </div>
            </div>

            <div class="mt-3 flex flex-wrap gap-2">
                <button class="flex items-center text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full mr-2">
                    Кешбек до 3%
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                </button>
                <button class="flex items-center text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full mr-2">
                    Новостройки
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                </button>
                <button class="flex items-center text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full mr-2">
                    Вторичка
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                </button>
                <button class="flex items-center text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full mr-2">
                    С балконом
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
      <!-- Main Content -->
    <div class="flex flex-col lg:flex-row h-[calc(100vh-135px)]">
        <!-- Objects List -->
        <div class="lg:w-96 xl:w-104 bg-white shadow-sm z-20 lg:overflow-y-auto lg:h-full">
                <div class="bg-white rounded-lg shadow-sm p-4 mb-4">
                    <div class="flex justify-between items-center mb-3">
                        <h3 class="font-semibold text-lg">184 объекта</h3>
                        <div class="flex items-center text-sm text-gray-500">
                            <span class="mr-2">Сортировка:</span>
                            <button class="font-medium text-blue-500">По цене</button>
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                            </svg>
                        </div>
                    </div>
                    <label class="flex items-center">
                        <input type="checkbox" class="rounded border-gray-300 text-blue-500 focus:ring-blue-500 mr-2">
                        <span>Только с кешбеком</span>
                    </label>
                </div>
                
                <!-- Object Cards -->
                <div class="space-y-4">
                    <!-- Card 1 -->
                    <div class="object-card bg-white rounded-lg shadow-sm overflow-hidden cursor-pointer transition" onclick="showObjectDetails(1)">
                        <div class="relative">
                            <img src="https://images.unsplash.com/photo-1560448204-603b3fc33ddc?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Apartment" class="w-full h-48 object-cover">
                            <div class="absolute top-2 right-2 bg-amber-400 text-xs font-medium px-2 py-1 rounded-full">Кешбек 3%</div>
                            <div class="absolute bottom-2 left-2 bg-white/90 text-xs font-medium px-2 py-1 rounded">10 фото</div>
                        </div>
                        <div class="p-4">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h3 class="font-bold text-lg">12.8 млн ₽</h3>
                                    <p class="text-gray-600">4-комн. квартира, 104 м²</p>
                                </div>
                                <div class="bg-blue-50 text-blue-600 px-2 py-1 rounded-2xl text-xs">5 этаж</div>
                            </div>
                            <p class="text-gray-800 mt-2">ЖК «Гранд Люкс» · <span class="text-blue-500">Гарантия-Инвест</span></p>
                            <p class="text-sm text-gray-500">Краснодар, ул. Красных Партизан</p>
                            <div class="flex items-center mt-3 text-sm text-gray-500">
                                <span class="mr-3">Апрель 2019</span>
                                <span>Дом на карте</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 2 -->
                    <div class="object-card bg-white rounded-lg shadow-sm overflow-hidden cursor-pointer transition" onclick="showObjectDetails(2)">
                        <div class="relative">
                            <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Apartment" class="w-full h-48 object-cover">
                            <div class="absolute top-2 right-2 bg-amber-400 text-xs font-medium px-2 py-1 rounded-full">Кешбек 2%</div>
                            <div class="absolute bottom-2 left-2 bg-white/90 text-xs font-medium px-2 py-1 rounded">8 фото</div>
                        </div>
                        <div class="p-4">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h3 class="font-bold text-lg">8.7 млн ₽</h3>
                                    <p class="text-gray-600">3-комн. квартира, 78 м²</p>
                                </div>
                                <div class="bg-blue-50 text-blue-600 px-2 py-1 rounded-2xl text-xs">15 этаж</div>
                            </div>
                            <p class="text-gray-800 mt-2">ЖК «Небесный» · <span class="text-blue-500">Эталон Юг</span></p>
                            <p class="text-sm text-gray-500">Краснодар, ул. 40 лет Победы</p>
                            <div class="flex items-center mt-3 text-sm text-gray-500">
                                <span class="mr-3">2022 год</span>
                                <span>Дом на карте</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 3 -->
                    <div class="object-card bg-white rounded-lg shadow-sm overflow-hidden cursor-pointer transition" onclick="showObjectDetails(3)">
                        <div class="relative">
                            <img src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="House" class="w-full h-48 object-cover">
                            <div class="absolute top-2 right-2 bg-red-500 text-white text-xs font-medium px-2 py-1 rounded-full">Акция</div>
                        </div>
                        <div class="p-4">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h3 class="font-bold text-lg">6.2 млн ₽</h3>
                                    <p class="text-gray-600">2-комн. квартира, 54 м²</p>
                                </div>
                                <div class="bg-blue-50 text-blue-600 px-2 py-1 rounded-2xl text-xs">3 этаж</div>
                            </div>
                            <p class="text-gray-800 mt-2">ЖК «Триумфальная Арка» · <span class="text-blue-500">ПИК-Юг</span></p>
                            <p class="text-sm text-gray-500">Краснодар, ул. Тургенева</p>
                            <div class="flex items-center mt-3 text-sm text-gray-500">
                                <span class="mr-3">2018 год</span>
                                <span>Дом на карте</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 4 - ЖК -->
                    <div class="object-card bg-white rounded-lg shadow-sm overflow-hidden cursor-pointer transition" onclick="event.stopPropagation();showObjectDetails(4)">
                        <div class="relative">
                            <img src="https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Residential Complex" class="w-full h-48 object-cover">
                            <div class="absolute top-2 right-2 bg-blue-500 text-white text-xs font-medium px-2 py-1 rounded-full">ЖК</div>
                        </div>
                        <div class="p-4">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h3 class="font-bold text-lg">ЖК «Гранд Люкс»</h3>
                                    <p class="text-gray-600">12 объектов от 6.2 млн ₽</p>
                                </div>
                                <div class="bg-blue-50 text-blue-600 px-2 py-1 rounded-2xl text-xs">2020-2024</div>
                            </div>
                            <p class="text-gray-800 mt-2">Краснодар, ул. Красных Партизан</p>
                            <div class="flex items-center mt-3 text-sm text-gray-500">
                                <span>Жилой комплекс</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Map -->
            <div class="flex-1 relative h-full">
                <div id="map" class="map-container rounded-xl shadow-sm overflow-hidden leaflet-container leaflet-touch leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom" tabindex="0" style="position: relative; outline: none;"></div>
            </div>

            <script>
                // Initialize map with random markers in Krasnodar
                const map = L.map('map').setView([45.0355, 38.9753], 13);

                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map);

                // Custom marker icons with pulse effect and TON style
                const tonMarkerIcon = (hasCashback) => {
                    return L.divIcon({
                        className: 'custom-marker',
                        html: `
                            <div class="relative transform hover:scale-110 transition-transform duration-200">
                                ${hasCashback ? 
                                  '<div class="absolute -inset-1 rounded-full bg-blue-400 opacity-20 animate-pulse"></div>' : 
                                  ''}
                                <div class="relative rounded-full w-10 h-10 flex items-center justify-center 
                                    ${hasCashback ? 'ton-gradient' : 'bg-gray-600'} shadow-md">
                                    <span class="text-white font-semibold text-xs">${hasCashback ? 'TON' : 'APT'}</span>
                                </div>
                                <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-0 h-0 
                                      border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent 
                                      ${hasCashback ? 'border-t-blue-500' : 'border-t-gray-600'}"></div>
                            </div>
                        `,
                        iconSize: [40, 50],
                        iconAnchor: [20, 50]
                    });
                };

                // Generate random markers in Krasnodar area
                const randomInRange = (min, max) => Math.random() * (max - min) + min;
                
                // Sample properties data with random positions in Krasnodar
                const generateRandomMarker = (id, isComplex) => {
                    const lat = randomInRange(45.01, 45.08);  // Krasnodar latitude range
                    const lng = randomInRange(38.95, 39.05);  // Krasnodar longitude range
                    const hasCashback = Math.random() > 0.3;  // 70% chance of cashback
                    
                    return {
                        id,
                        lat,
                        lng,
                        price: isComplex ? "ЖК" : `${(5 + Math.random() * 8).toFixed(1)}M`,
                        type: isComplex ? "ЖК" : "Квартира",
                        rooms: isComplex ? null : Math.floor(1 + Math.random() * 4),
                        hasCashback,
                        name: isComplex ? 
                            `ЖК ${['Центральный', 'Фестивальный', 'Речной', 'Южный'][Math.floor(Math.random() * 4)]}` : 
                            `${Math.floor(1 + Math.random() * 4)}-комн. кварт.`,
                        floor: isComplex ? "1-16" : `${Math.floor(1 + Math.random() * 15)}/${Math.floor(5 + Math.random() * 15)}`,
                        year: isComplex ? "2022-2024" : (2020 + Math.floor(Math.random() * 4)).toString()
                    };
                };

                // Generate 10 regular properties and 2 complexes
                const properties = [];
                for (let i = 1; i <= 10; i++) {
                    properties.push(generateRandomMarker(i, false));
                }
                for (let i = 11; i <= 12; i++) {
                    properties.push(generateRandomMarker(i, true));
                }

                // Add markers to map with custom icons and popups
                properties.forEach(property => {
                    const marker = L.marker([property.lat, property.lng], {
                        icon: tonMarkerIcon(property.hasCashback),
                        riseOnHover: true
                    }).addTo(map);

                    // Custom popup content
                    const popupContent = `
                        <div class="w-48">
                            <h3 class="font-bold">${property.name}</h3>
                            <p class="text-sm">${property.type === 'ЖК' ? 'Объекты от 6.2 млн ₽' : `${property.price} · ${property.rooms} комн.`}</p>
                            <p class="text-xs text-gray-500 mt-1">${property.type !== 'ЖК' ? `${property.floor} этаж · ` : ''}${property.year}</p>
                            ${property.hasCashback ? 
                              '<div class="mt-1 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">Кешбек</div>' : ''}
                            <button onclick="showObjectDetails(${property.id})" 
                                    class="mt-2 w-full bg-blue-500 text-white py-1 rounded text-sm hover:bg-blue-600">
                                Подробнее
                            </button>
                        </div>
                    `;

                    marker.bindPopup(popupContent);
                    marker.on('click', function() {
                        showObjectDetails(property.id);
                    });
                });

                // Add zoom controls in bottom right
                L.control.zoom({
                    position: 'bottomright'
                }).addTo(map);

                // Add basemap tiles with proper error handling
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    errorTileUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAB/ElEQVR4nO3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4K0G0wABlT6OoAAAAABJRU5ErkJggg=='
                }).addTo(map);

                // Add zoom controls in bottom right
                L.control.zoom({
                    position: 'bottomright'
                }).addTo(map);

                // Ensure map container is visible
                document.getElementById('map').style.visibility = 'visible';


                // TON style marker
                const propertyIcon = (property) => L.divIcon({
                    className: 'custom-marker',
                    html: `
                        <div class="relative transform hover:scale-110 transition-transform duration-200">
                            <div class="absolute -inset-1 rounded-full bg-blue-400 opacity-20 animate-pulse"></div>
                            <div class="relative rounded-full w-10 h-10 flex items-center justify-center ton-gradient shadow-md">
                                <span class="text-white font-semibold z-10 text-sm">
                                    ${property.type === 'ЖК' ? 'ЖК' : property.rooms}
                                </span>
                            </div>
                            <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-0 h-0 
                                    border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent 
                                    border-t-blue-500"></div>
                        </div>
                    `,
                    iconSize: [40, 50],
                    iconAnchor: [20, 50]
                });

                // TON style clusters
                const markers = L.markerClusterGroup({
                    iconCreateFunction: function(cluster) {
                        const count = cluster.getChildCount();
                        return L.divIcon({
                            html: `
                                <div class="relative">
                                    <div class="absolute inset-0 rounded-full bg-blue-500 opacity-20"></div>
                                    <div class="relative rounded-full w-12 h-12 flex items-center justify-center ton-gradient shadow-md">
                                        <span class="text-white font-bold">${count}</span>
                                    </div>
                                </div>
                            `,
                            className: 'marker-cluster-custom',
                            iconSize: L.point(40, 40)
                        });
                    },
                    spiderfyOnMaxZoom: true,
                    showCoverageOnHover: false,
                    zoomToBoundsOnClick: true
                });
                
                // Property data with more details
                const properties = [
                    { 
                        lat: 45.0435, 
                        lng: 38.9783, 
                        price: "12.8", 
                        count: 4,
                        type: "Квартира",
                        rooms: 4,
                        area: 104,
                        objectId: 1,
                        hasCashback: true
                    },
                    { 
                        lat: 45.0330, 
                        lng: 38.9680, 
                        price: "8.7", 
                        count: 5,
                        type: "Квартира",
                        rooms: 3,
                        area: 78,
                        objectId: 2,
                        hasCashback: true
                    },
                    { 
                        lat: 45.0180, 
                        lng: 38.9900, 
                        price: "6.2", 
                        count: 3,
                        type: "Квартира", 
                        rooms: 2,
                        area: 54,
                        objectId: 3,
                        hasCashback: false
                    },
                    { 
                        lat: 45.0250, 
                        lng: 38.9600, 
                        price: "ЖК", 
                        count: 8,
                        type: "ЖК",
                        area: "-",
                        objectId: 4,
                        hasCashback: true
                    }
                ];

                // Custom marker icons
                const propertyIcon = (property) => L.divIcon({
                    className: 'custom-marker',
                    html: `
                        <div class="relative">
                            <div class="marker-pulse ${property.hasCashback ? 'bg-blue-500' : 'bg-gray-500'}"></div>
                            <div class="marker-content ${property.hasCashback ? 'bg-blue-500' : 'bg-gray-500'}">
                                <span>${property.price.includes('ЖК') ? 'ЖК' : property.price}</span>
                            </div>
                        </div>
                    `,
                    iconSize: [32, 32],
                    iconAnchor: [16, 32]
                });

                // Add markers
                properties.forEach(property => {
                    const marker = L.marker([property.lat, property.lng], { 
                        icon: propertyIcon(property)
                    });
                    
                    const popupContent = `
                        <div class="popup-content w-52">
                            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                                <div class="ton-gradient p-3 text-white">
                                    <h3 class="font-bold text-lg">${property.price}${property.type === 'ЖК' ? '' : ' млн ₽'}</h3>
                                    <p class="text-blue-100 text-sm">
                                        ${property.type === 'ЖК' ? 'Жилой комплекс' : `${property.rooms}-комн. кв., ${property.area} м²`}
                                    </p>
                                </div>
                                <div class="p-3">
                                    <div class="flex items-center mb-2">
                                        <div class="w-8 h-8 rounded-full ton-gradient flex items-center justify-center text-white font-bold mr-2">
                                            ${property.type === 'ЖК' ? 'ЖК' : property.rooms}
                                        </div>
                                        <div>
                                            <p class="text-gray-700 text-sm">${property.floor} этаж</p>
                                            <p class="text-gray-400 text-xs">${property.year} год</p>
                                        </div>
                                    </div>
                                    ${property.hasCashback ? 
                                        '<div class="bg-blue-50 text-blue-600 text-xs px-2 py-1 rounded-full mb-3">Кешбек 3%</div>' : ''}
                                    <button onclick="showObjectDetails(${property.objectId})" 
                                            class="w-full ton-gradient text-white py-2 rounded-lg text-sm font-medium hover:opacity-90 transition">
                                        Подробнее
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    marker.bindPopup(popupContent);
                    markers.addLayer(marker);
                });
                
                // Add clusters to map
                map.addLayer(markers);

                // Show properties at specific location
                function showPropertiesAtLocation(lat, lng) {
                    // In a real app, this would fetch properties from API
                    // Here we just open the modal with sample data
                    showObjectDetails(lat > 45.04 ? 1 : 
                                    lat > 45.03 ? 2 : 
                                    lat > 45.02 ? 3 : 4);
                }
            </script>
        </div>
    </div>

    <!-- Modal -->
    <div id="objectModal" class="modal fixed inset-0 z-50 flex items-center justify-center bg-black/50 opacity-0 pointer-events-none transition">
        <div class="modal-content bg-white rounded-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto relative">
            <button onclick="hideModal()" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
            
            <div class="p-6">
                <div class="grid md:grid-cols-2 gap-6">
                    <div>
                        <!-- Image Gallery -->
                        <div class="relative">
                            <img id="modalImage" src="https://images.unsplash.com/photo-1560448204-603b3fc33ddc?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Object" class="w-full h-64 md:h-80 object-cover rounded-lg">
                            <div id="modalBadge" class="absolute top-2 right-2 bg-amber-400 text-xs font-medium px-2 py-1 rounded-full">Кешбек 3%</div>
                        </div>
                        <div class="grid grid-cols-4 gap-2 mt-2">
                            <img src="https://images.unsplash.com/photo-1560448204-603b3fc33ddc?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Thumbnail" class="h-16 object-cover rounded cursor-pointer hover:opacity-75" onclick="changeMainImage(this)">
                            <img src="https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Thumbnail" class="h-16 object-cover rounded cursor-pointer hover:opacity-75" onclick="changeMainImage(this)">
                            <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Thumbnail" class="h-16 object-cover rounded cursor-pointer hover:opacity-75" onclick="changeMainImage(this)">
                            <img src="https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Thumbnail" class="h-16 object-cover rounded cursor-pointer hover:opacity-75" onclick="changeMainImage(this)">
                        </div>
                    </div>
                    
                    <div>
                        <h2 id="modalTitle" class="text-2xl font-bold">4-комн. квартира, 104 м²</h2>
                        <p id="modalAddress" class="text-gray-600 mt-1">ЖК «Гранд Люкс», Краснодар, ул. Красных Партизан</p>
                        
                        <div class="bg-blue-50 rounded-lg p-4 mt-4">
                            <div class="flex justify-between items-center">
                                <div>
                                    <p class="text-sm text-gray-500">Цена</p>
                                    <p id="modalPrice" class="font-bold text-xl">12 800 000 ₽</p>
                                </div>
                                <div class="bg-blue-100 px-3 py-1 rounded-full">
                                    <span id="modalCashback" class="font-medium text-blue-600">Кешбек 3%</span>
                                </div>
                            </div>
                            <button class="ton-gradient w-full text-white py-3 rounded-lg font-medium mt-3 hover:opacity-90 transition">
                                Оставить заявку
                            </button>
                        </div>
                        
                        <!-- ЖК контент (скрыт по умолчанию) -->
                        <div id="modalJkContent" class="hidden">
                            <div class="mt-6">
                                <div class="grid grid-cols-2 gap-4 mb-6">
                                    <div>
                                        <p class="text-sm text-gray-500">Годы сдачи</p>
                                        <p id="modalJkYear" class="font-medium"></p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Этажность</p>
                                        <p id="modalJkFloors" class="font-medium"></p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Площади</p>
                                        <p id="modalJkArea" class="font-medium"></p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Застройщик</p>
                                        <p id="modalJkDev" class="font-medium"></p>
                                    </div>
                                </div>
                                
                                <h3 class="font-semibold text-lg mb-3">О жилом комплексе</h3>
                                <div id="modalJkDescription" class="text-gray-700"></div>
                                
                                <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h4 class="font-medium mb-2">Характеристики ЖК</h4>
                                        <div class="space-y-2 text-sm">
                                            <div class="flex justify-between">
                                                <span class="text-gray-500">Класс</span>
                                                <span id="modalJkClass" class="font-medium"></span>
                                            </div>
                                            <div class="flex justify-between">
                                                <span class="text-gray-500">Паркинг</span>
                                                <span class="font-medium">Подземный</span>
                                            </div>
                                            <div class="flex justify-between">
                                                <span class="text-gray-500">Высота потолков</span>
                                                <span class="font-medium">2.8 м</span>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h4 class="font-medium mb-2">Инфраструктура</h4>
                                        <div class="grid grid-cols-2 gap-2 text-sm">
                                            <p class="flex items-center">
                                                <svg class="w-4 h-4 mr-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                                                </svg>
                                                Школа
                                            </p>
                                            <p class="flex items-center">
                                                <svg class="w-4 h-4 mr-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                                                </svg>
                                                Детсад
                                            </p>
                                            <p class="flex items-center">
                                                <svg class="w-4 h-4 mr-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                                                </svg>
                                                Магазины
                                            </p>
                                            <p class="flex items-center">
                                                <svg class="w-4 h-4 mr-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                                                </svg>
                                                Парк
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Обычный контент (квартиры) -->
                        <div id="modalRegularContent">
                            <div class="mt-6">
                                <h3 class="font-semibold text-lg mb-3">Характеристики</h3>
                                <div class="grid grid-cols-2 gap-3">
                                    <div>
                                        <p class="text-sm text-gray-500">Этаж</p>
                                        <p id="modalFloor" class="font-medium">5/16</p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Год постройки</p>
                                        <p id="modalYear" class="font-medium">2019</p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Площадь</p>
                                        <p id="modalArea" class="font-medium">104 м²</p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Кухня</p>
                                        <p class="font-medium">17 м²</p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Балкон</p>
                                        <p class="font-medium">Да</p>
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-500">Ремонт</p>
                                        <p class="font-medium">Евро</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-8">
                    <h3 class="font-semibold text-lg mb-3">Информация о ЖК</h3>
                    <div id="modalDescription" class="text-gray-700"></div>
                    
                    <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <h4 class="font-medium mb-2">Характеристики ЖК</h4>
                            <div class="space-y-2 text-sm">
                                <div class="flex justify-between"><span class="text-gray-500">Застройщик</span><span id="modalDev" class="font-medium"></span></div>
                                <div class="flex justify-between"><span class="text-gray-500">Класс</span><span id="modalSeries" class="font-medium"></span></div>
                                <div class="flex justify-between"><span class="text-gray-500">Отделка</span><span id="modalDecoration" class="font-medium"></span></div>
                                <div class="flex justify-between"><span class="text-gray-500">Паркинг</span><span id="modalParking" class="font-medium"></span></div>
                            </div>
                        </div>
                        
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <h4 class="font-medium mb-2">Способы оплаты</h4>
                            <div id="modalPayment" class="flex flex-wrap gap-2"></div>
                        </div>
                    </div>
                    
                    <div class="mt-6">
                        <h4 class="font-medium mb-2">Особенности</h4>
                        <div id="modalFeatures" class="flex flex-wrap gap-2"></div>
                    </div>
                    
                    <div v-if="object.cashback" class="mt-6">
                        <div class="bg-green-50 border border-green-100 rounded-lg p-4">
                            <div class="flex items-start">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mt-0.5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                                </svg>
                                <div>
                                    <p class="font-medium">При покупке квартиры в этом ЖК через наш сервис вы получите кешбек 1%.</p>
                                    <p class="text-sm text-gray-600 mt-1">Кешбек зачисляется на ваш Tons кошелек в течение 5 рабочих дней после завершения сделки.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Floating Cashback Banner -->
    <div class="fixed bottom-6 right-6 bg-white shadow-lg rounded-lg p-4 max-w-xs z-40">
        <div class="flex items-center">
            <div class="bg-green-100 p-2 rounded-full mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <div>
                <h4 class="font-medium">Кешбек до 3%</h4>
                <p class="text-xs text-gray-500 mt-1">Возвращаем часть средств за покупку недвижимости</p>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        const mapboxToken = 'pk.eyJ1IjoidG9ucy1yZWFsLWVzdGF0ZSIsImEiOiJjbHVuY2k4aWswMnk0MmpwbmQ3ZG1pbWNvIn0.LLF3E8k3M0-XgP3-Kb1z6g';
        let map;
        let markers = [];
        
        // Initialize map with Leaflet
        function initMap() {
            const map = L.map('map').setView([45.0355, 38.9753], 12);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // Existing marker code would go here
            loadInitialProperties();
        }
        
        // Load initial properties on map
        function loadInitialProperties() {
            const initialProperties = [
                {
                    id: 1,
                    coordinates: [38.9783, 45.0435],
                    price: "12.8M",
                    color: "#0087F5",
                    onClick: () => showObjectDetails(1)
                },
                {
                    id: 2,
                    coordinates: [38.9680, 45.0330], 
                    price: "8.7M",
                    color: "#0087F5",
                    onClick: () => showObjectDetails(2)
                },
                {
                    id: 3,
                    coordinates: [38.9900, 45.0180],
                    price: "6.2M", 
                    color: "#0087F5",
                    onClick: () => showObjectDetails(3)
                },
                {
                    id: 4,
                    coordinates: [38.9600, 45.0250],
                    price: "ЖК",
                    color: "#0087F5",
                    onClick: () => showObjectDetails(4)
                }
            ];
            
            addMarkersToMap(initialProperties);
        }

        // Add markers to map
        function addMarkersToMap(properties) {
            // Clear existing markers
            clearMarkers();
            
            properties.forEach(property => {
                const el = document.createElement('div');
                el.className = 'custom-marker';
                el.innerHTML = `<div class="marker-pin"></div><span class="marker-price">${property.price}</span>`;
                el.style.width = '40px';
                el.style.height = '54px';
                
                const marker = new mapboxgl.Marker(el)
                    .setLngLat(property.coordinates)
                    .addTo(map);
                    
                el.addEventListener('click', property.onClick);
                
                markers.push(marker);
            });
        }
        
        // Clear all markers from map
        function clearMarkers() {
            markers.forEach(marker => marker.remove());
            markers = [];
        }
        
        // Search properties by address
        async function searchProperties() {
            const address = document.getElementById('addressInput').value;
            
            if (!address) {
                alert('Пожалуйста, введите адрес для поиска');
                return;
            }
            
            try {
                // Geocode address to get coordinates
                const response = await fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(address)}.json?access_token=${mapboxToken}`);
                const data = await response.json();
                
                if (data.features.length === 0) {
                    alert('Адрес не найден');
                    return;
                }
                
                const [lng, lat] = data.features[0].center;
                
                // Center map on the searched location
                map.flyTo({
                    center: [lng, lat],
                    zoom: 14
                });
                
                // In a real app, you would fetch properties from your API near these coordinates
                const nearbyProperties = await fetchNearbyProperties(lng, lat);
                addMarkersToMap(nearbyProperties);
                
            } catch (error) {
                console.error('Ошибка поиска:', error);
                alert('Произошла ошибка при поиске');
            }
        }
        
        // Mock function to fetch nearby properties - replace with real API call
        async function fetchNearbyProperties(lng, lat) {
            // This would normally be an API call to your backend
            // Here we mock some random properties near the search location
            
            const randomOffset = () => (Math.random() * 0.02 - 0.01); 
            
            return [
                {
                    id: 101,
                    coordinates: [lng + randomOffset(), lat + randomOffset()],
                    price: `${Math.floor(5 + Math.random() * 10)}.${Math.floor(Math.random() * 9)}M`,
                    color: "#0087F5",
                    onClick: () => showObjectDetails(101)
                },
                {
                    id: 102,
                    coordinates: [lng + randomOffset(), lat + randomOffset()],
                    price: `${Math.floor(5 + Math.random() * 10)}.${Math.floor(Math.random() * 9)}M`,
                    color: "#0087F5", 
                    onClick: () => showObjectDetails(102)
                }
            ];
        }
        
        // Initialize map when page loads
        window.onload = initMap;
        
        // Object Details
        const objects = {
            1: {
                title: "4-комн. квартира, 104 м²",
                price: "12 800 000 ₽",
                address: "ЖК «Гранд Люкс», Краснодар, ул. Красных Партизан",
                image: "https://images.unsplash.com/photo-1560448204-603b3fc33ddc?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                floor: "5/16",
                year: "2019",
                area: "104 м²",
                cashback: "Кешбек 3%",
                badge: "Кешбек 3%",
                badgeColor: "amber-400",
                description: "Просторная 4-комнатная квартира в современном жилом комплексе \"Гранд Люкс\". Квартира с качественным евроремонтом, готова к заселению. Большая кухня-гостиная 30 м² с панорамным остеклением. Три спальни и кабинет. Санузлы раздельные. Вся необходимая бытовая техника встроена. Двор закрыт от посторонних, детские и спортивные площадки, подземный паркинг. Развитая инфраструктура района - школы, детские сады, торговые центры в шаговой доступности. Кешбек 3% при покупке через Tons."
            },
            2: {
                title: "3-комн. квартира, 78 м²",
                price: "8 700 000 ₽",
                address: "ЖК «Небесный», Краснодар, ул. 40 лет Победы",
                image: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                floor: "15/25",
                year: "2022",
                area: "78 м²",
                cashback: "Кешбек 2%",
                badge: "Кешбек 2%",
                badgeColor: "amber-400",
                description: "Современная 3-комнатная квартира в новом жилом комплексе \"Небесный\". Высокий этаж с панорамным видом на город. Удобная планировка с изолированными комнатами. Кухня-гостиная 20 м². Есть балкон. Ремонт выполнен по дизайнерскому проекту. Встроенная техника, кондиционеры. Закрытая охраняемая территория, паркинг, детские площадки. Рядом парк и набережная. Кешбек 2% при покупке через Tons."
            },
            3: { 
            },
            4: {
                title: "2-комн. квартира, 54 м²",
                price: "6 200 000 ₽",
                address: "ЖК «Триумфальная Арка», Краснодар, ул. Тургенева",
                image: "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                floor: "3/9",
                year: "2018",
                area: "54 м²",
                cashback: "",
                badge: "Акция",
                badgeColor: "red-500 text-white",
                description: "Уютная 2-комнатная квартира в жилом комплексе \"Триумфальная Арка\". Хорошая транспортная доступность. Первый пул ремонта - стены, пол, сантехника. Возможен индивидуальный дизайн-проект. Балкон застеклен. Во дворе детская площадка, зоны отдыха. В шаговой доступности супермаркет, аптека, остановка общественного транспорта. Специальное предложение - скидка 5% при покупке до конца месяца."
            },
            4: {
                title: "ЖК «Гранд Люкс»",
                price: "12 объектов от 6.2 млн ₽",
                address: "Краснодар, ул. Красных Партизан, 108",
                image: "https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                floor: "5-16 этажей",
                year: "2020-2024 (3 очередь)",
                area: "от 33 м² до 125 м²",
                cashback: "Кешбек 1%",
                badge: "ЖК",
                badgeColor: "blue-500 text-white",
                developer: "Гарантия-Инвест",
                series: "Комфорт-класс",
                decoration: "Чистовая отделка",
                parking: "Подземный (платный)",
                ceiling: "2.7 м",
                infrastructure: "Школа, детсад, магазины",
                description: `
                    <p>Жилой комплекс бизнес-класса в экологически чистом районе Краснодара. Общая площадь 15 га.</p>
                    <ul class="mt-2 list-disc pl-5">
                        <li>7 жилых корпусов высотой 5-16 этажей</li>
                        <li>Собственная управляющая компания</li>
                        <li>Двор без машин, 70% озеленения</li>
                        <li>Детские и спортивные площадки</li>
                        <li>Фитнес-центр и SPA на территории</li>
                        <li>3 очереди строительства</li>
                        <li>Инфраструктура шаговой доступности</li>
                    </ul>
                    <p class="mt-2">Кешбек 1% при покупке квартиры через нашу платформу.</p>
                `,
                paymentTypes: ["Ипотека 4.8%", "Рассрочка 0%", "Trade-in"],
                features: ["Панорамные окна", "Тёплые полы", "Видеонаблюдение", "Пункт охраны"]
            }
        };
        
        // Modal functions
        function showObjectDetails(id) {
            if (!objects[id]) {
                console.error('Объект с id', id, 'не найден');
                return;
            }
            const object = objects[id];
            
            document.getElementById('modalTitle').textContent = object.title;
            document.getElementById('modalPrice').textContent = object.price;
            document.getElementById('modalAddress').textContent = object.address;
            document.getElementById('modalImage').src = object.image;
            document.getElementById('modalFloor').textContent = object.floor || '-';
            document.getElementById('modalYear').textContent = object.year || '-';
            document.getElementById('modalArea').textContent = object.area || '-';
            document.getElementById('modalCashback').textContent = object.cashback || 'Нет кешбека';
            document.getElementById('modalDescription').innerHTML = object.description || '';
            
            // ЖК-specific fields
            if (object.developer) {
                document.getElementById('modalDev').textContent = object.developer;
                document.getElementById('modalSeries').textContent = object.series;
                document.getElementById('modalDecoration').textContent = object.decoration;
                document.getElementById('modalParking').textContent = object.parking;
                
                // Render payment types
                const paymentEl = document.getElementById('modalPayment');
                paymentEl.innerHTML = '';
                object.paymentTypes?.forEach(type => {
                    const chip = document.createElement('span');
                    chip.className = 'bg-blue-100 text-blue-800 text-xs px-2.5 py-0.5 rounded';
                    chip.textContent = type;
                    paymentEl.appendChild(chip);
                });
                
                // Render features
                const featuresEl = document.getElementById('modalFeatures');
                featuresEl.innerHTML = '';
                object.features?.forEach(feat => {
                    const chip = document.createElement('span');
                    chip.className = 'bg-gray-100 text-gray-800 text-xs px-2.5 py-0.5 rounded';
                    chip.textContent = feat;
                    featuresEl.appendChild(chip);
                });
            }
            
            const badge = document.getElementById('modalBadge');
            badge.textContent = object.badge;
            badge.className = `absolute top-2 right-2 bg-${object.badgeColor} text-xs font-medium px-2 py-1 rounded-full`;
            
            const modal = document.getElementById('objectModal');
            modal.classList.add('open');
            document.body.style.overflow = 'hidden';

            // Special handling for ЖК (id=4)
            if (id === 4) {
                const jkContent = document.getElementById('modalJkContent');
                const regularContent = document.getElementById('modalRegularContent');
                jkContent.classList.remove('hidden');
                regularContent.classList.add('hidden');
                
                // ЖК-specific fields
                document.getElementById('modalJkTitle').textContent = 'ЖК «Гранд Люкс»';
                document.getElementById('modalJkPrice').textContent = '12 объектов от 6.2 млн ₽';
                document.getElementById('modalJkAddress').textContent = 'Краснодар, ул. Красных Партизан, 108';
                document.getElementById('modalJkYear').textContent = '2020-2024 (3 очередь)';
                document.getElementById('modalJkFloors').textContent = '5-16 этажей';
                document.getElementById('modalJkArea').textContent = 'от 33 м² до 125 м²';
                document.getElementById('modalJkDev').textContent = 'Гарантия-Инвест';
                document.getElementById('modalJkClass').textContent = 'Комфорт-класс';
                document.getElementById('modalJkDescription').innerHTML = `
                    <p>Жилой комплекс бизнес-класса в экологически чистом районе Краснодара. Общая площадь 15 га.</p>
                    <ul class="mt-2 list-disc pl-5">
                        <li>7 жилых корпусов высотой 5-16 этажей</li>
                        <li>Собственная управляющая компания</li>
                        <li>Двор без машин, 70% озеленения</li>
                        <li>Детские и спортивные площадки</li>
                    </ul>
                    <p class="mt-3">Кешбек 1% при покупке квартиры через нашу платформу.</p>
                `;
            } else {
                const jkContent = document.getElementById('modalJkContent');
                const regularContent = document.getElementById('modalRegularContent');
                jkContent.classList.add('hidden');
                regularContent.classList.remove('hidden');
            }
            
            // Center map on the object
            if (id === 1) map.setView([45.0435, 38.9783], 15);
            else if (id === 2) map.setView([45.0330, 38.9680], 15);
            else if (id === 3) map.setView([45.0180, 38.9900], 15);
            else if (id === 4) map.setView([45.0250, 38.9600], 15);
        }
        
        function hideModal() {
            const modal = document.getElementById('objectModal');
            modal.classList.remove('open');
            document.body.style.overflow = 'auto';
        }
        
        function changeMainImage(img) {
            document.getElementById('modalImage').src = img.src;
        }
        
        // Close modal when clicking outside
        document.getElementById('objectModal').addEventListener('click', function(e) {
            if (e.target === this) {
                hideModal();
            }
        });
        
        // Toggle advanced filters
        function toggleAdvancedFilters() {
            const filters = document.getElementById('advancedFilters');
            filters.classList.toggle('hidden');
        }
        
        // Toggle object list on mobile
        function toggleObjectList() {
            const list = document.querySelector('.lg\\:w-1\\/3');
            list.classList.toggle('hidden');
        }
    </script>
</body>
   

    <script>
        // Toggle FAQ items
        function toggleFAQ(id) {
            const content = document.getElementById(`faq-content-${id}`);
            const icon = document.getElementById(`faq-icon-${id}`);
            
            content.classList.toggle('hidden');
            icon.classList.toggle('rotate-180');
        }
        
        // Mobile menu toggle would be implemented here
    </script>
	
	<script>
        // Dropdown menu functionality
        function toggleDropdown(element) {
            const dropdown = element.closest('.dropdown');
            const menu = dropdown.querySelector('.dropdown-menu');
            const isOpen = menu.classList.contains('open');
            
            // Close all other dropdowns first
            document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('open');
                    openMenu.previousElementSibling.classList.remove('open');
                }
            });
            
            // Toggle current dropdown
            menu.classList.toggle('open');
            dropdown.querySelector('.dropdown-btn').classList.toggle('open');
        }

        // Close dropdowns when clicking outside
        function toggleDropdown(button) {
            const dropdown = button.closest('.dropdown');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            // Close all other open dropdowns first
            document.querySelectorAll('.dropdown-menu.open').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('open');
                    openMenu.previousElementSibling.classList.remove('open');
                }
            });
            
            // Toggle current dropdown
            menu.classList.toggle('open');
            button.classList.toggle('open');
        }

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.open').forEach(menu => {
                    menu.classList.remove('open');
                    menu.previousElementSibling.classList.remove('open');
                });
            }
        });

        // Footer menu functionality
        function toggleFooterMenu(header) {
            if (window.innerWidth >= 768) return;
            
            const group = header.closest('.footer-menu-group');
            const submenu = group.querySelector('.footer-submenu');
            const icon = header.querySelector('svg');
            
            // Toggle submenu
            submenu.classList.toggle('hidden');
            
            // Rotate icon
            icon.classList.toggle('rotate-180');
        }
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    menu.classList.remove('open');
                    menu.previousElementSibling.classList.remove('open');
                });
            }
        });

        // Initialize all carousels on page
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.carousel').forEach(carousel => {
                const inner = carousel.querySelector('.carousel-inner');
                const items = inner.querySelectorAll('.carousel-item');
                const dots = carousel.querySelectorAll('.carousel-dot');
                const prevBtn = carousel.querySelector('.carousel-prev');
                const nextBtn = carousel.querySelector('.carousel-next');
                
                let currentIndex = 0;
                
                function updateCarousel() {
                    inner.style.transform = `translateX(-${currentIndex * 100}%)`;
                    
                    // Update dots
                    dots.forEach((dot, index) => {
                        dot.classList.toggle('active', index === currentIndex);
                    });
                }
                
                // Navigation buttons
                if (prevBtn) {
                    prevBtn.addEventListener('click', () => {
                        currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
                        updateCarousel();
                    });
                }
                
                if (nextBtn) {
                    nextBtn.addEventListener('click', () => {
                        currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                        updateCarousel();
                    });
                }
                
                // Dot navigation
                dots.forEach((dot, index) => {
                    dot.addEventListener('click', () => {
                        currentIndex = index;
                        updateCarousel();
                    });
                });
                
                // Auto-rotate every 5 seconds
                let interval = setInterval(() => {
                    currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                    updateCarousel();
                }, 5000);
                
                // Pause on hover
                carousel.addEventListener('mouseenter', () => clearInterval(interval));
                carousel.addEventListener('mouseleave', () => {
                    interval = setInterval(() => {
                        currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                        updateCarousel();
                    }, 5000);
                });
            });
        });
    </script>
	  <script>
        // Typewriter animation
        function setupTypewriter() {
            const el = document.getElementById('typewriter');
            const changingTexts = [
                "кэшбеком до 5%",
                "платежами в подарок",
                "выгодой до 500 000 ₽"
            ];
            
            let part = '';
            const staticPrefix = 'с ';
            let textIndex = 0;
            let isDeleting = false;
            let typingSpeed = 100;
            let deletingSpeed = 50;
            let pauseAfterType = 2000;
            let pauseAfterDelete = 500;

            function tick() {
                const fullChangingText = changingTexts[textIndex];
                
                if (isDeleting) {
                    part = fullChangingText.substring(0, part.length - 1);
                    el.innerHTML = '<span class="typewriter-text gradient-text">' + part + '</span>';
                    
                    if (part === '') {
                        isDeleting = false;
                        textIndex = (textIndex + 1) % changingTexts.length;
                        setTimeout(tick, pauseAfterDelete);
                    } else {
                        setTimeout(tick, deletingSpeed);
                    }
                } else {
                    part = fullChangingText.substring(0, part.length + 1);
                    el.innerHTML = '<span class="typewriter-text">' + staticPrefix + part + '</span>';
                    
                    if (part === fullChangingText) {
                        isDeleting = true;
                        setTimeout(tick, pauseAfterType);
                    } else {
                        setTimeout(tick, typingSpeed);
                    }
                }
            }

            el.innerHTML = '<span class="typewriter-text gradient-text">' + staticPrefix + changingTexts[0].substring(0, 1) + '</span>';
            setTimeout(tick, 1000); // Start animation after 1 second
        }

        // Loading animation
        window.addEventListener('load', function() {
            setTimeout(function() {
                document.querySelector('.loading-animation').style.display = 'none';
            }, 2000);
        });

        // Mobile menu toggle
        function toggleMobileMenu() {
            const menu = document.getElementById('mobileMenu');
            menu.classList.toggle('hidden');
            // Close all submenus when closing main menu
            if (menu.classList.contains('hidden')) {
                document.querySelectorAll('.mobile-submenu').forEach(submenu => {
                    submenu.classList.add('hidden');
                });
            }
        }

        // Mobile submenu toggle
        function toggleSubMenu(id) {
            const submenu = document.getElementById(id);
            submenu.classList.toggle('hidden');
        }

        // Modal functions
        function openApplicationModal() {
            document.getElementById('applicationModal').classList.remove('hidden');
        }

        function openLoginModal() {
            document.getElementById('loginModal').classList.remove('hidden');
        }

        function openRegisterModal() {
            closeModal('loginModal');
            document.getElementById('registerModal').classList.remove('hidden');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.add('hidden');
        }

        // Login/logout simulation
        function loginUser() {
            closeModal('loginModal');
            document.getElementById('accountModal').classList.remove('hidden');
        }

        function logoutUser() {
            closeModal('accountModal');
        }

        // Toggle filters panel
        document.getElementById('toggleFilters').addEventListener('click', function() {
            const panel = document.getElementById('filtersPanel');
            panel.classList.toggle('hidden');
            this.querySelector('i').classList.toggle('fa-sliders-h');
            this.querySelector('i').classList.toggle('fa-times');
        });

        // Initialize all carousels
        function initCarousels() {
            document.querySelectorAll('.carousel').forEach(carousel => {
                const inner = carousel.querySelector('.carousel-inner');
                const items = inner.querySelectorAll('.carousel-item');
                const dots = carousel.querySelectorAll('.carousel-dot');
                
                // Set initial active dot
                dots[0].classList.add('active');
                
                // Clone first and last items for infinite scroll
                const firstClone = inner.firstElementChild.cloneNode(true);
                const lastClone = inner.lastElementChild.cloneNode(true);
                inner.appendChild(firstClone);
                inner.insertBefore(lastClone, inner.firstElementChild);
                
                let currentIndex = 1;
                const itemWidth = items[0].clientWidth;
                inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                
                // Auto-rotate every 5 seconds
                let interval = setInterval(nextSlide, 5000);
                
                function nextSlide() {
                    currentIndex++;
                    inner.style.transition = 'transform 0.5s ease-in-out';
                    inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    updateDots();
                }
                
                function prevSlide() {
                    currentIndex--;
                    inner.style.transition = 'transform 0.5s ease-in-out';
                    inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    updateDots();
                }
                
                function updateDots() {
                    let realIndex = currentIndex;
                    if (currentIndex === 0) realIndex = items.length - 2;
                    if (currentIndex === items.length - 1) realIndex = 1;
                    
                    dots.forEach((dot, index) => {
                        dot.classList.toggle('active', index === (realIndex - 1) % (items.length - 2));
                    });
                }
                
                // Reset position when reaching clones
                inner.addEventListener('transitionend', () => {
                    if (currentIndex === 0) {
                        inner.style.transition = 'none';
                        currentIndex = items.length - 2;
                        inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    } else if (currentIndex === items.length - 1) {
                        inner.style.transition = 'none';
                        currentIndex = 1;
                        inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                    }
                });
                
                // Navigation buttons
                if (carousel.querySelector('.carousel-next')) {
                    carousel.querySelector('.carousel-next').addEventListener('click', () => {
                        clearInterval(interval);
                        nextSlide();
                        interval = setInterval(nextSlide, 5000);
                    });
                }
                
                if (carousel.querySelector('.carousel-prev')) {
                    carousel.querySelector('.carousel-prev').addEventListener('click', () => {
                        clearInterval(interval);
                        prevSlide();
                        interval = setInterval(nextSlide, 5000);
                    });
                }
                
                // Dot navigation
                dots.forEach((dot, index) => {
                    dot.addEventListener('click', () => {
                        clearInterval(interval);
                        currentIndex = index + 1;
                        inner.style.transition = 'transform 0.5s ease-in-out';
                        inner.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
                        updateDots();
                        interval = setInterval(nextSlide, 5000);
                    });
                });
            });
        }
        
        // Count active filters
        function updateActiveFiltersCount() {
            const activeCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            const activeSelects = Array.from(document.querySelectorAll('select'))
                .filter(select => select.value !== '');
            
            // Count other active inputs like price ranges, area ranges etc.
            const activeTextInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
                .filter(input => input.value !== '');
            
            const totalFilters = activeCheckboxes.length + activeSelects.length + activeTextInputs.length;
            const badge = document.getElementById('activeFilterBadge');
            
            if (totalFilters > 0) {
                badge.textContent = totalFilters;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        }

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            // Add event listeners for all filter elements
            document.querySelectorAll('input[type="checkbox"], select, input[type="text"], input[type="number"]').forEach(element => {
                element.addEventListener('change', updateActiveFiltersCount);
                element.addEventListener('input', updateActiveFiltersCount);
            });
            
            setupDropdowns();
            setupTypewriter();
            initCarousels();
            
            // Initial count
            updateActiveFiltersCount();
            
            // Filter buttons functionality
            document.querySelectorAll('.room-filter-btn, .class-filter-btn, .condition-filter-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    if (this.classList.contains('active')) {
                        this.classList.remove('active');
                    } else {
                        // For radio-like behavior (only one active in group)
                        if (btn.classList.contains('class-filter-btn')) {
                            btn.closest('div').querySelectorAll('.class-filter-btn').forEach(b => b.classList.remove('active'));
                        }
                        this.classList.add('active');
                    }
                    updateSelectedFilters();
                });
            });
            
            function updateSelectedFilters() {
                const activeFilters = document.querySelectorAll('.room-filter-btn.active, .class-filter-btn.active, .condition-filter-btn.active');
                if (activeFilters.length > 0) {
                    document.getElementById('selectedFilters').classList.remove('hidden');
                } else {
                    document.getElementById('selectedFilters').classList.add('hidden');
                }
            }
        });

        // Calculator functionality
        const priceRange = document.getElementById('priceRange');
        const priceValue = document.getElementById('priceValue');
        const downPaymentRange = document.getElementById('downPaymentRange');
        const downPaymentValue = document.getElementById('downPaymentValue');
        const termRange = document.getElementById('termRange');
        const termValue = document.getElementById('termValue');
        const cashbackAmount = document.getElementById('cashbackAmount');
        const monthlyPayment = document.getElementById('monthlyPayment');

        function updateCalculator() {
            const price = parseInt(priceRange.value);
            const downPayment = parseInt(downPaymentRange.value);
            const downPaymentPercent = Math.round((downPayment / price) * 100);
            const term = parseInt(termRange.value);
            const cashbackPercent = 2.5; // Fixed at 2.5%
            
            // Format values
            priceValue.textContent = new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
            downPaymentValue.textContent = new Intl.NumberFormat('ru-RU').format(downPayment) + ' ₽ (' + downPaymentPercent + '%)';
            termValue.textContent = term + ' лет';
            
            // Calculate cashback amount
            const cashback = price * cashbackPercent / 100;
            cashbackAmount.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(cashback)) + ' ₽';
            
            // Calculate monthly payment at 6% rate (family mortgage)
            const loanAmount = price - downPayment;
            const monthlyRate = 0.06 / 12; // 6% annual rate
            const payments = term * 12;
            const monthly = loanAmount * monthlyRate * Math.pow(1 + monthlyRate, payments) / (Math.pow(1 + monthlyRate, payments) - 1);
            monthlyPayment.textContent = new Intl.NumberFormat('ru-RU').format(Math.round(monthly)) + ' ₽';
        }

        // Add event listeners
        priceRange.addEventListener('input', updateCalculator);
        downPaymentRange.addEventListener('input', updateCalculator);
        termRange.addEventListener('input', updateCalculator);
        cashbackRange.addEventListener('input', updateCalculator);

        // Initialize calculator
        updateCalculator();

        // Property carousel functionality
        document.querySelectorAll('.carousel').forEach(carousel => {
            const inner = carousel.querySelector('.carousel-inner');
            const prev = carousel.querySelector('.carousel-prev');
            const next = carousel.querySelector('.carousel-next');
            const items = carousel.querySelectorAll('img');
            let currentIndex = 0;
            
            function updateCarousel() {
                inner.style.transform = `translateX(-${currentIndex * 100}%)`;
            }
            
            prev.addEventListener('click', () => {
                currentIndex = (currentIndex > 0) ? currentIndex - 1 : items.length - 1;
                updateCarousel();
            });
            
            next.addEventListener('click', () => {
                currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                updateCarousel();
            });
            
            // Auto-rotate every 5 seconds
            setInterval(() => {
                currentIndex = (currentIndex < items.length - 1) ? currentIndex + 1 : 0;
                updateCarousel();
            }, 5000);
        });

        // Close modal when clicking outside
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.classList.add('hidden');
                }
            });
        });
    </script>
</body>
</html>