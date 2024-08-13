from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dados_categoria():
    response = client.get("/dados/producao")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_dados_categoria_invalid():
    response = client.get("/dados/categoria_invalida")
    assert response.status_code == 404
    assert response.json()["detail"] == "Categoria inválida."

def test_dados_categoria_with_filters():
    response = client.get("/dados/producao?ano_inicio=2020&ano_fim=2022&produto=Uva")
    assert response.status_code == 200
    # Adicione mais assertivas baseadas nos filtros aplicados