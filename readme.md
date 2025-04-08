# Обработка JSON-данных в Yandex Data Proc с Spark

Проект для обработки JSON-файлов с помощью Apache Spark в кластере Yandex Data Proc.

## Инструкция по запуску

### 1. Подготовка кластера

```bash
# Подключение к мастер-ноде
ssh -i ~/.ssh/your_key dataproc@<публичный_IP_кластера>
2. Запуск обработки данных

Шаги
•       Чтение JSON
•       Развертывание вложенных структур
•       Сохранение в Parquet
•       Проверку результатов
pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# 1. Чтение JSON
df = spark.read.option("multiline", True).json("s3a://study-backet/storage/catalog_ex.json")
df.printSchema()

# 2. Обработка catalogs
explode_catalogs = df.select(F.explode('catalogs'))
explode_catalogs.printSchema()

catalogs = explode_catalogs.select('col.*')
catalogs.write.parquet("s3a://study-backet/results/catalogs.parquet")

# 3. Проверка catalogs
read_catalogs = spark.read.parquet("s3a://study-backet/results/catalogs.parquet")
read_catalogs.show()

# 4. Обработка offers
explode_offers = df.select(F.explode('offers'))
explode_offers.printSchema()
offers = explode_offers.select('col.*')
offers.write.parquet("s3a://study-backet/results/offers.parquet")

# 5. Проверка offers
read_offers = spark.read.parquet("s3a://study-backet/results/offers.parquet")
read_offers.show()

