CREATE TABLE dim_municipio (
    id SERIAL PRIMARY KEY,
    nome_municipio VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    CONSTRAINT uq_dim_municipio UNIQUE (nome_municipio, uf)
);


CREATE OR REPLACE FUNCTION atualiza_dim_municipio()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO dim_municipio (nome_municipio, uf)
    VALUES (
        UPPER(TRIM(NEW.municipio)),
        UPPER(TRIM(NEW.uf))
    )
    ON CONFLICT (nome_municipio, uf) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_atualiza_dim_municipio_manipulados
AFTER INSERT OR UPDATE ON manipulados
FOR EACH ROW
EXECUTE FUNCTION atualiza_dim_municipio();
CREATE TRIGGER trg_atualiza_dim_municipio_industrializados
AFTER INSERT OR UPDATE ON industrializados
FOR EACH ROW
EXECUTE FUNCTION atualiza_dim_municipio();
INSERT INTO dim_municipio (nome_municipio, uf)
SELECT DISTINCT UPPER(TRIM(municipio)), UPPER(TRIM(uf)) FROM manipulados
UNION
SELECT DISTINCT UPPER(TRIM(municipio)), UPPER(TRIM(uf)) FROM industrializados
ON CONFLICT (nome_municipio, uf) DO NOTHING;