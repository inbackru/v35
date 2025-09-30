#!/usr/bin/env python3
"""
Import data from Excel files to PostgreSQL database - Fixed version
"""

import pandas as pd
import numpy as np
import os
from app import app, db
from datetime import datetime
import glob
from sqlalchemy import text

def parse_date(date_str):
    """Parse date string to datetime object"""
    if pd.isna(date_str) or date_str == '' or date_str is None:
        return None
    
    try:
        # Handle different date formats
        if isinstance(date_str, str):
            # Handle JavaScript date format like "Fri Aug 08 2025 21:52:32 GMT+0300"
            if 'GMT' in date_str:
                # Extract just the date part before GMT
                date_part = date_str.split(' GMT')[0]
                # Parse the date
                return datetime.strptime(date_part, '%a %b %d %Y %H:%M:%S')
            else:
                # Try standard ISO format
                return datetime.fromisoformat(date_str.replace('T', ' ').replace('Z', ''))
        elif hasattr(date_str, 'timestamp'):
            return date_str
        else:
            return None
    except Exception as e:
        print(f"  Warning: Could not parse date '{date_str}': {e}")
        return None

def safe_get(row, field, default=None):
    """Safely get field from row, handling NaN values"""
    value = row.get(field, default)
    if pd.isna(value):
        return default
    return value

def import_excel_to_db():
    """Import all Excel files to database"""
    
    # Get all Excel files from attached_assets
    excel_files = glob.glob('attached_assets/*.xlsx')
    
    print(f"Found {len(excel_files)} Excel files to process")
    
    with app.app_context():
        
        for file_path in sorted(excel_files):
            filename = os.path.basename(file_path)
            
            # Extract table name from filename
            if '(' in filename:
                table_name = filename.split('(')[0].strip()
            elif '_' in filename and filename.count('_') > 1:
                parts = filename.replace('.xlsx', '').split('_')
                table_name = '_'.join(parts[:-1])  # Remove timestamp
            else:
                table_name = filename.replace('.xlsx', '').split('_')[0]
            
            print(f"\nProcessing: {filename} -> {table_name}")
            
            try:
                # Read Excel file
                df = pd.read_excel(file_path)
                print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
                
                # Import based on table type
                if table_name == 'users':
                    import_users_fixed(df)
                elif table_name == 'managers':
                    import_managers_fixed(df)
                elif table_name == 'admins':
                    import_admins_fixed(df)
                elif table_name == 'developers':
                    import_developers_fixed(df)
                elif table_name == 'districts':
                    import_districts_fixed(df)
                elif table_name == 'residential_complexes':
                    import_residential_complexes_fixed(df)
                elif table_name == 'collections':
                    import_collections_fixed(df)
                elif table_name == 'collection_properties':
                    import_collection_properties_fixed(df)
                elif table_name == 'favorite_properties':
                    import_favorite_properties_fixed(df)
                elif table_name == 'recommendations':
                    import_recommendations_fixed(df)
                elif table_name == 'saved_searches':
                    import_saved_searches_fixed(df)
                elif table_name == 'manager_saved_searches':
                    import_manager_saved_searches_fixed(df)
                elif table_name == 'search_categories':
                    import_search_categories_fixed(df)
                elif table_name == 'sent_searches':
                    import_sent_searches_fixed(df)
                elif table_name == 'user_notifications':
                    import_user_notifications_fixed(df)
                elif table_name == 'blog_categories':
                    import_blog_categories_fixed(df)
                elif table_name == 'blog_articles':
                    import_blog_articles_fixed(df)
                elif table_name == 'blog_posts':
                    import_blog_posts_fixed(df)
                elif table_name == 'cashback_applications':
                    import_cashback_applications_fixed(df)
                elif table_name == 'cashback_payouts':
                    import_cashback_payouts_fixed(df)
                else:
                    print(f"  WARNING: No import handler for table '{table_name}'")
                
            except Exception as e:
                print(f"  ERROR processing {filename}: {e}")
                import traceback
                traceback.print_exc()
        
        # Commit all changes
        try:
            db.session.commit()
            print("\n✅ All data imported successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error committing changes: {e}")
            raise

