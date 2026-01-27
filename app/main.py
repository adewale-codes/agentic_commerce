from fastapi import FastAPI
from app.core.logging import setup_logging
from app.api.chat import router as chat_router
from app.api.products import router as products_router
from app.api.carts import router as carts_router

setup_logging()

app = FastAPI(title="Agentic Commerce Backend")

app.include_router(chat_router)
app.include_router(products_router)
app.include_router(carts_router)

@app.get("/health")
def health():
    return {"status": "ok"}
