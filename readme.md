# Работа с Apache Kafka в PySpark: запись и чтение сообщений
### Цель:
Записать сообщения в топик Apache Kafka® и прочитать сообщения из топика с помощью PySpark-задания в Yandex Data Processing.
## Шаги
1. Добавление сервисному аккауну необходимых ролей 
2. Создание бакета и загрузка скриптов чтения и записи
3. Создание кластера Managed Service for Kafka
4. Создание топика в кластере
5. Создание кластера Yandex Data Processing для выполнения PySpark-задания
6. Создание задания в кластере с типом `PySpark`
7. Запуск задания со скриптом на запись
8. Запуск задания со скриптом на чтение
9. Проверка результатов в бакете

# Шаг 1
Для сервисного аккаунта добавляем роли 
* `storage.viewer`;
* `storage.uploader`;
* `dataproc.agent`;
* `dataproc.user`.
# Шаг 2
Создаем бакет `dataproc-bucket-for-etl` и помещаем в него скрипты `kafka-write.py` и `kafka-read-stream.py`
![buc](https://github.com/katrinnaya/etl_proc/blob/hw_13/images/buc.jpg) 
Даем `FULL_CONTROL` разрешение сервисному аккаунту
# Шаг 3
Создаем кластер Managed Service for Kafka `dataproc-kafka`
![kaf](https://github.com/katrinnaya/etl_proc/blob/hw_13/images/kaf.jpg) 
# Шаг 4
Создаем топик `dataproc-kafka-topic` и создаем пользователя Kafka с разрешением на все топики
# Шаг 5
Создаем кластер Yandex Data Processing `dataproc-cluster`
![dp](https://github.com/katrinnaya/etl_proc/blob/hw_13/images/dp.jpg) 
# Шаг 6
Создаем задание со скриптом на запись и запускаем
![wr](https://github.com/katrinnaya/etl_proc/blob/hw_13/images/wr.jpg) 
# Шаг 7
Создаем задание со скриптом на чтение и запускаем
![read](https://github.com/katrinnaya/etl_proc/blob/hw_13/images/read.jpg) 
# Шаг 8
В бакете проверяем результат
![res1](https://github.com/katrinnaya/etl_proc/blob/hw_13/images/res1.jpg) 
![res2](https://github.com/katrinnaya/etl_proc/blob/hw_13/images/res2.jpg) 
