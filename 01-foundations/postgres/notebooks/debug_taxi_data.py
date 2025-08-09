import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import os
    return os, pd


@app.cell
def _(os):
    # Check what data files we have
    data_dir = "data"
    data_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    print(f"Found data files: {data_files}")
    return data_dir, data_files


@app.cell
def _(data_dir, data_files, os, pd):
    # Load the first CSV file to examine its structure
    if data_files:
        file_path = os.path.join(data_dir, data_files[0])
        print(f"Loading: {file_path}")
        df = pd.read_csv(file_path)
        print(f"Shape: {df.shape}")
        df
    else:
        print("No CSV files found!")
        df = None
    return (df,)


@app.cell
def _(df):
    def _():
        # Examine the column names to identify KeyError issues
        if df is not None:
            print("Column names:")
            for i, col in enumerate(df.columns):
                print(f"{i}: '{col}'")
        return print(f"\nTotal columns: {len(df.columns)}")


    _()
    return


@app.cell
def _(df):
    # Show basic info about the dataframe
    if df is not None:
        print("DataFrame Info:")
        df.info()
    return


@app.cell
def _(df):
    # Show first few rows
    if df is not None:
        print("First 5 rows:")
        df.head()
    else:
        print("No data to display")
    return


@app.cell
def _(df):
    def _():
        # Check for specific columns that might be causing KeyErrors
        if df is not None:
            expected_columns = [
                'tpep_pickup_datetime', 
                'tpep_dropoff_datetime',
                'fare_amount',
                'trip_distance',
                'pickup_longitude',
                'pickup_latitude',
                'PULocationID'
            ]

            print("Column existence check:")
            for col in expected_columns:
                exists = col in df.columns
                print(f"'{col}': {'✓' if exists else '✗'}")

            print(f"\nActual columns in dataset:")
        return print(list(df.columns))


    _()
    return


@app.cell
def _(df):
    # Check data types and missing values
    if df is not None:
        print("Data types and missing values:")
        for col in df.columns:
            missing = df[col].isnull().sum()
            dtype = df[col].dtype
            print(f"'{col}': {dtype}, missing: {missing}")
    return


@app.cell
def _(df):
    # Sample some data to see what we're working with
    if df is not None:
        print("Random sample of 3 rows:")
        df.sample(3) if len(df) >= 3 else df
    return


if __name__ == "__main__":
    app.run()
