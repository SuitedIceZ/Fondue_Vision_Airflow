from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

# Set the default arguments for the DAG
default_args = {
    'owner': 'FondueVision',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2023, 1, 1),
}

# Define the DAG
dag = DAG(
    'Re_Visualize_One_Month',
    default_args=default_args,
    description='Re Visualize every one month DAG',
    schedule_interval=timedelta(days=30),
    catchup=False,
)

# Define the tasks
scraping_data = DummyOperator(
    task_id='scraping_data',
    dag=dag,
)
# include drop table & translate & tokenization
preprocess_data = DummyOperator(
    task_id='preprocess_data',
    dag=dag,
)

predict_with_model = DummyOperator(
    task_id='predict_with_model',
    dag=dag,
)

send_to_visualize_frontend = DummyOperator(
    task_id='send_to_visualize_frontend',
    dag=dag,
)


# Set the task dependencies
scraping_data >> preprocess_data >> predict_with_model >> send_to_visualize_frontend
