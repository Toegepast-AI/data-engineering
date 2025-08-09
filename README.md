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

### 3. Create the table structure
```sql
CREATE TABLE yellow_tripdata_2021_01 (
	"VendorID" FLOAT(53), 
	tpep_pickup_datetime TIMESTAMP WITHOUT TIME ZONE, 
	tpep_dropoff_datetime TIMESTAMP WITHOUT TIME ZONE, 
	passenger_count FLOAT(53), 
	trip_distance FLOAT(53), 
	"RatecodeID" FLOAT(53), 
	store_and_fwd_flag TEXT, 
	"PULocationID" BIGINT, 
	"DOLocationID" BIGINT, 
	payment_type FLOAT(53), 
	fare_amount FLOAT(53), 
	extra FLOAT(53), 
	mta_tax FLOAT(53), 
	tip_amount FLOAT(53), 
	tolls_amount FLOAT(53), 
	improvement_surcharge FLOAT(53), 
	total_amount FLOAT(53), 
	congestion_surcharge FLOAT(53)
);
```

### 4. Load data into PostgreSQL
See Marimo notebook

### 5. Verify the data with pgcli
```sql
SELECT count(1) FROM yellow_tripdata_2021_1;
SELECT * FROM yellow_tripdata_2021_1 LIMIT 5;
```

## Run Data Pipeline

### With Docker (persists processed data)
```bash
docker run --rm -v "$(pwd)/data:/app/data" postgres:test
```

### Locally (in venv)
```bash
python datapipeline.py
```

