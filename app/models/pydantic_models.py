from enum import Enum

class Categoria(str, Enum):
    producao = "producao"
    processamento = "processamento"
    comercializacao = "comercializacao"
    importacao = "importacao"
    exportacao = "exportacao"