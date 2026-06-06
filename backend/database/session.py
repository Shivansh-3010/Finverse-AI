from sqlalchemy.orm import sessionmaker

from database.postgres import engine


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)