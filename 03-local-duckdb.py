from pathlib import Path

import duckdb
from dotenv import load_dotenv

load_dotenv()

Path('storage').mkdir(exist_ok=True)

con = duckdb.connect('storage/warehouse.duckdb')

con.execute('INSTALL httpfs;')
con.execute('LOAD httpfs;')

con.execute("""
CREATE SECRET (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN
);
""")

con.execute("""
CREATE SCHEMA IF NOT EXISTS bronze;
""")

con.execute("""
CREATE OR REPLACE TABLE bronze.clientes AS
SELECT *
FROM read_parquet(
    's3://dir-dados-abertos/bronze/**/*.parquet',
    union_by_name = true,
    filename = true
);
""")

df = con.execute("""
SELECT *
FROM bronze.clientes
LIMIT 5;
""").df()

print(df)

