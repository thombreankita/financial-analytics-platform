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
    df_grp = df.groupBy('type').agg(F.avg('amount').alias('avg_amount'))
    #F.broadcast(df_grp)
    df_join = df.join(F.broadcast(df_grp), on = 'type')
    df_new = df_join.withColumn('risk',F.when(df_join['amount']>3*df_join['avg_amount'], 'HIGH').when(df_join['isFraud'] == 1,'HIGH')
                                    .otherwise('LOW'))
    cols = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 
        'newbalanceOrig', 'nameDest', 'oldbalanceDest', 
        'newbalanceDest', 'isFraud', 'risk', 'isFlaggedFraud']
    df_new = df_new.select(cols)
    #df_new=df_new.drop('avg_amount')
    return df_new

def calculate_fraudrate_by_type (df: DataFrame) -> DataFrame:
    """
    Calculates the fraud rates by transaction types
    """
    df_g = df.groupBy('type').agg(F.sum('isFraud').alias('fraud_transactions'),
                                  F.count('*').alias('total_transactions'),
                                  F.round((F.sum('isFraud')/F.count('*')*100),2).alias('fraud_rate'))
    df_g = df_g.orderBy('fraud_rate', ascending = False)
    return df_g

def main():
    fpath = str(Path(__file__).parent.parent / "data" /"raw"/"PS_20174392719_1491204439457_log.csv")
    sp_sess = create_s_session("FinancialAnalytics")
    df = load_data_spark(sp_sess,fpath)
    volumndf = calculate_daily_transaction_volume(df)
    volumndf.show(20)
    print(f'Volumn aggregation: {volumndf.count()}')
    risk_df = flag_high_risk_transactions(df)
    risk_df.show(10)
    print(f'High risk transactions: {risk_df.filter(risk_df["risk"] == "HIGH").count()}')
    print(f'Total transactions: {risk_df.count()}')
    fraud_rate = calculate_fraudrate_by_type(risk_df)
    fraud_rate.show(20)
    sp_sess.stop()

 
if __name__ == "__main__":
    main()


