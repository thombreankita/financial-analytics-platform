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
The real problem with inferSchema is:
Spark reads a sample of the data to guess types. If the first 100 rows of amount are all whole numbers, Spark might infer integer instead of double. Row 50,000 has 9839.64 — now your pipeline fails or silently truncates decimals.
In production you define the schema explicitly using StructType so the types are guaranteed regardless of what the data looks like. 