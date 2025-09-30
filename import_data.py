#!/usr/bin/env python3
"""
Import data from Excel files to PostgreSQL database
"""

import pandas as pd
import os
from app import app, db
from models import *
import glob
from sqlalchemy import text

def import_excel_to_db():
    """Import all Excel files to database"""
    
    # Get all Excel files from attached_assets
    excel_files = glob.glob('attached_assets/*.xlsx')
    
    print(f"Found {len(excel_files)} Excel files to process")
    
    with app.app_context():
        # Clear existing data first (optional)
        # db.session.execute(text('TRUNCATE TABLE users CASCADE'))
        # db.session.commit()
        
        for file_path in excel_files:
            filename = os.path.basename(file_path)
            
            # Extract table name from filename
            if '(' in filename:
                table_name = filename.split('(')[0].strip()
            elif '_' in filename and filename.count('_') > 1:
                # Handle files like cashback_applications_1754939990699.xlsx
                parts = filename.replace('.xlsx', '').split('_')
                table_name = '_'.join(parts[:-1])  # Remove timestamp
            else:
                table_name = filename.replace('.xlsx', '').split('_')[0]
            
            print(f"\nProcessing: {filename} -> {table_name}")
            
            try:
                # Read Excel file
                df = pd.read_excel(file_path)
                print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
                print(f"  Columns: {list(df.columns)}")
                
                # Handle different table types
                if table_name == 'users':
                    import_users(df)
                elif table_name == 'managers':
                    import_managers(df)
                elif table_name == 'admins':
                    import_admins(df)
                elif table_name == 'developers':
                    import_developers(df)
                elif table_name == 'districts':
                    import_districts(df)
                elif table_name == 'residential_complexes':
                    import_residential_complexes(df)
                elif table_name == 'collections':
                    import_collections(df)
                elif table_name == 'collection_properties':
                    import_collection_properties(df)
                elif table_name == 'favorite_properties':
                    import_favorite_properties(df)
                elif table_name == 'recommendations':
                    import_recommendations(df)
                elif table_name == 'saved_searches':
                    import_saved_searches(df)
                elif table_name == 'manager_saved_searches':
                    import_manager_saved_searches(df)
                elif table_name == 'search_categories':
                    import_search_categories(df)
                elif table_name == 'sent_searches':
                    import_sent_searches(df)
                elif table_name == 'user_notifications':
                    import_user_notifications(df)
                elif table_name == 'blog_categories':
                    import_blog_categories(df)
                elif table_name == 'blog_articles':
                    import_blog_articles(df)
                elif table_name == 'blog_posts':
                    import_blog_posts(df)
                elif table_name == 'cashback_applications':
                    import_cashback_applications(df)
                elif table_name == 'cashback_payouts':
                    import_cashback_payouts(df)
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

def import_users(df):
    """Import users data"""
    print("  Importing users...")
    for _, row in df.iterrows():
        try:
            user = User(
                id=row.get('id'),
                username=row.get('username', ''),
                email=row.get('email', ''),
                password_hash=row.get('password_hash', ''),
                phone=row.get('phone', ''),
                full_name=row.get('full_name', ''),
                telegram_id=row.get('telegram_id'),
                whatsapp_phone=row.get('whatsapp_phone', ''),
                registration_date=pd.to_datetime(row.get('registration_date')) if row.get('registration_date') else None,
                last_active=pd.to_datetime(row.get('last_active')) if row.get('last_active') else None,
                email_notifications=row.get('email_notifications', True),
                telegram_notifications=row.get('telegram_notifications', False),
                whatsapp_notifications=row.get('whatsapp_notifications', False),
                is_verified=row.get('is_verified', False)
            )
            db.session.merge(user)
        except Exception as e:
            print(f"    Error importing user row: {e}")

def import_managers(df):
    """Import managers data"""
    print("  Importing managers...")
    for _, row in df.iterrows():
        try:
            manager = Manager(
                id=row.get('id'),
                username=row.get('username', ''),
                email=row.get('email', ''),
                password_hash=row.get('password_hash', ''),
                full_name=row.get('full_name', ''),
                phone=row.get('phone', ''),
                telegram_id=row.get('telegram_id'),
                whatsapp_phone=row.get('whatsapp_phone', ''),
                is_active=row.get('is_active', True),
                registration_date=pd.to_datetime(row.get('registration_date')) if row.get('registration_date') else None
            )
            db.session.merge(manager)
        except Exception as e:
            print(f"    Error importing manager row: {e}")

def import_admins(df):
    """Import admins data"""
    print("  Importing admins...")
    for _, row in df.iterrows():
        try:
            admin = Admin(
                id=row.get('id'),
                username=row.get('username', ''),
                email=row.get('email', ''),
                password_hash=row.get('password_hash', ''),
                full_name=row.get('full_name', ''),
                phone=row.get('phone', ''),
                is_active=row.get('is_active', True),
                created_date=pd.to_datetime(row.get('created_date')) if row.get('created_date') else None
            )
            db.session.merge(admin)
        except Exception as e:
            print(f"    Error importing admin row: {e}")

