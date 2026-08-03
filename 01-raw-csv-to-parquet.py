import pandas as pd
import os


input_dir = r'\csv_files'
output_dir = r'\parquet_files'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

for csv_file in csv_files:
    csv_path = os.path.join(input_dir, csv_file)
    df = pd.read_csv(csv_path, encoding='latin-1',sep=';', on_bad_lines='skip', quoting=3,low_memory=False)
    base_name = os.path.splitext(csv_file)[0]
    parquet_path = os.path.join(output_dir, f'{base_name}.parquet')
    df.to_parquet(parquet_path, engine='pyarrow')
    
    print(f'Salvo {csv_file} como {parquet_path}')

print('Todos os arquivos foram convertidos com sucesso.')
