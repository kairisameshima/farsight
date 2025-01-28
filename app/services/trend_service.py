from app.services.pinecone_service import PineconeService
from app.services.postgres_service import PostgresService
from app.models.models import Fundinground
from typing import List


class StageTrends:
    def __init__(self, stage:str, average:float, total:float):
        self.stage = stage
        self.average = average
        self.total = total

    def to_dict(self):
        return {
            "stage": self.stage,
            "average": self.average,
            "total": self.total
        }

class FundingYear:
    def __init__(self, year:int, total:float, average:float):
        self.year = year
        self.total = total
        self.average = average

    def to_dict(self):
        return {
            "year": self.year,
            "total": self.total,
            "average": self.average
        }

class TrendService():
    def __init__(self):
        self.PineconeService = PineconeService()
        self.PostgresService = PostgresService()

    def get_funding_trends_for_sector(self, sector:str) -> list[StageTrends]:
        # Get companies in the sector
        companies = self.PineconeService.query_pinecone(sector)
        company_uuids = [company["id"] for company in companies['matches']]

        # Get funding rounds for companies
        funding_rounds: List[Fundinground] = []
        for company_uuid in company_uuids:
            funding_rounds.extend(self.PostgresService.get_funding_rounds(company_uuid))

        # Aggegate Funding Trends
        funding_by_stage = {}
        # funding_round: Fundinground
        for funding_round in funding_rounds:
            funding_round: Fundinground
            stage = funding_round.stage
            if funding_round.fundraise_amount_usd is None:
                continue

            if stage not in funding_by_stage:
                funding_by_stage[stage] = []
            funding_by_stage[stage].append(funding_round.fundraise_amount_usd)

        funding_trends: List[StageTrends] = []
        for stage, amounts in funding_by_stage.items():
            average = sum(amounts) / len(amounts)
            total = sum(amounts)
            funding_trends.append(StageTrends(stage, average, total))
            
        return funding_trends
    
    

