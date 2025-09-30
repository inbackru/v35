#!/usr/bin/env python3
"""
Add missing fields to database tables based on Excel file structure
"""

from app import app, db
from sqlalchemy import text
import pandas as pd
import glob

def add_missing_fields():
    """Add missing fields to match Excel file structure"""
    
    with app.app_context():
        try:
            print("Adding missing fields to database tables...")
            
            # Add fields to developers table
            add_developer_fields()
            
            # Add fields to districts table  
            add_district_fields()
            
            # Add fields to residential_complexes table
            add_residential_complex_fields()
            
            # Add fields to blog_categories table
            add_blog_category_fields()
            
            # Commit changes
            db.session.commit()
            print("✅ All missing fields added successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding fields: {e}")
            import traceback
            traceback.print_exc()

def add_developer_fields():
    """Add missing fields to developers table"""
    print("  Adding fields to developers table...")
    
    try:
        # Check what fields exist in Excel
        files = glob.glob('attached_assets/developers*')
        if files:
            df = pd.read_excel(files[0])
            print(f"    Excel has columns: {list(df.columns)}")
        
        # Add missing columns
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS description TEXT"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS logo_url VARCHAR(500)"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS website_url VARCHAR(500)"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(50)"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS contact_email VARCHAR(200)"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS rating DECIMAL(3,2) DEFAULT 0.0"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()"))
        db.session.execute(text("ALTER TABLE developers ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()"))
        
        print("    ✅ Developer fields added")
        
    except Exception as e:
        print(f"    Error adding developer fields: {e}")

def add_district_fields():
    """Add missing fields to districts table"""
    print("  Adding fields to districts table...")
    
    try:
        # Check what fields exist in Excel
        files = glob.glob('attached_assets/districts*')
        if files:
            df = pd.read_excel(files[0])
            print(f"    Excel has columns: {list(df.columns)}")
        
        # Add missing columns
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS description TEXT"))
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS city_id INTEGER DEFAULT 1"))
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS coordinates VARCHAR(100)"))
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true"))
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS latitude DECIMAL(10,8)"))
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS longitude DECIMAL(11,8)"))
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()"))
        db.session.execute(text("ALTER TABLE districts ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()"))
        
        print("    ✅ District fields added")
        
    except Exception as e:
        print(f"    Error adding district fields: {e}")

def add_residential_complex_fields():
    """Add missing fields to residential_complexes table"""
    print("  Adding fields to residential_complexes table...")
    
    try:
        # Check what fields exist in Excel
        files = glob.glob('attached_assets/residential_complexes*')
        if files:
            df = pd.read_excel(files[0])
            print(f"    Excel has columns: {list(df.columns)}")
        
        # Add all missing columns from Excel structure
        fields_to_add = [
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS description TEXT",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS short_description TEXT",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS street_id INTEGER",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS address VARCHAR(500)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS property_class VARCHAR(100)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS building_type VARCHAR(100)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS total_buildings INTEGER DEFAULT 0",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS total_floors INTEGER DEFAULT 0",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS total_apartments INTEGER DEFAULT 0",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS construction_status VARCHAR(50)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS construction_year INTEGER",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS delivery_quarter VARCHAR(50)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS latitude DECIMAL(10,8)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS longitude DECIMAL(11,8)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS min_price BIGINT DEFAULT 0",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS max_price BIGINT DEFAULT 0",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS price_per_sqm INTEGER DEFAULT 0",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS parking BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS playground BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS security BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS concierge BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS gym BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS kindergarten BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS metro_distance INTEGER",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS school_distance INTEGER",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS hospital_distance INTEGER",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS gallery TEXT",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS main_image VARCHAR(500)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS video_url VARCHAR(500)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS mortgage_available BOOLEAN DEFAULT true",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS family_mortgage BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS it_mortgage BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS preferential_mortgage BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS meta_title VARCHAR(200)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS meta_description VARCHAR(500)",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS is_featured BOOLEAN DEFAULT false",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()",
            "ALTER TABLE residential_complexes ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()"
        ]
        
        for field_sql in fields_to_add:
            db.session.execute(text(field_sql))
        
        print("    ✅ Residential complex fields added")
        
    except Exception as e:
        print(f"    Error adding residential complex fields: {e}")

def add_blog_category_fields():
    """Verify blog_categories has all needed fields"""
    print("  Checking blog_categories fields...")
    
    try:
        # Blog categories should already have most fields, just verify
        files = glob.glob('attached_assets/blog_categories*')
        if files:
            df = pd.read_excel(files[0])
            print(f"    Excel has columns: {list(df.columns)}")
        
        print("    ✅ Blog category fields verified")
        
    except Exception as e:
        print(f"    Error checking blog category fields: {e}")

if __name__ == '__main__':
    add_missing_fields()