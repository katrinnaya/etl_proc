import uuid
import datetime
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.yandex.operators.yandexcloud_dataproc import (
    DataprocCreateClusterOperator,
    DataprocCreatePysparkJobOperator,
    DataprocDeleteClusterOperator,
)

# Данные инфраструктуры
YC_DP_AZ = 'ru-central1-a'
YC_DP_SSH_PUBLIC_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKh9Q5Xs/6mXEoBzS+2JQWwsT4b68KKs0z5WWjcN8mE/ katrinnaya@HP-Com-Palamarchyk'  
YC_DP_SUBNET_ID = 'e9bqkgd6rpk07eql4mls' 
YC_DP_SA_ID = 'ajeb6lic2lpm0p1t9tcu' 
YC_BUCKET = 'etl-bucket'             

with DAG(
    'process_transactions',
    schedule_interval=None,
    tags=['data-processing'],
    start_date=datetime.datetime.now(),
    max_active_runs=1,
    catchup=False
) as dag:
    
    # 1. Создание кластера Data Proc
    create_cluster = DataprocCreateClusterOperator(
        task_id='create_cluster',
        cluster_name=f'tmp-dp-{uuid.uuid4()}',
        cluster_description='Временный кластер для обработки транзакций',
        ssh_public_keys=YC_DP_SSH_PUBLIC_KEY,
        service_account_id=YC_DP_SA_ID,
        subnet_id=YC_DP_SUBNET_ID,
        s3_bucket=YC_BUCKET,
        zone=YC_DP_AZ,
        cluster_image_version='2.1',
        masternode_resource_preset='s2.medium',
        masternode_disk_type='network-hdd',
        masternode_disk_size=32,
        computenode_resource_preset='s2.medium',
        computenode_disk_type='network-hdd',
        computenode_disk_size=64,
        computenode_count=2,
        services=['YARN', 'SPARK'],
        datanode_count=0
    )

    # 2. Запуск PySpark задания
    run_spark_job = DataprocCreatePysparkJobOperator(
        task_id='run_spark_job',
        main_python_file_uri=f's3a://{YC_BUCKET}/scripts/process_transactions.py',
    )

    # 3. Удаление кластера
    delete_cluster = DataprocDeleteClusterOperator(
        task_id='delete_cluster',
        trigger_rule=TriggerRule.ALL_DONE,
    )

    # Оркестрация
    create_cluster >> run_spark_job >> delete_cluster