def import_developers(df):
    """Import developers data"""
    print("  Importing developers...")
    for _, row in df.iterrows():
        try:
            developer = Developer(
                id=row.get('id'),
                name=row.get('name', ''),
                description=row.get('description', ''),
                logo_url=row.get('logo_url', ''),
                website_url=row.get('website_url', ''),
                contact_phone=row.get('contact_phone', ''),
                contact_email=row.get('contact_email', ''),
                rating=row.get('rating', 0.0),
                is_active=row.get('is_active', True)
            )
            db.session.merge(developer)
        except Exception as e:
            print(f"    Error importing developer row: {e}")

def import_districts(df):
    """Import districts data"""
    print("  Importing districts...")
    for _, row in df.iterrows():
        try:
            district = District(
                id=row.get('id'),
                name=row.get('name', ''),
                description=row.get('description', ''),
                city_id=row.get('city_id', 1),  # Default to Krasnodar
                coordinates=row.get('coordinates', ''),
                is_active=row.get('is_active', True)
            )
            db.session.merge(district)
        except Exception as e:
            print(f"    Error importing district row: {e}")

def import_residential_complexes(df):
    """Import residential complexes data"""
    print("  Importing residential complexes...")
    for _, row in df.iterrows():
        try:
            complex_obj = ResidentialComplex(
                id=row.get('id'),
                name=row.get('name', ''),
                description=row.get('description', ''),
                developer_id=row.get('developer_id'),
                district_id=row.get('district_id'),
                address=row.get('address', ''),
                coordinates=row.get('coordinates', ''),
                total_buildings=row.get('total_buildings', 0),
                total_apartments=row.get('total_apartments', 0),
                construction_status=row.get('construction_status', ''),
                completion_date=pd.to_datetime(row.get('completion_date')) if row.get('completion_date') else None,
                min_price=row.get('min_price', 0),
                max_price=row.get('max_price', 0),
                is_active=row.get('is_active', True)
            )
            db.session.merge(complex_obj)
        except Exception as e:
            print(f"    Error importing residential complex row: {e}")

def import_collections(df):
    """Import collections data"""
    print("  Importing collections...")
    for _, row in df.iterrows():
        try:
            collection = Collection(
                id=row.get('id'),
                name=row.get('name', ''),
                description=row.get('description', ''),
                manager_id=row.get('manager_id'),
                created_date=pd.to_datetime(row.get('created_date')) if row.get('created_date') else None,
                is_active=row.get('is_active', True)
            )
            db.session.merge(collection)
        except Exception as e:
            print(f"    Error importing collection row: {e}")

def import_collection_properties(df):
    """Import collection properties data"""
    print("  Importing collection properties...")
    for _, row in df.iterrows():
        try:
            collection_property = CollectionProperty(
                id=row.get('id'),
                collection_id=row.get('collection_id'),
                property_id=row.get('property_id'),
                added_date=pd.to_datetime(row.get('added_date')) if row.get('added_date') else None
            )
            db.session.merge(collection_property)
        except Exception as e:
            print(f"    Error importing collection property row: {e}")

def import_favorite_properties(df):
    """Import favorite properties data"""
    print("  Importing favorite properties...")
    for _, row in df.iterrows():
        try:
            favorite = FavoriteProperty(
                id=row.get('id'),
                user_id=row.get('user_id'),
                property_id=row.get('property_id'),
                added_date=pd.to_datetime(row.get('added_date')) if row.get('added_date') else None
            )
            db.session.merge(favorite)
        except Exception as e:
            print(f"    Error importing favorite property row: {e}")

def import_recommendations(df):
    """Import recommendations data"""
    print("  Importing recommendations...")
    for _, row in df.iterrows():
        try:
            recommendation = Recommendation(
                id=row.get('id'),
                user_id=row.get('user_id'),
                manager_id=row.get('manager_id'),
                property_id=row.get('property_id'),
                title=row.get('title', ''),
                message=row.get('message', ''),
                category_id=row.get('category_id'),
                is_sent=row.get('is_sent', False),
                sent_date=pd.to_datetime(row.get('sent_date')) if row.get('sent_date') else None,
                created_date=pd.to_datetime(row.get('created_date')) if row.get('created_date') else None
            )
            db.session.merge(recommendation)
        except Exception as e:
            print(f"    Error importing recommendation row: {e}")

def import_saved_searches(df):
    """Import saved searches data"""
    print("  Importing saved searches...")
    for _, row in df.iterrows():
        try:
            saved_search = SavedSearch(
                id=row.get('id'),
                user_id=row.get('user_id'),
                search_name=row.get('search_name', ''),
                search_criteria=row.get('search_criteria', ''),
                created_date=pd.to_datetime(row.get('created_date')) if row.get('created_date') else None,
                is_active=row.get('is_active', True)
            )
            db.session.merge(saved_search)
        except Exception as e:
            print(f"    Error importing saved search row: {e}")

