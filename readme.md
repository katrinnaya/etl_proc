# Финальное задание по модулю 2. Работа с Яндекс.Облаком
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
### Шаг 3
Пишем Python-скрипт для создания датасета. См. файл `create_db` в папке `scripts`. Файл с датасетом `transactions_v2.csv` сохраняем локально
### Шаг 4
Загружаем данные в YDB через YDB CLI
4.1 Устанавливаем клиент
`curl -sSL https://install.ydb.tech/cli | bash`
4.2 Устанавливаем утилиту
`curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash`
4.3 Пишем скрипт на заливку данных в YDB. См. файл `upload_to_ydb.py` в папке `scripts`.
