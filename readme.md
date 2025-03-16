# Репликация данных из MongoDB в PostgreSQL с использованием Apache Airflow

## Описание задания

Цель задания — настроить репликацию данных из нереляционной базы данных (MongoDB) в реляционную базу данных (PostgreSQL) с использованием Apache Airflow. В процессе выполнения задания необходимо:

1. Сгенерировать данные в MongoDB.
2. Настроить репликацию данных из MongoDB в PostgreSQL.
3. Проверить корректность репликации.

## Инструменты

Для выполнения задания использовались следующие инструменты:
- **Apache Airflow** — для оркестрации процесса репликации.
- **MongoDB** — нереляционная база данных для хранения исходных данных.
- **PostgreSQL** — реляционная база данных для хранения реплицированных данных.
- **Docker Compose** — для развертывания окружения.

## Шаги выполнения

### 1. Генерация данных в MongoDB

1. **Создание базы данных и коллекции в MongoDB:**
   - В MongoDB была создана база данных `user_sessions` и коллекция `UserSessions`.
   - Структура документа в коллекции:
     ```json
     {
       "session_id": "уникальный идентификатор сессии",
       "user_id": "идентификатор пользователя",
       "start_time": "время начала сессии",
       "end_time": "время завершения сессии",
       "pages_visited": ["массив посещённых страниц"],
       "device": "информация об устройстве",
       "actions": ["массив действий пользователя"]
     }
     ```

2. **Запуск скрипта для генерации данных:**
   - Скрипт `generate_data.py` был скопирован в контейнер Apache Airflow:
     ```bash
     docker cp ~/'etl_proc (local)'/final_module_hw/generate_data.py <контейнер_ID>:/opt/airflow/
     ```
   - Вход в контейнер Apache Airflow:
     ```bash
     docker exec -it <контейнер_ID> bash
     ```
   - Установка Python 3 (если не установлен):
     ```bash
     apt-get update && apt-get install -y python3
     ```
   - Запуск скрипта:
     ```bash
     python3 /opt/airflow/generate_data.py
     ```

3. **Проверка данных в MongoDB:**
   - Вход в MongoDB:
     ```bash
     docker exec -it mongo_db mongosh -u root -p example --authenticationDatabase admin
     ```
   - Проверка количества документов в коллекции:
     ```bash
     use user_sessions;
     db.UserSessions.find().count();
     ```
   - Ожидаемый результат: `100` документов.

### 2. Настройка репликации с использованием Apache Airflow

1. **Создание и настройка DAG в Apache Airflow:**
   - Был создан DAG для репликации данных из MongoDB в PostgreSQL.
   - DAG включает задачи для извлечения данных из MongoDB, их преобразования и загрузки в PostgreSQL.

2. **Запуск DAG:**
   - DAG был запущен через веб-интерфейс Apache Airflow.

### 3. Проверка данных в PostgreSQL

1. **Подключение к PostgreSQL:**
   - Вход в контейнер PostgreSQL:
     ```bash
     docker exec -it etl_proc_finalhw_airflow psql -U airflow -d airflow
     ```
   - Проверка данных:
     ```sql
     SELECT * FROM <название_таблицы>;
     ```
   - Ожидаемый результат: данные из MongoDB успешно реплицированы в PostgreSQL.

## Заключение

В ходе выполнения задания были успешно выполнены следующие шаги:
- Генерация данных в MongoDB.
- Настройка репликации данных из MongoDB в PostgreSQL с использованием Apache Airflow.
- Проверка корректности репликации.

Все шаги были выполнены в контейнерах, развернутых с помощью Docker Compose.
