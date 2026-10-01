from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def ingestion_task():
    print('Ingestion starting')


def validation_task():
    print('Validation complete')

with DAG(
    dag_id='financial_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    run_ingestion = PythonOperator(
        task_id = "Ingest_data",
        python_callable = ingestion_task
    )

    run_validation  = PythonOperator(
        task_id = "Validate_data",
        python_callable = validation_task
    )

    run_ingestion >> run_validation