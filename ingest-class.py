#!/usr/bin/env python3
"""
NYC Taxi Data Upload Script

This script uploads NYC taxi data from CSV files to PostgreSQL database.
It processes the data in chunks to handle large files efficiently.
"""

import os
import sys
import pandas as pd
import logging
from time import time
from sqlalchemy import create_engine
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaxiDataUploader:
    """Upload taxi data to PostgreSQL database."""
    
    def __init__(self, db_host="localhost", db_port=5432, db_user="root", 
                 db_password="root", db_name="ny_taxi", chunk_size=100000):
        self.chunk_size = chunk_size
        self.engine = self._create_connection(db_host, db_port, db_user, db_password, db_name)
    
    def _create_connection(self, host, port, user, password, db_name):
        """Create database connection."""
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        try:
            engine = create_engine(connection_string)
            # Test connection
            with engine.connect() as conn:
                logger.info(f"Successfully connected to database: {db_name}")
            return engine
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            sys.exit(1)
    
    def download_file(self, url, output_filename=None):
        """Download file from URL."""
        if not output_filename:
            # Determine filename based on URL
            if url.endswith('.csv.gz'):
                output_filename = 'downloaded_data.csv.gz'
            else:
                output_filename = 'downloaded_data.csv'
        
        try:
            logger.info(f"Downloading file from: {url}")
            
            # Use wget (more reliable for large files)
            exit_code = os.system(f"wget {url} -O {output_filename}")
            
            if exit_code != 0:
                logger.error(f"Failed to download file using wget")
                return None
                
            logger.info(f"Successfully downloaded: {output_filename}")
            return output_filename
            
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return None
    def upload_csv_to_table(self, csv_file_path, table_name, if_exists="replace"):
        """
        Upload CSV file to PostgreSQL table in chunks.
        
        Args:
            csv_file_path (str): Path to the CSV file
            table_name (str): Name of the PostgreSQL table
            if_exists (str): What to do if table exists ('replace', 'append', 'fail')
        """
        if not os.path.exists(csv_file_path):
            logger.error(f"CSV file not found: {csv_file_path}")
            return False
        
        try:
            logger.info(f"Starting upload of {csv_file_path} to table {table_name}")
            
            # Read CSV in chunks
            df_iter = pd.read_csv(csv_file_path, iterator=True, chunksize=self.chunk_size)
            
            # Process first chunk to create table structure
            first_chunk = next(df_iter)
            logger.info(f"Processing first chunk with {len(first_chunk)} records")
            
            # Convert datetime columns
            first_chunk = self._convert_datetime_columns(first_chunk)
            
            # Create table with first chunk (just structure, no data)
            first_chunk.head(n=0).to_sql(
                name=table_name, 
                con=self.engine, 
                if_exists=if_exists, 
                index=False
            )
            logger.info(f"Created table structure for {table_name}")
            
            # Insert first chunk data
            t_start = time()
            first_chunk.to_sql(
                name=table_name, 
                con=self.engine, 
                if_exists="append", 
                index=False
            )
            t_end = time()
            logger.info(f"Inserted first chunk ({len(first_chunk)} records) in {t_end - t_start:.3f} seconds")
            
            # Process remaining chunks
            chunk_count = 1
            total_records = len(first_chunk)
            
            while True:
                try:
                    t_start = time()
                    chunk = next(df_iter)
                    chunk_count += 1
                    
                    # Convert datetime columns
                    chunk = self._convert_datetime_columns(chunk)
                    
                    # Insert chunk
                    chunk.to_sql(
                        name=table_name, 
                        con=self.engine, 
                        if_exists="append", 
                        index=False
                    )
                    
                    t_end = time()
                    total_records += len(chunk)
                    logger.info(f"Inserted chunk {chunk_count} ({len(chunk)} records) in {t_end - t_start:.3f} seconds. Total: {total_records}")
                    
                except StopIteration:
                    logger.info("Finished ingesting all chunks into the database")
                    break
            
            logger.info(f"✅ Upload completed! Total records uploaded: {total_records}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading data: {str(e)}")
            return False
    
    def upload_from_url(self, url, table_name, if_exists="replace", cleanup=True):
        """
        Download file from URL and upload to PostgreSQL table.
        
        Args:
            url (str): URL to download the CSV file from
            table_name (str): Name of the PostgreSQL table
            if_exists (str): What to do if table exists ('replace', 'append', 'fail')
            cleanup (bool): Whether to delete the downloaded file after upload
        """
        # Download file
        downloaded_file = self.download_file(url)
        if not downloaded_file:
            return False
        
        # Upload file
        success = self.upload_csv_to_table(downloaded_file, table_name, if_exists)
        
        # Cleanup downloaded file if requested
        if cleanup and os.path.exists(downloaded_file):
            try:
                os.remove(downloaded_file)
                logger.info(f"Cleaned up downloaded file: {downloaded_file}")
            except Exception as e:
                logger.warning(f"Could not delete downloaded file: {str(e)}")
        
        return success
    
    def _convert_datetime_columns(self, df):
        """Convert datetime columns to proper format."""
        datetime_columns = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
        
        for col in datetime_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        return df
    
    def verify_upload(self, table_name):
        """Verify the upload by checking record count and sample data."""
        try:
            with self.engine.connect() as conn:
                # Get record count
                result = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = result.fetchone()[0]
                logger.info(f"Table {table_name} contains {count:,} records")
                
                # Get sample data
                sample_df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", conn)
                logger.info("Sample data:")
                print(sample_df.to_string())
                
                return count
        except Exception as e:
            logger.error(f"Error verifying upload: {str(e)}")
            return None


def main():
    """Main entry point for the upload script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Upload NYC taxi data to PostgreSQL')
    
    # Input source options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--csv-file', help='Path to local CSV file')
    input_group.add_argument('--url', help='URL to download CSV file from')
    
    # Database connection options
    parser.add_argument('--table-name', required=True, help='PostgreSQL table name')
    parser.add_argument('--db-host', default='localhost', help='Database host')
    parser.add_argument('--db-port', type=int, default=5432, help='Database port')
    parser.add_argument('--db-user', default='root', help='Database user')
    parser.add_argument('--db-password', default='root', help='Database password')
    parser.add_argument('--db-name', default='ny_taxi', help='Database name')
    
    # Processing options
    parser.add_argument('--chunk-size', type=int, default=100000, help='Chunk size for processing')
    parser.add_argument('--if-exists', choices=['replace', 'append', 'fail'], 
                       default='replace', help='What to do if table exists')
    parser.add_argument('--no-cleanup', action='store_true', 
                       help='Do not delete downloaded file after upload (only for URL mode)')
    
    args = parser.parse_args()
    
    logger.info("NYC Taxi Data Upload - Starting...")
    
    # Initialize uploader
    uploader = TaxiDataUploader(
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_password=args.db_password,
        db_name=args.db_name,
        chunk_size=args.chunk_size
    )
    
    # Upload data based on input source
    if args.csv_file:
        # Upload from local file
        success = uploader.upload_csv_to_table(
            csv_file_path=args.csv_file,
            table_name=args.table_name,
            if_exists=args.if_exists
        )
    else:
        # Upload from URL
        success = uploader.upload_from_url(
            url=args.url,
            table_name=args.table_name,
            if_exists=args.if_exists,
            cleanup=not args.no_cleanup
        )
    
    if success:
        # Verify upload
        uploader.verify_upload(args.table_name)
        logger.info("Upload completed successfully!")
    else:
        logger.error("Upload failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
