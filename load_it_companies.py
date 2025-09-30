#!/usr/bin/env python3
import pandas as pd
import psycopg2
import os
import sys

def load_it_companies():
    """Загрузка IT компаний из Excel в базу данных"""
    try:
        # Читаем Excel файл
        file_path = 'attached_assets/it_companies_1757005426411.xlsx'
        print(f"Чтение файла: {file_path}")
        df = pd.read_excel(file_path)

        print(f'Загружено {len(df)} записей из Excel')
        print('Несколько примеров названий компаний:')
        print(df['company_name'].head(10).tolist())

        # Подключаемся к базе данных
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            print("Ошибка: DATABASE_URL не найден")
            return False
            
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Очищаем текущие данные
        cur.execute("DELETE FROM it_companies")
        print("Старые данные удалены")

        # Вставляем данные пакетами
        batch_size = 100
        inserted_count = 0

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            for _, row in batch.iterrows():
                inn = str(row['inn']).strip() if pd.notna(row['inn']) else None
                company_name = str(row['company_name']).strip() if pd.notna(row['company_name']) else ''
                
                if company_name:  # Только если есть название компании
                    try:
                        cur.execute("""
                            INSERT INTO it_companies (name, inn, status, region, created_at) 
                            VALUES (%s, %s, %s, %s, NOW())
                            ON CONFLICT DO NOTHING
                        """, (company_name, inn, 'active', 'Россия'))
                        inserted_count += cur.rowcount
                    except Exception as e:
                        print(f'Ошибка при вставке записи {company_name}: {e}')
                        continue
            
            conn.commit()
            
            if i % (batch_size * 10) == 0:
                print(f'Обработано {i} записей...')

        conn.close()
        print(f'Успешно загружено {inserted_count} IT компаний в базу данных')
        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        return False

if __name__ == "__main__":
    load_it_companies()