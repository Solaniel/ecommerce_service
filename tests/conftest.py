import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.main import app
from app.api.deps import get_db
from app.db.models import Product, Category

settings = get_settings()

engine = create_engine(settings.test_database_url, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="function")
def db_session():
    """
    Returns a SQLAlchemy Session for a single test.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Provides a TestClient where FastAPI's get_db dependency is overridden
    to use the test session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function", autouse=True)
def clean_db(db_session: Session):
    """
    Ensures the test DB is clean before each test.
    We delete in dependency order to avoid FK issues:
      products -> categories
    """
    # Use ORM deletes (simple and clear).
    db_session.query(Product).delete()
    db_session.query(Category).delete()
    db_session.commit()


@pytest.fixture(scope="function")
def seed_data(db_session: Session):
    """
    Inserts a small deterministic dataset for search tests.
    Returns a dict with created entities for convenience.
    """
    cat_electronics = Category(name="Electronics", parent_id=None)
    cat_clothing = Category(name="Clothing", parent_id=None)
    db_session.add_all([cat_electronics, cat_clothing])
    db_session.commit()
    db_session.refresh(cat_electronics)
    db_session.refresh(cat_clothing)
    cat_tshirts = Category(name="T-Shirts", parent_id=cat_clothing.id)
    db_session.add(cat_tshirts)
    db_session.commit()
    db_session.refresh(cat_tshirts)

    products = [
        Product(
            title="Phone Case",
            sku="SKU-CASE-001",
            description="Case",
            image=None,
            price=10.00,
            category_id=cat_electronics.id,
        ),
        Product(
            title="Smart Phone",
            sku="SKU-PHONE-001",
            description="Phone",
            image=None,
            price=500.00,
            category_id=cat_electronics.id,
        ),
        Product(
            title="T-Shirt",
            sku="SKU-TSHIRT-001",
            description="Shirt",
            image=None,
            price=25.00,
            category_id=cat_tshirts.id,
        ),
    ]
    db_session.add_all(products)
    db_session.commit()

    # refresh to get IDs
    for p in products:
        db_session.refresh(p)

    return {
        "categories": {
            "electronics": cat_electronics,
            "clothing": cat_clothing,
        },
        "products": products,
    }