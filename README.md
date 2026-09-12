# Banking DWH & Anti-Fraud Analytical Pipeline

A synthetic data pipeline and analytical layer modeling a retail banking data warehouse (DWH) for fraud detection, operational monitoring, and risk scoring.

## Architecture
- **Ingestion Layer (`/src` & `main.py`)**: Decoupled Python ETL pipeline leveraging SQLAlchemy, Pandas, and Faker to seed a relational PostgreSQL schema preserving foreign keys, chronological logic, and realistic weighted distributions.
- **Analytical Layer (`/sql`)**:
  - `01_fraud_monitoring.sql`: Merchant failure rate analysis using conditional aggregation (`COUNT CASE WHEN`).
  - `02_velocity_checks.sql`: Rapid succession detection using window functions (`LAG()`) to flag potential card abuse within 10-minute thresholds.
  - `03_customer_risk_mart.sql`: Customer risk profiling view (`v_customer_risk_profile`) calculating transactional volume, ticket sizes, and behavioral risk scoring (`HIGH`, `MEDIUM`, `LOW`).

### Database Schema (ERD)
![Banking Schema ERD](docs/images/schema_bank_erd_new.png)

## Tech Stack
- **Database**: PostgreSQL
- **Languages & Frameworks**: Python 3.14, SQLAlchemy, Pandas, psycopg2-binary
- **Environment & VCS**: Virtualenv, Git (Conventional Commits)

## Getting Started

### 1. **Repository Setup**
```bash
git clone https://github.com/dannygavrilyak/bank-structured-data.git
cd bank-structured-data
```

## 2. **Create and activate a virtual environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```
## 3.**Configure .env**:

    DB_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

## 4. **Schema Provisioning (DDL Bootstrap)**

Deploy the 3NF relational schema (tables, sequences, foreign keys) before running ingestion:

```bash 
psql -U postgres -d postgres -f sql/00_init_schema.sql
```
Alternatively, execute sql/00_init_schema.sql directly inside DBeaver or your preferred database client.

## 5. **Run the pipeline**:

    python3 main.py

## 6. **Analytical Marts & Monitoring**

Run fraud detection and velocity check queries against the populated warehouse:

    sql/01_fraud_monitoring.sql: Merchant failure rate & abnormal reversal metrics.
    sql/02_velocity_checks.sql: Rapid-succession transaction patterns via window functions (LAG()).
    sql/03_customer_risk_mart.sql: Production view (v_customer_risk_profile) for automated risk categorization.
