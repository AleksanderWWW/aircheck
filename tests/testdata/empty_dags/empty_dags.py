from datetime import datetime, timedelta

from airflow import DAG

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="empty_dag",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    ...


with DAG(
    dag_id="empty_dag1",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag1:
    ...
