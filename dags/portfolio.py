from airflow.decorators import dag
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from pendulum import datetime, timezone


@dag(
    start_date=datetime(2025, 1, 1, tz=timezone("America/Sao_Paulo")),
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Pedro", "retries": 0},
    tags=["Demo"],
)
def generate_portfolio():

    fetch_index_data = EcsRunTaskOperator(
        task_id="fetch_index_data",
        aws_conn_id="aws_ecr",
        cluster="AirflowECSCluster",
        task_definition="qam-tasks",
        launch_type="FARGATE",
        overrides={
            "containerOverrides": [
                {
                    "name": "task-executor",
                    "command": [
                        "fetch_indexes.py",
                        "--incremental_load",
                        "{{ dag_run.conf.get('incremental_load', True) | lower }}",
                    ],
                }
            ],
        },
        network_configuration={
            "awsvpcConfiguration": {
                "subnets": ["subnet-0714335b648c47443"],
                "securityGroups": ["sg-05fbf576de1cad860"],
                "assignPublicIp": "ENABLED",
            }
        },
        region="sa-east-1",
    )

    fetch_stock_data = EcsRunTaskOperator(
        task_id="fetch_stock_data",
        aws_conn_id="aws_ecr",
        cluster="AirflowECSCluster",
        task_definition="qam-tasks",
        launch_type="FARGATE",
        overrides={
            "containerOverrides": [
                {
                    "name": "task-executor",
                    "command": [
                        "fetch_stocks.py",
                        "--incremental_load",
                        "{{ dag_run.conf.get('incremental_load', True) | lower }}",
                    ],
                }
            ],
        },
        network_configuration={
            "awsvpcConfiguration": {
                "subnets": ["subnet-0714335b648c47443"],
                "securityGroups": ["sg-05fbf576de1cad860"],
                "assignPublicIp": "ENABLED",
            }
        },
        region="sa-east-1",
    )

    pick_stocks = EcsRunTaskOperator(
        task_id="pick_stocks",
        aws_conn_id="aws_ecr",
        cluster="AirflowECSCluster",
        task_definition="qam-tasks",
        launch_type="FARGATE",
        overrides={
            "containerOverrides": [
                {
                    "name": "task-executor",
                    "command": [
                        "pick_stocks.py",
                        "--start_date",
                        "{{ macros.ds_add(ds, -30) }}",
                        "--end_date",
                        "{{ ds }}",
                    ],
                }
            ],
        },
        network_configuration={
            "awsvpcConfiguration": {
                "subnets": ["subnet-0714335b648c47443"],
                "securityGroups": ["sg-05fbf576de1cad860"],
                "assignPublicIp": "ENABLED",
            }
        },
        region="sa-east-1",
    )

    [fetch_index_data, fetch_stock_data] >> pick_stocks


generate_portfolio()
