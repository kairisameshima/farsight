from fastapi import APIRouter, Query
from app.services.trend_service import TrendService
router = APIRouter()

@router.get("/trend/sector")
async def sector_trend(sector: str = Query(..., description="The sector to get trend data for")):
    # Instantiate TrendService
    trend_service = TrendService()
    data = trend_service.get_funding_trends_for_sector(sector)
    return {'data': data}

@router.get("/trend/funding")
async def funding_trend(company_ids: str):
    # Workflow logic here
    return {"company_ids": company_ids, "data": "funding trend"}
