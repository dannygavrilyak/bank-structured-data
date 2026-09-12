# Banking DWH & Anti-Fraud Analytical Pipeline

A synthetic data pipeline and analytical layer modeling a retail banking data warehouse (DWH) for fraud detection, operational monitoring, and risk scoring.

## Architecture
- **Ingestion Layer (`/src` & `main.py`)**: Decoupled Python ETL pipeline leveraging SQLAlchemy, Pandas, and Faker to seed a relational PostgreSQL schema preserving foreign keys, chronological logic, and realistic weighted distributions.
- **Analytical Layer (`/sql`)**:
  - `01_fraud_monitoring.sql`: Merchant failure rate analysis using conditional aggregation (`COUNT CASE WHEN`).
  - `02_velocity_checks.sql`: Rapid succession detection using window functions (`LAG()`) to flag potential card abuse within 10-minute thresholds.
  - `03_customer_risk_mart.sql`: Customer risk profiling view (`v_customer_risk_profile`) calculating transactional volume, ticket sizes, and behavioral risk scoring (`HIGH`, `MEDIUM`, `LOW`).

## Tech Stack
- **Database**: PostgreSQL
- **Languages & Frameworks**: Python 3.14, SQLAlchemy, Pandas, psycopg2-binary
- **Environment & VCS**: Virtualenv, Git (Conventional Commits)

## Getting Started
1. Clone the repository:
   ```bash
   git clone [https://github.com/dannygavrilyak/bank-structured-data.git](https://github.com/dannygavrilyak/bank-structured-data.git)
   cd bank-structured-data

##  **Create and activate a virtual environment**:
    python3 -m venv .venv 
    source .venv/bin/activate

##   **Install dependencies**:
    python3 -m pip install -r requirements.txt

##  **Configure .env**:
    DB_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

##  **Run the pipeline**:
    python3 main.py
