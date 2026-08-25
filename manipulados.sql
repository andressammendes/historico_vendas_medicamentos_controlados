CREATE OR REPLACE TABLE pg.manipulados AS 
SELECT 
    ano,
    mes,
    uf,
    municipio,
    NO_PRINCIPIO_ATIVO as principio_ativo,
    qt_ativo_por_unidade_farmacotec,
    qtd_unidade_farmacotecnica,
    NO_CONSELHO_PRESCRITOR as conselho_prescritor,
    cid,
    filename
FROM read_parquet(
    's3://dir-dados-abertos/bronze/Manipulados/**/*.parquet',
    union_by_name = true,
    filename = true
)
WHERE filename NOT LIKE '%2026%';