from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

import sys

sys.path.append("/opt/airflow/src")

from load_raw_penguins import load_raw_penguins
from preprocess_data import preprocess_data
from train_model import train_model

with DAG(
    dag_id="penguins_pipeline",
    start_date=datetime(2026, 3, 1),
    schedule=None,
    catchup=False,
    tags=["penguins", "mlops"],
) as dag:

    truncate_raw_table = SQLExecuteQueryOperator(
        task_id="truncate_raw_table",
        conn_id="mysql_penguins",
        sql="TRUNCATE TABLE penguins_raw;"
    )

    load_raw_task = PythonOperator(
        task_id="load_raw_penguins",
        python_callable=load_raw_penguins
    )

    preprocess_task = PythonOperator(
        task_id="preprocess_penguins",
        python_callable=preprocess_data
    )

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )

    truncate_raw_table >> load_raw_task >> preprocess_task >> train_task
