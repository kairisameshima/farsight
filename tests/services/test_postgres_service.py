from app.services.postgres_service import engine, PostgresService
from sqlalchemy import text

def test_engine_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

def test_postgres_service():
    db_service = PostgresService()

    foo = db_service.get_funding_rounds("e10aaff2-4d89-46d4-820b-b4f64b8d42ca")
    assert len(foo) > 0
