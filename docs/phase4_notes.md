Q1 — What is a DAG?
Ans: A DAG is the definition/container of the workflow and its dependencies.Directed → relationships have a direction: A → B means A comes before B.
Acyclic → you cannot eventually come back to where you started. No A → B → C → A loop.
Graph → a collection of things (nodes) connected by relationships.
So in Airflow:
Ingest → Validate → Transform → Load
is a DAG.

Q2 — What is the difference between a DAG and a task?
Ans: DAG is an approach that decides the order in which the tasks to be executed. Tasks I think are the individual operations that needs to be executed.Tasks are the individual units of work.
DAG = workflow structure + dependencies
Task = individual unit of work

Q3 — What is an Operator in Airflow?
Ans: An Airflow Operator is essentially a template/class that defines a type of work a task can perform.
Task = an instance of work in your DAG.
Operator = the mechanism/type that tells Airflow what kind of work that task performs.
PythonOperator — executes a Python function. You will use this to call your main() function from ingestion/ingest.py.
BashOperator — executes a bash command. You will use this to run dbt run and dbt test commands.
DummyOperator — does nothing. Used as a placeholder or to group tasks visually in complex DAGs.

Q4 — What does catchup=False do?
Ans:Your DAG has a start_date — say January 1, 2024. If you deploy it today in September 2026 with catchup=True, Airflow would try to run the DAG for every scheduled interval between January 2024 and today. For a daily DAG that would be hundreds of runs fired simultaneously. This almost always crashes your system.
catchup=False tells Airflow — only run from now forward, ignore the gap between start_date and today. This is what you want in almost every production scenario.

Q5 — What is idempotency in a pipeline context?
Ans: In pipeline context, idempotency means that no matter how many times we run the pipe it will give the same results. An operation is idempotent if executing it multiple times produces the same final state as executing it once.

Q6 — What does the >> operator do in an Airflow DAG?
python
ingest >> validate >> dbt_run
What does this line mean? What happens if validate fails — does dbt_run still execute?
Ans: The >> operator is Airflow's way of expressing a dependency between tasks. Run ingest before validate, and run validate before dbt_run.dbt_run won't execute because its upstream dependency, validate, did not successfully complete. >> means establishes a dependency.Airflow then uses that dependency to determine whether a task is eligible to run.

## Airflow doesn't replace your ingestion, validation, PySpark/dbt logic. It orchestrates them. ##
