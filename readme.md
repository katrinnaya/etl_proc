# Создание Python-приложения для работы с Yandex Managed Service for YDB
## Шаги выполнения
1. Добавление сервисному аккаунту необходимых ролей
2. Создание базы данных YDB
3. Создание тестовой базы данных
4. Создание функции в Cloud Functions
5. Конфигурация переменных окружения
6. Тестирование функции
## Шаг 1
Добавляем сервисному аккаунта роль `editor` для управления YDB
## Шаг 2
1. Создаем БД YDB с типом `Serverless`
![ydb](https://github.com/katrinnaya/etl_proc/blob/hw_12/images/ydb.jpg)  
2. Получаем параметры подключения и сохраняем значение для дальнейшего подключения
   * `Эндпоинт`
## Шаг 3
Создаем через веб-интерфейс тестовую БД
![db](https://github.com/katrinnaya/etl_proc/blob/hw_12/images/db.jpg)  
## Шаг 4
1. Создаем Python-функцию `index.py`
2. Создаем файл с зависимостями `requirements.txt`
## Шаг 5
Настраиваем переменные окружения
  * `YDB_ENDPOINT`
  * `YDB_DATABASE`

![func](https://github.com/katrinnaya/etl_proc/blob/hw_12/images/func.jpg)  
## Шаг 6
Запускаем тест

![test](https://github.com/katrinnaya/etl_proc/blob/hw_12/images/test.jpg)  
