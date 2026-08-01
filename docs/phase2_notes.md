Q1 — What is lazy evaluation?
Ans: Instead of processing the computations immediately, Spark remebers the opeations that needs to be done. When the user explicitly asks for the data only then it computes all the operations and then shows the final result. This results in efficient execution as the computation only happens at the time when the data actually needs to be given.

Q2 — What is the difference between a transformation and an action?
Ans: Any operation to be performed on the data set is a transformation and any operation that outputs the data explicitly is an action.
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
- Lazy evaluation improves performance because Spark dosen't need to do the transformation applied dataset/dataframe at every step. It simply stores all the operations and performs when its time to explicitly show the data. Thus no need to store and carry heavily transformed dataframe at everystep thus reducing the loading time for each subsequent transformation i.e. no need to store intermediate DataFrames at every step. 
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
local[*] — tasks run in parallel across all cores, faster for large data.
In production Spark does not run locally at all — it runs on a cluster where the master URL is something like spark://host:7077. local[*] is a development convenience that simulates a cluster on your own machine.


Partitions:
Partition = Piece of data
↓
Spark creates one Task for that partition
↓
A Worker executes that Task

# All actions are initiated and coordinated by the Driver. Some actions return results to the Driver (like show(), count(), collect()), while others perform work externally (like write()) and only return the status of the operation.

inferSchema:
Spark reads data to determine the types before building the final DataFrame schema. it has to inspect data before deciding on the schema. Thus in case of huge filespark inspects first with infer schema and then for operations/ action. Result increased I/O

The real problem with inferSchema is:
Spark reads a sample of the data to guess types. If the first 100 rows of amount are all whole numbers, Spark might infer integer instead of double. Row 50,000 has 9839.64 — now your pipeline fails or silently truncates decimals.
In production you define the schema explicitly using StructType so the types are guaranteed regardless of what the data looks like. 
Thus schema inference requires Spark to inspect the data before processing it, which adds overhead. More importantly, inferred types can change as the input data changes, leading to inconsistent pipelines. In production, I prefer defining an explicit schema so the pipeline is faster, deterministic, and aligned with business expectations.

orderBy():
orderBy is a wide transformation because it requires a shuffle. All data must be sorted globally across partitions, not just within each partition. This is one of the most expensive operations in Spark. In production you only sort when absolutely necessary.

* Output of volume aggregation is like 8.550078961000006E7. Spark is displaying large doubles in scientific notation. This is fine for pipeline processing but will need formatting in Power BI *

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


 If Spark has reliable statistics and the estimated size of one side is below the configured threshold (by default around 10 MB, though this is configurable), it can automatically choose a broadcast join.
 So yes, Spark can automatically broadcast.
Q."Why do we use broadcast() if Spark can automatically broadcast?"
Ans: Spark can automatically choose a broadcast join when it has accurate statistics and the table is below the auto-broadcast threshold. The broadcast() function is a hint to the optimizer, allowing the developer to influence the execution plan when they know broadcasting is appropriate or when automatic detection may not choose it.

 193,505 is 3% of 6.3M rows. Think about it from the other direction — if you flag 3% of all transactions as HIGH risk, a fraud analyst has to investigate 190,000 cases. That is too many to be actionable. The real confirmed fraud is 8,213 rows — 0.13%. Your threshold of 3x average is catching a lot of high-value legitimate transactions alongside actual fraud. This is the classic precision vs recall tradeoff in fraud detection.

 TRANSFER transactions have the highest fraud rate at 0.77% (4,097 fraud out of 532,909 total). CASH_OUT is second at 0.18%. CASH_IN, PAYMENT, and DEBIT have zero confirmed fraud in PaySim. This validates the Phase 1 business rule targeting TRANSFER balance anomalies as the primary fraud detection signal.

Functionalities of all the functions:
calculate_daily_transaction_volume — groups 6.3M rows into 744 steps × ~5 types = 2,729 summary rows. Rows collapsed.
flag_high_risk_transactions — adds a column to every existing row. Row count unchanged at 6,362,620.
calculate_fraudrate_by_type — groups by type only = 5 rows. One row per transaction type.

### The pattern: aggregations reduce rows, withColumn preserves rows.

