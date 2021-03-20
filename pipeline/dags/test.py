from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def print_john():
    print("john")
    return "john printed successfully"


dag = DAG(
    dag_id="john_test", default_args={"owner": "airflow", "start_date": days_ago(2)}
)

t1 = PythonOperator(task_id="print_john", python_callable=print_john, dag=dag)

t1