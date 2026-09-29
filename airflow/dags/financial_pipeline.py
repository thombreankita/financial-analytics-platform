from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_ingestion():
    print{f'Ingestion starting'}

with DAG(
    dag_id='financial_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    run_ingestion = PythonOperator(
        task_id = "Ingest data"
        python_callable = run_ingestion
    )