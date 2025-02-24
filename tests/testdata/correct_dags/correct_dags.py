from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ABC-dag1",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag1:
    Variable.get("env")
    start = EmptyOperator(task_id="start")

    def print_hello():
        print("Hello from DAG 1!")

    task1 = PythonOperator(
        task_id="print_hello",
        python_callable=print_hello,
    )

    end = EmptyOperator(task_id="end")

    start >> task1 >> end


with DAG(
    dag_id="ABC-dag2",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag2:
    start = EmptyOperator(task_id="start")

    def print_hello():
        print("Hello from DAG 2!")

    task1 = PythonOperator(
        task_id="print_hello",
        python_callable=print_hello,
    )

    end = EmptyOperator(task_id="end")

    start >> task1 >> end
