from pathlib import Path
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType
from pyspark.sql import functions as F

def create_s_session(app_name: str ) -> SparkSession:
    spark = (SparkSession.builder.appName(app_name).master("local[*]").getOrCreate())
    return spark

def load_data_spark(spark: SparkSession, filepath: str) -> DataFrame:
    schema = StructType([
    StructField("step", IntegerType(), True),
    StructField("type", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("nameOrig", StringType(), True),
    StructField("oldbalanceOrg", DoubleType(), True),
    StructField("newbalanceOrig", DoubleType(), True),
    StructField("nameDest", StringType(), True),
    StructField("oldbalanceDest", DoubleType(), True),
    StructField("newbalanceDest", DoubleType(), True),
    StructField("isFraud", IntegerType(), True),
    StructField("isFlaggedFraud", IntegerType(), True),
    ])
    df = spark.read.csv(filepath, header=True, schema=schema)
    #df = spark.read.csv(filepath, header = True, inferSchema="true")
    df.printSchema()
    df.show(5)
    print(f'Row Count: {df.count()}')
    return df

def calculate_daily_transaction_volume(df: DataFrame) -> DataFrame:
    df_r = df.groupBy('step','type').agg(
        F.count('*').alias('transaction_count'),
        F.sum('amount').alias('total_amount'),
        F.avg('amount').alias('avg_amount')
    ).orderBy('step')
    return df_r
    
def flag_high_risk_transactions(df: DataFrame) -> DataFrame:
    """
    Adds a risk_level column — HIGH or LOW.
    HIGH if amount > 3x type average OR isFraud == 1.
    Uses a broadcast join on type averages.
    """

def main():
    fpath = str(Path(__file__).parent.parent / "data" /"raw"/"PS_20174392719_1491204439457_log.csv")
    sp_sess = create_s_session("FinancialAnalytics")
    df = load_data_spark(sp_sess,fpath)
    volumndf = calculate_daily_transaction_volume(df)
    volumndf.show(20)
    print(f'Volumn aggregation: {volumndf.count()}')
    sp_sess.stop()

 
if __name__ == "__main__":
    main()


