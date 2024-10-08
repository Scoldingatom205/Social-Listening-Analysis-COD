# Airflow DAGs
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'cod_analysis_pipeline',
    default_args=default_args,
    description='A DAG for COD Data Collection, Preprocessing, and Analysis',
    schedule_interval='@daily',  # Adjust as necessary
    start_date=days_ago(1),
    catchup=False
) as dag:

    # Task 1: Collect data from Steam and Reddit
    def collect_data():
        from scripts.extract_data import run_data_collection
        run_data_collection()

    collect_data_task = PythonOperator(
        task_id='collect_data',
        python_callable=collect_data
    )

    # Task 2: Preprocess the collected data
    def preprocess_data():
        from scripts.preprocess_data import run_preprocessing
        run_preprocessing()

    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data
    )

    # Task 3: Perform sentiment analysis and topic modeling
    def run_analysis():
        from scripts.analysis import run_analysis
        run_analysis()

    analysis_task = PythonOperator(
        task_id='perform_analysis',
        python_callable=run_analysis
    )

    # Task 4: Store the analysis results into MongoDB
    def store_data():
        from scripts.store_data import run_storage
        run_storage()

    store_data_task = PythonOperator(
        task_id='store_data',
        python_callable=store_data
    )

    # Task dependencies
    collect_data_task >> preprocess_data_task >> analysis_task >> store_data_task
