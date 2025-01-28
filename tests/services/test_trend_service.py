from app.services.trend_service import get_combined_trend

def test_get_combined_trend():
    sector = "Healthcare"
    result = get_combined_trend(sector)
    assert result["sector"] == sector
    assert len(result["company_data"]) > 0
    assert len(result["funding_trend"]) > 0