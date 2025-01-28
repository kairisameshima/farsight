from sqlalchemy import create_engine, func, cast
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from app.config import POSTGRES_DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
from app.models.models import Fundinground, Organization

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
        """Get the funding rounds for a given organization"""
        with self.SessionLocal() as session:
            query = session.query(Fundinground).filter(Fundinground.org_uuid == org_uuid, Fundinground.fundraise_amount_usd.isnot(None))
            funding_rounds = query.all()

        if not funding_rounds:
            return []

        return funding_rounds
    
    def get_organization(self, org_uuid:str) -> Organization:
        """Get the organization for a given organization UUID"""
        with self.SessionLocal() as session:
            query = session.query(Organization).filter(Organization.org_uuid == org_uuid)
            organization = query.first()

        return organization
    
    def get_most_active_investors(self, org_uuids: list[str]):
        """Get the most active investors for the given organizations"""
        with self.SessionLocal() as session:
             # Step 1: Create a subquery to unnest the investors array
            subquery = session.query(
                Fundinground.funding_round_uuid.label("funding_round_uuid"),
                cast(func.unnest(Fundinground.investors), UUID).label("investor_uuid"),
                Fundinground.fundraise_amount_usd
            ).filter(
                Fundinground.org_uuid.in_(org_uuids) ,
                Fundinground.fundraise_amount_usd.isnot(None)
            
            ).subquery()

            # Step 2: Join the subquery with the Organizations table
            results = session.query(
                subquery.c.investor_uuid,  # Investor UUID
                func.count(subquery.c.funding_round_uuid).label("deal_count"),  # Count deals
                func.sum(subquery.c.fundraise_amount_usd).label("total_funding")  # Total funding
            ).group_by(
                subquery.c.investor_uuid,
            ).order_by(
                func.count(subquery.c.funding_round_uuid).desc()  # Rank by deal count
            ).limit(10).all()

        return results