from dotenv import dotenv_values
# Load environment variables from .env file
env_vars = dotenv_values()

import sys
sys.path.insert(0, env_vars['FILE_PLUGINS_PATH'])

import drive_upload_call
import drive_download_call

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
default_args = {
    'owner': 'FondueVision',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

def greet():
    print('Hello, world!')

with DAG(
    default_args=default_args,
    dag_id='create_dag_with_python_operator',
    description="Our first DAG with PythonOperator",
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
    )
    upload_csv = PythonOperator(
        task_id='upload_csv',
        python_callable=drive_upload_call.upload_to_drive,
    )
    download_csv = PythonOperator(
        task_id='download_csv',
        python_callable=drive_download_call.download_from_drive,
    )

# Set the task dependencies
task1 >> upload_csv >> download_csv
