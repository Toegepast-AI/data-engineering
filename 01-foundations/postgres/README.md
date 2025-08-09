# PostgreSQL Data Engineering Patterns

This section covers PostgreSQL fundamentals for data engineering, including data ingestion, containerization, and analysis patterns.

## 🎯 What You'll Learn

- Setting up PostgreSQL with Docker
- Data ingestion from various sources (CSV, URLs)
- Chunked processing for large datasets
- Database connection patterns
- Data exploration with Jupyter/Marimo notebooks
- Container orchestration with docker-compose

## 📁 Structure

```
postgres/
├── README.md                    # This file
├── docker-compose.yml          # Full stack setup
├── data/                       # Sample datasets
├── scripts/
│   ├── ingest-data.py          # Data ingestion script
│   ├── datapipeline.py         # Data processing pipeline
│   └── setup-db.sql            # Database initialization
├── notebooks/
│   ├── explore_data.py         # Marimo exploration notebook
│   └── debug_taxi_data.py      # Data debugging notebook
├── containers/
│   ├── Dockerfile.ingest       # Ingestion container
│   └── Dockerfile.pipeline     # Pipeline container
└── docs/
    ├── setup-guide.md          # Setup instructions
    └── troubleshooting.md      # Common issues
```

## 🚀 Quick Start

1. **Start the full stack:**
   ```bash
   cd 01-foundations/postgres
   docker-compose up -d
   ```

2. **Ingest sample data using the container:**
   ```bash
   docker-compose run --rm data-ingestion \
     --url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz" \
     --table-name yellow_tripdata_2021_01 \
     --user root \
     --password root \
     --host postgres \
     --db ny_taxi
   ```

3. **Or ingest data locally:**
   ```bash
   python scripts/ingest-data.py \
     --url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz" \
     --table-name yellow_tripdata_2021_01 \
     --user root \
     --password root \
     --host localhost \
     --db ny_taxi
   ```

4. **Explore data with Marimo:**
   ```bash
   # Access via browser at http://localhost:2718
   # or run locally: marimo edit notebooks/explore_data.py
   ```

## 🔧 Services

- **PostgreSQL** (port 5432) - Primary database
- **pgAdmin** (port 8080) - Web-based database admin  
- **Data Explorer** (port 2718) - Marimo notebook interface
- **Data Ingestion** - CSV ingestion service (run manually)

## 🌐 Multi-Cloud Considerations

The patterns here work across:
- **GCP**: Cloud SQL, BigQuery migration paths
- **AWS**: RDS, Redshift integration
- **Azure**: PostgreSQL service, Synapse Analytics
