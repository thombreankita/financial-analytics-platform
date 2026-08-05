*** DBT Notes***

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