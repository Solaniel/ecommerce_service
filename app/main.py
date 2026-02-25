from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.api.routers import products, categories
from app.core.errors import ValidationErrors

app = FastAPI()

# Global error handling for ValueErrors
@app.exception_handler(ValidationErrors)
async def validation_errors_handler(request: Request, exc: ValidationErrors):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Validation failed",
            "errors": exc.errors,
        },
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

app.include_router(products.router)
app.include_router(categories.router)