import os
import duckdb
from dotenv import load_dotenv
from datetime import datetime
import boto3

load_dotenv()

# Importa o conteúdo das queries
with open('connections.sql', 'r') as f:
    con_pg_script = f.read()

with open('industrializados.sql', 'r') as f:
    s3_to_pg_script = f.read()

# Obtém a lista de arquivos no s3
s3_client = boto3.client("s3")
response = s3_client.list_objects_v2(Bucket='dir-dados-abertos', Prefix='bronze/')

arquivos = []
for obj in response.get("Contents", []):
    if ('Industrializados' in obj["Key"]) and ('2026' not in obj["Key"]):
        arquivos.append(obj["Key"])
# print(arquivos[:4])

# Preenche a query de conexão com as variáveis de ambiente
for key, val in os.environ.items():
    if val:
        target = '${' + key + '}'
        con_pg_script = con_pg_script.replace(target, val)

# Loop na lista de arquivos
for arquivo in arquivos[:2]:
    print(50*'-')
    print(f'Arquivo: {arquivo.split('/')[-1]}')
    abs_path = f's3://dir-dados-abertos/{arquivo}'

    # Preenche a query de transferêcia de dados com o caminho do arquivo em processamento
    s3_to_pg_script_replaced = s3_to_pg_script.replace('{arquivo}', abs_path)
    #print(s3_to_pg_script_replaced)
    inicio = datetime.now()
    print(f'Início: {inicio.strftime('%H:%M')}')

    try:
        # Verifica se a tebela já possui linhas do arquivo em processamento
        print('Abrindo conexão com o duckdb...')
        con = duckdb.connect()
        print('Abrindo conexão com o postgres...')
        verify_rows = con.execute(f"""
            {con_pg_script}
            SELECT COUNT(filename)
            FROM pg.industrializados
            WHERE filename = '{abs_path}'
        """).fetchone()
        # Se a tabela já possuir dados do arquivo em processamento, pula para o proximo arquivo
        if verify_rows[0]:
            print('Já existem dados deste arquivo na tabela\nCarregando o próximo arquivo...')
            con.execute("DETACH pg;")
            continue
        print('Transferindo dados...')
        con.execute(s3_to_pg_script_replaced)
        print('Dados transferidos com sucesso!')
        con.execute("DETACH pg;")
        print('Fechando conexão com o postgres...')
    except Exception as e:
        print(f"Problema com a conexão: {e}")
        con.execute("DETACH pg;")
        break
    finally:
        print('Fechando conexão com o duckdb...')
        con.close()

    fim = datetime.now()
    print(f'Fim: {fim.strftime('%H:%M')}')

    tempo = fim - inicio
    print(f'Tempo da transferência: {tempo}')
