from datetime import datetime, timedelta
from pytz import timezone
from airflow import DAG
from airflow.operators.bash import BashOperator

# Set the timezone to Casablanca
casablanca_tz = timezone('Africa/Casablanca')

default_args = {
    'owner': 'akram_fouguir',
    'depends_on_past': False,
    'start_date': datetime.now(casablanca_tz),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'Weather_app',
    default_args=default_args,
    description='An Airflow DAG to fetch weather data and update the CSV file',
    schedule_interval='0 */3 * * *',  # Run every 3 hours
    max_active_runs=1,  # Ensure only one run at a time
    catchup=False,  # Do not run backfill for the intervals between start_date and the current date
)



# Task to execute the Python script
execute_script_task_1 = BashOperator(
    task_id='task_1',
    bash_command='python /opt/airflow/dags/scripts/main.py',
    dag=dag
)

# Task to execute the Python script
execute_script_task_2 = BashOperator(
    task_id='task_2',
    bash_command='python /opt/airflow/dags/scripts/Projet_ML2.py',
    dag=dag
)

execute_script_task_3 = BashOperator(
    task_id='task_3',
    bash_command='streamlit run --server.address 0.0.0.0 --server.enableWebsocketCompression=false --server.enableCORS=false --server.enableXsrfProtection=false /opt/airflow/dags/scripts/streamlit/streamlit_app.py',
    dag=dag
)

# Set task dependencies
execute_script_task_1 >> execute_script_task_2 >> execute_script_task_3
