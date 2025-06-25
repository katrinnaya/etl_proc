#!/usr/bin/env python3

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_json, struct, col

def main():
    spark = None
    try:
        # 1. Инициализация Spark с подробным логированием
        spark = SparkSession.builder \
            .appName("transactions-to-kafka") \
            .config("spark.sql.shuffle.partitions", "2") \
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider") \
            .config("spark.hadoop.fs.s3a.endpoint", "storage.yandexcloud.net") \
            .getOrCreate()
        
        spark.sparkContext.setLogLevel("INFO")
        print("Spark session created successfully")

        # 2. Чтение данных из S3
        print("🔍 Reading parquet file from s3a://etl-bucket/transactions.parquet")
        df = spark.read.parquet("s3a://etl-bucket/transactions.parquet")
        print(f"Successfully loaded {df.count()} rows")
        df.show(5, truncate=False)

        # 3. Подготовка данных для Kafka
        kafka_df = df.select(
            to_json(struct([col(c) for c in df.columns])).alias("value")
        )
        print("Sample Kafka message:")
        kafka_df.show(5, truncate=False)

        # 4. Отправка в Kafka
        print("Sending data to Kafka...")
        kafka_df.write.format("kafka") \
            .option("kafka.bootstrap.servers", "rc1b-fbg7mfam0tpd6g0r.mdb.yandexcloud.net:9091") \
            .option("topic", "transactions-topic") \
            .option("kafka.security.protocol", "SASL_SSL") \
            .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
            .option("kafka.sasl.jaas.config",
                   "org.apache.kafka.common.security.scram.ScramLoginModule required "
                   "username=\"user1\" "
                   "password=\"useruser1\";") \
            .save()
        
        print("Data successfully sent to Kafka!")
        sys.exit(0)
        
    except Exception as e:
        print(f"Critical error: {str(e)}", file=sys.stderr)
        if spark:
            spark.sparkContext.parallelize([str(e)]).saveAsTextFile("s3a://etl-bucket/error-log")
        sys.exit(1)
    finally:
        if spark:
            spark.stop()
            print("Spark session stopped")

if __name__ == "__main__":
    main()