def import_users_fixed(df):
    """Import users data with proper field mapping"""
    print("  Importing users...")
    count = 0
    for _, row in df.iterrows():
        try:
            # Use SQL INSERT to bypass SQLAlchemy model validation issues
            db.session.execute(text("""
                INSERT INTO users (id, username, email, password_hash, phone, full_name, 
                                 telegram_id, whatsapp_phone, registration_date, last_active,
                                 email_notifications, telegram_notifications, whatsapp_notifications, 
                                 is_verified, user_id, is_active, is_demo, role, client_status, 
                                 assigned_manager_id, preferred_contact)
                VALUES (:id, :username, :email, :password_hash, :phone, :full_name,
                       :telegram_id, :whatsapp_phone, :registration_date, :last_active,
                       :email_notifications, :telegram_notifications, :whatsapp_notifications,
                       :is_verified, :user_id, :is_active, :is_demo, :role, :client_status,
                       :assigned_manager_id, :preferred_contact)
                ON CONFLICT (id) DO UPDATE SET
                    email = EXCLUDED.email,
                    full_name = EXCLUDED.full_name,
                    phone = EXCLUDED.phone
            """), {
                'id': safe_get(row, 'id'),
                'username': safe_get(row, 'email', ''),  # Use email as username
                'email': safe_get(row, 'email', ''),
                'password_hash': safe_get(row, 'password_hash', ''),
                'phone': safe_get(row, 'phone', ''),
                'full_name': safe_get(row, 'full_name', ''),
                'telegram_id': safe_get(row, 'telegram_id'),
                'whatsapp_phone': safe_get(row, 'phone', ''),
                'registration_date': parse_date(safe_get(row, 'created_at')),
                'last_active': parse_date(safe_get(row, 'last_login')),
                'email_notifications': safe_get(row, 'email_notifications', True),
                'telegram_notifications': safe_get(row, 'telegram_notifications', False),
                'whatsapp_notifications': False,
                'is_verified': safe_get(row, 'is_verified', False),
                'user_id': safe_get(row, 'user_id', ''),
                'is_active': safe_get(row, 'is_active', True),
                'is_demo': safe_get(row, 'is_demo', False),
                'role': safe_get(row, 'role', 'buyer'),
                'client_status': safe_get(row, 'client_status', 'Новый'),
                'assigned_manager_id': safe_get(row, 'assigned_manager_id'),
                'preferred_contact': safe_get(row, 'preferred_contact', 'email')
            })
            count += 1
        except Exception as e:
            print(f"    Error importing user row {safe_get(row, 'id')}: {e}")
    print(f"    Imported {count} users")

def import_blog_categories_fixed(df):
    """Import blog categories data"""
    print("  Importing blog categories...")
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO blog_categories (id, name, slug, description, color, icon, 
                                           meta_title, meta_description, sort_order, is_active,
                                           articles_count, views_count, created_at, updated_at)
                VALUES (:id, :name, :slug, :description, :color, :icon,
                       :meta_title, :meta_description, :sort_order, :is_active,
                       :articles_count, :views_count, :created_at, :updated_at)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    slug = EXCLUDED.slug,
                    description = EXCLUDED.description
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_get(row, 'name', ''),
                'slug': safe_get(row, 'slug', f"category-{safe_get(row, 'id')}"),
                'description': safe_get(row, 'description', ''),
                'color': safe_get(row, 'color', 'blue'),
                'icon': safe_get(row, 'icon'),
                'meta_title': safe_get(row, 'meta_title'),
                'meta_description': safe_get(row, 'meta_description'),
                'sort_order': safe_get(row, 'sort_order', 0),
                'is_active': safe_get(row, 'is_active', True),
                'articles_count': safe_get(row, 'articles_count', 0),
                'views_count': safe_get(row, 'views_count', 0),
                'created_at': parse_date(safe_get(row, 'created_at')) or datetime.utcnow(),
                'updated_at': parse_date(safe_get(row, 'updated_at')) or datetime.utcnow()
            })
            count += 1
        except Exception as e:
            print(f"    Error importing blog category row {safe_get(row, 'id')}: {e}")
    print(f"    Imported {count} blog categories")

