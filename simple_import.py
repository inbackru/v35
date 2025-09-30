#!/usr/bin/env python3
"""
Simple import script that handles all data properly
"""

import pandas as pd
import numpy as np
import os
from app import app, db
from datetime import datetime
import glob
from sqlalchemy import text

def safe_get(row, field, default=None):
    """Safely get field from row, handling NaN values"""
    value = row.get(field, default)
    if pd.isna(value):
        return default
    return value

def safe_str(value, default=''):
    """Convert value to string safely"""
    if pd.isna(value) or value is None:
        return default
    return str(value)

def safe_int(value, default=0):
    """Convert value to int safely"""
    if pd.isna(value) or value is None:
        return default
    try:
        return int(float(value))
    except:
        return default

def safe_bool(value, default=False):
    """Convert value to bool safely"""
    if pd.isna(value) or value is None:
        return default
    if isinstance(value, bool):
        return value
    try:
        return bool(int(value))
    except:
        return default

def parse_date(date_str):
    """Parse date string to datetime object"""
    if pd.isna(date_str) or date_str == '' or date_str is None:
        return datetime.utcnow()
    
    try:
        if isinstance(date_str, str):
            if 'GMT' in date_str:
                date_part = date_str.split(' GMT')[0]
                return datetime.strptime(date_part, '%a %b %d %Y %H:%M:%S')
            else:
                return datetime.fromisoformat(date_str.replace('T', ' ').replace('Z', ''))
        elif hasattr(date_str, 'timestamp'):
            return date_str
        else:
            return datetime.utcnow()
    except Exception as e:
        return datetime.utcnow()

def simple_data_import():
    """Simple import that works around foreign key issues"""
    
    with app.app_context():
        try:
            print("🔄 Starting simple data import...")
            
            # Clear any existing transaction
            db.session.rollback()
            
            # Import in order, but handle missing foreign keys gracefully
            import_users_simple()
            import_districts_simple()
            import_developers_simple()
            import_residential_complexes_simple()
            import_blog_categories_simple()
            
            db.session.commit()
            print("\n✅ Simple data import finished successfully!")
            
            # Show summary
            show_summary()
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error during import: {e}")
            import traceback
            traceback.print_exc()

def import_users_simple():
    """Import users data"""
    print("\n=== IMPORTING USERS ===")
    
    files = glob.glob('attached_assets/users*')
    if not files:
        print("No user files found")
        return
    
    df = pd.read_excel(files[0])
    print(f"Found {len(df)} users to import")
    
    count = 0
    for _, row in df.iterrows():
        try:
            # Insert or update users
            db.session.execute(text("""
                INSERT INTO users (
                    id, email, phone, full_name, password_hash, role, is_active, 
                    user_id, telegram_id, preferred_contact, email_notifications, 
                    telegram_notifications, created_at, updated_at, last_login
                ) VALUES (
                    :id, :email, :phone, :full_name, :password_hash, :role, :is_active,
                    :user_id, :telegram_id, :preferred_contact, :email_notifications,
                    :telegram_notifications, :created_at, :updated_at, :last_login
                ) ON CONFLICT (id) DO UPDATE SET
                    email = EXCLUDED.email,
                    full_name = EXCLUDED.full_name,
                    phone = EXCLUDED.phone,
                    updated_at = EXCLUDED.updated_at
            """), {
                'id': safe_get(row, 'id'),
                'email': safe_str(safe_get(row, 'email')),
                'phone': safe_str(safe_get(row, 'phone')),
                'full_name': safe_str(safe_get(row, 'full_name')),
                'password_hash': safe_str(safe_get(row, 'password_hash')),
                'role': safe_str(safe_get(row, 'role'), 'buyer'),
                'is_active': safe_bool(safe_get(row, 'is_active'), True),
                'user_id': safe_str(safe_get(row, 'user_id')),
                'telegram_id': safe_str(safe_get(row, 'telegram_id')),
                'preferred_contact': safe_str(safe_get(row, 'preferred_contact'), 'email'),
                'email_notifications': safe_bool(safe_get(row, 'email_notifications'), True),
                'telegram_notifications': safe_bool(safe_get(row, 'telegram_notifications'), False),
                'created_at': parse_date(safe_get(row, 'created_at')),
                'updated_at': parse_date(safe_get(row, 'updated_at')),
                'last_login': parse_date(safe_get(row, 'last_login'))
            })
            count += 1
        except Exception as e:
            print(f"    Error importing user {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} users")

