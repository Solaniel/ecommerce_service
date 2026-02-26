from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

engine = None
SessionLocal = None

def init_engine():
    global engine, SessionLocal
    if engine is None:
        settings = get_settings()
        engine = create_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
        )
        SessionLocal = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
        )

def get_session_local():
    init_engine()
    return SessionLocal