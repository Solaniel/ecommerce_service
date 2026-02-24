from fastapi import FastAPI
from app.api.routers import products, categories

app = FastAPI()

app.include_router(products.router)
app.include_router(categories.router)