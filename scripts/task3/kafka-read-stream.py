#!/usr/bin/env python3

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DecimalType, TimestampType
import sys
import time

def main():
    spark = None
    try:
        # 1. Инициализация Spark с явным указанием пакетов
        spark = SparkSession.builder \
            .appName("transactions-kafka-to-postgres") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.postgresql:postgresql:42.5.4") \
            .config("spark.executor.memory", "2g") \
            .config("spark.driver.memory", "2g") \
            .config("spark.sql.shuffle.partitions", "2") \
            .getOrCreate()
        
        spark.sparkContext.setLogLevel("INFO")
        print("🟢 Spark session initialized")

        # 2. Проверка подключения к PostgreSQL перед началом
        print("🔍 Testing PostgreSQL connection...")
        test_df = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://rc1d-2cujrbr0l1vrep9c.mdb.yandexcloud.net:6432/db_for_etl") \
            .option("dbtable", "(SELECT 1 AS test) t") \
            .option("user", "user") \
            .option("password", "password") \
            .option("sslmode", "require") \
            .load()
        
        print(f"✅ PostgreSQL connection test passed: {test_df.collect()}")

        # 3. Определение схемы Kafka
        schema = StructType([
            StructField("transaction_id", StringType(), False),
            StructField("user_id", StringType(), False),
            StructField("amount", DecimalType(15, 2), False),
            StructField("currency", StringType(), False),
            StructField("transaction_date", TimestampType(), False),
            StructField("status", StringType(), False),
            StructField("merchant", StringType(), False)
        ])

        # 4. Чтение из Kafka
        kafka_df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "rc1b-fbg7mfam0tpd6g0r.mdb.yandexcloud.net:9091") \
            .option("subscribe", "transactions-topic") \
            .option("startingOffsets", "earliest") \
            .option("kafka.security.protocol", "SASL_SSL") \
            .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
            .option("kafka.sasl.jaas.config", 
                    "org.apache.kafka.common.security.scram.ScramLoginModule required "
                    "username=\"user1\" "
                    "password=\"useruser1\";") \
            .load()

        # 5. Парсинг данных
        parsed_df = kafka_df \
            .selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), schema).alias("data")) \
            .select("data.*") \
            .withColumn("user_id", col("user_id").cast("integer"))

        # 6. Запись в PostgreSQL с обработкой ошибок
        def write_to_postgres(batch_df, batch_id):
            try:
                print(f"Processing batch {batch_id} with {batch_df.count()} rows")
                batch_df.write \
                    .format("jdbc") \
                    .option("url", "jdbc:postgresql://rc1d-2cujrbr0l1vrep9c.mdb.yandexcloud.net:6432/db_for_etl") \
                    .option("dbtable", "transactions_stream") \
                    .option("user", "user") \
                    .option("password", "password") \
                    .option("sslmode", "require") \
                    .mode("append") \
                    .save()
                print(f"✅ Batch {batch_id} written to PostgreSQL")
            except Exception as e:
                print(f"❌ Error writing batch {batch_id}: {str(e)}")
                raise

        query = parsed_df.writeStream \
            .foreachBatch(write_to_postgres) \
            .trigger(processingTime="10 seconds") \
            .start()

        print("🚀 Streaming query started")
        query.awaitTermination()

    except Exception as e:
        print(f"🔥 Critical error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        if spark:
            spark.stop()
            print("🔴 Spark session stopped")

if __name__ == "__main__":
    main()