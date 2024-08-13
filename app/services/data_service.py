import pandas as pd
import requests
import io
import chardet
from typing import Optional

def get_data(url: str) -> Optional[pd.DataFrame]:
    """
    Obtém dados de um URL e retorna como um DataFrame do pandas.

    Args:
        url (str): URL para obter os dados CSV.

    Returns:
        Optional[pd.DataFrame]: DataFrame com os dados ou None se ocorrer um erro.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP ruins
        
        # Detectar a codificação do conteúdo recebido
        result = chardet.detect(response.content)
        encoding = result["encoding"]

        # Ler o CSV com a codificação detectada
        df = pd.read_csv(
            io.StringIO(response.content.decode(encoding)),
            on_bad_lines="skip",
            sep=";",
        )

        # Remover espaços em branco das colunas e dos valores
        df.columns = df.columns.str.strip().str.lower()  # Normalizar para lowercase
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        return df
    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar o CSV: {e}")
        return None