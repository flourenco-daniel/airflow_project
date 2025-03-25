from airflow.decorators import dag, task
from datetime import datetime



@dag(
    dag_id='taskflow_with_decorator',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['taskflow']
)

def taskflow():
    
    @task
    def task_a():
        print("Task A")
        return 42

    @task
    def task_b(value):
        print("Task B")
        print(value)

    task_b(task_a())

taskflow()