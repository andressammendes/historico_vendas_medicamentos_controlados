import re
import boto3
import pandas as pd
from io import BytesIO
from tqdm import tqdm
from dotenv import load_dotenv
from schemas import SCHEMAS_POR_ARQUIVO

load_dotenv()


def detectar_schema(nome_arquivo: str) -> dict:
    for padrao, schema in SCHEMAS_POR_ARQUIVO.items():
        if padrao in nome_arquivo:
            print(f"  Schema detectado: '{padrao}'")
            return schema
    raise ValueError(
        f"Nenhum schema encontrado para '{nome_arquivo}'. "
        f"Esperado um dos padrões: {list(SCHEMAS_POR_ARQUIVO.keys())}"
    )


def detectar_classificacao(nome_arquivo: str) -> str:
    nome_lower = nome_arquivo.lower()
    
    # >>> AJUSTE AQUI: defina os padrões que identificam cada classificação
    if 'industrializados' in nome_lower or 'ind' in nome_lower:
        return 'Industrializados'
    elif 'manipulados' in nome_lower or 'manip' in nome_lower:
        return 'Manipulados'
    else:
        # Fallback: se não identificar, salva numa pasta genérica ou levanta erro
        raise ValueError(
            f"Não foi possível classificar o arquivo '{nome_arquivo}'. "
            f"Esperado padrão 'Industrializado' ou 'Manipulado' no nome."
        )


def converter_tipos_seguro(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    for coluna, tipo in schema.items():
        if coluna not in df.columns:
            print(f"  ⚠ '{coluna}' não encontrada.")
            continue
        
        tipo_str = str(tipo).lower().strip()
        
        if tipo_str in ('str', 'string', 'object'):
            df[coluna] = df[coluna].astype('string')
            print(f"  ✓ '{coluna}' → string")
        
        elif tipo_str in ('float', 'float64', 'float32', 'double'):
            df[coluna] = (
                df[coluna]
                .astype(str)
                .str.replace(',', '.', regex=False)
                .pipe(pd.to_numeric, errors='coerce')
                .astype('float64')
            )
            print(f"  ✓ '{coluna}' → float (vírgula corrigida)")
        
        elif tipo_str in ('int', 'int64', 'int32', 'int16', 'int8', 'integer'):
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce').astype('Int64')
            print(f"  ✓ '{coluna}' → int")
        
        else:
            df[coluna] = df[coluna].astype(tipo)
            print(f"  ✓ '{coluna}' → {tipo}")
    
    return df


def processar_e_salvar_parquet(
    nome_arquivo: str,
    base_path_leitura: str = 's3://dir-dados-abertos/parquet/',
    base_path_escrita: str = 's3://dir-dados-abertos/bronze/',
    region_name: str = 'us-east-1',
    strip_quotes: bool = True
) -> None:
    
    s3_path_leitura = f"{base_path_leitura.rstrip('/')}/{nome_arquivo.lstrip('/')}"
    
    df = pd.read_parquet(
        s3_path_leitura,
        storage_options={
            'client_kwargs': {'region_name': region_name}
        }
    )
    
    if strip_quotes:
        df = df.map(lambda x: x.strip('".,') if isinstance(x, str) else x)
    
    print(f'\nProcessando: {nome_arquivo}')
    schema = detectar_schema(nome_arquivo)
    df = converter_tipos_seguro(df, schema)
    
    match = re.search(r'_(\d{4})\d{2}\.', nome_arquivo)
    if not match:
        raise ValueError(f'Ano não encontrado no nome do arquivo: {nome_arquivo}')
    
    ano = match.group(1)
    
    classificacao = detectar_classificacao(nome_arquivo)
    
    s3_path_escrita = (
        f"{base_path_escrita.rstrip('/')}"
        f"/{classificacao}"
        f"/{ano}"
        f"/{nome_arquivo.lstrip('/')}"
    )

    buffer = BytesIO()
    df = df.rename(
        columns={
            'NU_ANO_VENDA': 'ano',
            'NU_MES_VENDA': 'mes',
            'SG_UF_VENDA': 'uf',
            'NO_MUNICIPIO_VENDA': 'municipio',
            'DS_PRINCIPIO_ATIVO': 'principio_ativo',
            'DS_DESCRICAO_APRESENTACAO':'descricao',
            'QT_VENDIDA': 'qt_vendida',
            'DS_UNIDADE_MEDIDA':'unidade_medida',
            'NO_CONSEITOR':'conselho_prescritor',
            'SG_UF_CONSELHO_PRESCRITOR': 'uf_conselho_prescritor',
            'TP_RECEITUARIO': 'tipo_receituario',
            'CO_CID10': 'cid',
            'SG_SEXO': 'sexo',
            'NU_IDADE': 'idade',
            'NU_UNIDADE_IDADE': 'unidade_idade',
            'DS_DCB':'ds_dcb',
            'QT_ATIVO_POR_UNID_FARMACOTEC': 'qt_ativo_por_unidade_farmacotec',
            'DS_UNIDADE_MEDIDA_PRINCIPIO_ATIVO':'ds_unidade_medida_principio_ativo',
            'QT_UNIDADE_FARMACOTECNICA': 'qtd_unidade_farmacotecnica',
            'DS_TIPO_UNIDADE_FARMACOTECNICA': 'ds_tipo_unidade_farmacotecnica',
            }
    )
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    
    s3_path_escrita = s3_path_escrita.replace("s3://", "")
    bucket_destino, key_destino = s3_path_escrita.split("/", 1)
    
    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.put_object(
        Bucket=bucket_destino,
        Key=key_destino,
        Body=buffer.getvalue()
    )
    
    print(f"✓ {nome_arquivo} → s3://{bucket_destino}/{key_destino}")


# running
BUCKET = 'dir-dados-abertos'
s3_client = boto3.client("s3")
response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix='parquet/')
arquivos = [obj["Key"] for obj in response.get("Contents", [])]
arquivos = [s.removeprefix('parquet/') for s in arquivos]

for arquivo in tqdm(arquivos, desc='processando arquivos ...', unit='arquivo'):
    try:
        processar_e_salvar_parquet(
            nome_arquivo=arquivo,
            base_path_leitura='s3://dir-dados-abertos/parquet/',
            base_path_escrita='s3://dir-dados-abertos/bronze/'
            )
    except Exception as e:
        print(f'\n✗ Erro ao processar {arquivo}: {e}')
        raise