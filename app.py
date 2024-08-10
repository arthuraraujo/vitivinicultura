from flask import Flask, jsonify, request
import pandas as pd
import requests
import io
import chardet

app = Flask(__name__)

# URLs dos dados CSV
URLS = {
    "producao": "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv",
    "processamento": "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv",
    "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv",
    "importacao": "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv",
    "exportacao": "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv",
}

# Colunas específicas para cada categoria
CATEGORIA_COLUNAS = {
    "producao": ["id", "control", "produto"],
    "processamento": ["id", "control", "cultivar"],
    "comercializacao": ["id", "control", "produto"],
    "importacao": ["id", "país"],
    "exportacao": ["id", "país"],
}


def clean_encoding_issues(text):
    """Função para substituir caracteres especiais."""
    replacements = {
        "Ã£": "ã",
        "Ã©": "é",
        "Ãª": "ê",
        "Ã§": "ç",
        "Ãº": "ú",
        "Ã³": "ó",
        "Ã­": "í",
        "Ã‰": "É",
        "Ã ": "à",
        "Ã©": "é",
        "Ã‰": "É",
        "â€“": "–",
        "â€œ": "“",
        "â€": "”",
        "â€˜": "‘",
        "â€™": "’",
        "Ã³": "ó",
        "Ãº": "ú",
        "Ã ": "à",
        "Ã¬": "ì",
        "Ã³": "ó",
        "â€¡": "Ç",
        "â€º": "º",
        "Âª": "ª",
    }
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    return text


def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:

            # Tentar leitura com UTF-8, se falhar, tentar ISO-8859-1
            try:
                df = pd.read_csv(
                    io.StringIO(response.text),
                    on_bad_lines="skip",
                    sep=";",
                    encoding="utf-8",
                )
            except UnicodeDecodeError:
                df = pd.read_csv(
                    io.StringIO(response.text),
                    on_bad_lines="skip",
                    sep=";",
                    encoding="ISO-8859-1",
                )

            # Imprimir os nomes das colunas para diagnóstico
            print("Colunas disponíveis no DataFrame:", df.columns.tolist())

            # Remover espaços em branco das colunas e dos valores
            df.columns = df.columns.str.strip().str.lower()  # Normalizar para lowercase
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Limpar problemas de codificação nos dados
            df = clean_encoding_issues(df)

            print(df.head())

            return df
        except pd.errors.ParserError as e:
            print(f"Erro ao processar o CSV: {e}")
            return None
    else:
        return None


@app.route("/dados/<categoria>", methods=["GET"])
def dados_categoria(categoria):
    categoria = categoria.lower()
    if categoria in URLS:
        df = get_data(URLS[categoria])
        if df is not None:
            # Aplicando filtros, se fornecidos
            filters = request.args.to_dict()

            # Normalizar nomes de colunas
            colunas_base = [col.lower() for col in CATEGORIA_COLUNAS.get(categoria, [])]

            # Filtrar por ano se o parâmetro 'ano' for fornecido
            ano = filters.get("ano")
            if ano:
                # Encontrar a coluna correspondente ao ano, que pode ter sido renomeada
                ano_col = next((col for col in df.columns if col.startswith(ano)), None)
                if ano_col:
                    colunas_filtradas = [
                        col for col in colunas_base if col in df.columns
                    ]
                    df = df[colunas_filtradas + [ano_col]]
                    df = df[df[ano_col].notna()]  # Filtrar somente onde o ano tem valor

            # Aplicar filtros para cada coluna base
            for col in colunas_base:
                valor_filtro = filters.get(col)
                if valor_filtro and col in df.columns:
                    df = df[df[col].str.contains(valor_filtro, case=False, na=False)]

            # Garantir que as colunas base e do ano estejam na resposta
            if ano:
                colunas_resposta = colunas_base + [ano_col]
            else:
                colunas_resposta = colunas_base

            # Selecionar apenas as colunas necessárias
            df = df[colunas_resposta]

            # Remover colunas de indexação (caso existam)
            if "unnamed: 0" in df.columns:
                df = df.drop(columns=["unnamed: 0"])

            data = df.to_dict(orient="records")
            return jsonify(data), 200
        else:
            return jsonify({"error": "Não foi possível obter os dados."}), 500
    else:
        return jsonify({"error": "Categoria inválida."}), 404


if __name__ == "__main__":
    app.run(debug=True)
