# Postgres setup locally & GCP with taxi data

## Setup PostgreSQL Database

### 1. Run postgres container locally
```bash
docker run -it \
    -e POSTGRES_USER="root"\
    -e POSTGRES_PASSWORD="root"\
    -e POSTGRES_DB="ny_taxi"\
    -v "$PWD/postgres-nyc-taxi-data:/var/lib/postgresql/data"\
    -p 5432:5432 \
    postgres:13
```

### 2. Access postgres with pgcli (venv)
```bash
pip install pgcli
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## Data Ingestion

### Option 1: Download and ingest from URL (Recommended)
```bash
# Download and ingest yellow taxi data from January 2021
python ingest-data.py \
    --url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz" \
    --table-name yellow_tripdata_2021_01 \
    --user root \
    --password root \
    --host localhost \
    --port 5432 \
    --db ny_taxi
```

### Option 2: Ingest from local CSV file
```bash
# If you have a local CSV file
python ingest-data.py \
    --csv-file data/yellow_tripdata_2021-01.csv \
    --table-name yellow_tripdata_2021_01 \
    --user root \
    --password root
```

### Other available datasets:
```bash
# February 2021
python ingest-data.py \
    --url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-02.csv.gz" \
    --table-name yellow_tripdata_2021_02

# March 2021
python ingest-data.py \
    --url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-03.csv.gz" \
    --table-name yellow_tripdata_2021_03
```

### 3. Verify the data with pgcli
```sql
SELECT count(1) FROM yellow_tripdata_2021_01;
SELECT * FROM yellow_tripdata_2021_01 LIMIT 5;
```

## Ingest Data with Docker

### Build the ingestion container
```bash
docker build -t taxi_ingest:v001 .
```

### Option 1: Run with environment variable
```bash
docker run --rm \
    --network=pg-network \
    taxi_ingest:v001 \
        --url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz" \
        --table-name yellow_tripdata_2021_01 \
        --user root \
        --password root \
        --host pg-database \
        --port 5432 \
        --db ny_taxi
```

## Connecting pgAdmin and Postgres
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```

```bash
docker network create pg-network
```

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v "$PWD/postgres-nyc-taxi-data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    --network=pg-network \
    --name=pg-database \
    postgres:13
```

```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name=pgadmin \
    dpage/pgadmin4
```