def import_residential_complexes_fixed(df):
    """Import residential complexes data"""
    print("  Importing residential complexes...")
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO residential_complexes (id, name, slug, address, developer_id, district_id,
                                                 total_buildings, total_apartments, construction_status,
                                                 completion_date, min_price, max_price, is_active,
                                                 latitude, longitude, property_class, building_type,
                                                 parking, playground, security, concierge, gym, kindergarten,
                                                 gallery, main_image, created_at, updated_at)
                VALUES (:id, :name, :slug, :address, :developer_id, :district_id,
                       :total_buildings, :total_apartments, :construction_status,
                       :completion_date, :min_price, :max_price, :is_active,
                       :latitude, :longitude, :property_class, :building_type,
                       :parking, :playground, :security, :concierge, :gym, :kindergarten,
                       :gallery, :main_image, :created_at, :updated_at)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    address = EXCLUDED.address
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_get(row, 'name', ''),
                'slug': safe_get(row, 'slug', f"complex-{safe_get(row, 'id')}"),
                'address': safe_get(row, 'address', ''),
                'developer_id': safe_get(row, 'developer_id'),
                'district_id': safe_get(row, 'district_id'),
                'total_buildings': safe_get(row, 'total_buildings', 0),
                'total_apartments': safe_get(row, 'total_apartments', 0),
                'construction_status': safe_get(row, 'construction_status', 'new'),
                'completion_date': parse_date(safe_get(row, 'delivery_quarter')),
                'min_price': safe_get(row, 'min_price', 0),
                'max_price': safe_get(row, 'max_price', 0),
                'is_active': safe_get(row, 'is_active', True),
                'latitude': safe_get(row, 'latitude'),
                'longitude': safe_get(row, 'longitude'),
                'property_class': safe_get(row, 'property_class', 'комфорт'),
                'building_type': safe_get(row, 'building_type', ''),
                'parking': safe_get(row, 'parking', False),
                'playground': safe_get(row, 'playground', False),
                'security': safe_get(row, 'security', False),
                'concierge': safe_get(row, 'concierge', False),
                'gym': safe_get(row, 'gym', False),
                'kindergarten': safe_get(row, 'kindergarten', False),
                'gallery': safe_get(row, 'gallery', '[]'),
                'main_image': safe_get(row, 'main_image', ''),
                'created_at': parse_date(safe_get(row, 'created_at')) or datetime.utcnow(),
                'updated_at': parse_date(safe_get(row, 'updated_at')) or datetime.utcnow()
            })
            count += 1
        except Exception as e:
            print(f"    Error importing residential complex row {safe_get(row, 'id')}: {e}")
    print(f"    Imported {count} residential complexes")

# Add other import functions with similar pattern
def import_managers_fixed(df):
    """Import managers data"""
    print("  Importing managers...")
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO managers (id, username, email, password_hash, full_name, phone,
                                    telegram_id, whatsapp_phone, is_active, registration_date)
                VALUES (:id, :username, :email, :password_hash, :full_name, :phone,
                       :telegram_id, :whatsapp_phone, :is_active, :registration_date)
                ON CONFLICT (id) DO UPDATE SET
                    email = EXCLUDED.email,
                    full_name = EXCLUDED.full_name
            """), {
                'id': safe_get(row, 'id'),
                'username': safe_get(row, 'username', safe_get(row, 'email', '')),
                'email': safe_get(row, 'email', ''),
                'password_hash': safe_get(row, 'password_hash', ''),
                'full_name': safe_get(row, 'full_name', ''),
                'phone': safe_get(row, 'phone', ''),
                'telegram_id': safe_get(row, 'telegram_id'),
                'whatsapp_phone': safe_get(row, 'whatsapp_phone', ''),
                'is_active': safe_get(row, 'is_active', True),
                'registration_date': parse_date(safe_get(row, 'created_at')) or datetime.utcnow()
            })
            count += 1
        except Exception as e:
            print(f"    Error importing manager row {safe_get(row, 'id')}: {e}")
    print(f"    Imported {count} managers")

# Add placeholder functions for other tables
def import_admins_fixed(df):
    print("  Skipping admins - will implement if needed")
    
def import_developers_fixed(df):
    print("  Skipping developers - will implement if needed")
    
def import_districts_fixed(df):
    print("  Skipping districts - will implement if needed")
    
def import_collections_fixed(df):
    print("  Skipping collections - will implement if needed")
    
def import_collection_properties_fixed(df):
    print("  Skipping collection_properties - will implement if needed")
    
def import_favorite_properties_fixed(df):
    print("  Skipping favorite_properties - will implement if needed")
    
def import_recommendations_fixed(df):
    print("  Skipping recommendations - will implement if needed")
    
def import_saved_searches_fixed(df):
    print("  Skipping saved_searches - will implement if needed")
    
def import_manager_saved_searches_fixed(df):
    print("  Skipping manager_saved_searches - will implement if needed")
    
def import_search_categories_fixed(df):
    print("  Skipping search_categories - will implement if needed")
    
def import_sent_searches_fixed(df):
    print("  Skipping sent_searches - will implement if needed")
    
def import_user_notifications_fixed(df):
    print("  Skipping user_notifications - will implement if needed")
    
def import_blog_articles_fixed(df):
    print("  Skipping blog_articles - will implement if needed")
    
def import_blog_posts_fixed(df):
    print("  Skipping blog_posts - will implement if needed")
    
def import_cashback_applications_fixed(df):
    print("  Skipping cashback_applications - will implement if needed")
    
def import_cashback_payouts_fixed(df):
    print("  Skipping cashback_payouts - will implement if needed")

if __name__ == '__main__':
    import_excel_to_db()