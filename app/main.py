from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.api.routers import products, categories
from app.core.errors import ValidationErrors

import psycopg

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
    status = 409
    detail = "Request violates a database constraint."

    orig = getattr(exc, "orig", None)

    # psycopg3 exceptions
    if isinstance(orig, psycopg.errors.ForeignKeyViolation):
        detail = "Foreign key constraint failed. Check related resource IDs."
    elif isinstance(orig, psycopg.errors.UniqueViolation):
        detail = "Unique constraint failed. A resource with the same unique field already exists."

    return JSONResponse(status_code=status, content={"detail": detail})

app.include_router(products.router)
app.include_router(categories.router)