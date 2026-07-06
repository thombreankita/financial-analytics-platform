# Financial Transactions Analytics Platform

> End-to-end data engineering pipeline on 6.3M synthetic financial transactions — built to demonstrate production-grade pipeline design, layered validation, and modern DE tooling.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![PySpark](https://img.shields.io/badge/PySpark-3.5-orange)](https://spark.apache.org)
[![dbt](https://img.shields.io/badge/dbt-1.8-red)](https://getdbt.com)
[![Airflow](https://img.shields.io/badge/Airflow-2.x-green)](https://airflow.apache.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## What This Project Does

Most DE portfolios show a dashboard. This project shows a **pipeline** — the engineering that makes dashboards trustworthy.

Starting from raw synthetic financial data (PaySim — 6.3 million transactions, fraud labels, realistic balance logic), this project builds every layer of a modern data stack from scratch:

- **Ingestion** — Python pipeline with layered validation catching bad data before it reaches downstream systems
- **Transformation** — PySpark aggregations on full 6.3M rows, written to Parquet
- **Modeling** — dbt staging and mart layers with automated data tests
- **Orchestration** — Apache Airflow DAG running the full pipeline on a schedule with retry logic
- **Reporting** — Power BI dashboard connected to the dbt mart layer

---

## Project Status

| Phase | Description | Status |
|---|---|---|
| Phase 0 | Python basics + environment setup | ✅ Complete |
| Phase 1 | Python ingestion layer with validation | ✅ Complete |
| Phase 2 | PySpark transformation layer | 🔄 In Progress |
| Phase 3 | dbt modeling layer | ⏳ Upcoming |
| Phase 4 | Airflow orchestration | ⏳ Upcoming |
| Phase 5 | Power BI dashboard + documentation | ⏳ Upcoming |

---

## Architecture

```
PaySim CSV (6.3M transactions)
        │
        ▼
┌─────────────────────┐
│   Python Ingestion  │  check_file_ready → required_columns
│   ingestion/        │  → validate_schema → validate_business_rules
│   ingest.py         │  → write_partitioned_output (by transaction type)
└────────┬────────────┘
         │ Partitioned CSV files (5 transaction types)
         ▼
┌─────────────────────┐
│  PySpark Transform  │  Daily volume aggregations
│  transformation/    │  Fraud rate by type
│  spark_transform.py │  High-risk transaction flagging
└────────┬────────────┘
         │ Parquet files
         ▼
┌─────────────────────┐
│   dbt Models        │  stg_transactions (staging + type checks)
│   dbt_project/      │  mart_daily_fraud_summary (Power BI ready)
│   models/           │  Automated tests on every column
└────────┬────────────┘
         │ DuckDB mart tables
         ▼
┌─────────────────────┐
│  Airflow DAG        │  Daily schedule
│  airflow/dags/      │  Retry logic (2 retries, 5 min delay)
│  financial_         │  Idempotent — safe to re-run
│  pipeline.py        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Power BI          │  Transaction volume trends
│   dashboards/       │  Fraud rate by type
│                     │  High-risk monitoring
└─────────────────────┘
```

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Ingestion | Python 3.11, Pandas | Pipeline-first Python — file handling, validation, partitioned output |
| Transformation | PySpark 3.5 | Full 6.3M row processing, columnar Parquet output |
| Modeling | dbt-duckdb 1.8 | Modular SQL, lineage tracking, automated tests |
| Orchestration | Apache Airflow 2.x | DAG scheduling, retry logic, failure handling |
| Warehouse | DuckDB | Zero-config local warehouse — fast, free, SQL-native |
| Reporting | Power BI | Executive-facing dashboards — DAX measures, live DuckDB connection |
| Testing | pytest | Automated validation tests — all ingestion functions covered |
| Version Control | Git + GitHub | Daily commits throughout development — full history visible |

---

## Dataset

**PaySim Synthetic Financial Dataset** — [Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)

- **6,362,620 transactions** across 31 simulated days (744 steps, 1 step = 1 hour)
- **5 transaction types** — PAYMENT, TRANSFER, CASH_OUT, DEBIT, CASH_IN
- **8,213 confirmed fraud transactions** (`isFraud = 1`)
- **16 system-flagged fraud transactions** (`isFlaggedFraud = 1`) — only 0.19% detection rate
- **11 columns** — sender/receiver identities, balances before and after, fraud labels

The gap between `isFraud` (8,213) and `isFlaggedFraud` (16) is what makes this dataset analytically interesting — the existing fraud detection system misses 99.8% of actual fraud.

---

## Phase 1 — Ingestion Layer (Complete)

### What Was Built

The ingestion layer is a four-function validation pipeline in `ingestion/validate.py` and `ingestion/ingest.py`.

**`check_file_ready(fp)`** — Hard validation before reading
- Checks file exists → raises `FileNotFoundError` with path context
- Checks `.csv` extension → raises `ValueError` for wrong format
- Checks non-empty file → raises `ValueError` for empty files

**`required_columns(df, required)`** — Schema presence check
- Collects ALL missing columns before raising — not just the first one
- Error message lists every missing column in one `ValueError`

**`validate_schema(df)`** — Data type enforcement
- Verifies 8 numeric columns have correct dtype using `pd.api.types.is_numeric_dtype`
- Calls `required_columns` internally — guaranteed columns exist before type check
- Raises `TypeError` with column name and actual type found

**`validate_business_rules(df)`** — Soft validation with threshold
- 6 domain-specific checks on actual data values
- Collects all violation counts before raising — soft validation pattern
- Raises `ValueError` only if any rule exceeds `VIOLATION_THRESHOLD` (5% of rows)
- Returns summary dict of violation counts per rule for logging

### Business Rules Validation Results on Full Dataset

| Rule | Violations | % of Total | Interpretation |
|---|---|---|---|
| Amount ≤ 0 | 16 | 0.00025% | Invalid transactions — drop in transformation |
| Same sender/receiver | 0 | 0% | Clean |
| Null critical columns | 0 | 0% | PaySim is synthetic — no missing data |
| TRANSFER balance mismatch | 8,105 | 0.13% | Merchant accounts (M prefix) don't record balance changes |
| DEBIT insufficient funds | 11,786 | 0.19% | Legitimate overdraft or fraud — flagged for analysis |
| Invalid transaction type | 0 | 0% | All types match expected values |

### Design Decisions Worth Discussing

**Hard vs soft validation** — Schema violations (wrong column, wrong type) raise immediately and stop the pipeline. Business rule violations are collected and summarised — bad rows are logged, not silently dropped, and the pipeline continues unless violation rate exceeds 5%.

**Partitioned output by transaction type** — Writing 5 separate CSV files instead of one large file means downstream PySpark jobs can process only the transaction type they need. If CASH_OUT transformation fails, PAYMENT data is unaffected.

**Idempotency** — Running the pipeline twice produces identical output. All write operations use overwrite mode. Verified by running the full pipeline twice and comparing row counts.

### Pipeline Output

```
Pipeline Started....
Loading Raw Data....
Rows Loaded: 6,362,620
File Validation: Passed
Schema Validation: Passed
Business Rule Validation Summary:
  {'Amount': 16, 'Error': 0, 'Not Null_Columns': 0,
   'Transfer_valid': 8105, 'Debit_valid': 11786, 'Type_valid': 0}
Writing Partitioned Output........
  {'PAYMENT': 2151495, 'TRANSFER': 532909, 'CASH_OUT': 2237500,
   'DEBIT': 41432, 'CASH_IN': 1399284}
Pipeline Completed. Total Time: 54.6 seconds
```

---

## How to Run Locally

**Requirements**
- Python 3.11
- Java 11 (required for PySpark)
- Git

**Setup**

```bash
# Clone the repository
git clone https://github.com/thombreankita/financial-analytics-platform.git
cd financial-analytics-platform

# Create and activate virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
# source .venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

**Download Dataset**

Download PaySim from [Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1) and place the CSV in:
```
data/raw/PS_20174392719_1491204439457_log.csv
```

**Run the ingestion pipeline**

```bash
# Development run — 10,000 rows, fast feedback
python -m ingestion.ingest

# Full run — 6.3M rows, ~55 seconds
# Change nrows=10000 to nrows=None in main() first
python -m ingestion.ingest
```

**Run tests**

```bash
python -m pytest tests/ -v
```

---

## Repository Structure

```
financial-analytics-platform/
│
├── ingestion/
│   ├── ingest.py           # Main pipeline — load, validate, partition
│   └── validate.py         # Four validation functions
│
├── transformation/
│   └── spark_transform.py  # PySpark aggregations (Phase 2)
│
├── dbt_project/
│   └── models/
│       ├── staging/        # stg_transactions.sql
│       └── marts/          # mart_daily_fraud_summary.sql
│
├── airflow/
│   └── dags/
│       └── financial_pipeline.py   # Full pipeline DAG
│
├── dashboards/
│   └── financial_analytics.pbix
│
├── tests/
│   └── test_validate.py    # pytest suite for all validation functions
│
├── docs/
│   ├── phase1_notes.md     # Data understanding + design decisions
│   └── article_drafts/     # Writing anchor articles (in progress)
│
├── data/
│   ├── raw/                # PaySim CSV (gitignored — too large)
│   └── processed/          # Pipeline output (gitignored)
│
├── requirements.txt
└── README.md
```

---

## What I Would Do Differently in Production

**Alerting** — Failed pipeline tasks would send alerts via PagerDuty or Slack webhook. Right now failures print to terminal. In production, nobody watches terminals at 3am.

**Incremental loading** — Currently the pipeline re-processes all 6.3M rows on every run. In production with daily transaction feeds, only new records would be processed using Airflow's `execution_date` and dbt incremental materialisation.

**Data quality monitoring** — The business rules validation produces a summary dict. In production this would write to a monitoring table and feed a data quality dashboard — not just print to console.

**Secrets management** — Credentials and connection strings would use environment variables with a `.env` file locally and a secrets manager (Azure Key Vault, AWS Secrets Manager) in production. Currently local paths are used.

**Containerisation** — The pipeline would run inside a Docker container in production for environment consistency. Airflow tasks would be `DockerOperator` calls, not `PythonOperator`.

**Unit test coverage** — Current pytest suite covers validation functions. Production would add integration tests covering the full pipeline end-to-end and data contract tests between each layer.

---

## About This Project

This project is being built in parallel with a full-time data engineering role at L&T Technology Services, where I work on Azure Synapse and Microsoft Fabric pipelines for financial reporting. The goal is to bridge from enterprise Microsoft-stack work into modern open-source DE tooling — and to build every layer from scratch rather than follow a tutorial.

Every commit in this repository represents real work, real errors hit and debugged, and real design decisions made and documented.

**Author:** Ankita Thombre
**LinkedIn:** [linkedin.com/in/ankitathombre](https://linkedin.com/in/ankitathombre)
**GitHub:** [github.com/thombreankita](https://github.com/thombreankita)
