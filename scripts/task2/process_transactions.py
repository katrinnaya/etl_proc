from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum

def main():
    # Инициализация Spark с настройками для Yandex Object Storage
    spark = SparkSession.builder \
        .appName("TransactionAnalysis") \
        .config("spark.hadoop.fs.s3a.endpoint", "storage.yandexcloud.net") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .getOrCreate()
    
    try:
        # 1. Чтение данных
        input_path = "s3a://etl-bucket/input/transactions_v2.csv"
        df = spark.read.option("header", "true").csv(input_path)
        
        # 2. Фильтрация failed-транзакций
        failed_transactions = df.filter(col("status") == "failed")
        
        # 3. Аналитика
        print("\n=== Основная статистика ===")
        print(f"Всего failed-транзакций: {failed_transactions.count()}")
        
        # Аналитика по валютам
        currency_stats = failed_transactions.groupBy("currency") \
            .agg(
                count("*").alias("count"),
                spark_sum("amount").alias("total_amount")
            ) \
            .orderBy("currency")
        
        print("\n=== Статистика по валютам ===")
        currency_stats.show(truncate=False)
        
        # Топ-5 мерчантов по количеству failed-транзакций
        merchant_stats = failed_transactions.groupBy("merchant") \
            .agg(count("*").alias("failed_count")) \
            .orderBy(col("failed_count").desc()) \
            .limit(5)
        
        print("\n=== Топ-5 мерчантов по failed-транзакциям ===")
        merchant_stats.show(truncate=False)
        
        # 4. Сохранение результатов
        output_path = "s3a://etl-bucket/output/failed_transactions/"
        stats_path = "s3a://etl-bucket/output/transaction_stats/"
        
        print(f"\nСохранение failed-транзакций в: {output_path}")
        failed_transactions.write.mode("overwrite").parquet(output_path)
        
        print(f"Сохранение статистики в: {stats_path}")
        currency_stats.write.mode("overwrite").parquet(f"{stats_path}currency_stats/")
        merchant_stats.write.mode("overwrite").parquet(f"{stats_path}merchant_stats/")
        
        print("\n✅ Обработка завершена успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()