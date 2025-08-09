#!/usr/bin/env python3
"""
NYC Taxi Data Pipeline

This script processes NYC taxi data for analysis and transformation.
"""

import os
import sys
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaxiDataPipeline:
    """Data pipeline for processing NYC taxi data."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.output_dir = os.path.join(data_dir, "processed")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_taxi_data(self, filename):
        """Load taxi data from CSV file."""
        file_path = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
            
        try:
            logger.info(f"Loading data from {file_path}")
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None
    
    def clean_taxi_data(self, df):
        """Clean and validate taxi data."""
        if df is None:
            return None
            
        logger.info("Starting data cleaning...")
        original_count = len(df)
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
        
        # Convert datetime columns
        datetime_columns = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
        for col in datetime_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # Remove invalid trips (negative duration, fare, etc.)
        if 'fare_amount' in df.columns:
            df = df[df['fare_amount'] > 0]
        
        if 'trip_distance' in df.columns:
            df = df[df['trip_distance'] > 0]
        
        # Remove unrealistic coordinates
        if 'pickup_longitude' in df.columns and 'pickup_latitude' in df.columns:
            df = df[
                (df['pickup_longitude'].between(-75, -73)) &
                (df['pickup_latitude'].between(40, 41))
            ]
        
        logger.info(f"Cleaned data: {original_count} -> {len(df)} records")
        return df
    
    def analyze_data(self, df):
        """Perform basic analysis on the taxi data."""
        if df is None:
            return
            
        logger.info("Performing data analysis...")
        
        # Basic statistics
        print("\n=== TAXI DATA ANALYSIS ===")
        print(f"Total trips: {len(df):,}")
        
        if 'fare_amount' in df.columns:
            print(f"Average fare: ${df['fare_amount'].mean():.2f}")
            print(f"Total revenue: ${df['fare_amount'].sum():,.2f}")
        
        if 'trip_distance' in df.columns:
            print(f"Average trip distance: {df['trip_distance'].mean():.2f} miles")
        
        # Date range
        if 'tpep_pickup_datetime' in df.columns:
            start_date = df['tpep_pickup_datetime'].min()
            end_date = df['tpep_pickup_datetime'].max()
            print(f"Date range: {start_date} to {end_date}")
        
        # Top pickup locations
        if 'PULocationID' in df.columns:
            top_locations = df['PULocationID'].value_counts().head(5)
            print("\nTop 5 pickup locations:")
            for location_id, count in top_locations.items():
                print(f"  Location {location_id}: {count:,} trips")
    
    def save_processed_data(self, df, filename):
        """Save processed data to output directory."""
        if df is None:
            return
            
        output_path = os.path.join(self.output_dir, filename)
        try:
            df.to_csv(output_path, index=False)
            logger.info(f"Saved processed data to {output_path}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
    
    def run_pipeline(self):
        """Execute the complete data pipeline."""
        logger.info("Starting NYC Taxi Data Pipeline...")
        
        # Check available data files
        data_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
        
        if not data_files:
            logger.error("No CSV files found in data directory")
            return
        
        logger.info(f"Found data files: {data_files}")
        
        for file in data_files:
            logger.info(f"Processing {file}...")
            
            # Load data
            df = self.load_taxi_data(file)
            if df is None:
                continue
            
            # Clean data
            df_clean = self.clean_taxi_data(df)
            
            # Analyze data
            self.analyze_data(df_clean)
            
            # Save processed data
            processed_filename = f"processed_{file}"
            self.save_processed_data(df_clean, processed_filename)
        
        logger.info("Pipeline completed successfully!")


def main():
    """Main entry point for the data pipeline."""
    logger.info("NYC Taxi Data Pipeline - Starting...")
    
    # Initialize and run pipeline
    pipeline = TaxiDataPipeline()
    pipeline.run_pipeline()
    
    logger.info("NYC Taxi Data Pipeline - Completed!")


if __name__ == "__main__":
    main()