Spark partitions are logical chunks of data used during execution for parallel processing.
Partitioned Parquet files are a storage layout where data is organized into directories (such as year=2025/month=07) so Spark can skip entire folders using partition pruning. partition pruning is powerful—it avoids unnecessary disk I/O before any data is read.
"Parquet is a columnar storage format that enables column pruning and predicate pushdown. When the data is also stored using directory partitioning, Spark can apply partition pruning to skip entire folders. Together, these optimizations drastically reduce disk I/O, making Parquet much faster than CSV for analytical workloads."
When would you use partitionBy()? --> choose partition columns based on expected query patterns and cardinality. The goal is to maximize partition pruning while avoiding excessive small files.

No partitionBy ==> One Spark partition → One output file
With partitionBy("type") ==> Spark creates folders:

output/
├── type=PAYMENT/
├── type=CASH_OUT/
├── type=TRANSFER/
...

Inside each folder there may be:

part-0000.parquet
part-0001.parquet

The number of files is not simply the number of transaction types.

It depends on:

Spark partitions
How the data is distributed
How tasks write their output

Why are too many small Parquet files bad?
1. Filesystem Metadata Overhead
Every file has its own metadata (file name, size, permissions, timestamps, etc.).
The operating system or distributed filesystem must manage metadata for every single file.
Millions of small files consume significantly more metadata resources than a few large files.

Example:

❌ 20,000 files × 100 KB each
✅ 20 files × 100 MB each

Both store the same amount of data, but the second option is much more efficient.

2. File Open/Close Overhead (Disk I/O)

Before Spark can read a file, it must:

Locate the file.
Read its metadata.
Open the file.
Read the data.
Close the file.

With thousands of tiny files, Spark spends a large amount of time opening and closing files instead of processing data.

Result: Increased I/O overhead and slower jobs.

3. Task Scheduling Overhead

Spark generally creates one read task per input partition/file.

If there are:

20 files → ~20 tasks ✅
20,000 files → ~20,000 tasks ❌

The driver now has to:

Schedule thousands of tasks.
Track task execution.
Manage task completion.

The scheduling overhead itself becomes expensive.

==> Creating too many small Parquet files hurts Spark performance because it increases filesystem metadata overhead, file open/close I/O overhead, and task scheduling overhead. Instead of spending time processing data, Spark spends a significant amount of time managing files.

repartition(n) changes the number of Spark execution partitions, and during a write, each partition is typically written as a separate output file.
repartition(500) performs a shuffle to create exactly 500 Spark execution partitions. When the DataFrame is written, each partition is typically written as one Parquet file, resulting in about 500 output files. Although repartitioning adds an expensive shuffle, it helps avoid the small files problem and creates a more efficient dataset for future reads by reducing file management and task scheduling overhead."

Does repartition(500) always produce exactly 500 Parquet files?"
"It generally produces about 500 output files when writing normally. However, if partitionBy() is used, the final number of files depends on how the execution partitions are distributed across the storage partitions. A single execution partition can write files into multiple partition directories, so the output file count is not guaranteed to be exactly 500."

Method Chaining in Spark is called Fluent Interface
Ex. df.filter().select().groupBy()
Ex. df.write.mode().partitionBy().parquet()


Spark uses immutable DataFrames and writers because every transformation returns a new logical plan instead of modifying the existing object. This makes lazy evaluation, optimization, and reuse of the original DataFrame possible.

A good partition column has low to moderate cardinality and is frequently used in filters. risk has only two values (HIGH, LOW), so Spark creates only two partition directories, making partition pruning highly effective. nameOrig has millions of unique values, which would create millions of directories and tiny files, causing the small files problem with very little pruning benefit because queries rarely filter on a single account ID.

inferSchema:
Spark reads the data to determine the data types before building the final DataFrame schema.
It has to inspect the data before deciding on the schema.
Thus, in the case of huge files, Spark first inspects the data using inferSchema and then performs operations/actions.
Result: Increased I/O.

Q.Why does PySpark need Hadoop at all when running in local[] mode with no cluster?
Ans: PySpark is built on top of Hadoop's filesystem abstraction layer — called HDFS — even when running locally. When you write files, Spark uses Hadoop's file system APIs under the hood to handle permissions, directory creation, and file writes. On Linux/Mac this works without winutils because the native libraries are compatible. On Windows, Spark needs winutils.exe to translate Hadoop's Unix file system calls into Windows equivalents. Without it, any operation that touches the filesystem — including writing Parquet — fails.

After writing the output we see '_SUCCESS' and '._SUCCESS.crc' files in every output folder. These are Hadoop marker files — Spark writes them to signal that a job completed successfully. They contain no data. Every downstream tool that reads Parquet knows to ignore them.