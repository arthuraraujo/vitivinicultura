URLS = {
    "producao": "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv",
    "processamento": "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv",
    "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv",
    "importacao": "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv",
    "exportacao": "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv",
}

CATEGORIA_COLUNAS = {
    "producao": ["id", "control", "produto"],
    "processamento": ["id", "control", "cultivar"],
    "comercializacao": ["id", "control", "produto"],
    "importacao": ["id", "país"],
    "exportacao": ["id", "país"],
}