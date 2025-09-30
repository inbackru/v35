#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенный скрипт восстановления данных InBack из Excel бэкапов
Обрабатывает дубли и ошибки транзакций
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
        logging.FileHandler('restore_improved.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ImprovedBackupRestorer:
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
            'updated_records': 0,
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

    def safe_clear_table(self, table_name):
        """Безопасно очистить таблицу (только DELETE, без сброса constraints)"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.fetchone()[0]
                
                if count > 0:
                    conn.execute(text(f"DELETE FROM {table_name}"))
                    conn.commit()
                    logger.info(f"Удалено {count} записей из таблицы {table_name}")
                else:
                    logger.info(f"Таблица {table_name} уже пуста")
                    
        except Exception as e:
            logger.warning(f"Не удалось очистить таблицу {table_name}: {e}")

    def upsert_record(self, conn, table_name, data, unique_columns=['id']):
        """Вставить или обновить запись (UPSERT)"""
        try:
            # Проверяем существует ли запись
            conditions = []
            check_params = {}
            
            for col in unique_columns:
                if col in data:
                    conditions.append(f"{col} = :{col}_check")
                    check_params[f"{col}_check"] = data[col]
            
            if not conditions:
                # Нет уникальных колонок, просто вставляем
                cols = list(data.keys())
                insert_sql = text(f"""
                    INSERT INTO {table_name} ({', '.join(cols)})
                    VALUES ({', '.join([f':{col}' for col in cols])})
                """)
                conn.execute(insert_sql, data)
                return 'inserted'
            
            check_sql = text(f"SELECT id FROM {table_name} WHERE {' AND '.join(conditions)}")
            existing = conn.execute(check_sql, check_params).fetchone()
            
            if existing:
                # Обновляем существующую запись
                set_clauses = []
                update_params = check_params.copy()
                
                for col, value in data.items():
                    if col not in unique_columns:
                        set_clauses.append(f"{col} = :{col}_update")
                        update_params[f"{col}_update"] = value
                
                if set_clauses:
                    update_sql = text(f"""
                        UPDATE {table_name} 
                        SET {', '.join(set_clauses)}
                        WHERE {' AND '.join(conditions)}
                    """)
                    conn.execute(update_sql, update_params)
                    return 'updated'
                else:
                    return 'skipped'
            else:
                # Вставляем новую запись
                cols = list(data.keys())
                insert_sql = text(f"""
                    INSERT INTO {table_name} ({', '.join(cols)})
                    VALUES ({', '.join([f':{col}' for col in cols])})
                """)
                conn.execute(insert_sql, data)
                return 'inserted'
                
        except Exception as e:
            logger.error(f"Ошибка UPSERT в {table_name}: {e}")
            raise

    def parse_date_string(self, date_str):
        """Парсит различные форматы дат"""
        if not date_str or pd.isna(date_str):
            return None
            
        if not isinstance(date_str, str):
            return date_str
            
        if 'GMT' in date_str:
            try:
                # Формат: 'Wed Aug 27 2025 10:37:41 GMT+0300 (Москва, стандартное время)'
                date_part = date_str.split(' GMT')[0]
                parsed_date = pd.to_datetime(date_part)
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            except:
                logger.warning(f"Не удалось парсить дату: {date_str}")
                return None
        
        return date_str

    def process_row_data(self, row, df_columns):
        """Обработать данные строки"""
        data = {}
        
        for col in df_columns:
            value = row[col]
            
            if pd.isna(value):
                continue
                
            # Обрабатываем даты
            if isinstance(value, str) and ('GMT' in value or 'created_at' in col or 'updated_at' in col):
                parsed_date = self.parse_date_string(value)
                if parsed_date:
                    data[col] = parsed_date
            else:
                data[col] = value
                
        return data

    def restore_users(self):
        """Восстановить пользователей с UPSERT"""
        logger.info("=== ВОССТАНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ===")
        
        file = self.get_latest_file('users')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} пользователей в {file}")
            
            restored = 0
            updated = 0
            
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        data = self.process_row_data(row, df.columns)
                        if not data:
                            continue
                            
                        result = self.upsert_record(conn, 'users', data, ['id'])
                        
                        if result == 'inserted':
                            restored += 1
                        elif result == 'updated':
                            updated += 1
                        
                    except Exception as e:
                        logger.error(f"Ошибка обработки пользователя {row.get('id', 'unknown')}: {e}")
                        self.stats['errors'] += 1
                
                conn.commit()
                
            logger.info(f"Пользователи - Новых: {restored}, Обновлено: {updated}")
            self.stats['restored_records'] += restored
            self.stats['updated_records'] += updated
            
        except Exception as e:
            logger.error(f"Ошибка восстановления пользователей: {e}")
            self.stats['errors'] += 1

    def restore_managers(self):
        """Восстановить менеджеров с UPSERT"""
        logger.info("=== ВОССТАНОВЛЕНИЕ МЕНЕДЖЕРОВ ===")
        
        file = self.get_latest_file('managers')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} менеджеров в {file}")
            
            restored = 0
            updated = 0
            
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        data = self.process_row_data(row, df.columns)
                        if not data:
                            continue
                            
                        result = self.upsert_record(conn, 'managers', data, ['id'])
                        
                        if result == 'inserted':
                            restored += 1
                        elif result == 'updated':
                            updated += 1
                        
                    except Exception as e:
                        logger.error(f"Ошибка обработки менеджера {row.get('id', 'unknown')}: {e}")
                        self.stats['errors'] += 1
                
                conn.commit()
                
            logger.info(f"Менеджеры - Новых: {restored}, Обновлено: {updated}")
            self.stats['restored_records'] += restored
            self.stats['updated_records'] += updated
            
        except Exception as e:
            logger.error(f"Ошибка восстановления менеджеров: {e}")
            self.stats['errors'] += 1

    def restore_excel_properties(self):
        """Восстановить недвижимость с UPSERT"""
        logger.info("=== ВОССТАНОВЛЕНИЕ НЕДВИЖИМОСТИ ===")
        
        file = self.get_latest_file('excel_properties')
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} записей недвижимости в {file}")
            
            restored = 0
            updated = 0
            chunk_size = 25  # Уменьшаем размер порции
            
            with self.engine.connect() as conn:
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i + chunk_size]
                    logger.info(f"Обрабатываем записи {i+1}-{min(i+chunk_size, len(df))}")
                    
                    for _, row in chunk.iterrows():
                        try:
                            data = self.process_row_data(row, df.columns)
                            if not data or 'inner_id' not in data:
                                continue
                                
                            result = self.upsert_record(conn, 'excel_properties', data, ['inner_id'])
                            
                            if result == 'inserted':
                                restored += 1
                            elif result == 'updated':
                                updated += 1
                            
                        except Exception as e:
                            logger.error(f"Ошибка обработки недвижимости {row.get('inner_id', 'unknown')}: {e}")
                            self.stats['errors'] += 1
                    
                    conn.commit()  # Коммитим каждую порцию
                
            logger.info(f"Недвижимость - Новых: {restored}, Обновлено: {updated}")
            self.stats['restored_records'] += restored
            self.stats['updated_records'] += updated
            
        except Exception as e:
            logger.error(f"Ошибка восстановления недвижимости: {e}")
            self.stats['errors'] += 1

    def restore_generic_table(self, table_pattern, table_name, unique_cols=['id']):
        """Универсальное восстановление таблицы"""
        logger.info(f"=== ВОССТАНОВЛЕНИЕ {table_name.upper()} ===")
        
        file = self.get_latest_file(table_pattern)
        if not file:
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"Найдено {len(df)} записей в таблице {table_name}")
            
            if len(df) == 0:
                logger.info(f"Таблица {table_name} пуста, пропускаем")
                return
            
            restored = 0
            updated = 0
            
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    try:
                        data = self.process_row_data(row, df.columns)
                        if not data:
                            continue
                            
                        result = self.upsert_record(conn, table_name, data, unique_cols)
                        
                        if result == 'inserted':
                            restored += 1
                        elif result == 'updated':
                            updated += 1
                        elif result == 'skipped':
                            self.stats['skipped'] += 1
                            
                    except Exception as e:
                        logger.error(f"Ошибка обработки записи в {table_name}: {e}")
                        self.stats['errors'] += 1
                
                conn.commit()
                
            logger.info(f"{table_name} - Новых: {restored}, Обновлено: {updated}")
            self.stats['restored_records'] += restored
            self.stats['updated_records'] += updated
            
        except Exception as e:
            logger.error(f"Ошибка восстановления таблицы {table_name}: {e}")
            self.stats['errors'] += 1

    def check_database_status(self):
        """Проверить состояние базы данных"""
        try:
            with self.engine.connect() as conn:
                # Проверяем основные таблицы
                tables_to_check = ['users', 'managers', 'excel_properties', 'developers', 'districts']
                
                logger.info("=== СОСТОЯНИЕ БД ПОСЛЕ ВОССТАНОВЛЕНИЯ ===")
                for table in tables_to_check:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        logger.info(f"{table}: {count} записей")
                    except Exception as e:
                        logger.error(f"Ошибка проверки {table}: {e}")
                        
        except Exception as e:
            logger.error(f"Ошибка проверки состояния БД: {e}")

    def run_restore(self):
        """Запустить улучшенное восстановление"""
        logger.info("🚀 НАЧИНАЕМ УЛУЧШЕННОЕ ВОССТАНОВЛЕНИЕ ДАННЫХ INBACK")
        logger.info(f"База данных: {self.db_url[:50]}...")
        
        start_time = datetime.now()
        
        try:
            # Восстанавливаем основные таблицы
            self.restore_generic_table('districts', 'districts', ['id'])
            self.restore_generic_table('developers', 'developers', ['id']) 
            self.restore_managers()
            self.restore_users()
            self.restore_excel_properties()
            
            # Восстанавливаем дополнительные таблицы
            additional_tables = [
                ('applications', 'applications'),
                ('blog_articles', 'blog_articles'), 
                ('blog_categories', 'blog_categories'),
                ('blog_posts', 'blog_posts'),
                ('buildings', 'buildings'),
                ('callback_requests', 'callback_requests'),
                ('cities', 'cities'),
                ('collections', 'collections'),
                ('favorite_properties', 'favorite_properties'),
                ('favorite_complexes', 'favorite_complexes'),
                ('it_companies', 'it_companies'),
                ('residential_complexes', 'residential_complexes')
            ]
            
            for pattern, table in additional_tables:
                self.restore_generic_table(pattern, table)
            
            # Проверяем итоговое состояние
            self.check_database_status()
            
            # Выводим финальную статистику
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("=" * 60)
            logger.info("✅ УЛУЧШЕННОЕ ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО")
            logger.info(f"🕒 Время выполнения: {duration}")
            logger.info(f"✅ Новых записей: {self.stats['restored_records']}")
            logger.info(f"🔄 Обновлено записей: {self.stats['updated_records']}")
            logger.info(f"⏭️ Пропущено записей: {self.stats['skipped']}")
            logger.info(f"❌ Ошибок: {self.stats['errors']}")
            logger.info("=" * 60)
            
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
        restorer = ImprovedBackupRestorer()
        success = restorer.run_restore()
        
        if success:
            print("\n🎉 Улучшенное восстановление данных завершено успешно!")
            print("📋 Подробный лог сохранен в файл: restore_improved.log")
        else:
            print("\n❌ Восстановление завершилось с ошибками!")
            print("📋 Проверьте лог файл: restore_improved.log")
            
    except Exception as e:
        print(f"\n💥 Критическая ошибка запуска: {e}")
        sys.exit(1)