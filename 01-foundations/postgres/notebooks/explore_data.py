import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    from sqlalchemy import create_engine
    return (create_engine,)


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell
def _(create_engine):
    import os
    # Use environment variable or default to host.docker.internal for Docker
    db_host = os.getenv('DB_HOST', 'host.docker.internal')
    engine = create_engine(f"postgresql://root:root@{db_host}:5432/ny_taxi")
    return (engine,)


@app.cell
def _(engine):
    engine.connect()
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
def _(df_chunk, engine):
    df_chunk.head(n=0).to_sql(name="yellow_tripdata_2021_01", con=engine, if_exists="replace", index=False)
    return


@app.cell
def _(df_chunk, pd):
    df_chunk.tpep_pickup_datetime=pd.to_datetime(df_chunk.tpep_pickup_datetime)
    df_chunk.tpep_dropoff_datetime=pd.to_datetime(df_chunk.tpep_dropoff_datetime)
    return


@app.cell
def _(df_chunk, engine):
    df_chunk.to_sql(name="yellow_tripdata_2021_01", con=engine, if_exists="append", index=False)
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


if __name__ == "__main__":
    app.run()
