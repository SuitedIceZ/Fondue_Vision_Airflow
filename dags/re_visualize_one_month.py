from dotenv import dotenv_values
# Load environment variables from .env file
env_vars = dotenv_values()

import sys
sys.path.insert(0, env_vars['FILE_PLUGINS_PATH'])

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator

# implemented plugins pythonOperator
import scraping_data_call
import preprocess_data_call
import model_predict_call
import extract_top_word_call
import drive_upload_viz_call

from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
import csv




# Set the default arguments for the DAG
default_args = {
    'owner': 'FondueVision',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2023, 6, 19),
}

# Define the DAG
dag = DAG(
    'Re_Visualize_One_Month',
    default_args=default_args,
    description='Re-Visualize every one month DAG',
    schedule_interval=timedelta(days=30),
    catchup=False,
)

# Define the tasks
scraping_data = PythonOperator(
    task_id='scraping_data',
    dag=dag,
    python_callable=scraping_data_call.scrape_from_traffy,
)

# include drop table & translate & tokenization
preprocess_data = PythonOperator(
    task_id='preprocess_data',
    dag=dag,
    python_callable=preprocess_data_call.preprocess_data,
)

predict_with_model = PythonOperator(
    task_id='predict_with_model',
    dag=dag,
    python_callable=model_predict_call.relabel_data,
)

count_top_word = PythonOperator(
    task_id='count_top_word',
    dag=dag,
    python_callable=extract_top_word_call.extract_top_word,
)

send_to_visualize_frontend = PythonOperator(
    task_id='send_to_visualize_frontend',
    dag=dag,
    python_callable=drive_upload_viz_call.upload_to_drive,
)


# Set the task dependencies
scraping_data >> preprocess_data >> predict_with_model >> count_top_word >> send_to_visualize_frontend
