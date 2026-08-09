-- 1. Extensões
INSTALL httpfs; LOAD httpfs;
INSTALL postgres; LOAD postgres;

-- 2. Credenciais S3
SET s3_region = '${AWS_REGION}';
SET s3_access_key_id = '${AWS_ACCESS_KEY_ID}';
SET s3_secret_access_key = '${AWS_SECRET_ACCESS_KEY}';

-- 3. Conexão Postgres
ATTACH '${PG_CONNECTION}' AS pg (TYPE POSTGRES);