#!/bin/bash
# Migration script to reorganize the repository

echo "🔄 Reorganizing data-engineering-gcp repository..."

# Create the new structure
mkdir -p 01-foundations/postgres/{scripts,notebooks,containers,docs,data}
mkdir -p 02-ingestion/{batch-processing,streaming,apis,file-formats}
mkdir -p 03-storage/{cloud-storage,data-lakes,data-warehouses,nosql}
mkdir -p 04-processing/{dataflow,spark,dbt,airflow}
mkdir -p 05-analytics/{bigquery,looker,ml-pipelines,reporting}
mkdir -p 06-infrastructure/{terraform,kubernetes,monitoring,security}
mkdir -p 07-multi-cloud/{aws-patterns,azure-patterns,hybrid-cloud}
mkdir -p examples/{end-to-end-projects,use-cases,datasets}
mkdir -p docs/{architecture-patterns,best-practices,troubleshooting}
mkdir -p tools/{scripts,containers,templates}

# Move current files to postgres section
echo "📦 Moving PostgreSQL files..."
mv ingest-data.py 01-foundations/postgres/scripts/ 2>/dev/null || echo "ingest-data.py not found"
mv ingest-simple.py 01-foundations/postgres/scripts/ 2>/dev/null || echo "ingest-simple.py not found"
mv datapipeline.py 01-foundations/postgres/scripts/ 2>/dev/null || echo "datapipeline.py not found"
mv explore_data.py 01-foundations/postgres/notebooks/ 2>/dev/null || echo "explore_data.py not found"
mv debug_taxi_data.py 01-foundations/postgres/notebooks/ 2>/dev/null || echo "debug_taxi_data.py not found"

# Move Docker files
mv Dockerfile 01-foundations/postgres/containers/Dockerfile.pipeline 2>/dev/null || echo "Dockerfile not found"
mv Dockerfile.explore 01-foundations/postgres/containers/ 2>/dev/null || echo "Dockerfile.explore not found"
mv docker-compose.yml 01-foundations/postgres/ 2>/dev/null || echo "docker-compose.yml not found"

# Move data and requirements
mv data/ 01-foundations/postgres/ 2>/dev/null || echo "data/ directory not found"
mv requirements*.txt 01-foundations/postgres/ 2>/dev/null || echo "requirements files not found"

# Move current README to postgres docs
mv README.md 01-foundations/postgres/docs/setup-guide.md 2>/dev/null || echo "README.md not found"

echo "✅ Migration complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review the new structure in 01-foundations/postgres/"
echo "2. Update paths in scripts and Docker files"
echo "3. Test the setup with: cd 01-foundations/postgres && docker-compose up"
echo "4. Replace root README.md with NEW_README.md"
