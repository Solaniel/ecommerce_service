# E-commerce Product Service

A REST API service for managing products and categories in an e-commerce system.

Built with FastAPI, SQLAlchemy, PostgreSQL, and Alembic.

## Tech Stack

- **FastAPI** - async web framework
- **SQLAlchemy 2.0** - ORM with modern mapped column syntax
- **PostgreSQL** - relational database
- **Alembic** - database migrations
- **Pydantic v2** - request/response validation
- **Docker** - local PostgreSQL container
- **pytest** - unit testing

## Data Models

### Product

| Field       | Type           | Constraints                        |
|-------------|----------------|------------------------------------|
| id          | Integer        | Primary key, auto-generated        |
| title       | String(255)    | Required, indexed                  |
| sku         | String(64)     | Required, unique, indexed          |
| description | Text           | Optional                           |
| image       | String(2048)   | Optional, validated as URL         |
| price       | Decimal(12, 2) | Required, >= 0                     |
| category_id | Integer        | Required, foreign key to Category  |

### Category

| Field     | Type        | Constraints                                  |
|-----------|-------------|----------------------------------------------|
| id        | Integer     | Primary key, auto-generated                  |
| name      | String(255) | Required                                     |
| parent_id | Integer     | Optional, self-referencing foreign key       |

Categories support a tree structure through the self-referencing `parent_id` field, allowing nested hierarchies (e.g. Clothing > T-Shirts).

## API Endpoints

### Products

| Method   | Path                  | Description            | Status Codes |
|----------|-----------------------|------------------------|--------------|
| `GET`    | `/products/`          | List all products      | 200          |
| `GET`    | `/products/{id}`      | Get product by ID      | 200, 404     |
| `GET`    | `/products/search`    | Search/filter products | 200, 400     |
| `POST`   | `/products/`          | Create a product       | 201, 400, 409|
| `PATCH`  | `/products/{id}`      | Partially update       | 200, 404, 400|
| `DELETE` | `/products/{id}`      | Delete a product       | 204, 404     |

### Categories

| Method   | Path                  | Description            | Status Codes |
|----------|-----------------------|------------------------|--------------|
| `GET`    | `/categories/`        | List all categories    | 200          |
| `GET`    | `/categories/{id}`    | Get category by ID     | 200, 404     |
| `POST`   | `/categories/`        | Create a category      | 201, 400, 409|
| `PATCH`  | `/categories/{id}`    | Partially update       | 200, 404, 400|
| `DELETE` | `/categories/{id}`    | Delete a category      | 204, 404     |

### Search Endpoint

`GET /products/search` accepts the following query parameters:

| Parameter   | Type    | Description                                      |
|-------------|---------|--------------------------------------------------|
| title       | string  | Partial, case-insensitive match on product title  |
| sku         | string  | Exact match on SKU                                |
| min_price   | decimal | Minimum price (inclusive)                         |
| max_price   | decimal | Maximum price (inclusive)                         |
| category_id | integer | Filter by exact category ID                       |
| limit       | integer | Max results per page (default: 100, max: 100)     |
| offset      | integer | Number of results to skip (default: 0)             |

All filters are optional. When multiple filters are provided, they are combined with **logical AND** -- only products matching all specified criteria are returned.

**Examples:**

    GET /products/search?title=phone
    GET /products/search?min_price=10&max_price=50
    GET /products/search?title=phone&category_id=1&min_price=100
    GET /products/search?limit=10&offset=20


## Assumptions & Design Decisions

- **Image as URL** -- the `image` field stores a URL reference (validated by Pydantic), not binary data. File storage would be handled by a separate service/CDN.
- **Decimal for price** -- `NUMERIC(12,2)` avoids floating-point rounding errors inherent to `FLOAT` types.
- **Category deletion** -- deleting a parent category sets `parent_id` to `NULL` on its children (`ON DELETE SET NULL`). Products cannot be orphaned; deleting a category that still has products is blocked (`ON DELETE RESTRICT`).
- **PATCH semantics** -- update endpoints use partial updates. Only fields included in the request body are modified; omitted fields are left unchanged.
- **Validation** -- input validation is handled at two layers: Pydantic schemas (type, format, range) and a CRUD validation layer (uniqueness, foreign key existence).

## Setup

### 1. Clone the repository

    git clone <repo-url>
    cd ecommerce_service

### 2. Create virtual environment

    python -m venv .venv
    source .venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Configure environment

    cp .env.example .env

### 5. Start PostgreSQL

    docker compose up -d

### 6. Run database migrations

    alembic upgrade head

### 7. Run the API

    fastapi dev app/main.py

The interactive API docs are available at `http://localhost:8000/docs`.

## Running Tests

Create the test database, then run pytest:

    docker exec -it ecommerce_db psql -U postgres -c "CREATE DATABASE ecommerce_test;"
    pytest
