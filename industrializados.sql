INSERT INTO pg.industrializados_temp
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
    '{arquivo}',
    union_by_name = true,
    filename = true
);