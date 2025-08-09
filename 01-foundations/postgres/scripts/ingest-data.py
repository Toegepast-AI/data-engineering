#!/usr/bin/env python3
"""
Simple NYC Taxi Data Ingest Script
Based on the straightforward online example
"""

import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # Download file if URL provided
    if url:
        # Determine output filename
        if url.endswith('.csv.gz'):
            csv_name = 'output.csv.gz'
        else:
            csv_name = 'output.csv'
        
        print(f"Downloading {url}...")
        os.system(f"wget {url} -O {csv_name}")
    else:
        csv_name = params.csv_file

    # Connect to database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # Read CSV in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    
    # Process first chunk
    df = next(df_iter)
    
    # Convert datetime columns
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    # Create table structure
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    
    # Insert first chunk
    df.to_sql(name=table_name, con=engine, if_exists='append')
    
    print(f"Inserted first chunk ({len(df)} records)")
    
    # Process remaining chunks
    while True:
        try:
            t_start = time()
            
            df = next(df_iter)
            
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            
            print('Inserted another chunk (%d records), took %.3f seconds' % (len(df), t_end - t_start))
            
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break
    
    # Cleanup downloaded file
    if url and os.path.exists(csv_name):
        os.remove(csv_name)
        print(f"Cleaned up {csv_name}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--url', help='URL of the CSV file to download')
    input_group.add_argument('--csv-file', help='Path to local CSV file')
    
    # Database options
    parser.add_argument('--user', default='root', help='User name for postgres')
    parser.add_argument('--password', default='root', help='Password for postgres')
    parser.add_argument('--host', default='localhost', help='Host for postgres')
    parser.add_argument('--port', default='5432', help='Port for postgres')
    parser.add_argument('--db', default='ny_taxi', help='Database name for postgres')
    parser.add_argument('--table-name', required=True, help='Name of the table to write results to')
    
    args = parser.parse_args()
    
    main(args)
