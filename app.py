from flask import Flask, jsonify, request
import pandas as pd
import requests
import io
import chardet
import json

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


def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            # Detectar a codificação do conteúdo recebido
            result = chardet.detect(response.content)
            encoding = result["encoding"]
            print(f"Codificação detectada: {encoding}")

            # Ler o CSV com a codificação detectada
            df = pd.read_csv(
                io.StringIO(response.content.decode(encoding)),
                on_bad_lines="skip",
                sep=";",
            )

            # Imprimir os nomes das colunas para diagnóstico
            print("Colunas disponíveis no DataFrame:", df.columns.tolist())

            # Remover espaços em branco das colunas e dos valores
            df.columns = df.columns.str.strip().str.lower()  # Normalizar para lowercase
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            print(df.head())

            return df
        except Exception as e:
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

            # Selecionar todas as colunas que são anos
            colunas_anos = [col for col in df.columns if col.isdigit()]

            # Filtrar por ano ou intervalo de anos se os parâmetros forem fornecidos
            ano_inicio = filters.get("ano_inicio")
            ano_fim = filters.get("ano_fim")
            if ano_inicio and ano_fim:
                # Encontrar todas as colunas dentro do intervalo de anos
                colunas_anos = [
                    col for col in colunas_anos if ano_inicio <= col <= ano_fim
                ]
            elif ano_inicio:
                colunas_anos = [col for col in colunas_anos if col >= ano_inicio]
            elif ano_fim:
                colunas_anos = [col for col in colunas_anos if col <= ano_fim]

            # Aplicar filtros para cada coluna base
            for col in colunas_base:
                valor_filtro = filters.get(col)
                if valor_filtro and col in df.columns:
                    df = df[df[col].str.contains(valor_filtro, case=False, na=False)]

            # Garantir que as colunas base e do(s) ano(s) estejam na resposta
            colunas_resposta = colunas_base + colunas_anos

            # Selecionar apenas as colunas necessárias
            df = df[colunas_resposta]

            # Remover colunas de indexação (caso existam)
            if "unnamed: 0" in df.columns:
                df = df.drop(columns=["unnamed: 0"])

            # Retornar a resposta JSON sem escapar os caracteres Unicode
            data = df.to_dict(orient="records")
            return app.response_class(
                response=json.dumps(data, ensure_ascii=False),
                status=200,
                mimetype="application/json",
            )
        else:
            return jsonify({"error": "Não foi possível obter os dados."}), 500
    else:
        return jsonify({"error": "Categoria inválida."}), 404


if __name__ == "__main__":
    app.run(debug=True)
