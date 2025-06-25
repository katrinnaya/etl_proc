# Финальное задание по модулю 4. Работа с Яндекс.Облаком
## Задание 1. Работа с Yandex DataTransfer
### Шаги для выполнения
1. Создание БД Yandex Database (YDB)
2. Создание таблицы в YDB
3. Подготовка скрипта для создания датасета 
4. Загрузка данных в YDB
5. Создание бакета в Object Storage
6. Настройка трансфера через Data Transfer
7. Проверка работоспособности

### Шаг 1
Создаем базу данных Yandex Database `etl-db`
### Шаг 2
Создаем таблицу в YDB через интерфейс
![ydb](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task1/ydb.jpg) 
### Шаг 3
Пишем Python-скрипт для создания датасета. См. файл `create_db` в папке `scripts`. Файл с датасетом `transactions_v2.csv` сохраняем локально
### Шаг 4
Загружаем данные в YDB через YDB CLI
#### Шаг 4.1
Устанавливаем клиент
`curl -sSL https://install.ydb.tech/cli | bash`
#### Шаг 4.2
Устанавливаем утилиту
`curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash`
#### Шаг 4.3
Пишем скрипт на заливку данных в YDB. См. файл `upload_to_ydb.py` или `upload_to_ydb.sh` в папке `scripts`
### Шаг 5
Создаем бакет `etl-bucket` в Object Storage 
![back](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task1/back.jpg) 
### Шаг 6
Cоздаем два эндпоинта и активируем трансфер
![endp](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task1/endp.jpg) 
![transfer](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task1/transfer.jpg) 
### Шаг 7
Заходим в бакет и проверяем, что появился файл с данными из базы данных
![back2](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task1/back2.jpg) 

# Задание 2. Автоматизация работы с Yandex Data Processing при помощи Apache AirFlow
### Шаги для выполнения
1. Создание кластера Managed Service for Apache Airflow
2. Написание DAG для Airflow и PySpark-скрипта для обработки данных
3. Загрузка данных в бакет
4. Запуск DAG и проверка результатов
### Шаг 1
Создаем кластер `airflow-etl-cluster`
### Шаг 2
Пишем необходимые скрипты. См. файлы `transaction_processing_dag.py` и `process_transactions.py` в папке `scripts`. 
Раздаем права сервисному аккаунту на бакет 


![acl](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task2/acl.jpg) 
### Шаг 3
Загружаем файл с датасетом `transactions_v2.csv` и необходимые скрипты в бакет 
### Шаг 4
Запускаем DAG вручную в интерфейсе Airflow
![dag](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task2/dag.jpg) 
Pyskark-задание отработало: 
* Статистика по валютам:
  * Количество failed-транзакций для каждой валюты
  * Сумма amounts для каждой валюты
* Топ-5 мерчантов: мерчанты с наибольшим количеством failed-транзакций
![pyspark](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task2/pyspark.jpg) 
Результаты появились в бакете
![back3](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task2/back3.jpg)

## Задание 3. Работа с топиками Apache Kafka с помощью PySpark-заданий в Yandex Data Processing
### Шаги для выполнения
1. Подготовка архитектуры
2. Создание PySpark-заданий
3. Запуск заданий в Data Proc
4. Проверка результатов
### Шаг 1.1
Запускаем кластеры
* Managed Service for Kafka
* Data Proc
* Managed Service for PostgreSQL
### Шаг 1.2
* Создаем топик в кластере Kafka
* Создаем пользователя для подключения к Kafka
### Шаг 1.3
Настраиваем PostgreSQL
* Через WebSQL в уже созданной базе даных создаем таблицу для хранения транзакций
![db](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task3/db.jpg)
* Грантуем права пользователю на БД
![grant](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task3/grant.jpg)
### Шаг 1.4
Подготовим Object Storage. Загрузим датасет из предыдущего задания в формате Parquet по статистике failed-транзакций в бакет. См. файл `transactions.parquet`в папке `data`
### Шаг 2
Пишем скрипты и помещаем их в бакет. См. файлы `kafka-write.py` и `kafka-read-stream.py`в папке `scripts`
### Шаг 3
Запускаем задания в Data Proc

![task1](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task3/task1.jpg)
![task2](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task3/task2.jpg) 
### Шаг 4
Проверяем, что данные появились в базе данных
![result](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task3/result.jpg)
![result2](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task3/result2.jpg)
Как результат, все сообщения из Kafka (от начала до конца топика) прочитаны, данные преобразованы согласно схеме и записаны в PostgreSQL одной операцией
# Задание 4: Визуализация в DataLens
Настроили подключение, загрузили датасет в бакет, сформировали чарты в DataLens


Итоговый дашборд 
![viz](https://github.com/katrinnaya/etl_proc/blob/final_module2_hw/images/task4/viz.jpg) 
