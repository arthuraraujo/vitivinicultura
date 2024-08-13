import pandas as pd
import requests
import io
import chardet

def get_data(url: str) -> pd.DataFrame:
    response = requests.get(url)
    if response.status_code == 200:
        try:
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
        except Exception as e:
            print(f"Erro ao processar o CSV: {e}")
            return None
    else:
        return None