# Docker + PostgreSQL + dbt + Airflow Project

A complete data pipeline project using Docker with PostgreSQL, dbt, and Apache Airflow.

## Architecture

- **PostgreSQL**: Database for both Airflow metadata and dbt transformations
- **dbt**: Data transformation tool for building models
- **Airflow**: Workflow orchestration with webserver, scheduler, worker, and triggerer
- **Redis**: Message broker for Celery executor

## Prerequisites

- Docker and Docker Compose installed
- Ports 5432 (PostgreSQL) and 8080 (Airflow) available

## Quick Start

### 1. Start the Services

```powershell
docker-compose up -d
```

Wait about 1-2 minutes for all services to become healthy.

### 2. Access Airflow UI

Open http://localhost:8080

**Login credentials:**
- Username: `airflow`
- Password: `airflow`

### 3. Run dbt Commands

Execute dbt commands inside the Airflow container:

```powershell
# Test dbt configuration
docker exec -it dbt-airflow-webserver bash -c "cd /dbt && dbt debug"

# Run dbt models
docker exec -it dbt-airflow-webserver bash -c "cd /dbt && dbt run"

# Test dbt models
docker exec -it dbt-airflow-webserver bash -c "cd /dbt && dbt test"

# Generate documentation
docker exec -it dbt-airflow-webserver bash -c "cd /dbt && dbt docs generate"
```

### 4. Access PostgreSQL

```powershell
# Connect to PostgreSQL
docker exec -it dbt-postgres psql -U airflow -d dbt_db

# View dbt models
\dt public.*
\dv public.*

# Query the data
SELECT * FROM public.stg_sample_data;
SELECT * FROM public.fct_sample_processed;
```

## Project Structure

```
.
├── docker-compose.yml          # Docker services configuration
├── .env                        # Environment variables
├── airflow/
│   ├── Dockerfile              # Custom Airflow image with dbt
│   ├── requirements.txt        # Python dependencies
│   ├── config/
│   │   └── profiles.yml        # dbt profiles configuration
│   ├── dags/
│   │   └── dbt_sample_dag.py   # Sample DAG for dbt orchestration
│   ├── logs/                   # Airflow logs
│   └── plugins/                # Airflow plugins
├── dbt/
│   ├── dbt_project.yml         # dbt project configuration
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_sample_data.sql
│   │   └── marts/
│   │       └── fct_sample_processed.sql
│   └── logs/                   # dbt logs
└── postgres/
    └── init-multiple-databases.sh  # Database initialization script
```

## dbt Models

### Staging Layer (`models/staging/`)
- `stg_sample_data`: Sample staging view with test data

### Marts Layer (`models/marts/`)
- `fct_sample_processed`: Processed data as a table

## Airflow DAGs

### `dbt_sample_dag`
Orchestrates dbt model execution:
1. **dbt_debug**: Validates configuration
2. **dbt_run**: Executes dbt models
3. **dbt_test**: Runs dbt tests

Schedule: Daily at midnight

## Database Configuration

PostgreSQL creates three databases:
- `airflow`: Airflow metadata database
- `dbt_db`: Main dbt transformation database
- `analytics_db`: Additional database for analytics

## Environment Variables

Configure in `.env` file:

```
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow

DBT_POSTGRES_HOST=postgres
DBT_POSTGRES_PORT=5432
DBT_POSTGRES_USER=airflow
DBT_POSTGRES_PASSWORD=airflow
DBT_POSTGRES_DB=dbt_db
DBT_POSTGRES_SCHEMA=public
```

## Common Commands

### Docker Management

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f airflow-webserver

# Restart a service
docker-compose restart airflow-webserver
```

### dbt Development

```powershell
# Interactive shell in container
docker exec -it dbt-airflow-webserver bash

# Inside container
cd /dbt
dbt run --select stg_sample_data
dbt run --models marts
dbt test
```

## Troubleshooting

### Airflow UI not loading
- Wait 1-2 minutes after startup for services to be healthy
- Check webserver logs: `docker-compose logs airflow-webserver`
- Restart: `docker-compose restart airflow-webserver`

### PostgreSQL connection issues
- Verify container is healthy: `docker ps`
- Check logs: `docker-compose logs postgres`
- Test connection: `docker exec -it dbt-postgres pg_isready -U airflow`

### dbt errors
- Run debug: `docker exec -it dbt-airflow-webserver bash -c "cd /dbt && dbt debug"`
- Check profiles.yml: `docker exec -it dbt-airflow-webserver cat /opt/airflow/config/profiles.yml`

## Next Steps

1. Add your own dbt models in `dbt/models/`
2. Create custom Airflow DAGs in `airflow/dags/`
3. Add dbt tests in `dbt/tests/`
4. Configure connections in Airflow UI
5. Set up dbt sources and seeds

## Useful Links

- [dbt Documentation](https://docs.getdbt.com/)
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
