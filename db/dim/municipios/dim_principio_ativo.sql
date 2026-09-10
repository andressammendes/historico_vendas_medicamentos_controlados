-- 1. Cria a tabela dimensão
CREATE TABLE dim_principio_ativo (
    id SERIAL PRIMARY KEY,
    nome_principio_ativo VARCHAR(150) NOT NULL,
    CONSTRAINT uq_dim_principio_ativo UNIQUE (nome_principio_ativo)
);

-- 2. Function com TRIM + tratamento de caixa
CREATE OR REPLACE FUNCTION atualiza_dim_principio_ativo()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO dim_principio_ativo (nome_principio_ativo)
    VALUES (UPPER(TRIM(NEW.principio_ativo)))
    ON CONFLICT (nome_principio_ativo) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3. Trigger em manipulados
CREATE TRIGGER trg_atualiza_dim_principio_ativo_manipulados
AFTER INSERT OR UPDATE ON manipulados
FOR EACH ROW
EXECUTE FUNCTION atualiza_dim_principio_ativo();

-- 4. Trigger em industrializados
CREATE TRIGGER trg_atualiza_dim_principio_ativo_industrializados
AFTER INSERT OR UPDATE ON industrializados
FOR EACH ROW
EXECUTE FUNCTION atualiza_dim_principio_ativo();
INSERT INTO dim_principio_ativo (nome_principio_ativo)
SELECT DISTINCT UPPER(TRIM(principio_ativo)) FROM manipulados
UNION
SELECT DISTINCT UPPER(TRIM(principio_ativo)) FROM industrializados
ON CONFLICT (nome_principio_ativo) DO NOTHING;