def import_manager_saved_searches(df):
    """Import manager saved searches data"""
    print("  Importing manager saved searches...")
    for _, row in df.iterrows():
        try:
            manager_search = ManagerSavedSearch(
                id=row.get('id'),
                manager_id=row.get('manager_id'),
                search_name=row.get('search_name', ''),
                search_criteria=row.get('search_criteria', ''),
                created_date=pd.to_datetime(row.get('created_date')) if row.get('created_date') else None,
                is_active=row.get('is_active', True)
            )
            db.session.merge(manager_search)
        except Exception as e:
            print(f"    Error importing manager saved search row: {e}")

def import_search_categories(df):
    """Import search categories data"""
    print("  Importing search categories...")
    for _, row in df.iterrows():
        try:
            category = SearchCategory(
                id=row.get('id'),
                name=row.get('name', ''),
                description=row.get('description', ''),
                is_active=row.get('is_active', True)
            )
            db.session.merge(category)
        except Exception as e:
            print(f"    Error importing search category row: {e}")

def import_sent_searches(df):
    """Import sent searches data"""
    print("  Importing sent searches...")
    for _, row in df.iterrows():
        try:
            sent_search = SentSearch(
                id=row.get('id'),
                user_id=row.get('user_id'),
                manager_id=row.get('manager_id'),
                search_criteria=row.get('search_criteria', ''),
                results_count=row.get('results_count', 0),
                sent_date=pd.to_datetime(row.get('sent_date')) if row.get('sent_date') else None
            )
            db.session.merge(sent_search)
        except Exception as e:
            print(f"    Error importing sent search row: {e}")

def import_user_notifications(df):
    """Import user notifications data"""
    print("  Importing user notifications...")
    for _, row in df.iterrows():
        try:
            notification = UserNotification(
                id=row.get('id'),
                user_id=row.get('user_id'),
                title=row.get('title', ''),
                message=row.get('message', ''),
                notification_type=row.get('notification_type', 'info'),
                is_read=row.get('is_read', False),
                created_date=pd.to_datetime(row.get('created_date')) if row.get('created_date') else None
            )
            db.session.merge(notification)
        except Exception as e:
            print(f"    Error importing user notification row: {e}")

def import_blog_categories(df):
    """Import blog categories data"""
    print("  Importing blog categories...")
    for _, row in df.iterrows():
        try:
            category = BlogCategory(
                id=row.get('id'),
                name=row.get('name', ''),
                description=row.get('description', ''),
                is_active=row.get('is_active', True)
            )
            db.session.merge(category)
        except Exception as e:
            print(f"    Error importing blog category row: {e}")

def import_blog_articles(df):
    """Import blog articles data"""
    print("  Importing blog articles...")
    for _, row in df.iterrows():
        try:
            article = BlogArticle(
                id=row.get('id'),
                title=row.get('title', ''),
                content=row.get('content', ''),
                category_id=row.get('category_id'),
                author_id=row.get('author_id'),
                published_date=pd.to_datetime(row.get('published_date')) if row.get('published_date') else None,
                is_published=row.get('is_published', False)
            )
            db.session.merge(article)
        except Exception as e:
            print(f"    Error importing blog article row: {e}")

def import_blog_posts(df):
    """Import blog posts data"""
    print("  Importing blog posts...")
    for _, row in df.iterrows():
        try:
            post = BlogPost(
                id=row.get('id'),
                title=row.get('title', ''),
                content=row.get('content', ''),
                author_id=row.get('author_id'),
                category_id=row.get('category_id'),
                published_date=pd.to_datetime(row.get('published_date')) if row.get('published_date') else None,
                is_published=row.get('is_published', False),
                views_count=row.get('views_count', 0)
            )
            db.session.merge(post)
        except Exception as e:
            print(f"    Error importing blog post row: {e}")

def import_cashback_applications(df):
    """Import cashback applications data"""
    print("  Importing cashback applications...")
    for _, row in df.iterrows():
        try:
            application = CashbackApplication(
                id=row.get('id'),
                user_id=row.get('user_id'),
                property_id=row.get('property_id'),
                cashback_amount=row.get('cashback_amount', 0),
                status=row.get('status', 'pending'),
                application_date=pd.to_datetime(row.get('application_date')) if row.get('application_date') else None,
                approval_date=pd.to_datetime(row.get('approval_date')) if row.get('approval_date') else None
            )
            db.session.merge(application)
        except Exception as e:
            print(f"    Error importing cashback application row: {e}")

def import_cashback_payouts(df):
    """Import cashback payouts data"""
    print("  Importing cashback payouts...")
    for _, row in df.iterrows():
        try:
            payout = CashbackPayout(
                id=row.get('id'),
                application_id=row.get('application_id'),
                amount=row.get('amount', 0),
                payout_date=pd.to_datetime(row.get('payout_date')) if row.get('payout_date') else None,
                payment_method=row.get('payment_method', ''),
                status=row.get('status', 'pending')
            )
            db.session.merge(payout)
        except Exception as e:
            print(f"    Error importing cashback payout row: {e}")

if __name__ == '__main__':
    import_excel_to_db()