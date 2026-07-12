from pathlib import Path
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

def create_s_session(app_name: str ) -> SparkSession:
    spark = (SparkSession.builder.appName(app_name).master("local[*]").getOrCreate())
    return spark

def load_data_spark(spark: SparkSession, filepath: str) -> DataFrame:
    df = spark.read.csv(filepath, header = "true", inferSchema="true")
    df.printSchema()
    df.show(5)
    print(f'Row Count: {df.count()}')
    return df

def main():
    fpath = str(Path(__file__).parent.parent / "data" /"raw"/"PS_20174392719_1491204439457_log.csv")
    sp_sess = create_s_session("FinancialAnalytics")
    df = load_data_spark(sp_sess,fpath)
    sp_sess.stop()

 
if __name__ == "__main__":
    main()


