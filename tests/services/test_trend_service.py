from app.services.trend_service import TrendService

def test_get_funding_trends_for_sector():
    # Arrange
    trend_service = TrendService()
    sector = "Healthcare"

    # Act
    result = trend_service.get_funding_trends_for_sector(sector)

    # Assert
    assert result is not None
    for stage_trend in result:
        assert stage_trend.stage is not None
        assert stage_trend.average is not None
        assert stage_trend.total is not None
