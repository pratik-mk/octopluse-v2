from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "octopluse.db"

# SQLite connection
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False, connect_args={"check_same_thread": False})

# Base class for ORM models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
