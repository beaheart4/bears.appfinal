import os
from sqlmodel import create_engine, Session
from typing import Generator


DB_PATH = os.path.join(os.path.dirname(__file__), 'bears.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, 
    echo=False
)

def get_session() -> Generator:
    """FastAPI dependency to get database session"""
    with Session(engine) as session:
        yield session
     

