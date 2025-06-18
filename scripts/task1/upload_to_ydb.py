import ydb
import pandas as pd
import os
import time
from datetime import datetime

# Настройки
CSV_PATH = 'transactions_v2.csv'
TOKEN_PATH = '/home/katrinnaya/ydb_token.txt'
YDB_ENDPOINT = 'grpcs://ydb.serverless.yandexcloud.net:2135'
YDB_DATABASE = '/ru-central1/b1gehnfakkccqg95ngb5/etnt2qc89uq0j2cmceq4'
TABLE_NAME = 'transactions_v2'
BATCH_SIZE = 300  # Размер пакета уменьшен для надежности

def clear_table(session):
    """Полностью очищает таблицу."""
    try:
        session.transaction().execute(
            f"DELETE FROM {TABLE_NAME} WHERE true;",
            commit_tx=True
        )
        print(f"Таблица {TABLE_NAME} успешно очищена.")
    except Exception as e:
        print(f"Ошибка при очистке таблицы: {str(e)}")
        raise

def prepare_batch(df_batch):
    """Подготавливает данные для загрузки."""
    return [
        {
            'transaction_id': str(row['transaction_id']),
            'user_id': int(row['user_id']),
            'amount': float(row['amount']),
            'currency': str(row['currency']),
            'transaction_date': datetime.strptime(
                row['transaction_date'], 
                '%Y-%m-%d %H:%M:%S.%f'
            ),
            'status': str(row['status']),
            'merchant': str(row['merchant'])
        }
        for _, row in df_batch.iterrows()
    ]

def main():
    # Подключение к YDB
    driver_config = ydb.DriverConfig(
        endpoint=YDB_ENDPOINT,
        database=YDB_DATABASE,
        credentials=ydb.AccessTokenCredentials(open(TOKEN_PATH).read().strip())
    )

    driver = ydb.Driver(driver_config)
    try:
        driver.wait(timeout=15)
        
        # Создаем отдельную сессию для очистки таблицы
        session = driver.table_client.session().create()
        try:
            clear_table(session)
        finally:
            session.delete()  # Явное закрытие сессии
        
        # Чтение CSV
        df = pd.read_csv(CSV_PATH)
        print(f"Найдено {len(df)} строк для загрузки.")
        
        # Загрузка данных
        total_loaded = 0
        for i in range(0, len(df), BATCH_SIZE):
            batch = df.iloc[i:i + BATCH_SIZE]
            rows = prepare_batch(batch)
            
            # Создаем новую сессию для каждого пакета
            session = driver.table_client.session().create()
            try:
                tx = session.transaction(ydb.SerializableReadWrite()).begin()
                
                # Объединяем все запросы в одну транзакцию
                upsert_queries = []
                for row in rows:
                    query = f"""
                    UPSERT INTO `{TABLE_NAME}` 
                    (transaction_id, user_id, amount, currency, transaction_date, status, merchant)
                    VALUES ('{row['transaction_id']}', {row['user_id']}, {row['amount']}, '{row['currency']}', 
                            CAST('{row['transaction_date'].strftime('%Y-%m-%dT%H:%M:%SZ')}' AS Datetime), 
                            '{row['status']}', '{row['merchant']}');
                    """
                    upsert_queries.append(query)
                
                combined_query = "\n".join(upsert_queries)
                tx.execute(combined_query)
                tx.commit()
                
                total_loaded += len(rows)
                print(f"Загружено: {total_loaded}/{len(df)}")
                time.sleep(0.5)  # Задержка между пакетами
            except Exception as e:
                print(f"Ошибка пакета {i}-{i + BATCH_SIZE}: {str(e)}")
            finally:
                session.delete()  # Явное закрытие сессии
        
        print(f"\nИтог: успешно загружено {total_loaded} из {len(df)} строк.")
    finally:
        driver.stop()  # Корректное закрытие драйвера

if __name__ == "__main__":
    main()