# Обработка JSON-данных в Yandex Data Proc с Spark

Обработка JSON-файлов с помощью Apache Spark в кластере Yandex Data Proc.

## Запуск

### 1. Подготовка кластера
Создаем кластер Yandex Data Processing. В бакет ```study-backet ``` папку ``` storage ``` кладем пример json-файла ```catalog_ex.json```
#### 1.1. Подключаемся к мастер-ноде по ssh
``` ssh -i ~/.ssh/your_key ubuntu@<публичный_IP_кластера> ```
#### 1.1. Инициализириуем сессию PySpark
``` pyspark ```
### 2. Запуск обработки данных
```
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
```
#### Шаги
* Чтение JSON
* Развертывание вложенных структур
* Сохранение в Parquet
* Проверкf результатов
#### 1. Чтение JSON
```
df = spark.read.option("multiline", True).json("s3a://study-backet/storage/catalog_ex.json")
df.printSchema()
root
 |-- catalogs: array (nullable = true)
 |    |-- element: struct (containsNull = true)
 |    |    |-- conditions: string (nullable = true)
 |    |    |-- date_end: string (nullable = true)
 |    |    |-- date_start: string (nullable = true)
 |    |    |-- id: string (nullable = true)
 |    |    |-- image: string (nullable = true)
 |    |    |-- is_main: boolean (nullable = true)
 |    |    |-- offers: array (nullable = true)
 |    |    |    |-- element: string (containsNull = true)
 |    |    |-- target_regions: array (nullable = true)
 |    |    |    |-- element: string (containsNull = true)
 |    |    |-- target_shops: array (nullable = true)
 |    |    |    |-- element: string (containsNull = true)
 |-- offers: array (nullable = true)
 |    |-- element: struct (containsNull = true)
 |    |    |-- barcode: string (nullable = true)
 |    |    |-- date_end: string (nullable = true)
 |    |    |-- date_start: string (nullable = true)
 |    |    |-- description: string (nullable = true)
 |    |    |-- discount_label: string (nullable = true)
 |    |    |-- id: string (nullable = true)
 |    |    |-- image: string (nullable = true)
 |    |    |-- price_is_from: boolean (nullable = true)
 |    |    |-- price_new: long (nullable = true)
 |    |    |-- price_old: long (nullable = true)
 |-- version: long (nullable = true)
```
#### 2. Обработка catalogs
```
explode_catalogs = df.select(F.explode('catalogs'))
explode_catalogs.printSchema()
root
 |-- col: struct (nullable = true)
 |    |-- conditions: string (nullable = true)
 |    |-- date_end: string (nullable = true)
 |    |-- date_start: string (nullable = true)
 |    |-- id: string (nullable = true)
 |    |-- image: string (nullable = true)
 |    |-- is_main: boolean (nullable = true)
 |    |-- offers: array (nullable = true)
 |    |    |-- element: string (containsNull = true)
 |    |-- target_regions: array (nullable = true)
 |    |    |-- element: string (containsNull = true)
 |    |-- target_shops: array (nullable = true)
 |    |    |-- element: string (containsNull = true)
```
```
catalogs = explode_catalogs.select('col.*')
catalogs.write.parquet("s3a://study-backet/results/catalogs.parquet")
```
#### 3. Проверка catalogs
```
read_catalogs = spark.read.parquet("s3a://study-backet/results/catalogs.parquet")
read_catalogs.show() # Показ первых нескольких строк для проверки
+--------------------+----------+----------+----+--------------------+-------+--------------------+--------------------+--------------------+
|          conditions|  date_end|date_start|  id|               image|is_main|              offers|      target_regions|        target_shops|
+--------------------+----------+----------+----+--------------------+-------+--------------------+--------------------+--------------------+
|Предложения дейс...|2020-06-12|2020-06-05|1234|https://retailer1...|   true|[11111, 22222, 33...|[Россия, Москва, ...|                null|
|Предложения дейс...|2020-06-12|2020-06-05|5678|https://retailer1...|   true|      [22222, 33333]|                null|[Владимир, улица ...|
+--------------------+----------+----------+----+--------------------+-------+--------------------+--------------------+--------------------+
```
#### 4. Обработка offers
```
explode_offers = df.select(F.explode('offers'))
explode_offers.printSchema()
root
 |-- col: struct (nullable = true)
 |    |-- barcode: string (nullable = true)
 |    |-- date_end: string (nullable = true)
 |    |-- date_start: string (nullable = true)
 |    |-- description: string (nullable = true)
 |    |-- discount_label: string (nullable = true)
 |    |-- id: string (nullable = true)
 |    |-- image: string (nullable = true)
 |    |-- price_is_from: boolean (nullable = true)
 |    |-- price_new: long (nullable = true)
 |    |-- price_old: long (nullable = true)
```
```
offers = explode_offers.select('col.*')
offers.write.parquet("s3a://study-backet/results/offers.parquet")
```
#### 5. Проверка offers
```
read_offers = spark.read.parquet("s3a://study-backet/results/offers.parquet")
read_offers.show() # Показ первых нескольких строк для проверки
+-------------+----------+----------+--------------------+--------------+-----+--------------------+-------------+---------+---------+
|      barcode|  date_end|date_start|         description|discount_label|   id|               image|price_is_from|price_new|price_old|
+-------------+----------+----------+--------------------+--------------+-----+--------------------+-------------+---------+---------+
|7501031311309|2020-06-10|2020-06-05|Молоко "Домик в д...|           1+1|11111|https://retailer1...|        false|       50|      100|
|3113097501031|      null|      null|Огурцы маринованн...|          null|22222|https://retailer1...|        false|       70|       75|
|1097501031133|      null|      null|Жевательная резин...|          null|33333|https://retailer1...|         true|       10|     null|
+-------------+----------+----------+--------------------+--------------+-----+--------------------+-------------+---------+---------+
```
## Итог
* Файл до парсинга https://github.com/katrinnaya/etl_proc/blob/hw_9/jsons/catalog_ex.json , UI: ![before_parse](https://github.com/katrinnaya/etl_proc/blob/hw_9/images/before_parse.jpg)
* Файлы после парсинга: https://github.com/katrinnaya/etl_proc/tree/hw_9/jsons/parquets , UI: ![after_parse](https://github.com/katrinnaya/etl_proc/blob/hw_9/images/after_parse.jpg)
### 1. Catalogs
```
{"conditions":"Предложения действительны для Москвы, Переславль-Залесского и Костромской области. Информацию об ассортименте товаров, участвующих в акции, уточняйте в магазине. Количество товаров ограничено, не является публичной офертой.","date_end":"2020-06-12","date_start":"2020-06-05","id":"1234","image":"https://retailer1234.ru/catalogs/1234.jpg","is_main":true,"offers":["11111","22222","33333"],"target_regions":["Россия, Москва","Россия, Ярославская область, Переславль-Залесский","Россия, Костромская область, Островский район, село Адищево"],"target_shops":null}
{"conditions":"Предложения действительны в магазине по адресу: Владимир, улица Куйбышева, 26К","date_end":"2020-06-12","date_start":"2020-06-05","id":"5678","image":"https://retailer1234.ru/catalogs/1234.jpg","is_main":true,"offers":["22222","33333"],"target_regions":null,"target_shops":["Владимир, улица Куйбышева, 26К"]}
```
### 2. Offers
```
{"barcode":"7501031311309","date_end":"2020-06-10","date_start":"2020-06-05","description":"Молоко \"Домик в деревне\" 3,2% 0,93 л","discount_label":"1+1","id":"11111","image":"https://retailer1234.ru/offers/1234567.jpg","price_is_from":false,"price_new":50,"price_old":100}
{"barcode":"3113097501031","date_end":null,"date_start":null,"description":"Огурцы маринованные \"Дядя Ваня\" 680 г","discount_label":null,"id":"22222","image":"https://retailer1234.ru/offers/5671234.jpg","price_is_from":false,"price_new":70,"price_old":75}
{"barcode":"1097501031133","date_end":null,"date_start":null,"description":"Жевательная резинка Orbit в ассортименте","discount_label":null,"id":"33333","image":"https://retailer1234.ru/offers/10488.jpg","price_is_from":true,"price_new":10,"price_old":null}
```
