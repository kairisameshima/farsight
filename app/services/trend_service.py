from app.services.pinecone_service import PineconeService
from app.services.postgres_service import PostgresService
from app.models.models import Fundinground, Organization
from typing import List
from datetime import datetime

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


class StageTrendsChartData:
    def __init__(self, stage:str, fundraising_date:datetime,  fundraising_amount:float, organization_name:str, organizaztion_uuid:str):
        self.stage = stage
        self.fundraising_amount = fundraising_amount
        self.organization_name = organization_name
        self.organizaztion_uuid = organizaztion_uuid
        self.fundraising_date = fundraising_date

class InvestorTrends:
    def __init__(self, investor_uuid: str,  num_deals: int, total_funding: float):
        self.investor_uuid = investor_uuid
        self.num_deals = num_deals
        self.total_funding = total_funding

    def to_dict(self):
        return {
            "investor_uuid": self.investor_uuid,
            "num_deals": self.num_deals,
            "total_funding": self.total_funding
        }

    
class TrendService():
    def __init__(self):
        self.PineconeService = PineconeService()
        self.PostgresService = PostgresService()

    def get_funding_trends_for_sector(self, sector:str) -> list[StageTrends]:
        # Get companies in the sector
        companies = self.PineconeService.query_pinecone(sector)
        organization_uuids = [company["id"] for company in companies['matches']]

        # Get funding rounds for companies
        funding_rounds: List[Fundinground] = []
        for organization_uuid in organization_uuids:
            funding_rounds.extend(self.PostgresService.get_funding_rounds(organization_uuid))

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
    
    def get_data_for_funding_trends_chart(self, sector:str) -> list[StageTrendsChartData]:
        # Get companies in the sector
        companies = self.PineconeService.query_pinecone(sector)
        organization_uuids = [company["id"] for company in companies['matches']]

        # Get funding rounds for companies
        funding_rounds: List[Fundinground] = []
        organizations: dict[str, Organization] = {}
        for organization_uuid in organization_uuids:
            funding_rounds.extend(self.PostgresService.get_funding_rounds(organization_uuid))
            organizations[organization_uuid] = self.PostgresService.get_organization(organization_uuid)

        # Aggegate Funding Trends
        fundraising_data: List[StageTrendsChartData] = []
        # funding_round: Fundinground
        for funding_round in funding_rounds:
            funding_round: Fundinground

            fundraising_data.append(
                StageTrendsChartData(
                    stage= funding_round.stage,
                    fundraising_date= funding_round.investment_date,
                    fundraising_amount= funding_round.fundraise_amount_usd,
                    organization_name= organizations[funding_round.org_uuid].name,
                    organizaztion_uuid= funding_round.org_uuid
                )
            )

        return fundraising_data
    
    def get_top_investors_for_sector(self, sector:str):
        # Get companies in the sector
        companies = self.PineconeService.query_pinecone(sector)
        organization_uuids = [company["id"] for company in companies['matches']]

        # Get most active investors
        investors = self.PostgresService.get_most_active_investors(organization_uuids)

        investor_trends: List[InvestorTrends] = []

        for investor in investors:
            investor_uuid, deal_count, total_funding = investor
            investor_trends.append(InvestorTrends(investor_uuid, deal_count, total_funding))
        
        return investor_trends
        

