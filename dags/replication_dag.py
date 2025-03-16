from datetime import datetime, timedelta  # Импорт datetime и timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pymongo import MongoClient
import psycopg2
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def replicate_user_sessions():
    try:
        # Подключение к MongoDB
        mongo_client = MongoClient('mongodb://root:example@mongo_db:27017/?authSource=admin')
        mongo_db = mongo_client['user_sessions']  
        user_sessions = mongo_db.UserSessions.find()  # Коллекция UserSessions

        # Подключение к PostgreSQL
        pg_conn = psycopg2.connect(
            dbname="airflow",
            user="airflow",
            password="airflow",
            host="etl_proc_finalhw_airflow",  # Имя контейнера PostgreSQL
            port="5432"
        )
        pg_cursor = pg_conn.cursor()

        # Создание таблицы, если её нет
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                pages_visited JSONB,
                device TEXT,
                actions JSONB
            );
        """)
        pg_conn.commit()

        # Вставка данных в PostgreSQL
        for session in user_sessions:
            # Преобразование полей pages_visited и actions в JSONB
            pages_visited_jsonb = psycopg2.extras.Json(session['pages_visited'])  # Преобразуем массив в JSONB
            actions_jsonb = psycopg2.extras.Json(session['actions'])              # Аналогично для действий

            pg_cursor.execute("""
                INSERT INTO user_sessions (session_id, user_id, start_time, end_time, pages_visited, device, actions)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_id) DO NOTHING;  
            """, (
                session['session_id'],
                session['user_id'],
                session['start_time'],
                session['end_time'],
                pages_visited_jsonb,         # Используем преобразованные значения
                session['device'],
                actions_jsonb                 # Используем преобразованные значения
            ))
        pg_conn.commit()
        logger.info("Данные успешно реплицированы в PostgreSQL")

    except Exception as e:
        logger.error(f"Ошибка при репликации данных: {e}")
        raise

    finally:
        # Закрытие соединений
        if 'pg_cursor' in locals():
            pg_cursor.close()
        if 'pg_conn' in locals():
            pg_conn.close()
        if 'mongo_client' in locals():
            mongo_client.close()


# Определение DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),  # Теперь работает благодаря импорту datetime
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mongo_to_postgres_replication',
    default_args=default_args,
    description='Replicate data from MongoDB to PostgreSQL',
    schedule_interval=timedelta(days=1),
)

replicate_user_sessions_task = PythonOperator(
    task_id='replicate_user_sessions',
    python_callable=replicate_user_sessions,
    dag=dag,
)

