import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell
def _(pd):
    df = pd.read_csv("data/yellow_tripdata_2021-01.csv")
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df, pd):
    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
    return


@app.cell
def _():
    from sqlalchemy import create_engine
    return (create_engine,)


@app.cell
def _(create_engine):
    engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
    return (engine,)


@app.cell
def _(engine):
    engine.connect()
    return


@app.cell
def _(df, engine, pd):
    print(pd.io.sql.get_schema(df, name="yellow_tripdata_2021_01", con=engine))
    return


@app.cell
def _(pd):
    df_iter = pd.read_csv("data/yellow_tripdata_2021-01.csv", iterator=True, chunksize=100000)
    return (df_iter,)


@app.cell
def _(df_iter):
    df_chunk = next(df_iter)
    return (df_chunk,)


@app.cell
def _(df_chunk, pd):
    df_chunk.tpep_pickup_datetime=pd.to_datetime(df_chunk.tpep_pickup_datetime)
    df_chunk.tpep_dropoff_datetime=pd.to_datetime(df_chunk.tpep_dropoff_datetime)
    return


@app.cell
def _(df_chunk, engine):
    df_chunk.head(n=0).to_sql(name="yellow_tripdata_2021_01", con=engine, if_exists="replace", index=False)
    return


@app.cell
def _(df_chunk, engine):
    import time

    start_time = time.time()  # Record the start time
    df_chunk.to_sql(name="yellow_tripdata_2021_01", con=engine, if_exists="append", index=False)
    end_time = time.time()  # Record the end time

    execution_time = end_time - start_time  # Calculate the execution time
    execution_time  # Display the execution time
    return


@app.cell
def _(df_iter, engine, pd):
    def _():
        while True:
            try:
                df_chunk = next(df_iter)
                df_chunk.tpep_pickup_datetime = pd.to_datetime(df_chunk.tpep_pickup_datetime)
                df_chunk.tpep_dropoff_datetime = pd.to_datetime(df_chunk.tpep_dropoff_datetime)
                df_chunk.to_sql(name="yellow_tripdata_2021_01", con=engine, if_exists="append", index=False)
            except StopIteration:
                return print("All chunks have been processed.")
                break
    _()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
