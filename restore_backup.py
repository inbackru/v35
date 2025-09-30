#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт восстановления данных InBack из Excel бэкапов
Автоматически восстанавливает все данные из attached_assets
"""

import os
import sys
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('restore_backup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BackupRestorer:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        if not self.db_url:
            raise ValueError("DATABASE_URL не найден в переменных окружения")
        
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'total_records': 0,
            'restored_records': 0,
            'errors': 0,
            'skipped': 0
        }
        
    def get_latest_file(self, pattern):
        """Получить самый свежий файл по паттерну"""
        files = []
        for file in os.listdir('attached_assets'):
            if file.startswith(pattern) and file.endswith('.xlsx'):
                # Извлекаем timestamp из имени файла
                try:
                    timestamp = file.split('_')[-1].replace('.xlsx', '')
                    files.append((int(timestamp), file))
                except:
                    files.append((0, file))
        
        if not files:
            logger.warning(f"Файлы с паттерном '{pattern}' не найдены")
            return None
            
        # Сортируем по timestamp и берем самый новый
        files.sort(reverse=True)
        latest_file = files[0][1]
        logger.info(f"Выбран файл: {latest_file}")
        return latest_file

    def clear_table(self, table_name):
        """Очистить таблицу перед загрузкой"""
        try:
            with self.engine.connect() as conn:
                # Отключаем проверки внешних ключей
                conn.execute(text("SET session_replication_role = replica;"))
                conn.execute(text(f"DELETE FROM {table_name}"))
                conn.execute(text("SET session_replication_role = DEFAULT;"))
                conn.commit()
                logger.info(f"Таблица {table_name} очищена")
        except Exception as e:
            logger.error(f"Ошибка очистки таблицы {table_name}: {e}")

    def restore_users(self):
        """Восстановить пользователей"""
        logger.info("=== ВОССТАНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ===")
        
        file = self.get_latest_file('users')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} пользователей в {file}")
            
            # Очищаем таблицу
            self.clear_table('users')
            
            # Восстанавливаем данные
            restored = 0
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        # Подготавливаем SQL запрос
                        insert_sql = text("""
                            INSERT INTO users (
                                id, email, phone, telegram_id, full_name, password_hash,
                                temp_password_hash, created_by_admin, preferred_contact,
                                email_notifications, telegram_notifications, notify_recommendations,
                                notify_saved_searches, notify_applications, notify_cashback,
                                notify_marketing, profile_image, user_id, role, is_active,
                                is_verified, verification_token, is_demo, verified,
                                registration_source, client_notes, assigned_manager_id,
                                client_status, preferred_district, property_type, room_count,
                                budget_range, quiz_completed, created_at, updated_at, last_login
                            ) VALUES (
                                :id, :email, :phone, :telegram_id, :full_name, :password_hash,
                                :temp_password_hash, :created_by_admin, :preferred_contact,
                                :email_notifications, :telegram_notifications, :notify_recommendations,
                                :notify_saved_searches, :notify_applications, :notify_cashback,
                                :notify_marketing, :profile_image, :user_id, :role, :is_active,
                                :is_verified, :verification_token, :is_demo, :verified,
                                :registration_source, :client_notes, :assigned_manager_id,
                                :client_status, :preferred_district, :property_type, :room_count,
                                :budget_range, :quiz_completed, :created_at, :updated_at, :last_login
                            )
                        """)
                        
                        # Подготавливаем параметры
                        params = {}
                        for col in df.columns:
                            value = row[col]
                            if pd.isna(value):
                                params[col] = None
                            elif isinstance(value, str) and 'GMT' in value:
                                # Парсим дату
                                try:
                                    # Парсим формат: 'Wed Aug 27 2025 10:37:41 GMT+0300 (Москва, стандартное время)'
                                    date_part = value.split(' GMT')[0]
                                    params[col] = pd.to_datetime(date_part).strftime('%Y-%m-%d %H:%M:%S')
                                except:
                                    params[col] = None
                            else:
                                params[col] = value
                        
                        conn.execute(insert_sql, params)
                        restored += 1
                        
                    except Exception as e:
                        logger.error(f"Ошибка восстановления пользователя {row.get('id', 'unknown')}: {e}")
                        self.stats['errors'] += 1
                
                conn.commit()
                
            logger.info(f"Восстановлено {restored} пользователей")
            self.stats['restored_records'] += restored
            
        except Exception as e:
            logger.error(f"Ошибка восстановления пользователей: {e}")
            self.stats['errors'] += 1

    def restore_managers(self):
        """Восстановить менеджеров"""
        logger.info("=== ВОССТАНОВЛЕНИЕ МЕНЕДЖЕРОВ ===")
        
        file = self.get_latest_file('managers')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} менеджеров в {file}")
            
            # Очищаем таблицу
            self.clear_table('managers')
            
            # Восстанавливаем данные
            restored = 0
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        insert_sql = text("""
                            INSERT INTO managers (
                                id, email, password_hash, first_name, last_name, phone,
                                position, can_approve_cashback, can_manage_documents,
                                can_create_collections, max_cashback_approval, is_active,
                                profile_image, manager_id, created_at, updated_at, last_login
                            ) VALUES (
                                :id, :email, :password_hash, :first_name, :last_name, :phone,
                                :position, :can_approve_cashback, :can_manage_documents,
                                :can_create_collections, :max_cashback_approval, :is_active,
                                :profile_image, :manager_id, :created_at, :updated_at, :last_login
                            )
                        """)
                        
                        params = {}
                        for col in df.columns:
                            value = row[col]
                            if pd.isna(value):
                                params[col] = None
                            elif isinstance(value, str) and 'GMT' in value:
                                try:
                                    date_part = value.split(' GMT')[0]
                                    params[col] = pd.to_datetime(date_part).strftime('%Y-%m-%d %H:%M:%S')
                                except:
                                    params[col] = None
                            else:
                                params[col] = value
                        
                        conn.execute(insert_sql, params)
                        restored += 1
                        
                    except Exception as e:
                        logger.error(f"Ошибка восстановления менеджера {row.get('id', 'unknown')}: {e}")
                        self.stats['errors'] += 1
                
                conn.commit()
                
            logger.info(f"Восстановлено {restored} менеджеров")
            self.stats['restored_records'] += restored
            
        except Exception as e:
            logger.error(f"Ошибка восстановления менеджеров: {e}")
            self.stats['errors'] += 1

    def restore_developers(self):
        """Восстановить застройщиков"""
        logger.info("=== ВОССТАНОВЛЕНИЕ ЗАСТРОЙЩИКОВ ===")
        
        file = self.get_latest_file('developers')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} застройщиков в {file}")
            
            # Очищаем таблицу
            self.clear_table('developers')
            
            # Восстанавливаем данные
            restored = 0
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        # Создаем динамический SQL на основе доступных колонок
                        available_cols = [col for col in row.index if not pd.isna(row[col]) or col in ['id', 'name', 'slug']]
                        
                        cols_str = ', '.join(available_cols)
                        values_str = ', '.join([f':{col}' for col in available_cols])
                        
                        insert_sql = text(f"""
                            INSERT INTO developers ({cols_str})
                            VALUES ({values_str})
                        """)
                        
                        params = {}
                        for col in available_cols:
                            value = row[col]
                            if pd.isna(value):
                                params[col] = None
                            elif isinstance(value, str) and 'GMT' in value:
                                try:
                                    date_part = value.split(' GMT')[0]
                                    params[col] = pd.to_datetime(date_part).strftime('%Y-%m-%d %H:%M:%S')
                                except:
                                    params[col] = None
                            else:
                                params[col] = value
                        
                        conn.execute(insert_sql, params)
                        restored += 1
                        
                    except Exception as e:
                        logger.error(f"Ошибка восстановления застройщика {row.get('id', 'unknown')}: {e}")
                        self.stats['errors'] += 1
                
                conn.commit()
                
            logger.info(f"Восстановлено {restored} застройщиков")
            self.stats['restored_records'] += restored
            
        except Exception as e:
            logger.error(f"Ошибка восстановления застройщиков: {e}")
            self.stats['errors'] += 1

    def restore_districts(self):
        """Восстановить районы"""
        logger.info("=== ВОССТАНОВЛЕНИЕ РАЙОНОВ ===")
        
        file = self.get_latest_file('districts')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} районов в {file}")
            
            # Восстанавливаем данные
            restored = 0
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        # Проверяем существует ли район
                        check_sql = text("SELECT id FROM districts WHERE id = :id")
                        result = conn.execute(check_sql, {'id': row['id']}).fetchone()
                        
                        if result:
                            # Обновляем существующий
                            update_sql = text("""
                                UPDATE districts SET name = :name, slug = :slug WHERE id = :id
                            """)
                            conn.execute(update_sql, {
                                'id': row['id'],
                                'name': row['name'],
                                'slug': row['slug']
                            })
                        else:
                            # Создаем новый
                            insert_sql = text("""
                                INSERT INTO districts (id, name, slug) VALUES (:id, :name, :slug)
                            """)
                            conn.execute(insert_sql, {
                                'id': row['id'],
                                'name': row['name'], 
                                'slug': row['slug']
                            })
                        
                        restored += 1
                        
                    except Exception as e:
                        logger.error(f"Ошибка восстановления района {row.get('id', 'unknown')}: {e}")
                        self.stats['errors'] += 1
                
                conn.commit()
                
            logger.info(f"Восстановлено {restored} районов")
            self.stats['restored_records'] += restored
            
        except Exception as e:
            logger.error(f"Ошибка восстановления районов: {e}")
            self.stats['errors'] += 1

    def restore_excel_properties(self):
        """Восстановить свойства недвижимости"""
        logger.info("=== ВОССТАНОВЛЕНИЕ НЕДВИЖИМОСТИ ===")
        
        file = self.get_latest_file('excel_properties')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} записей недвижимости в {file}")
            
            # Очищаем таблицу
            self.clear_table('excel_properties')
            
            # Восстанавливаем данные порциями по 50 записей
            restored = 0
            chunk_size = 50
            
            with self.engine.connect() as conn:
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i + chunk_size]
                    logger.info(f"Обрабатываем записи {i+1}-{min(i+chunk_size, len(df))}")
                    
                    for _, row in chunk.iterrows():
                        try:
                            # Подготавливаем только непустые колонки
                            non_null_cols = []
                            params = {}
                            
                            for col in df.columns:
                                value = row[col]
                                if not pd.isna(value):
                                    non_null_cols.append(col)
                                    params[col] = value
                                    
                            if non_null_cols:
                                cols_str = ', '.join(non_null_cols)
                                values_str = ', '.join([f':{col}' for col in non_null_cols])
                                
                                insert_sql = text(f"""
                                    INSERT INTO excel_properties ({cols_str})
                                    VALUES ({values_str})
                                """)
                                
                                conn.execute(insert_sql, params)
                                restored += 1
                            
                        except Exception as e:
                            logger.error(f"Ошибка восстановления недвижимости {row.get('inner_id', 'unknown')}: {e}")
                            self.stats['errors'] += 1
                    
                    conn.commit()  # Коммитим каждую порцию
                
            logger.info(f"Восстановлено {restored} записей недвижимости")
            self.stats['restored_records'] += restored
            
        except Exception as e:
            logger.error(f"Ошибка восстановления недвижимости: {e}")
            self.stats['errors'] += 1

    def restore_additional_tables(self):
        """Восстановить дополнительные таблицы"""
        additional_tables = [
            'applications',
            'blog_articles', 
            'blog_categories',
            'blog_posts',
            'buildings',
            'callback_requests',
            'cities',
            'collections',
            'favorite_properties',
            'favorite_complexes',
            'it_companies',
            'residential_complexes'
        ]
        
        for table in additional_tables:
            logger.info(f"=== ВОССТАНОВЛЕНИЕ {table.upper()} ===")
            
            file = self.get_latest_file(table)
            if not file:
                continue
                
            try:
                df = pd.read_excel(f'attached_assets/{file}')
                logger.info(f"Найдено {len(df)} записей в таблице {table}")
                
                if len(df) == 0:
                    logger.info(f"Таблица {table} пуста, пропускаем")
                    continue
                
                restored = 0
                with self.engine.connect() as conn:
                    for _, row in df.iterrows():
                        try:
                            # Динамически создаем SQL на основе непустых колонок
                            non_null_cols = []
                            params = {}
                            
                            for col in df.columns:
                                value = row[col]
                                if not pd.isna(value):
                                    non_null_cols.append(col)
                                    if isinstance(value, str) and 'GMT' in value:
                                        try:
                                            date_part = value.split(' GMT')[0]
                                            params[col] = pd.to_datetime(date_part).strftime('%Y-%m-%d %H:%M:%S')
                                        except:
                                            params[col] = value
                                    else:
                                        params[col] = value
                                        
                            if non_null_cols:
                                cols_str = ', '.join(non_null_cols)
                                values_str = ', '.join([f':{col}' for col in non_null_cols])
                                
                                # Проверяем существует ли запись (если есть id)
                                if 'id' in params:
                                    check_sql = text(f"SELECT id FROM {table} WHERE id = :id")
                                    existing = conn.execute(check_sql, {'id': params['id']}).fetchone()
                                    
                                    if existing:
                                        logger.info(f"Запись {params['id']} уже существует в {table}, пропускаем")
                                        self.stats['skipped'] += 1
                                        continue
                                
                                insert_sql = text(f"""
                                    INSERT INTO {table} ({cols_str})
                                    VALUES ({values_str})
                                """)
                                
                                conn.execute(insert_sql, params)
                                restored += 1
                            
                        except Exception as e:
                            logger.error(f"Ошибка восстановления записи в {table}: {e}")
                            self.stats['errors'] += 1
                    
                    conn.commit()
                    
                logger.info(f"Восстановлено {restored} записей в таблице {table}")
                self.stats['restored_records'] += restored
                
            except Exception as e:
                logger.error(f"Ошибка восстановления таблицы {table}: {e}")
                self.stats['errors'] += 1

    def run_restore(self):
        """Запустить полное восстановление"""
        logger.info("🚀 НАЧИНАЕМ ВОССТАНОВЛЕНИЕ ДАННЫХ INBACK")
        logger.info(f"База данных: {self.db_url[:50]}...")
        
        start_time = datetime.now()
        
        try:
            # Восстанавливаем в правильном порядке (учитывая зависимости)
            self.restore_districts()      # Сначала районы (независимые)
            self.restore_developers()     # Затем застройщики  
            self.restore_managers()       # Менеджеры
            self.restore_users()          # Пользователи
            self.restore_excel_properties()  # Недвижимость (может зависеть от районов и застройщиков)
            self.restore_additional_tables()  # Остальные таблицы
            
            # Выводим финальную статистику
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("=" * 50)
            logger.info("✅ ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО")
            logger.info(f"🕒 Время выполнения: {duration}")
            logger.info(f"📁 Всего файлов: {self.stats['total_files']}")
            logger.info(f"✅ Обработано файлов: {self.stats['processed_files']}")
            logger.info(f"📝 Всего записей: {self.stats['total_records']}")
            logger.info(f"✅ Восстановлено записей: {self.stats['restored_records']}")
            logger.info(f"⏭️ Пропущено записей: {self.stats['skipped']}")
            logger.info(f"❌ Ошибок: {self.stats['errors']}")
            logger.info("=" * 50)
            
            if self.stats['errors'] > 0:
                logger.warning(f"⚠️ При восстановлении возникло {self.stats['errors']} ошибок. Проверьте логи.")
            else:
                logger.info("🎉 Восстановление прошло без ошибок!")
                
        except Exception as e:
            logger.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
            return False
            
        return True

if __name__ == "__main__":
    try:
        restorer = BackupRestorer()
        success = restorer.run_restore()
        
        if success:
            print("\n🎉 Восстановление данных завершено успешно!")
            print("📋 Подробный лог сохранен в файл: restore_backup.log")
        else:
            print("\n❌ Восстановление завершилось с ошибками!")
            print("📋 Проверьте лог файл: restore_backup.log")
            
    except Exception as e:
        print(f"\n💥 Критическая ошибка запуска: {e}")
        sys.exit(1)