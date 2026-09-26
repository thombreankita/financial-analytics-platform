*** DBT Notes***

## SQL transforms the data. dbt transforms how SQL transformations are organized, connected, tested, documented, and executed.##

Q1. What problem does dbt solve that plain SQL does not? 
Ans: Version control for SQL. Plain SQL in stored procedures or views has no version history. You cannot see who changed what and when. dbt models are .sql files in Git — every change is tracked, reviewable, and reversible.

Dependency management. If mart_fraud_summary depends on stg_transactions which depends on raw data — plain SQL has no way to know this chain. If you drop stg_transactions, mart_fraud_summary breaks silently. dbt knows the full dependency graph and runs models in the correct order automatically.

Testing built in. Plain SQL has no testing framework. dbt has dbt test which runs schema tests on every model automatically.Often queries depend on multiple tables and the datatype of these table columns might be different sometimes, even if the data is same for ex. one table might have period as varchar and another might have the column as the datetime viz used in the a view. that can be a solution when the dbt is used as dbt handles the structure of each table.

Q2 — What is a dbt model?
Ans: A dbt model is just a .sql file with a SELECT statement. dbt handles the CREATE TABLE or CREATE VIEW part for you. Wedon't need to write any DDL. Additionally,because you only write SELECT statements, every dbt model is rerunnable. Run it twice, get the same result. This is idempotency.

Q3. What is the difference between a view materialisation and a table materialisation?
Ans: view materialization is when a view is called as the data is not stored physically it is computed as and when the view is called. Table materialisation I think isfaster becase the data is stored in a physical table.
View — no data stored, always reads from source at query time. Use when: data changes frequently, downstream query volume is low, you want always-fresh data.
Table — data physically stored, faster to query. Use when: the model is queried frequently, the underlying query is expensive, you want to avoid recomputing every time.
The rule of thumb: staging models are usually views (lightweight, always fresh), mart models are usually tables (queried by Power BI repeatedly, must be fast).

Q4. What is data lineage and why does it matter?
Ans: If the source data or file changes, it might affect all the parts depending on that file. If a pipe fails at any point of time without lienage it becomes difficult to manually trace which tables it depends on. With dbt lineage you open the lineage graph and immediately sees which table depends on which one For ex.: mart_daily_fraud_summary → stg_transactions → raw.paysim. You check stg_transactions first. The fix is in one place. Total diagnosis time: 2 minutes instead of 20.

Q5. What does {{ ref('stg_transactions') }} do in a dbt model?
Ans: {{ ref('stg_transactions') }} does two things:
First — it resolves to the correct table name in the correct schema for your environment. In development it might be dev.stg_transactions. In production prod.stg_transactions. You never hardcode environment names.
Second — and this is the important one — dbt uses ref() to build its dependency graph. When dbt sees ref('stg_transactions') inside mart_daily_fraud_summary, it knows: run stg_transactions first, then run mart_daily_fraud_summary. Without ref(), dbt is blind to this dependency and might run models in the wrong order.
One-sentence summary: ref() is how dbt knows what depends on what, and how it ensures models always run in the correct order.

Notes: Git and dbt solve completely different problems. Git is a version control system that tracks changes to files and enables collaboration. dbt is a transformation framework that understands the relationships between data models, manages dependencies, enables testing and documentation, and orchestrates SQL transformations. In practice, production teams use both together because they complement each other.
SQL transforms data; dbt provides the engineering framework for organizing, connecting, testing, documenting, and executing SQL transformations at scale.
dbt manages the transformation layer inside/against the warehouse.
The warehouse is still responsible for storing and processing the data.

## Connection vs Cursor:
The connection establishes communication between the database and the program.
The cursor is what you use to execute SQL statements through that connection.

In dbt specifically, SELECT * breaks lineage tracking. dbt cannot document columns it does not know about explicitly. When you run dbt docs generate, undeclared columns from SELECT * do not appear in the documentation. Always select columns explicitly so dbt knows what your model produces.

Q1. Your staging model reads from paysim_raw which is raw data you loaded externally — not a dbt model. To reference it in dbt you use {{ source() }} not {{ ref() }}. What is the difference between the two and when do you use each?
Ans: {{ source() }} is usually used to reference a dataset external to the dbt. For any table created and situated inside the dbt we use {{ ref() }} as {{ ref() }} helps creates a linkage between the tables in our dbt. any table derieved from paysim_raw   willbe using {{ ref() }}. but since the  paysim_raw is the base inside the dbt we use {{ source() }}  here.

Q3: You will write SELECT with explicit column selection — no SELECT *.
Ans:It means that for the staging purpose only the views are created. whatever data will be the result of staging it will be created as a view.Only the gold layer will be created as a physical table.

--> The view stored no data. When you queried stg_transactions, DuckDB executed the underlying SELECT statement against paysim_raw in real time. The view is just a saved query — a named SQL expression. Every time you query it, it reads from paysim_raw fresh. This is why views are appropriate for staging — they are always current and use zero additional storage.
-->The WARNING says models.financial_analytics.marts has no resources.It means dbt_project.yml has a config block for marts but no SQL files exist in models/marts/ yet. dbt is telling you the config exists but has nothing to apply it to.
The view stored no data. When you queried stg_transactions, DuckDB executed the underlying SELECT statement against paysim_raw in real time. The view is just a saved query — a named SQL expression. Every time you query it, it reads from paysim_raw fresh. This is why views are appropriate for staging — they are always current and use zero additional storage.

