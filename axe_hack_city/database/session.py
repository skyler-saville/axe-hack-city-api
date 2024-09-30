# database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
