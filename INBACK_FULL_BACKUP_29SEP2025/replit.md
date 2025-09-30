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
- **Comprehensive Geographical Data Integration (September 27, 2025)**: Successfully integrated Excel files containing 53 districts and 1648 streets with comprehensive coordinates and infrastructure data. Updated districts table with precise coordinates, zoom levels, and detailed infrastructure_data in JSON format including schools, hospitals, shops, transport information. Created enhanced streets table with infrastructure_data and distance_to_center columns. Imported 1400+ streets with coordinates and infrastructure data, significantly enriching the geographical database for improved user experience on districts page
- **Database Integration Enhancement (September 2025)**: Connected "Эксклюзивные предложения" block to dynamically load only the best 6 residential complexes from database with smart filtering (excludes "IV кв. 2025 г. Строится" developments), ensuring full data consistency with /residential-complexes page including photos, buildings, and apartments data
- **Manager Presentation System (September 12, 2025)**: Created internal presentation view page at `/manager/presentation/<id>` inside manager dashboard with complete functionality matching user requirements - includes action buttons (email sharing, download all, link generation), social media integration (Telegram, WhatsApp, VK), property management controls, and robust API integration
- **Manager Favorites System (September 17, 2025)**: Implemented complete favorites functionality for managers with database models (ManagerFavoriteProperty, ManagerFavoriteComplex), API endpoints (/api/manager/favorites/*), and UI integration in manager dashboard. Fixed critical CSS visibility bug where global `.hidden` class was breaking site header and UI elements - replaced with scoped `.manager-favorites-hidden` class for targeted component control
- **Unified Favorites System (September 18, 2025)**: Completed unification of favorites functionality - existing user favorite buttons now automatically work for both regular users and managers without separate interfaces. Implemented centralized user type detection via `FavoritesManager.isManager()`, fixed API endpoint routing for managers, and eliminated conflicts between legacy localStorage and new API systems. All favorites interactions now use consistent logic and appropriate backend endpoints based on user type
- **Comparison Page Enhancement (September 24, 2025)**: Resolved all critical comparison page issues - fixed race condition where buildPropertiesComparison called before data loading, corrected HTTP method from POST to DELETE for removal API endpoints, eliminated unwanted tab switching after deletion, and ensured external URL access functions identically to internal Replit environment. Comparison removal now works in database (not just localStorage) with confirmed API responses {"success":true}
- **Insurance System Integration (September 25, 2025)**: Implemented comprehensive insurance system to replace "transaction support" in mortgage menu. Created complete `/insurance` page based on external example with InBack branding, featuring insurance calculator, application forms, and detailed information sections. Integrated CSRF-protected email handling via SendGrid for insurance applications, with professional HTML email templates. Updated navigation menu "Ипотека" → "Помощь и поддержка" replacing "Сопровождение сделки" with "Страхование". System includes full server-side validation, error handling, and security measures ready for production use
- **Complete Platform Restoration (September 27, 2025)**: Successfully restored entire InBack.ru platform from comprehensive backup. Imported 47 districts from JSON data with coordinates for 15 major districts. All database tables recreated (47 districts, 355 properties, 3 residential complexes, 12 users). Districts page (/districts) fully functional with HTML generation of 48 district cards. Platform verification completed with 31/31 successful checks. All core features operational including property search, cashback system, smart search, and manager interface
- **Interactive Maps with District Boundaries (September 27, 2025)**: Implemented comprehensive geographic mapping system using OpenStreetMap Nominatim API and Yandex Maps. Created InBackMaps JavaScript class for polygon rendering, district boundary visualization, and street highlighting similar to kayan.ru. Built API endpoints for real-time boundary data and coordinate lookup. Established test interface at `/test-maps` for functionality demonstration. Successfully integrated with existing 47-district and 1400+ street database for enhanced user experience
- **Complete Deal Management System (September 27, 2025)**: Implemented comprehensive deal management system between managers and clients with full UI interfaces. Created Deal model with relationships to Manager, User, and ResidentialComplex tables including property price, cashback amount, status tracking, and timestamps. Developed complete API endpoints suite (/api/deals) with CRUD operations, proper authorization, validation, and Decimal serialization. Built manager interface in templates/manager/deals.html with deal creation forms, management tables, status update modals, and statistics dashboard. Created client interface integrated into existing dashboard (templates/auth/dashboard.html) with deal viewing, status filtering (All, Pending, Approved, Rejected), and categorization features. All endpoints properly secured with @manager_required/@login_required decorators and CSRF protection. Deal status workflow supports: new deal → object reserved → mortgage → successful/rejected transitions. System maintains automatic street coordinate enrichment achieving 89.64% coverage while adding new functionality

### Data Architecture
Property and residential complex information is stored in structured JSON files, with a normalized structure using relational IDs, designed for easy transition to a relational database.

### Map Integration
Interactive property maps are powered by both Leaflet.js and Yandex Maps integration. Core mapping features include:

**Traditional Maps**: Leaflet.js with OpenStreetMap tiles, marker clustering for properties, and coordinate-based filtering.

**Advanced Geographic Features (September 27, 2025)**: 
- **OpenStreetMap Nominatim API Integration**: Real-time district boundary polygon retrieval using GeoJSON format
- **Yandex Maps with Boundaries**: InBackMaps JavaScript class for rendering district polygons and street polylines similar to kayan.ru
- **Interactive District Boundaries**: Dynamic loading of district boundaries with visual highlighting
- **Street Highlighting System**: Polyline-based street highlighting with coordinate mapping
- **API Endpoints**: `/api/district/boundaries/<slug>` and `/api/street/coordinates/<slug>` for geographic data access

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

## Current System Status (September 27, 2025)

### Replit Environment Setup (September 19, 2025)
- **Application Status**: ✅ Successfully running on Replit
- **Flask Server**: Configured with gunicorn on port 5000 (0.0.0.0:5000)
- **Database**: PostgreSQL connected and tables created successfully
- **Dependencies**: Cleaned and optimized requirements.txt with 20 core packages
- **Deployment**: Configured for autoscale deployment target
- **Frontend**: Fully functional with responsive design and JavaScript components

### Database State
- **Database Connection**: PostgreSQL successfully configured with DATABASE_URL
- **Tables**: All database models created and initialized
- **excel_properties**: Property records structure ready for import
- **residential_complexes**: Complex data structure available  
- **users**: User management system active
- **managers**: Manager account system operational

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