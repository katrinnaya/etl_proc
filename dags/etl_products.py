from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def process_csv():
    # 1. Подключение к S3 
    s3 = S3Hook(aws_conn_id='yandex_cloud_s3')
    
    # 2. Чтение CSV из  папки input нужного бакета
    csv_data = s3.read_key(
        bucket_name='bucket-for-etl',
        key='input/products.csv'
    )
    
    # 3. Обработка данных (фильтруем и оставляем только in_stock=true)
    lines = csv_data.split('\n')
    header = lines[0]
    filtered_lines = [line for line in lines[1:] if 'true' in line.lower()]
    
    # 4. Сохранение обработанного файла в папке output нужного бакета
    s3.load_string(
        string_data=header + '\n' + '\n'.join(filtered_lines),
        bucket_name='bucket-for-etl',
        key='output/filtered_products.csv'
    )

# Настройка DAG
dag = DAG(
    dag_id='etl_products',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False
)

# Задача
task = PythonOperator(
    task_id='filter_csv_task',
    python_callable=process_csv,
    dag=dag
)