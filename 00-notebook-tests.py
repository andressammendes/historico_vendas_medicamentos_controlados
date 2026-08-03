#%%
import re
import boto3
import pandas as pd
from io import BytesIO
from tqdm import tqdm
from dotenv import load_dotenv
from schemas import SCHEMAS_POR_ARQUIVO

load_dotenv()

#%%
df = pd.read_parquet(
    "s3://dir-dados-abertos/parquet/EDA_Industrializados_201811.parquet",
    storage_options={
            "client_kwargs": {
            "region_name": "us-east-1"
        }
    }
)

df = df.map(lambda x: x.strip('".,') if isinstance(x, str) else x)