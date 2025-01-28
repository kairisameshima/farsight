from app.services.pinecone_service import query_pinecone
from app.services.postgres_service import SessionLocal
from sqlalchemy import text

def get_combined_trend(sector):
    # Query Pinecone
    companies = query_pinecone(sector)
    company_ids = [item['id'] for item in companies.matches]

    # Query PostgreSQL
    with SessionLocal() as session:
        query = session.execute(
            text("SELECT * FROM FundingRounds WHERE org_uuid IN :ids"),
            {"ids": tuple(company_ids)}
        )
        funding_data = query.fetchall()

    return {
        "sector": sector,
        "company_data": companies.matches,
        "funding_trend": funding_data
    }