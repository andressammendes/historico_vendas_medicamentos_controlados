CREATE OR REPLACE TABLE pg.manipulados_novo AS 
WITH tb_filtro AS (
    SELECT
        ano,
        mes,
        uf,
        municipio,
        NO_PRINCIPIO_ATIVO AS principio_ativo,
        qt_ativo_por_unidade_farmacotec,
        qtd_unidade_farmacotecnica,
        NO_CONSELHO_PRESCRITOR AS conselho_prescritor,
        cid
    FROM read_parquet(
        's3://dir-dados-abertos/bronze/Manipulados/**/*.parquet',
        union_by_name = true,
        filename = true
    )
    WHERE ano NOT IN [2014, 2015, 2016, 2026]
)

SELECT 
    CAST(ano AS VARCHAR) || '/' || LPAD(CAST(mes AS VARCHAR), 2, '0') AS ano_mes,
    uf,
    municipio,
    principio_ativo,
    COUNT(principio_ativo) AS qt_vendida,
    SUM(qt_ativo_por_unidade_farmacotec) AS qt_ativo_por_unidade_farmacotec,
    SUM(qtd_unidade_farmacotecnica) AS qt_unidade_farmacotecnica,
    conselho_prescritor,
    cid
FROM tb_filtro
GROUP BY
    ano,
    mes,
    uf,
    municipio,
    principio_ativo,
    conselho_prescritor,
    cid
ORDER BY ano, mes;