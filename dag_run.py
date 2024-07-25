
from datetime import datetime

from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.dbt.cloud.operators.dbt import (
    DbtCloudRunJobOperator,
)

with DAG(
    dag_id="dbt_cloud_job_runner",
    default_args={"dbt_cloud_conn_id": "dbt_cloud", "account_id": 247356},
    start_date=datetime(2021, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    # extract = DummyOperator(task_id="extract")
    # load = DummyOperator(task_id="load")
    # ml_training = DummyOperator(task_id="ml_training")

    # trigger_dbt_cloud_job_run = DbtCloudRunJobOperator(
    #     task_id="trigger_dbt_cloud_job_run",
    #     job_id=65767,
    #     check_interval=10,
    #     timeout=300,
    # )

    run_dbt_job_development = DbtCloudRunJobOperator(
    task_id='run_dbt_cloud_job_development',
    job_id=538687,
    check_interval=10,
    timeout=300,
    )

    run_dbt_job_production = DbtCloudRunJobOperator(
        task_id='run_dbt_cloud_job_production',
        job_id=539456,
        check_interval=10,
        timeout=300,
    )

    run_dbt_job_development >> run_dbt_job_production 