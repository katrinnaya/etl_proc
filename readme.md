# Обработка данных из Yandex Object Storage с помощью сервиса Yandex Apache AirFlow, используя мощности Yandex Data Processing.
Шаги для выполнения:
1. Создать бакет `bucket-for-etl` в Yandex Object Storage, загрузить в него тестовый CSV-файл `products.csv`.
2. Создать DAG-файл для обработки данных и загрузить его в бакет.
3. Развернуть кластер Managed Service for Apache Airflow. 
4. Запустить ETL-процесс через Airflow.

## Шаг 1
1. Создаем бакет, создаем структуру папок:
   *  `input` - для загрузки исходного файла для обработки
   *  `output` - для сохранения обработанного файла
   *  `dags` - для загрузки DAG-файла
2. Добавляем файл `products.csv` в папку `input` текущего бакета
## Шаг 2
Добавляем для сервисного аккаунта роли:
   * `managed-airflow.integrationProvider`
   * `monitoring.editor` 
## Шаг 3
Создаем DAG-файл и загружаем в папку `dags` текущего бакета
## Шаг 4
Создаем кластер Airflow 
## Шаг 5
Подключение к UI
## Шаг 6
Запускаем ETL. Запускаем DAG `etl_products` вручную через Trigger DAG

## Шаг 7
Проверяем результат

В бакете bucket-for-etl/output/ появится файл filtered_products.csv с товарами, где in_stock=true.
