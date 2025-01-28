from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import POSTGRES_DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
from app.models.models import Fundinground

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class PostgresService:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def get_funding_rounds(self, org_uuid:str) -> list[Fundinground]:
        with self.SessionLocal() as session:
            query = session.query(Fundinground).filter(Fundinground.org_uuid == org_uuid)
            funding_rounds = query.all()

        if not funding_rounds:
            return []

        return funding_rounds