# Перенос базы данных из Yandex Managed Service for PostgreSQL в Yandex Object Storage
## Создание кластера-источника Managed Service for PostgreSQL
![claster](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/claster.jpg)
## Создание простой таблицы в кластере
![db](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/db.jpg) 
## Проверка, что таблица создана
![db1](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/db1.jpg) 
## Добавление ролей сервисному аккаунту
![serv](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/serv.jpg) 
## Создание эндпоинтов приемник и источник
![endp](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/endp.jpg) 
## Запуск трансфера
![tr1](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/tr1.jpg) 
## Проверка работы копирования в бакет
![buck1](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/buck1.jpg) 
## Внесение изменений в исходную таблицу
![db2](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/db2.jpg) 
## Проверка работы копирования при повторной активации
![buck2](https://github.com/katrinnaya/etl_proc/blob/hw_10/images/buck2.jpg) 
### Файлы
* `public_test_products.csv` - файл после первой активации
* `public_test_products (1).csv` - файл после повторной активации с изменением таблицы

