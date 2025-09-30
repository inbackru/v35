#!/usr/bin/env python3
"""
Final data import script for all Excel files
"""
import pandas as pd
import numpy as np
from app import app, db
from sqlalchemy import text
import glob
from datetime import datetime

def safe_get(row, field, default=None):
    value = row.get(field, default)
    return default if pd.isna(value) else value

def safe_str(value, default=''):
    return default if pd.isna(value) or value is None else str(value)

def safe_int(value, default=0):
    if pd.isna(value) or value is None:
        return default
    try:
        return int(float(value))
    except:
        return default

def safe_bool(value, default=False):
    if pd.isna(value) or value is None:
        return default
    return bool(value) if isinstance(value, bool) else default

def parse_date(date_str):
    if pd.isna(date_str) or not date_str:
        return datetime.utcnow()
    try:
        if isinstance(date_str, str) and 'GMT' in date_str:
            date_part = date_str.split(' GMT')[0]
            return datetime.strptime(date_part, '%a %b %d %Y %H:%M:%S')
        return datetime.utcnow()
    except:
        return datetime.utcnow()

def final_import():
    with app.app_context():
        print("🔄 Starting final complete import...")
        
        try:
            # Import all tables systematically
            
            # 1. Users
            user_files = glob.glob('attached_assets/users*xlsx')
            if user_files:
                df = pd.read_excel(user_files[0])
                print(f"📝 Importing {len(df)} users...")
                for _, row in df.iterrows():
                    db.session.execute(text("""
                        INSERT INTO users (id, email, phone, full_name, password_hash, role, is_active, user_id, created_at) 
                        VALUES (:id, :email, :phone, :full_name, :password_hash, :role, :is_active, :user_id, :created_at)
                        ON CONFLICT (id) DO UPDATE SET 
                            email = EXCLUDED.email,
                            full_name = EXCLUDED.full_name,
                            phone = EXCLUDED.phone
                    """), {
                        'id': safe_get(row, 'id'),
                        'email': safe_str(safe_get(row, 'email')),
                        'phone': safe_str(safe_get(row, 'phone')),
                        'full_name': safe_str(safe_get(row, 'full_name')),
                        'password_hash': safe_str(safe_get(row, 'password_hash')),
                        'role': safe_str(safe_get(row, 'role'), 'buyer'),
                        'is_active': safe_bool(safe_get(row, 'is_active'), True),
                        'user_id': safe_str(safe_get(row, 'user_id')),
                        'created_at': parse_date(safe_get(row, 'created_at'))
                    })
                print(f"   ✅ Users imported")
            
            # 2. Districts  
            district_files = glob.glob('attached_assets/districts*xlsx')
            if district_files:
                df = pd.read_excel(district_files[0])
                print(f"🏘️ Importing {len(df)} districts...")
                for _, row in df.iterrows():
                    db.session.execute(text("""
                        INSERT INTO districts (id, name, slug, description, city_id, is_active) 
                        VALUES (:id, :name, :slug, :description, 1, true)
                        ON CONFLICT (id) DO UPDATE SET 
                            name = EXCLUDED.name,
                            description = EXCLUDED.description
                    """), {
                        'id': safe_get(row, 'id'),
                        'name': safe_str(safe_get(row, 'name')),
                        'slug': safe_str(safe_get(row, 'slug'), f"district-{safe_get(row, 'id')}"),
                        'description': safe_str(safe_get(row, 'description'))
                    })
                print(f"   ✅ Districts imported")
            
            # 3. Managers
            manager_files = glob.glob('attached_assets/managers*xlsx')
            if manager_files:
                df = pd.read_excel(manager_files[0])
                print(f"👥 Importing {len(df)} managers...")
                for _, row in df.iterrows():
                    db.session.execute(text("""
                        INSERT INTO managers (id, email, password_hash, first_name, last_name, phone, position, is_active, manager_id, created_at) 
                        VALUES (:id, :email, :password_hash, :first_name, :last_name, :phone, :position, :is_active, :manager_id, :created_at)
                        ON CONFLICT (id) DO UPDATE SET 
                            email = EXCLUDED.email,
                            first_name = EXCLUDED.first_name,
                            last_name = EXCLUDED.last_name
                    """), {
                        'id': safe_get(row, 'id'),
                        'email': safe_str(safe_get(row, 'email')),
                        'password_hash': safe_str(safe_get(row, 'password_hash')),
                        'first_name': safe_str(safe_get(row, 'first_name')),
                        'last_name': safe_str(safe_get(row, 'last_name')),
                        'phone': safe_str(safe_get(row, 'phone')),
                        'position': safe_str(safe_get(row, 'position'), 'Менеджер'),
                        'is_active': safe_bool(safe_get(row, 'is_active'), True),
                        'manager_id': safe_str(safe_get(row, 'manager_id')),
                        'created_at': parse_date(safe_get(row, 'created_at'))
                    })
                print(f"   ✅ Managers imported")
            
            # 4. Blog Categories
            blog_files = glob.glob('attached_assets/blog_categories*xlsx')
            if blog_files:
                df = pd.read_excel(blog_files[0])
                print(f"📝 Importing {len(df)} blog categories...")
                for _, row in df.iterrows():
                    db.session.execute(text("""
                        INSERT INTO blog_categories (id, name, slug, description, color, icon, sort_order, is_active, articles_count, views_count, created_at, updated_at) 
                        VALUES (:id, :name, :slug, :description, :color, :icon, :sort_order, :is_active, :articles_count, :views_count, :created_at, :updated_at)
                        ON CONFLICT (id) DO UPDATE SET 
                            name = EXCLUDED.name,
                            description = EXCLUDED.description
                    """), {
                        'id': safe_get(row, 'id'),
                        'name': safe_str(safe_get(row, 'name')),
                        'slug': safe_str(safe_get(row, 'slug'), f"category-{safe_get(row, 'id')}"),
                        'description': safe_str(safe_get(row, 'description')),
                        'color': safe_str(safe_get(row, 'color'), 'blue'),
                        'icon': safe_str(safe_get(row, 'icon'), 'fas fa-folder'),
                        'sort_order': safe_int(safe_get(row, 'sort_order'), 0),
                        'is_active': safe_bool(safe_get(row, 'is_active'), True),
                        'articles_count': safe_int(safe_get(row, 'articles_count'), 0),
                        'views_count': safe_int(safe_get(row, 'views_count'), 0),
                        'created_at': parse_date(safe_get(row, 'created_at')),
                        'updated_at': parse_date(safe_get(row, 'updated_at'))
                    })
                print(f"   ✅ Blog categories imported")
                
            # 5. Residential Complexes
            complex_files = glob.glob('attached_assets/residential_complexes*xlsx')
            if complex_files:
                df = pd.read_excel(complex_files[0])
                print(f"🏢 Importing {len(df)} residential complexes...")
                for _, row in df.iterrows():
                    db.session.execute(text("""
                        INSERT INTO residential_complexes (id, name, slug, developer_id, district_id) 
                        VALUES (:id, :name, :slug, :developer_id, :district_id)
                        ON CONFLICT (id) DO UPDATE SET 
                            name = EXCLUDED.name,
                            developer_id = EXCLUDED.developer_id,
                            district_id = EXCLUDED.district_id
                    """), {
                        'id': safe_get(row, 'id'),
                        'name': safe_str(safe_get(row, 'name')),
                        'slug': safe_str(safe_get(row, 'slug'), f"complex-{safe_get(row, 'id')}"),
                        'developer_id': safe_get(row, 'developer_id') or 1,
                        'district_id': safe_get(row, 'district_id')
                    })
                print(f"   ✅ Residential complexes imported")
                
            # 6. Import other important tables if they exist
            additional_tables = [
                ('collections', 'collections'),
                ('saved_searches', 'saved searches'),
                ('recommendations', 'recommendations'),
                ('favorite_properties', 'favorite properties'),
                ('cashback_applications', 'cashback applications')
            ]
            
            for table, display_name in additional_tables:
                files = glob.glob(f'attached_assets/{table}*xlsx')
                if files:
                    try:
                        df = pd.read_excel(files[0])
                        print(f"📊 Found {len(df)} {display_name} - basic structure import")
                        
                        # For now just track that we found the files
                        print(f"   📁 {display_name} file available for future import")
                    except Exception as e:
                        print(f"   ⚠️ Could not process {display_name}: {e}")
            
            # Commit all changes
            db.session.commit()
            print("\n✅ Final import completed successfully!")
            
            # Show final summary
            print("\n=== DATABASE SUMMARY ===")
            tables = ['users', 'districts', 'developers', 'residential_complexes', 'blog_categories', 'managers']
            for table in tables:
                result = db.session.execute(text(f'SELECT COUNT(*) FROM {table}'))
                count = result.fetchone()[0]
                print(f"  {table}: {count} records")
                
        except Exception as e:
            print(f"\n❌ Error during import: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    final_import()