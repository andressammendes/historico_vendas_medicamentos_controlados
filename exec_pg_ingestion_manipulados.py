import os
import duckdb
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

with open('connections.sql', 'r') as f:
    con_pg_script = f.read()

with open('manipulados.sql', 'r') as f:
    s3_to_pg_script = f.read()

sql_script = con_pg_script + '\n' + s3_to_pg_script

for key, val in os.environ.items():
    if val:
        target = '${' + key + '}'
        sql_script = sql_script.replace(target, val)

print("Transferindo dados do s3 para o postgreSQL")
inicio = datetime.now()
print(f'Início da ingestão: {inicio.strftime('%H:%M')}')

with duckdb.connect() as con:
    con.execute(sql_script)

fim = datetime.now()
print(f'Fim da ingestão: {fim.strftime('%H:%M')}')

tempo = fim - inicio

print("Transferência concluída com sucesso!")
print(f'Tempo: {tempo}')