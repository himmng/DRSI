import dask.dataframe as dd
from sqlalchemy import create_engine
import pandas as pd

def load_data_from_csv(file_path):
    return dd.read_csv(file_path)

def load_data_from_sql(table_name, connection_string, index_col):
    """
    Load table from database using SQLAlchemy + Dask
    """
    engine = create_engine(connection_string)
    # Dask reads SQL tables in parallel for big data
    ddf = dd.read_sql_table(table_name, con=engine, index_col=index_col)
    return ddf
