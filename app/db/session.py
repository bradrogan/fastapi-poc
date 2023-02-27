from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URI: str = "sqlite:///example.db"

engine = create_engine(
    DB_URI,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
)