def import_districts_simple():
    """Import districts data"""
    print("\n=== IMPORTING DISTRICTS ===")
    
    files = glob.glob('attached_assets/districts*')
    if not files:
        print("No district files found")
        return
    
    df = pd.read_excel(files[0])
    print(f"Found {len(df)} districts to import")
    
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO districts (
                    id, name, slug, description, city_id, is_active, created_at
                ) VALUES (
                    :id, :name, :slug, :description, :city_id, :is_active, :created_at
                ) ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    slug = EXCLUDED.slug,
                    description = EXCLUDED.description
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_str(safe_get(row, 'name')),
                'slug': safe_str(safe_get(row, 'slug'), f"district-{safe_get(row, 'id')}"),
                'description': safe_str(safe_get(row, 'description')),
                'city_id': 1,
                'is_active': True,
                'created_at': parse_date(safe_get(row, 'created_at'))
            })
            count += 1
        except Exception as e:
            print(f"    Error importing district {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} districts")

def import_developers_simple():
    """Import developers data"""
    print("\n=== IMPORTING DEVELOPERS ===")
    
    files = glob.glob('attached_assets/developers*')
    if not files:
        print("No developer files found - creating default developer")
        # Create default developer for residential complexes
        try:
            db.session.execute(text("""
                INSERT INTO developers (
                    id, name, slug, description, is_active, created_at, updated_at
                ) VALUES (
                    1, 'Стандартный застройщик', 'default-developer', 'Застройщик по умолчанию', true, NOW(), NOW()
                ) ON CONFLICT (id) DO NOTHING
            """))
            print("    ✅ Created default developer")
        except Exception as e:
            print(f"    Error creating default developer: {e}")
        return
    
    # Try to read file with different methods
    df = None
    for engine in ['openpyxl', 'xlrd', None]:
        try:
            df = pd.read_excel(files[0], engine=engine)
            print(f"Successfully read developer file with engine: {engine}")
            break
        except Exception as e:
            print(f"    Failed with engine {engine}: {e}")
    
    if df is None:
        print("    Could not read developer file - creating default")
        try:
            db.session.execute(text("""
                INSERT INTO developers (
                    id, name, slug, description, is_active, created_at, updated_at
                ) VALUES (
                    1, 'Стандартный застройщик', 'default-developer', 'Застройщик по умолчанию', true, NOW(), NOW()
                ) ON CONFLICT (id) DO NOTHING
            """))
            print("    ✅ Created default developer")
        except Exception as e:
            print(f"    Error creating default developer: {e}")
        return
    
    print(f"Found {len(df)} developers to import")
    
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO developers (
                    id, name, slug, description, is_active, created_at, updated_at
                ) VALUES (
                    :id, :name, :slug, :description, :is_active, :created_at, :updated_at
                ) ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_str(safe_get(row, 'name')),
                'slug': safe_str(safe_get(row, 'slug'), f"developer-{safe_get(row, 'id')}"),
                'description': safe_str(safe_get(row, 'description')),
                'is_active': safe_bool(safe_get(row, 'is_active'), True),
                'created_at': parse_date(safe_get(row, 'created_at')),
                'updated_at': parse_date(safe_get(row, 'updated_at'))
            })
            count += 1
        except Exception as e:
            print(f"    Error importing developer {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} developers")

