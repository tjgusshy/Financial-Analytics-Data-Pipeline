"""
Sample Airflow DAG for running dbt models
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_sample_dag',
    default_args=default_args,
    description='A simple DAG to run dbt models',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 11, 15),
    catchup=False,
    tags=['dbt', 'sample'],
) as dag:

    dbt_debug = BashOperator(
        task_id='dbt_debug',
        bash_command='cd /dbt && dbt debug',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /dbt && dbt run',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /dbt && dbt test',
    )

    dbt_debug >> dbt_run >> dbt_test
