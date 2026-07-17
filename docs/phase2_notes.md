Q1 — What is lazy evaluation?
Ans: Instead of processing the computations immediately, Spark remebers the opeations that needs to be done. When the user explicitly asks for the data only then it computes all the operations and then shows the final result. This results in efficient execution as the computation only happens at the time when the data actually needs to be given.

Q2 — What is the difference between a transformation and an action?
Ans: Any operation to be performed on the data set is a transformation and any operation that outputs the data explicitly is an action.
Classify each of these as transformation or action and explain your reasoning:
df.filter(...) ==> transformation
df.groupBy(...).agg(...) ==> transformation
df.show() ==> action
df.count() ==> action
df.write.parquet(...) ==> action
df.select(...) ==> transformation

## If Spark has to return a final result to you, it's probably an Action. ##

Q3 — What is a DAG in the Spark context?
Ans: Directed Acyclic Graphs in Spark are related to the lazy evaluation. Spark remembers the operations to be performed, creates an optimised execution plan and then execute. This optimised execution plan uses DAG. Spark's DAG is optimised by the Catalyst Optimizer before execution. It can reorder operations, push filters down to run earlier, and combine steps. This is why Spark can sometimes be faster than hand-written optimised SQL — the optimizer does work you did not ask for.

Q4 — Why does lazy evaluation improve performance?
Ans: 
- Lazy evaluation improves performance because Spark dosen't need to the transformation applied dataset/dataframe at every step. It simply stores all the operations and performs when its time to explicitly show the data. Thus no need to store and carry heavily transformed dataframe at everystep thus reducing the loading time for each subsequent transformation i.e. no need to store intermediate DataFrames at every step. 
- Predicate pushdown. Because Spark has the full plan before executing, it can push a filter operation all the way down to the data source — reading only the rows it needs from disk rather than reading everything and then filtering. Without lazy evaluation this is impossible because Spark would have already read all the data before it knew about the filter.

Q5 — What is the difference between a narrow transformation and a wide transformation?
Ans: Narrow transformation run on individual partitions, are faster as no shuffle is involved. Wide transformations transfer data between the partitions, this is a slow transfer hence expensive.
Narrow: filter(), select(), map() — each partition processes independently
Wide: groupBy(), join(), orderBy() — data must move between partitions, called a shuffle
shuffles are expensive because data travels across the network between executor nodes. Minimising wide transformations is one of the primary PySpark optimisation strategies.

## SparkSession.builder.master("local[*]").getOrCreate().stop():
Here [*] means use all available CPU cores on your machine — whatever number that is. If your machine has 8 cores, local[*] gives Spark all 8. If it has 4, it gets 4.
It is not adaptive. It is simply "use everything available right now."
The difference matters because:

local[1] — tasks run one at a time, sequentially
local[*] — tasks run in parallel across all cores, faster for large data

In production Spark does not run locally at all — it runs on a cluster where the master URL is something like spark://host:7077. local[*] is a development convenience that simulates a cluster on your own machine.

Partitions:
Partition = Piece of data

↓

Spark creates one Task for that partition

↓

A Worker executes that Task

# All actions are initiated and coordinated by the Driver. Some actions return results to the Driver (like show(), count(), collect()), while others perform work externally (like write()) and only return the status of the operation.

inferSchema:
Spark reads data to determine the types before building the final DataFrame schema. it has to inspect data before deciding on the schema. Thus in case of huge filespark inspects first with infer schema and hten for operations/ action. Result increased I/O

The real problem with inferSchema is:
Spark reads a sample of the data to guess types. If the first 100 rows of amount are all whole numbers, Spark might infer integer instead of double. Row 50,000 has 9839.64 — now your pipeline fails or silently truncates decimals.
In production you define the schema explicitly using StructType so the types are guaranteed regardless of what the data looks like. 
Thus schema inference requires Spark to inspect the data before processing it, which adds overhead. More importantly, inferred types can change as the input data changes, leading to inconsistent pipelines. In production, I prefer defining an explicit schema so the pipeline is faster, deterministic, and aligned with business expectations.

orderBy():
orderBy is a wide transformation because it requires a shuffle. All data must be sorted globally across partitions, not just within each partition. This is one of the most expensive operations in Spark. In production you only sort when absolutely necessary.

Output of volume aggregation is like 8.550078961000006E7. Spark is displaying large doubles in scientific notation. This is fine for pipeline processing but will need formatting in Power BI

Q1: Your aggregation produced 2,729 rows from 6.3M. Where did the other rows go — what happened to them conceptually?
-->  Conceptually, the 6.3M rows are grouped together based on their similarity viz. step and type in our case - aggregation collapses rows into groups. The 6.3M individual transaction rows are reduced to 2,729 group summaries. The original rows are not deleted — they are summarised. The original DataFrame df still exists in memory unchanged. Only volume_df has 2,729 rows.

Q2: groupBy is a wide transformation. What happened under the hood when Spark executed it — what is a shuffle and why did it happen here specifically?
--> In a wide transformation, we cannot rely on one executor to run and compute individually because same data can be present at the othe partitions or executors, thus they need to exchange the information. This transfer of data or exchange between the executors is called shuffle and it happened bcoz we used groupBy().
Each executor writes its partial results to disk — this is the shuffle write
Other executors read from those disk locations to collect all rows belonging to the same group — this is the shuffle read
The driver does not get involved in moving data — executors talk to each other
The driver only receives the final result when an action like show() or count() is called.

Q3: Look at step 1, TRANSFER row:
276 transactions | 1.24E8 total | 450,352 average
The average TRANSFER amount is ₹450,352. The average PAYMENT is ₹6,090. What does this tell you about the fraud risk profile of TRANSFER transactions compared to PAYMENT? 
--> TRANSFER transactions have 74x higher average amount than PAYMENT transactions. This cross-referenced that with Phase 1 validation I found 8,105 TRANSFER balance anomalies — where newbalanceDest did not increase after a transfer. High-value transactions with missing destination balance updates are the strongest fraud signal in this dataset, thus we will use this as our fraud risk flagging logic.

## SPARK##
                     Spark
                        │
        ┌───────────────┴────────────────┐
        │                                │
  Architecture                     DataFrame API
        │                                │
 Driver, Executor                  read()
 Partitions                        select()
 Tasks                             filter()
 DAG                               withColumn()
 Lazy Evaluation                   groupBy()
 Catalyst                          join()