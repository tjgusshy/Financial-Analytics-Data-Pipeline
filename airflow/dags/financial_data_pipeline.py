"""
Complete Airflow DAG for generating and loading financial data
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'financial_data_pipeline',
    default_args=default_args,
    description='Generate synthetic financial data and run dbt transformations',
    schedule_interval='@daily',
    start_date=datetime(2025, 11, 15),
    catchup=False,
    tags=['financial', 'dbt', 'etl'],
) as dag:

    # Step 1: Generate synthetic data
    generate_data = BashOperator(
        task_id='generate_financial_data',
        bash_command='cd /dbt && python scripts/generate_financial_data.py',
    )

    # Step 2: Load data into PostgreSQL
    load_data = BashOperator(
        task_id='load_data_to_postgres',
        bash_command='cd /dbt && python scripts/load_data.py',
    )

    # Step 3: Run dbt models
    dbt_run = BashOperator(
        task_id='dbt_run_models',
        bash_command='cd /dbt && dbt run',
    )

    # Step 4: Run dbt tests
    dbt_test = BashOperator(
        task_id='dbt_test_models',
        bash_command='cd /dbt && dbt test',
    )

    # Define task dependencies
    generate_data >> load_data >> dbt_run >> dbt_test
