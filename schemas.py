# Centraliza todos os schemas do projeto

EDA_MANIPULADOS = {
    'NU_ANO_VENDA': 'int',
    'NU_MES_VENDA': 'int',
    'SG_UF_VENDA': 'str',
    'NO_MUNICIPIO_VENDA': 'str',
    'DS_DCB':'str',
    'NO_PRINCIPIO_ATIVO': 'str',
    'QT_ATIVO_POR_UNID_FARMACOTEC': 'float',
    'DS_UNIDADE_MEDIDA_PRINCIPIO_ATIVO': 'str',
    'QT_UNIDADE_FARMACOTECNICA': 'float',
    'DS_TIPO_UNIDADE_FARMACOTECNICA': 'str',
    'NO_CONSELHO_PRESCRITOR': 'str',
    'SG_UF_CONSELHO_PRESCRITOR': 'str',
    'TP_RECEITUARIO': 'str',
    'CO_CID10': 'str',
    'SG_SEXO': 'Int64',
    'NU_IDADE': 'float',
    'NU_UNIDADE_IDADE': 'float'
}

EDA_INDUSTRIALIZADOS = {
    'NU_ANO_VENDA': 'int',
    'NU_MES_VENDA': 'int',
    'SG_UF_VENDA': 'str',
    'NO_MUNICIPIO_VENDA': 'str',
    'DS_PRINCIPIO_ATIVO': 'str',
    'DS_DESCRICAO_APRESENTACAO':'str',
    'QT_VENDIDA': 'Int64',
    'DS_UNIDADE_MEDIDA':'str',
    'NO_CONSEITOR':'str',
    'SG_UF_CONSELHO_PRESCRITOR': 'str',
    'TP_RECEITUARIO': 'str',
    'CO_CID10': 'str',
    'SG_SEXO': 'Int64',
    'NU_IDADE': 'float',
    'NU_UNIDADE_IDADE': 'float'
    
}

# Dicionário mestre: mapeia padrão no nome do arquivo → schema
SCHEMAS_POR_ARQUIVO = {
    'Manipulados': EDA_MANIPULADOS,
    'Industrializados': EDA_INDUSTRIALIZADOS,
}