from fastapi import APIRouter, Query
from app.services.trend_service import TrendService
router = APIRouter()

@router.get("/trend/sector")
async def sector_trend(sector: str = Query(..., description="The sector to get trend data for")):
    trend_service = TrendService()
    data = trend_service.get_funding_trends_for_sector(sector)
    return {'data': data}


@router.get("/trend/sector_chart")
async def sector_trend_chart(sector: str = Query(..., description="The sector to get trend data for")):
    trend_service = TrendService()
    data = trend_service.get_data_for_funding_trends_chart(sector)
    return {'data': data}

@router.get("/trend/top_investors")
async def funding_trend(sector: str = Query(..., description="The sector to get trend data for")):
    trend_service = TrendService()
    data = trend_service.get_top_investors_for_sector(sector)
    return {'data': data}
