-- ========================================
-- 1. Desabilita as triggers antes da carga
-- ========================================
ALTER TABLE manipulados DISABLE TRIGGER ALL;
ALTER TABLE industrializados DISABLE TRIGGER ALL;

-- ========================================
-- 2. Sincroniza dim_municipio manualmente
-- ========================================
INSERT INTO dim_municipio (nome_municipio, uf)
SELECT DISTINCT UPPER(TRIM(municipio)), UPPER(TRIM(uf)) FROM manipulados
UNION
SELECT DISTINCT UPPER(TRIM(municipio)), UPPER(TRIM(uf)) FROM industrializados
ON CONFLICT (nome_municipio, uf) DO NOTHING;

-- ========================================
-- 3. Sincroniza dim_principio_ativo manualmente
-- ========================================
INSERT INTO dim_principio_ativo (nome_principio_ativo)
SELECT DISTINCT UPPER(TRIM(principio_ativo)) FROM manipulados
UNION
SELECT DISTINCT UPPER(TRIM(principio_ativo)) FROM industrializados
ON CONFLICT (nome_principio_ativo) DO NOTHING;

-- ========================================
-- 4. Reabilita as triggers
-- ========================================
ALTER TABLE manipulados ENABLE TRIGGER ALL;
ALTER TABLE industrializados ENABLE TRIGGER ALL;
/*
BEGIN;

ALTER TABLE manipulados DISABLE TRIGGER ALL;
ALTER TABLE industrializados DISABLE TRIGGER ALL;

INSERT INTO dim_municipio (nome_municipio, uf)
SELECT DISTINCT UPPER(TRIM(municipio)), UPPER(TRIM(uf)) FROM manipulados
UNION
SELECT DISTINCT UPPER(TRIM(municipio)), UPPER(TRIM(uf)) FROM industrializados
ON CONFLICT (nome_municipio, uf) DO NOTHING;

INSERT INTO dim_principio_ativo (nome_principio_ativo)
SELECT DISTINCT UPPER(TRIM(principio_ativo)) FROM manipulados
UNION
SELECT DISTINCT UPPER(TRIM(principio_ativo)) FROM industrializados
ON CONFLICT (nome_principio_ativo) DO NOTHING;

ALTER TABLE manipulados ENABLE TRIGGER ALL;
ALTER TABLE industrializados ENABLE TRIGGER ALL;

COMMIT;*/