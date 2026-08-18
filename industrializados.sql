CREATE OR REPLACE TABLE pg.industrializados AS 
SELECT 
    ano,
    mes,
    uf,
    municipio,
    principio_ativo,
    qt_vendida,
    conselho_prescritor,
    cid,
    filename
FROM read_parquet(
    's3://dir-dados-abertos/bronze/Industrializados/**/*.parquet',
    union_by_name = true,
    filename = true
)
WHERE filename NOT LIKE '%2026%'
LIMIT 100;