def import_residential_complexes_simple():
    """Import residential complexes with foreign key handling"""
    print("\n=== IMPORTING RESIDENTIAL COMPLEXES ===")
    
    files = glob.glob('attached_assets/residential_complexes*')
    if not files:
        print("No residential complex files found")
        return
    
    df = pd.read_excel(files[0])
    print(f"Found {len(df)} residential complexes to import")
    
    count = 0
    for _, row in df.iterrows():
        try:
            # Use basic fields that exist in current schema plus newly added ones
            db.session.execute(text("""
                INSERT INTO residential_complexes (
                    id, name, slug, developer_id, district_id, description, 
                    address, min_price, max_price, is_active, created_at, updated_at
                ) VALUES (
                    :id, :name, :slug, :developer_id, :district_id, :description,
                    :address, :min_price, :max_price, :is_active, :created_at, :updated_at
                ) ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    address = EXCLUDED.address
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_str(safe_get(row, 'name')),
                'slug': safe_str(safe_get(row, 'slug'), f"complex-{safe_get(row, 'id')}"),
                'developer_id': safe_get(row, 'developer_id') or 1,  # Use default if None
                'district_id': safe_get(row, 'district_id'),
                'description': safe_str(safe_get(row, 'description')),
                'address': safe_str(safe_get(row, 'address')),
                'min_price': safe_int(safe_get(row, 'min_price'), 0),
                'max_price': safe_int(safe_get(row, 'max_price'), 0),
                'is_active': safe_bool(safe_get(row, 'is_active'), True),
                'created_at': parse_date(safe_get(row, 'created_at')),
                'updated_at': parse_date(safe_get(row, 'updated_at'))
            })
            count += 1
        except Exception as e:
            print(f"    Error importing complex {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} residential complexes")

def import_blog_categories_simple():
    """Import blog categories"""
    print("\n=== IMPORTING BLOG CATEGORIES ===")
    
    files = glob.glob('attached_assets/blog_categories*')
    if not files:
        print("No blog category files found")
        return
    
    df = pd.read_excel(files[0])
    print(f"Found {len(df)} blog categories to import")
    
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO blog_categories (
                    id, name, slug, description, color, icon, sort_order, 
                    is_active, articles_count, views_count, created_at, updated_at
                ) VALUES (
                    :id, :name, :slug, :description, :color, :icon, :sort_order,
                    :is_active, :articles_count, :views_count, :created_at, :updated_at
                ) ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    color = EXCLUDED.color
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_str(safe_get(row, 'name')),
                'slug': safe_str(safe_get(row, 'slug'), f"category-{safe_get(row, 'id')}"),
                'description': safe_str(safe_get(row, 'description')),
                'color': safe_str(safe_get(row, 'color'), 'blue'),
                'icon': safe_str(safe_get(row, 'icon')),
                'sort_order': safe_int(safe_get(row, 'sort_order'), 0),
                'is_active': safe_bool(safe_get(row, 'is_active'), True),
                'articles_count': safe_int(safe_get(row, 'articles_count'), 0),
                'views_count': safe_int(safe_get(row, 'views_count'), 0),
                'created_at': parse_date(safe_get(row, 'created_at')),
                'updated_at': parse_date(safe_get(row, 'updated_at'))
            })
            count += 1
        except Exception as e:
            print(f"    Error importing blog category {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} blog categories")

def show_summary():
    """Show summary of imported data"""
    print("\n=== IMPORT SUMMARY ===")
    
    tables = ['users', 'districts', 'developers', 'residential_complexes', 'blog_categories']
    
    for table in tables:
        try:
            result = db.session.execute(text(f"SELECT COUNT(*) as count FROM {table}"))
            count = result.fetchone()[0]
            print(f"  {table}: {count} records")
        except Exception as e:
            print(f"  {table}: Error getting count - {e}")

if __name__ == '__main__':
    simple_data_import()