### A data test is a SQL query that tries to find bad records or SELECT statements that seek to return failing records.

--> generic tests are parameterized queries that accept arguments.
Normally, a data test query will calculate failures as part of its execution. If you set the optional --store-failures flag, the store_failures, or the store_failures_as configs, dbt will first save the results of a test query to a table in the database, and then query that table to calculate the number of failures.

| Test              | Question                                |
| ----------------- | --------------------------------------- |
| `unique`          | Are there duplicates?                   |
| `not_null`        | Are there NULLs?                        |
| `accepted_values` | Are values from the allowed list?       |
| `relationships`   | Does this value exist in another model? |

--> specifically recommend testing assumptions about source data.

Q1. dbt has four built-in schema tests.
- The four built in schemas are unique, not null, relatioships and accepted values. Unique test returns the rows which are not unique stating where the test fails, not null checks if any rows have null value, relationships checks the referential integrity and accepted values check if the correct vales are present or any additional values in specified columns are also present.

Q2.Your stg_transactions has an is_fraud column that should only contain 0 or 1. Which built-in test catches this?
- accepted values catches it

Q3. What is the difference between a schema test and a custom data test in dbt?
- custom data tests are built based on the specific business logic that is needed in any particuar cas. Schema tests will only check for any data or integrity constraints mainly.

Q4. A failing dbt test means data quality issue found. What should happen in your pipeline when dbt test fails — should the pipeline stop, log and continue, or something else? And who decides this — the data engineer or the business?
- The data engineer defines which tests are blocking and which are warnings. In dbt you can set severity: warn on a test so it logs the failure but does not stop the pipeline. Without that setting, a failed test returns a non-zero exit code which Airflow treats as a task failure and stops the DAG. So the engineer decides by configuring severity — the business decides which data quality rules are non-negotiable.Critical tests — like not_null on sender_id or accepted_values on is_fraud — should be blocking. If fraud labels are corrupted, everything downstream is wrong. Less critical tests — like balance anomaly checks — can be warnings that log and continue.


Q1: Your mart model uses {{ ref('stg_transactions') }} not {{ source() }}. Write the exact FROM clause you will use.
-> select * from {{ ref('stg_transactions') }}

Q2: Your mart model is materialised as a table — set in dbt_project.yml. What does this mean differently from the staging view? Why does the mart layer need to be a table specifically?
the mart layer has the tables that are directly fetched in the powerbi thus the fetch operation is faster on the table and hence the mart layer is materialised as table

Q3: Write the business question this mart model answers in one sentence. Every model should have a clear purpose.
-> this mart model gives the summary of the data viz. PaySim and how many records are frauds and belong to which transaction type

Q1. What is the difference between {{ ref() }} and {{ source() }} in dbt? Give an example of when you used each in your project.
Ans: ref() is used when the table or view that needs to be considered as source is already present inside dbt. Using ref() creates a linkage between thetables thus stating what all tables and views are getting affected if there is any change in one of the table.
source() is used when the data source needed is to be referenced from outside the dbt i.e. external source to dbt needs to be fetched.

Q2. What is the difference between a view materialisation and a table materialisation? Why did you choose view for staging and table for marts?
Ans: View materialisation creates the view in runtime, while the table materialisation stores the resultset in a physical table that can be easily fetched in the final application thus reducing the fetching overhead. Thus the table materialisation is used in the marts as the physical tables can be easily fetched in the application.

Q3. If a dbt test fails in production at 6am, walk through your exact response process — what do you check first, second, third?
Ans: Step 1- Run the dbt test. Identify which test has failed. the failing test will specify the column name that gave the issue.
Step 2 - check the source if the nulls are also present in the source table.
Step 3 -IF the nulls are not present in source, and the column giving issue is a critical column, block the pipeline until issue is fixed. If the column is not severe and doesn't affect the results, a warning must be raised but no need to block the pipe.

Q4. What is data lineage and how does dbt's ref() function enable it? What would break if you hardcoded table names instead of using ref()?
Ans: Data lineage shows which table is dependent on which table, basically maintaining a track of dependency. If the table names are directly hardcoded then if any table structure gets changed, the changes also need to implemented in the dependent tables and the hardcoded table names make it tideious to backtrack. Lineage on the other hand readily has the list of dependent views that can be modified as required.

Q5. You have 13 tests passing. A new engineer joins and adds a column to paysim_raw that contains nulls. Which of your tests would catch this and which would not? Why?
Ans: This test could not be noticed untill the pipeline failes at production because there is no entry of this new column in the schema file, thus this will go unnoticed. This is because we have not used select * in our transactioin.sql, wehave specified the column names required. The lineage tracks model dependencies, not column changes. Thus the new column will be completely ignored in the staging table itself
