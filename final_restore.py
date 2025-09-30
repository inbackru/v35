#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный скрипт восстановления недостающих данных InBack
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalRestorer:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        self.engine = create_engine(self.db_url)

    def get_latest_file(self, pattern):
        """Получить самый свежий файл по паттерну"""
        files = []
        for file in os.listdir('attached_assets'):
            if file.startswith(pattern) and file.endswith('.xlsx'):
                try:
                    timestamp = file.split('_')[-1].replace('.xlsx', '')
                    files.append((int(timestamp), file))
                except:
                    files.append((0, file))
        
        if not files:
            return None
        
        files.sort(reverse=True)
        return files[0][1]

    def restore_missing_properties(self):
        """Восстановить недостающие записи недвижимости"""
        logger.info("=== ВОССТАНОВЛЕНИЕ НЕДОСТАЮЩИХ ЗАПИСЕЙ НЕДВИЖИМОСТИ ===")
        
        file = self.get_latest_file('excel_properties')
        if not file:
            logger.info("Файл excel_properties не найден")
            return
            
        try:
            df = pd.read_excel(f'attached_assets/{file}')
            logger.info(f"В бэкапе: {len(df)} записей недвижимости")
            
            # Получаем существующие inner_id
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT inner_id FROM excel_properties"))
                existing_ids = {row[0] for row in result}
                logger.info(f"В базе уже есть: {len(existing_ids)} записей")
                
                # Находим недостающие записи
                missing_records = df[~df['inner_id'].isin(existing_ids)]
                logger.info(f"Нужно добавить: {len(missing_records)} записей")
                
                if len(missing_records) == 0:
                    logger.info("Все записи уже восстановлены!")
                    return
                
                # Добавляем недостающие записи по порциям
                restored = 0
                chunk_size = 20
                
                for i in range(0, len(missing_records), chunk_size):
                    chunk = missing_records.iloc[i:i + chunk_size]
                    logger.info(f"Добавляем записи {i+1}-{min(i+chunk_size, len(missing_records))}")
                    
                    for _, row in chunk.iterrows():
                        try:
                            # Подготавливаем только непустые колонки
                            data = {}
                            for col in df.columns:
                                if not pd.isna(row[col]):
                                    data[col] = row[col]
                            
                            if 'inner_id' not in data:
                                continue
                                
                            # Создаем INSERT запрос
                            cols = list(data.keys())
                            values_placeholder = ', '.join([f':{col}' for col in cols])
                            
                            insert_sql = text(f"""
                                INSERT INTO excel_properties ({', '.join(cols)})
                                VALUES ({values_placeholder})
                            """)
                            
                            conn.execute(insert_sql, data)
                            restored += 1
                            
                        except Exception as e:
                            logger.error(f"Ошибка добавления {row.get('inner_id', 'unknown')}: {e}")
                    
                    conn.commit()
                
                logger.info(f"✅ Добавлено {restored} новых записей недвижимости")
                
        except Exception as e:
            logger.error(f"Ошибка восстановления недвижимости: {e}")

    def restore_additional_data(self):
        """Восстановить дополнительные данные"""
        tables_config = [
            ('residential_complexes', 'residential_complexes', 'id'),
            ('buildings', 'buildings', 'id'),
            ('it_companies', 'it_companies', 'id'),
            ('blog_articles', 'blog_articles', 'id'),
            ('applications', 'applications', 'id'),
            ('collections', 'collections', 'id'),
            ('favorite_properties', 'favorite_properties', 'id'),
            ('callback_requests', 'callback_requests', 'id')
        ]
        
        for file_pattern, table_name, id_column in tables_config:
            logger.info(f"=== ВОССТАНОВЛЕНИЕ {table_name.upper()} ===")
            
            file = self.get_latest_file(file_pattern)
            if not file:
                logger.info(f"Файл {file_pattern} не найден")
                continue
                
            try:
                df = pd.read_excel(f'attached_assets/{file}')
                
                if len(df) == 0:
                    logger.info(f"Файл {table_name} пустой")
                    continue
                    
                logger.info(f"В бэкапе: {len(df)} записей")
                
                with self.engine.connect() as conn:
                    # Проверяем сколько записей уже есть
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                        existing_count = result.fetchone()[0]
                        logger.info(f"В базе уже есть: {existing_count} записей")
                        
                        if existing_count >= len(df):
                            logger.info(f"Таблица {table_name} уже заполнена, пропускаем")
                            continue
                            
                    except Exception:
                        logger.info(f"Таблица {table_name} пуста или недоступна")
                    
                    # Добавляем записи
                    restored = 0
                    for _, row in df.iterrows():
                        try:
                            # Подготавливаем данные
                            data = {}
                            for col in df.columns:
                                value = row[col]
                                if not pd.isna(value):
                                    # Обрабатываем даты
                                    if isinstance(value, str) and 'GMT' in value:
                                        try:
                                            date_part = value.split(' GMT')[0]
                                            data[col] = pd.to_datetime(date_part).strftime('%Y-%m-%d %H:%M:%S')
                                        except:
                                            data[col] = value
                                    else:
                                        data[col] = value
                            
                            if not data:
                                continue
                            
                            # Проверяем существует ли запись
                            if id_column in data:
                                check_sql = text(f"SELECT {id_column} FROM {table_name} WHERE {id_column} = :{id_column}")
                                existing = conn.execute(check_sql, {id_column: data[id_column]}).fetchone()
                                
                                if existing:
                                    continue  # Запись уже есть
                            
                            # Вставляем новую запись
                            cols = list(data.keys())
                            insert_sql = text(f"""
                                INSERT INTO {table_name} ({', '.join(cols)})
                                VALUES ({', '.join([f':{col}' for col in cols])})
                            """)
                            
                            conn.execute(insert_sql, data)
                            restored += 1
                            
                        except Exception as e:
                            logger.error(f"Ошибка добавления записи в {table_name}: {e}")
                    
                    conn.commit()
                    logger.info(f"✅ Добавлено {restored} записей в {table_name}")
                    
            except Exception as e:
                logger.error(f"Ошибка восстановления {table_name}: {e}")

    def check_final_status(self):
        """Проверить итоговое состояние базы данных"""
        logger.info("=== ИТОГОВОЕ СОСТОЯНИЕ БАЗЫ ДАННЫХ ===")
        
        tables_to_check = [
            'users', 'managers', 'excel_properties', 'developers', 
            'districts', 'residential_complexes', 'buildings', 
            'it_companies', 'applications', 'collections',
            'favorite_properties', 'callback_requests'
        ]
        
        with self.engine.connect() as conn:
            total_records = 0
            for table in tables_to_check:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    logger.info(f"✅ {table}: {count} записей")
                    total_records += count
                except Exception as e:
                    logger.error(f"❌ {table}: ошибка проверки - {e}")
            
            logger.info(f"🎯 ОБЩИЙ ИТОГ: {total_records} записей восстановлено")

    def run(self):
        """Запустить финальное восстановление"""
        logger.info("🚀 ФИНАЛЬНОЕ ВОССТАНОВЛЕНИЕ ДАННЫХ INBACK")
        
        try:
            # Восстанавливаем недостающие записи недвижимости
            self.restore_missing_properties()
            
            # Восстанавливаем дополнительные таблицы
            self.restore_additional_data()
            
            # Проверяем итоговое состояние
            self.check_final_status()
            
            logger.info("✅ ФИНАЛЬНОЕ ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!")
            
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    restorer = FinalRestorer()
    restorer.run()