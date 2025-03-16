# Репликация данных из MongoDB в PostgreSQL с использованием Apache Airflow

## Описание 

Настройка репликации данных из нереляционной базы данных (MongoDB) в реляционную базу данных (PostgreSQL) с использованием Apache Airflow. В процессе выполнения необходимо:

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

1. **Создать локально проектную папку и создать папки для логов и плагинов, чтобы не было ошибки с правами на запись от Airflow:**
   - ``` mkdir logs ```
   - ``` mkdir plagins ```
2. **Запуск контейнера:**
   - ``` docker-compose up -d ```
2.1. **Провека:**
Вводим ``` docker ps ``` и узнаем статус контейнеров. Контейнер ``` airflow-init ``` после того, как отработает пропадет из списка.
```  
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS                   PORTS                      NAMES
d79c3230b07c   apache/airflow:2.6.2   "/usr/bin/dumb-init …"   3 minutes ago   Up 3 minutes             8080/tcp                   airflow-scheduler
910782a73ade   apache/airflow:2.6.2   "/usr/bin/dumb-init …"   3 minutes ago   Up 3 minutes             0.0.0.0:8080->8080/tcp     airflow-webserver
3b0662edbf20   postgres:13            "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:5432->5432/tcp     etl_proc_finalhw_airflow
ab8a7a98e661   mongo:latest           "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes             0.0.0.0:27017->27017/tcp   mongo_db
```
3. **Подключение к Airflow:**
  
Airflow будет доступен через веб-интерфейс на порту 8080:

Открываем в браузере: ``` http://localhost:8080 ```.
   - Логин: ``` admin ```
   - Пароль: ``` admin ```

4. **Запуск скрипта для генерации данных:**
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
5. **Проверка создания базы данных и коллекции в MongoDB:**
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

5.1. **Проверка данных в MongoDB:**
   - Вход в MongoDB:
     ```bash
     docker exec -it mongo_db mongosh -u root -p example --authenticationDatabase admin
     ```
   - Проверка количества документов в коллекции:
     ```bash
     use user_sessions;
     db.UserSessions.find().count();
     ```
   - Результат: `100` документов.

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
     SELECT * FROM user_sessions;
     ```
   - Результат: данные из MongoDB успешно реплицированы в PostgreSQL.
```
session_id              |               user_id                |     start_time      |      end_time       |                                                                                                                                                        pages_visited                                                                                                                                                         |                                                                       device                                                                       |                             actions
--------------------------------------+--------------------------------------+---------------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------
 5ffc1153-d477-4716-b3bf-3582e6d35ea8 | ab445ef4-f9ab-4e16-bf0b-69713e7e3b31 | 2025-02-14 22:49:57 | 2025-01-09 09:47:34 | ["https://www.phillips.com/", "http://martin.com/", "http://www.nelson.info/"]                                                                                                                                                                                                                                               | Mozilla/5.0 (iPod; U; CPU iPhone OS 3_3 like Mac OS X; cs-CZ) AppleWebKit/534.28.6 (KHTML, like Gecko) Version/3.0.5 Mobile/8B111 Safari/6534.28.6 | ["but"]
 5443ae0a-3bb0-4e38-9d36-17a9402307cf | f60f35e2-ebfa-4694-8352-2df67d0b1124 | 2025-02-17 02:28:10 | 2025-02-02 09:08:23 | ["https://hudson.net/", "https://www.delgado-graham.com/", "http://www.powers-brown.com/", "https://rivera.net/", "http://fisher.com/", "http://ramirez.com/", "http://www.aguirre-hurst.com/", "http://www.smith-cox.info/"]                                                                                                | Mozilla/5.0 (Android 4.0.1; Mobile; rv:9.0) Gecko/9.0 Firefox/9.0                                                                                  | ["evening", "view"]
 24b2bd34-bba8-4b6a-a394-c37565966b03 | e285128f-72d7-41f4-8d01-1124a4a04b58 | 2025-01-24 20:12:48 | 2025-01-28 12:32:00 | ["http://gray-harris.com/", "http://bell.com/", "http://obrien.com/", "http://thornton-knapp.com/"]                                                                                                                                                                                                                          | Opera/9.49.(X11; Linux x86_64; mni-IN) Presto/2.9.169 Version/11.00                                                                                | ["other", "here"]
 de4c5a89-7379-49cc-9f6e-68af46121e58 | 79013c18-ba09-49c8-82af-708643699e64 | 2025-03-11 14:18:53 | 2025-02-03 12:09:17 | ["https://goodman-guerrero.com/", "https://www.blackburn.org/", "http://www.durham.biz/", "https://marquez-thompson.com/", "http://www.diaz.com/", "https://buckley-vargas.com/", "https://www.alvarez.biz/", "https://www.johnson.org/"]                                                                                    | Mozilla/5.0 (compatible; MSIE 9.0; Windows 98; Win 9x 4.90; Trident/3.1)                                                                           | ["similar", "family", "sure", "security"]
```
