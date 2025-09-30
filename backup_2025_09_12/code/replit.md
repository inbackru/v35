# InBack Real Estate Platform

## Overview
InBack is a modern real estate platform specializing in cashback-enabled property purchases in Krasnodar, Russia. It connects users with new construction properties from trusted developers, offering significant cashback rewards. Key capabilities include property search with interactive maps, detailed property catalogs, residential complex information, comparison tools, and comprehensive resources on districts, mortgages, streets, and a real estate blog. The business vision is to provide a transparent and rewarding experience for property buyers in the Krasnodar market, with ambitions for market expansion and revenue optimization.

## User Preferences
Preferred communication style: Simple, everyday language.
Design approach: "аккуратный дизайн" (neat/tidy) minimalist design with clean, professional styling.
Language: Russian for all user-facing content and communications.
Design consistency: Single corporate blue color scheme (from-blue-600 to-blue-700) for all district cards.

## System Architecture

### Frontend Architecture
The frontend utilizes a Vanilla JavaScript approach for core functionality, prioritizing fast loading and minimal dependencies through modular design. Styling combines custom CSS with Tailwind utility classes for responsive design and consistent theming. The platform employs progressive enhancement, ensuring core features are accessible without JavaScript, with interactive elements layered on top. UI/UX design patterns include typewriter animations, card-based layouts with hover effects, interactive dropdowns, and a mobile-responsive design using CSS Grid and Flexbox with the Inter font family. The platform has undergone complete rebranding to InBack.ru. All pages utilize a `base.html` template for consistent styling.

**Recent Updates (August-September 2025):**
- Implemented unified blue corporate design for all district cards
- Mass updated 40+ district cards to consistent styling with from-blue-600 to-blue-700 gradients  
- Fixed district link routing issues - corrected 25 mismatched URL patterns
- Enhanced card structure with improved typography, icons, and hover animations
- **Database Integration Enhancement (September 2025)**: Connected "Эксклюзивные предложения" block to dynamically load only the best 6 residential complexes from database with smart filtering (excludes "IV кв. 2025 г. Строится" developments), ensuring full data consistency with /residential-complexes page including photos, buildings, and apartments data

### Data Architecture
Property and residential complex information is stored in structured JSON files, with a normalized structure using relational IDs, designed for easy transition to a relational database.

### Map Integration
Interactive property maps are powered by Leaflet.js, utilizing OpenStreetMap tiles. Features include marker clustering for efficient display of multiple properties and coordinate-based filtering for location-based search.

### Search and Filtering System
The platform offers multi-criteria filtering (price range, room count, developer, location) and real-time search without page reloads. Smart search, integrated with PostgreSQL, provides real-time, categorized suggestions (districts, developers, complexes, streets, room types) via an API endpoint, with JavaScript-powered autocomplete. It includes a favorites system for bookmarking properties and tools for side-by-side property comparison.

### Business Logic
Core business logic includes dynamic cashback calculation based on property prices, property status tracking, structured data for real estate developers, and a comprehensive apartment selection system within residential complexes.

### System Design Choices
Comprehensive SEO optimization is implemented, including meta-tags, JSON-LD structured data, XML sitemap, `robots.txt`, and canonical URLs, specifically geo-targeted for Krasnodar. Features include an animated favorites system with `localStorage` persistence, a unified comparison page for properties and residential complexes, consistent modern button styling, and a personalized, role-based manager interface with quick action widgets and real-time statistics. The system also includes a planned hierarchical structure for `Developer → Residential Complex → Building → Apartments`.

## External Dependencies

### Mapping Services
- **Leaflet.js**: Open-source JavaScript library for interactive maps.
- **OpenStreetMap**: Provides map tile data.

### Fonts and Assets
- **Google Fonts**: Used for the Inter font family.

### Database
- **PostgreSQL**: Full production database with a comprehensive schema supporting users, properties, managers, notifications, favorites, collections, recommendations, a blog system, and business process management.

### Notification System
- **SMTP Email Service**: Standard SMTP integration with professional HTML templates for various notifications.
- **Telegram Bot API**: Advanced bot integration for user notifications and account management.
- **WhatsApp Business API**: Integration for instant client communication.
- **Unified Notifications**: Multi-channel system supporting email, Telegram, and WhatsApp, with user preference management for communication channels and types.

### Third-party Services (Integrated)
- **Telegram, WhatsApp, VKontakte**: Social media integration for sharing and contact.

## Current System Status (August 29, 2025)

### Database State
- **excel_properties**: 462 property records with 77 fields from Excel import
- **residential_complexes**: 29 residential complexes with photos and details  
- **it_companies**: 7,579 IT organizations for mortgage verification
- **users**: 7 registered users
- **managers**: 3 manager accounts with enhanced permissions

### Known Issues
- **complex_id conflicts**: 3 complex_ids have multiple ЖК names requiring periodic cleanup
  - complex_id 113046: "ЖК Летний" (main) + 3 other names
  - complex_id 115226: "ЖК Кислород" (main) + 2 other names  
  - complex_id 116104: "ЖК Чайные холмы" (main) + 2 other names

### Critical Files for Backup/Restore
- **app.py**: Main Flask application (499KB, core functionality)
- **models.py**: Database models (1759 lines, complete schema)
- **templates/**: 67 HTML templates for all pages
- **attached_assets/**: Excel files with property data
- **SYSTEM_BACKUP_RESTORE_GUIDE.md**: Complete restoration instructions
- **DATABASE_BACKUP_COMMANDS.sql**: Database verification and fix commands
- **QUICK_RESTORE_CHECKLIST.md**: 5-minute restoration checklist

### Emergency Recovery Procedures
1. Use Replit Checkpoints for project rollback
2. Follow QUICK_RESTORE_CHECKLIST.md for manual restoration  
3. Use DATABASE_BACKUP_COMMANDS.sql for database integrity checks
4. Re-import Excel data if needed using import functions in app.py