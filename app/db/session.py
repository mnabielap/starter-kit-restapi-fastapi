from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Determine if we are using SQLite to add specific arguments
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # check_same_thread is needed for SQLite in multi-threaded environments like FastAPI
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True # Helps with lost connections in Postgres
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# New SQLAlchemy 2.0 style for declarative base
class Base(DeclarativeBase):
    pass