# VitiAPI - API de Dados sobre Viticultura e Produção de Vinhos

## Visão Geral

VitiAPI é uma API FastAPI projetada para fornecer acesso a dados sobre viticultura e produção de vinhos. Esta API oferece endpoints para consultar informações sobre produção, processamento, comercialização, importação e exportação de vinhos e uvas.

## Características

- Consulta de dados por categoria (produção, processamento, comercialização, importação, exportação)
- Filtragem por ano ou intervalo de anos
- Filtros adicionais baseados em colunas específicas de cada categoria
- Documentação interativa com Swagger UI

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- Pandas
- Requests
- Other dependencies (ver `requirements.txt`)

## Instalação

1. Clone o repositório:

   ```
   git clone https://github.com/seu-usuario/vitiapi.git
   cd vitiapi
   ```

2. Crie e ative um ambiente virtual:

   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Inicie o servidor:

   ```
   uvicorn app.main:app --reload
   ```

2. Acesse a documentação interativa em `http://localhost:8000/docs`

3. Use a interface Swagger UI para testar os endpoints ou faça requisições HTTP diretamente para a API.

## Estrutura do Projeto

```
vitiapi/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── pydantic_models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── dados_route.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_service.py
│   └── utils/
│       ├── __init__.py
│       └── scraping.py
│
├── tests/
│   ├── __init__.py
│   ├── test_routes/
│   │   └── test_dados_route.py
│   └── test_services/
│       └── test_data_service.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Endpoints

### GET /dados/{categoria}

Retorna dados filtrados por categoria e opcionalmente por ano e outros filtros.

Parâmetros:

- `categoria` (path): Categoria dos dados (producao, processamento, comercializacao, importacao, exportacao)
- `ano_inicio` (query, opcional): Ano inicial para filtrar os dados
- `ano_fim` (query, opcional): Ano final para filtrar os dados
- `filters` (query, opcional): Filtros adicionais baseados nas colunas da categoria

Exemplo de uso:

```
GET /dados/producao?ano_inicio=2020&ano_fim=2022&filters={"produto":"Uva"}
```

## Desenvolvimento

### Executando Testes

Para executar os testes unitários:

```
pytest
```

### Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [MIT](LICENSE) para detalhes.
