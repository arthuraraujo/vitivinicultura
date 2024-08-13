from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.data_service import get_data
from app.config import URLS, CATEGORIA_COLUNAS

router = APIRouter()

@router.get("/dados/{categoria}", summary="Obter dados por categoria")
async def dados_categoria(
        categoria: str,
        ano_inicio: Optional[str] = Query(None, description="Ano inicial para filtrar os dados"),
        ano_fim: Optional[str] = Query(None, description="Ano final para filtrar os dados"),
        **filters
):
    """
    Retorna dados filtrados por categoria e opcionalmente por ano e outros filtros.

    - **categoria**: Categoria dos dados (producao, processamento, comercializacao, importacao, exportacao)
    - **ano_inicio**: Ano inicial para filtrar os dados (opcional)
    - **ano_fim**: Ano final para filtrar os dados (opcional)
    - **filters**: Filtros adicionais baseados nas colunas da categoria
    """
    categoria = categoria.lower()
    if categoria not in URLS:
        raise HTTPException(status_code=404, detail="Categoria inválida.")

    df = get_data(URLS[categoria])
    if df is None:
        raise HTTPException(status_code=500, detail="Não foi possível obter os dados.")

    # Normalizar nomes de colunas
    colunas_base = [col.lower() for col in CATEGORIA_COLUNAS.get(categoria, [])]

    # Selecionar todas as colunas que são anos
    colunas_anos = [col for col in df.columns if col.isdigit()]

    # Filtrar por ano ou intervalo de anos
    if ano_inicio and ano_fim:
        colunas_anos = [col for col in colunas_anos if ano_inicio <= col <= ano_fim]
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
    return JSONResponse(content=data)