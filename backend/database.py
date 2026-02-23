# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL") # La sacamos del Docker Compose

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Esta función abre una conexión y la cierra cuando la API termina su respuesta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()