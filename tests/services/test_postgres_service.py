from app.services.postgres_service import engine
from sqlalchemy import text

def test_engine_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1