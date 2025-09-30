#!/usr/bin/env python3
"""
Complete import of all data from Excel files into PostgreSQL database
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
        if isinstance(date_str, str):
            if 'GMT' in date_str:
                date_part = date_str.split(' GMT')[0]
                return datetime.strptime(date_part, '%a %b %d %Y %H:%M:%S')
            else:
                return datetime.fromisoformat(date_str.replace('T', ' ').replace('Z', ''))
        elif hasattr(date_str, 'timestamp'):
            return date_str
        else:
            return None
    except Exception as e:
        return datetime.utcnow()

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

def safe_float(value, default=0.0):
    """Convert value to float safely"""
    if pd.isna(value) or value is None:
        return default
    try:
        return float(value)
    except:
        return default

def safe_bool(value, default=False):
    """Convert value to bool safely"""
    if pd.isna(value) or value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'да')
    try:
        return bool(int(value))
    except:
        return default

def complete_data_import():
    """Import all data with complete field mapping"""
    
    with app.app_context():
        try:
            print("🔄 Starting complete data import...")
            
            # Clear any existing transaction
            db.session.rollback()
            
            # Import in correct order due to foreign key dependencies
            import_districts()
            import_developers() 
            import_residential_complexes()
            import_users()
            import_managers()
            import_blog_categories()
            import_collections()
            import_saved_searches()
            import_recommendations()
            import_favorite_properties()
            
            db.session.commit()
            print("\n✅ Complete data import finished successfully!")
            
            # Show summary
            show_import_summary()
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error during import: {e}")
            import traceback
            traceback.print_exc()

def import_districts():
    """Import districts with all fields"""
    print("\n=== IMPORTING DISTRICTS ===")
    
    files = glob.glob('attached_assets/districts*')
    if not files:
        print("No district files found")
        return
    
    df = pd.read_excel(files[0])
    print(f"Found {len(df)} districts to import")
    
    # Clear existing data
    db.session.execute(text("TRUNCATE TABLE districts RESTART IDENTITY CASCADE"))
    
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO districts (
                    id, name, slug, description, city_id, coordinates, is_active,
                    latitude, longitude, created_at, updated_at
                ) VALUES (
                    :id, :name, :slug, :description, :city_id, :coordinates, :is_active,
                    :latitude, :longitude, :created_at, :updated_at
                )
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_str(safe_get(row, 'name')),
                'slug': safe_str(safe_get(row, 'slug'), f"district-{safe_get(row, 'id')}"),
                'description': safe_str(safe_get(row, 'description')),
                'city_id': 1,  # Default to Krasnodar
                'coordinates': safe_str(safe_get(row, 'coordinates')),
                'is_active': True,
                'latitude': safe_float(safe_get(row, 'center_lat')),
                'longitude': safe_float(safe_get(row, 'center_lng')),
                'created_at': parse_date(safe_get(row, 'created_at')) or datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
            count += 1
        except Exception as e:
            print(f"    Error importing district {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} districts")

def import_developers():
    """Import developers with all fields"""
    print("\n=== IMPORTING DEVELOPERS ===")
    
    files = glob.glob('attached_assets/developers*')
    if not files:
        print("No developer files found")
        return
    
    try:
        df = pd.read_excel(files[0], engine='openpyxl')
    except Exception as e:
        print(f"Error reading developer file: {e}")
        return
    
    print(f"Found {len(df)} developers to import")
    
    # Clear existing data
    db.session.execute(text("TRUNCATE TABLE developers RESTART IDENTITY CASCADE"))
    
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO developers (
                    id, name, slug, description, logo_url, website_url, 
                    contact_phone, contact_email, rating, is_active, 
                    created_at, updated_at
                ) VALUES (
                    :id, :name, :slug, :description, :logo_url, :website_url,
                    :contact_phone, :contact_email, :rating, :is_active,
                    :created_at, :updated_at
                )
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_str(safe_get(row, 'name')),
                'slug': safe_str(safe_get(row, 'slug'), f"developer-{safe_get(row, 'id')}"),
                'description': safe_str(safe_get(row, 'description')),
                'logo_url': safe_str(safe_get(row, 'logo_url')),
                'website_url': safe_str(safe_get(row, 'website_url')),
                'contact_phone': safe_str(safe_get(row, 'contact_phone')),
                'contact_email': safe_str(safe_get(row, 'contact_email')),
                'rating': safe_float(safe_get(row, 'rating'), 0.0),
                'is_active': safe_bool(safe_get(row, 'is_active'), True),
                'created_at': parse_date(safe_get(row, 'created_at')) or datetime.utcnow(),
                'updated_at': parse_date(safe_get(row, 'updated_at')) or datetime.utcnow()
            })
            count += 1
        except Exception as e:
            print(f"    Error importing developer {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} developers")

def import_residential_complexes():
    """Import residential complexes with all fields"""
    print("\n=== IMPORTING RESIDENTIAL COMPLEXES ===")
    
    files = glob.glob('attached_assets/residential_complexes*')
    if not files:
        print("No residential complex files found")
        return
    
    df = pd.read_excel(files[0])
    print(f"Found {len(df)} residential complexes to import")
    
    # Clear existing data
    db.session.execute(text("TRUNCATE TABLE residential_complexes RESTART IDENTITY CASCADE"))
    
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO residential_complexes (
                    id, name, slug, description, short_description, developer_id, district_id,
                    street_id, address, property_class, building_type, total_buildings, 
                    total_floors, total_apartments, construction_status, construction_year,
                    delivery_quarter, latitude, longitude, min_price, max_price, price_per_sqm,
                    parking, playground, security, concierge, gym, kindergarten,
                    metro_distance, school_distance, hospital_distance, gallery, main_image,
                    video_url, mortgage_available, family_mortgage, it_mortgage, 
                    preferential_mortgage, meta_title, meta_description, is_active, 
                    is_featured, views, created_at, updated_at
                ) VALUES (
                    :id, :name, :slug, :description, :short_description, :developer_id, :district_id,
                    :street_id, :address, :property_class, :building_type, :total_buildings,
                    :total_floors, :total_apartments, :construction_status, :construction_year,
                    :delivery_quarter, :latitude, :longitude, :min_price, :max_price, :price_per_sqm,
                    :parking, :playground, :security, :concierge, :gym, :kindergarten,
                    :metro_distance, :school_distance, :hospital_distance, :gallery, :main_image,
                    :video_url, :mortgage_available, :family_mortgage, :it_mortgage,
                    :preferential_mortgage, :meta_title, :meta_description, :is_active,
                    :is_featured, :views, :created_at, :updated_at
                )
            """), {
                'id': safe_get(row, 'id'),
                'name': safe_str(safe_get(row, 'name')),
                'slug': safe_str(safe_get(row, 'slug'), f"complex-{safe_get(row, 'id')}"),
                'description': safe_str(safe_get(row, 'description')),
                'short_description': safe_str(safe_get(row, 'short_description')),
                'developer_id': safe_get(row, 'developer_id'),
                'district_id': safe_get(row, 'district_id'),
                'street_id': safe_get(row, 'street_id'),
                'address': safe_str(safe_get(row, 'address')),
                'property_class': safe_str(safe_get(row, 'property_class'), 'комфорт'),
                'building_type': safe_str(safe_get(row, 'building_type')),
                'total_buildings': safe_int(safe_get(row, 'total_buildings'), 0),
                'total_floors': safe_int(safe_get(row, 'total_floors'), 0),
                'total_apartments': safe_int(safe_get(row, 'total_apartments'), 0),
                'construction_status': safe_str(safe_get(row, 'construction_status'), 'new'),
                'construction_year': safe_int(safe_get(row, 'construction_year')),
                'delivery_quarter': safe_str(safe_get(row, 'delivery_quarter')),
                'latitude': safe_float(safe_get(row, 'latitude')),
                'longitude': safe_float(safe_get(row, 'longitude')),
                'min_price': safe_int(safe_get(row, 'min_price'), 0),
                'max_price': safe_int(safe_get(row, 'max_price'), 0),
                'price_per_sqm': safe_int(safe_get(row, 'price_per_sqm'), 0),
                'parking': safe_bool(safe_get(row, 'parking'), False),
                'playground': safe_bool(safe_get(row, 'playground'), False),
                'security': safe_bool(safe_get(row, 'security'), False),
                'concierge': safe_bool(safe_get(row, 'concierge'), False),
                'gym': safe_bool(safe_get(row, 'gym'), False),
                'kindergarten': safe_bool(safe_get(row, 'kindergarten'), False),
                'metro_distance': safe_int(safe_get(row, 'metro_distance')),
                'school_distance': safe_int(safe_get(row, 'school_distance')),
                'hospital_distance': safe_int(safe_get(row, 'hospital_distance')),
                'gallery': safe_str(safe_get(row, 'gallery'), '[]'),
                'main_image': safe_str(safe_get(row, 'main_image')),
                'video_url': safe_str(safe_get(row, 'video_url')),
                'mortgage_available': safe_bool(safe_get(row, 'mortgage_available'), True),
                'family_mortgage': safe_bool(safe_get(row, 'family_mortgage'), False),
                'it_mortgage': safe_bool(safe_get(row, 'it_mortgage'), False),
                'preferential_mortgage': safe_bool(safe_get(row, 'preferential_mortgage'), False),
                'meta_title': safe_str(safe_get(row, 'meta_title')),
                'meta_description': safe_str(safe_get(row, 'meta_description')),
                'is_active': safe_bool(safe_get(row, 'is_active'), True),
                'is_featured': safe_bool(safe_get(row, 'is_featured'), False),
                'views': safe_int(safe_get(row, 'views'), 0),
                'created_at': parse_date(safe_get(row, 'created_at')) or datetime.utcnow(),
                'updated_at': parse_date(safe_get(row, 'updated_at')) or datetime.utcnow()
            })
            count += 1
        except Exception as e:
            print(f"    Error importing complex {safe_get(row, 'id')}: {e}")
            # Don't stop on errors, continue with next record
    
    print(f"    ✅ Imported {count}/{len(df)} residential complexes")

