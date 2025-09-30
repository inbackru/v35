<?php
require_once __DIR__ . '/../includes/property_functions.php';

// Get property ID from URL
$property_id = $_GET['property_id'] ?? null;

if (!$property_id) {
    header('HTTP/1.1 400 Bad Request');
    die('Property ID is required');
}

// Get property data
$property = getPropertyById($property_id);
if (!$property) {
    header('HTTP/1.1 404 Not Found');
    die('Property not found');
}

// Get residential complex data
$residential_complex = getResidentialComplexById($property['residential_complex_id']);

// Install TCPDF if not already installed
if (!class_exists('TCPDF')) {
    // For this example, we'll create a simple HTML-to-PDF solution
    // In production, you would use TCPDF or similar library
    
    // Set content type for PDF
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="property_' . $property_id . '.pdf"');
    
    // Create a simple HTML version that can be printed as PDF
    generateHTMLPdf($property, $residential_complex);
    exit;
}

function generateHTMLPdf($property, $residential_complex) {
    ?>
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Карточка объекта - <?= htmlspecialchars($property['title']) ?></title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
                color: #333;
            }
            
            .header {
                text-align: center;
                border-bottom: 2px solid #0088cc;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }
            
            .logo {
                background: linear-gradient(135deg, #0088cc, #00a3e0);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                display: inline-block;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            h1 {
                color: #0088cc;
                margin: 0;
                font-size: 24px;
            }
            
            .property-info {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }
            
            .info-section {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
            
            .info-section h2 {
                color: #0088cc;
                margin-top: 0;
                font-size: 18px;
                border-bottom: 1px solid #dee2e6;
                padding-bottom: 10px;
            }
            
            .price {
                font-size: 28px;
                color: #0088cc;
                font-weight: bold;
                margin: 10px 0;
            }
            
            .cashback {
                background: linear-gradient(135deg, #0088cc, #00a3e0);
                color: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                margin: 20px 0;
            }
            
            .cashback-amount {
                font-size: 24px;
                font-weight: bold;
            }
            
            .details-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin: 20px 0;
            }
            
            .detail-item {
                text-align: center;
                padding: 15px;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
            
            .detail-value {
                font-size: 20px;
                font-weight: bold;
                color: #0088cc;
            }
            
            .detail-label {
                font-size: 12px;
                color: #6c757d;
                text-transform: uppercase;
            }
            
            .amenities {
                margin: 20px 0;
            }
            
            .amenities-list {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-top: 15px;
            }
            
            .amenity-item {
                background: #e3f2fd;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 14px;
            }
            
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #0088cc;
                text-align: center;
                color: #6c757d;
                font-size: 12px;
            }
            
            .contact-info {
                background: #0088cc;
                color: white;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
            
            @media print {
                body { margin: 0; }
                .no-print { display: none; }
            }
        </style>
    </head>
    <body>
        <!-- Header -->
        <div class="header">
            <div class="logo">ClickBack</div>
            <h1><?= htmlspecialchars($property['title']) ?></h1>
            <p>Карточка объекта недвижимости</p>
        </div>

        <!-- Main Property Info -->
        <div class="property-info">
            <div class="info-section">
                <h2>Основная информация</h2>
                <div class="price"><?= formatPrice($property['price']) ?></div>
                <?php if ($property['price_per_sqm']): ?>
                    <p><strong>Стоимость за м²:</strong> <?= formatPrice($property['price_per_sqm']) ?></p>
                <?php endif; ?>
                
                <p><strong>Адрес:</strong> <?= htmlspecialchars($property['address']) ?></p>
                <p><strong>Район:</strong> <?= htmlspecialchars($property['district']) ?></p>
                <p><strong>Застройщик:</strong> <?= htmlspecialchars($property['developer']) ?></p>
                
                <?php if ($residential_complex): ?>
                    <p><strong>Жилой комплекс:</strong> <?= htmlspecialchars($residential_complex['name']) ?></p>
                <?php endif; ?>
            </div>

            <div class="info-section">
                <h2>Характеристики квартиры</h2>
                <div class="details-grid">
                    <div class="detail-item">
                        <div class="detail-value"><?= $property['rooms'] ?></div>
                        <div class="detail-label">Комнат</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-value"><?= $property['area'] ?></div>
                        <div class="detail-label">м²</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-value"><?= $property['floor'] ?></div>
                        <div class="detail-label">Этаж</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-value"><?= $property['total_floors'] ?></div>
                        <div class="detail-label">Этажность</div>
                    </div>
                </div>
                
                <p><strong>Год сдачи:</strong> <?= $property['completion_year'] ?></p>
                <p><strong>Ипотека:</strong> <?= $property['mortgage_available'] ? 'Доступна' : 'Не доступна' ?></p>
            </div>
        </div>

        <!-- Cashback Block -->
        <div class="cashback">
            <h3 style="margin: 0 0 10px 0;">Кэшбек с ClickBack</h3>
            <div class="cashback-amount"><?= formatPrice($property['cashback']) ?></div>
            <p style="margin: 10px 0 0 0;">Вернём до 2,5% от стоимости квартиры</p>
        </div>

        <!-- Description -->
        <?php if ($property['description']): ?>
            <div class="info-section">
                <h2>Описание</h2>
                <p><?= nl2br(htmlspecialchars($property['description'])) ?></p>
            </div>
        <?php endif; ?>

        <!-- Amenities -->
        <?php if (!empty($property['amenities'])): ?>
            <div class="amenities">
                <h2 style="color: #0088cc;">Удобства и инфраструктура</h2>
                <div class="amenities-list">
                    <?php foreach ($property['amenities'] as $amenity): ?>
                        <div class="amenity-item">✓ <?= htmlspecialchars($amenity) ?></div>
                    <?php endforeach; ?>
                </div>
            </div>
        <?php endif; ?>

        <!-- Residential Complex Info -->
        <?php if ($residential_complex): ?>
            <div class="info-section">
                <h2>О жилом комплексе</h2>
                <p><strong>Название:</strong> <?= htmlspecialchars($residential_complex['name']) ?></p>
                <p><strong>Застройщик:</strong> <?= htmlspecialchars($residential_complex['developer']) ?></p>
                <p><strong>Количество корпусов:</strong> <?= $residential_complex['total_buildings'] ?></p>
                <p><strong>Общее количество квартир:</strong> <?= $residential_complex['total_apartments'] ?></p>
                <p><strong>Год сдачи:</strong> <?= $residential_complex['completion_year'] ?></p>
                
                <?php if ($residential_complex['description']): ?>
                    <p><strong>Описание:</strong> <?= htmlspecialchars($residential_complex['description']) ?></p>
                <?php endif; ?>
                
                <?php if (!empty($residential_complex['amenities'])): ?>
                    <p><strong>Инфраструктура комплекса:</strong></p>
                    <div class="amenities-list">
                        <?php foreach ($residential_complex['amenities'] as $amenity): ?>
                            <div class="amenity-item">✓ <?= htmlspecialchars($amenity) ?></div>
                        <?php endforeach; ?>
                    </div>
                <?php endif; ?>
            </div>
        <?php endif; ?>

        <!-- Contact Info -->
        <div class="contact-info">
            <h3 style="margin: 0 0 15px 0;">Получить кэшбек</h3>
            <p><strong>Телефон:</strong> +7 (800) 123-12-12</p>
            <p><strong>Email:</strong> info@clickback.ru</p>
            <p><strong>Сайт:</strong> clickback.ru</p>
            <p style="margin: 15px 0 0 0; font-size: 14px;">
                Обратитесь к нам для получения подробной консультации и оформления кэшбека при покупке данной квартиры.
            </p>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>ClickBack</strong> - официальный сервис возврата кэшбека при покупке недвижимости</p>
            <p>Дата создания: <?= date('d.m.Y H:i') ?></p>
            <p>© 2024 ClickBack. Все права защищены.</p>
        </div>

        <script>
            // Auto-print for PDF generation
            window.onload = function() {
                window.print();
            }
        </script>
    </body>
    </html>
    <?php
}
?>
