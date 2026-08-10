CREATE OR REPLACE TABLE pg.minha_tabela AS 
SELECT 
    *
FROM read_parquet(
    's3://dir-dados-abertos/bronze/**/*.parquet',
    union_by_name = true,
    filename = true
)
LIMIT 100;