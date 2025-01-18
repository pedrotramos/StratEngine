from airflow.decorators import dag, task
from pendulum import datetime, timezone


@dag(
    start_date=datetime(2025, 1, 1, tz=timezone("America/Sao_Paulo")),
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Pedro", "retries": 3},
    tags=["Demo"],
)
def generate_portfolio():
    @task
    def test():
        print("Hello")

    test()


generate_portfolio()
