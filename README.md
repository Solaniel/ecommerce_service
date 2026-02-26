# E-commerce Product Service

A REST API service for managing products and categories in an e-commerce system.

Built with FastAPI, SQLAlchemy, PostgreSQL, and Alembic.

## Tech Stack

- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic (database migrations)
- Docker (PostgreSQL container)

## Assumptions & Design Decisions

- The `image` field stores a URL reference, not binary image data.
- Price is stored as a DECIMAL type to avoid floating point inaccuracies.
- Category deletion cascades to subcategories.
- Search filters are combined using logical AND.
- Title search performs partial matching.
- SKU search performs exact matching.
- Price filters are inclusive.

## Setup

### 1. Clone the repository

git clone ...
cd ecommerce_service

### 2. Create virtual environment

python -m venv .venv
source .venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Start PostgreSQL

docker compose up -d

### 5. Run the API

fastapi run dev