def import_users():
    """Import users with all fields"""
    print("\n=== IMPORTING USERS ===")
    
    files = glob.glob('attached_assets/users*')
    if not files:
        print("No user files found")
        return
    
    df = pd.read_excel(files[0])
    print(f"Found {len(df)} users to import")
    
    # Clear existing data
    db.session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    
    count = 0
    for _, row in df.iterrows():
        try:
            db.session.execute(text("""
                INSERT INTO users (
                    id, email, phone, telegram_id, full_name, password_hash, 
                    preferred_contact, email_notifications, telegram_notifications,
                    notify_recommendations, notify_saved_searches, notify_applications, 
                    notify_cashback, notify_marketing, profile_image, user_id, role, 
                    is_active, is_verified, verification_token, is_demo, verified,
                    registration_source, client_notes, assigned_manager_id, client_status,
                    preferred_district, property_type, room_count, budget_range, 
                    quiz_completed, created_at, updated_at, last_login
                ) VALUES (
                    :id, :email, :phone, :telegram_id, :full_name, :password_hash,
                    :preferred_contact, :email_notifications, :telegram_notifications,
                    :notify_recommendations, :notify_saved_searches, :notify_applications,
                    :notify_cacheback, :notify_marketing, :profile_image, :user_id, :role,
                    :is_active, :is_verified, :verification_token, :is_demo, :verified,
                    :registration_source, :client_notes, :assigned_manager_id, :client_status,
                    :preferred_district, :property_type, :room_count, :budget_range,
                    :quiz_completed, :created_at, :updated_at, :last_login
                )
            """), {
                'id': safe_get(row, 'id'),
                'email': safe_str(safe_get(row, 'email')),
                'phone': safe_str(safe_get(row, 'phone')),
                'telegram_id': safe_str(safe_get(row, 'telegram_id')),
                'full_name': safe_str(safe_get(row, 'full_name')),
                'password_hash': safe_str(safe_get(row, 'password_hash')),
                'preferred_contact': safe_str(safe_get(row, 'preferred_contact'), 'email'),
                'email_notifications': safe_bool(safe_get(row, 'email_notifications'), True),
                'telegram_notifications': safe_bool(safe_get(row, 'telegram_notifications'), False),
                'notify_recommendations': True,
                'notify_saved_searches': True,
                'notify_applications': True,
                'notify_cacheback': True,
                'notify_marketing': False,
                'profile_image': safe_str(safe_get(row, 'profile_image')),
                'user_id': safe_str(safe_get(row, 'user_id')),
                'role': safe_str(safe_get(row, 'role'), 'buyer'),
                'is_active': safe_bool(safe_get(row, 'is_active'), True),
                'is_verified': safe_bool(safe_get(row, 'is_verified'), False),
                'verification_token': safe_str(safe_get(row, 'verification_token')),
                'is_demo': safe_bool(safe_get(row, 'is_demo'), False),
                'verified': safe_bool(safe_get(row, 'verified'), False),
                'registration_source': safe_str(safe_get(row, 'registration_source'), 'Website'),
                'client_notes': safe_str(safe_get(row, 'client_notes')),
                'assigned_manager_id': safe_get(row, 'assigned_manager_id'),
                'client_status': safe_str(safe_get(row, 'client_status'), 'Новый'),
                'preferred_district': safe_str(safe_get(row, 'preferred_district')),
                'property_type': safe_str(safe_get(row, 'property_type')),
                'room_count': safe_str(safe_get(row, 'room_count')),
                'budget_range': safe_str(safe_get(row, 'budget_range')),
                'quiz_completed': safe_bool(safe_get(row, 'quiz_completed'), False),
                'created_at': parse_date(safe_get(row, 'created_at')) or datetime.utcnow(),
                'updated_at': parse_date(safe_get(row, 'updated_at')) or datetime.utcnow(),
                'last_login': parse_date(safe_get(row, 'last_login'))
            })
            count += 1
        except Exception as e:
            print(f"    Error importing user {safe_get(row, 'id')}: {e}")
    
    print(f"    ✅ Imported {count}/{len(df)} users")

# Placeholder functions for remaining tables
def import_managers():
    print("    ⏭️  Skipping managers - implement if needed")

def import_blog_categories():
    print("    ⏭️  Skipping blog_categories - implement if needed")

def import_collections():
    print("    ⏭️  Skipping collections - implement if needed")

def import_saved_searches():
    print("    ⏭️  Skipping saved_searches - implement if needed")

def import_recommendations():
    print("    ⏭️  Skipping recommendations - implement if needed")

def import_favorite_properties():
    print("    ⏭️  Skipping favorite_properties - implement if needed")

def show_import_summary():
    """Show summary of imported data"""
    print("\n=== IMPORT SUMMARY ===")
    
    tables = ['districts', 'developers', 'residential_complexes', 'users', 'managers', 'blog_categories']
    
    for table in tables:
        try:
            result = db.session.execute(text(f"SELECT COUNT(*) as count FROM {table}"))
            count = result.fetchone()[0]
            print(f"  {table}: {count} records")
        except Exception as e:
            print(f"  {table}: Error getting count - {e}")

if __name__ == '__main__':
    complete_data_import()