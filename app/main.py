from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes import dados_route
from app.models.pydantic_models import Categoria

app = FastAPI(
    title="VitiAPI",
    description="API para dados sobre viticultura e produção de vinhos",
    version="1.0.0"
)

app.include_router(dados_route.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)