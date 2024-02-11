from sqlalchemy import create_engine, Date, String, Float, Integer, text
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import os

#################################################
# Database Setup
#################################################
# Create engine to the database path
owner_username = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host_name_address = 'localhost'
db_name = 'listings_db'
engine = create_engine(f"postgresql://{owner_username}:{password}@{host_name_address}:5432/{db_name}")
# Create database if it does not exist already, and add data
if not database_exists(engine.url):
    print('Creating database...')
    create_database(engine.url)
    # List of table names
    tables = ['toronto_listings', 'neighbourhoods', 'beds', 'baths', 'dens']
    # Loop through tables and add them to db
    for table_name in tables:
        # Define variables for primary key and dtypes
        if not table_name == 'toronto_listings':
            p_key = 'index'
            value_col = 'neighbourhood' if table_name == 'neighbourhoods' else table_name
            dtype_dict = {
                p_key: Integer,
                value_col: String(100)
            }
        else:
            p_key = 'mls_id'
            dtype_dict = {
                p_key: String(100),
                "property_type": String(100),
                "address": String(100),
                "street": String(100),
                "neighbourhood": String(100),
                "city": String(100),
                "price": Integer,
                "baths": Integer,
                "beds": Integer,
                "dens": Integer,
                "latitude": Float,
                "longitude": Float,
                "date_scraped": Date,
                "url": String(100)
            }
        
        # Read data
        df = pd.read_csv(f"resources/{table_name}.csv")
        # Add data to sql database
        df.to_sql(
            table_name,
            engine,
            if_exists='replace',
            index=False,
            chunksize=500,
            dtype=dtype_dict
        )
        # Alter table to set primary key
        with engine.connect() as conn:
            conn.execute(text(f'ALTER TABLE {table_name} ADD PRIMARY KEY ({p_key})'))
    # Log successful database creation
    print('Database creation was successful.')
