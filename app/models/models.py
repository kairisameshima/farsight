# coding: utf-8
from sqlalchemy import ARRAY, BigInteger, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Organization(Base):
    __tablename__ = 'organizations'

    org_uuid = Column(UUID, primary_key=True)
    cb_url = Column(Text)
    categories = Column(ARRAY(Text()))
    category_groups = Column(ARRAY(Text()))
    closed_on = Column(DateTime)
    closed_on_precision = Column(Text)
    company_profit_type = Column(Text)
    created_at = Column(DateTime)
    raw_description = Column(Text)
    web_scrape = Column(Text)
    rewritten_description = Column(Text)
    total_funding_native = Column(BigInteger)
    total_funding_currency = Column(Text)
    total_funding_usd = Column(BigInteger)
    exited_on = Column(DateTime)
    exited_on_precision = Column(Text)
    founding_date = Column(DateTime)
    founding_date_precision = Column(Text)
    general_funding_stage = Column(Text)
    logo_url = Column(Text)
    ipo_status = Column(Text)
    last_fundraise_date = Column(DateTime)
    last_funding_total_native = Column(BigInteger)
    last_funding_total_currency = Column(Text)
    last_funding_total_usd = Column(BigInteger)
    stage = Column(Text)
    org_type = Column(Text)
    city = Column(Text)
    state = Column(Text)
    country = Column(Text)
    continent = Column(Text)
    name = Column(Text)
    num_acquisitions = Column(Integer)
    employee_count = Column(Text)
    num_funding_rounds = Column(Integer)
    num_investments = Column(Integer)
    num_portfolio_organizations = Column(Integer)
    operating_status = Column(Text)
    cb_rank = Column(Integer)
    revenue_range = Column(Text)
    org_status = Column(Text)
    updated_at = Column(DateTime)
    valuation_native = Column(BigInteger)
    valuation_currency = Column(Text)
    valuation_usd = Column(BigInteger)
    valuation_date = Column(DateTime)
    org_domain = Column(Text)


class Acquisition(Base):
    __tablename__ = 'acquisitions'

    acquisition_uuid = Column(UUID, primary_key=True)
    acquiree_uuid = Column(ForeignKey('organizations.org_uuid'))
    acquirer_uuid = Column(ForeignKey('organizations.org_uuid'))
    acquisition_type = Column(Text)
    acquisition_announce_date = Column(DateTime)
    acquisition_price_usd = Column(BigInteger)
    terms = Column(Text)
    acquirer_type = Column(Text)

    organization = relationship('Organization', primaryjoin='Acquisition.acquiree_uuid == Organization.org_uuid')
    organization1 = relationship('Organization', primaryjoin='Acquisition.acquirer_uuid == Organization.org_uuid')


class Fundinground(Base):
    __tablename__ = 'fundingrounds'

    funding_round_uuid = Column(UUID, primary_key=True)
    investment_date = Column(DateTime)
    org_uuid = Column(ForeignKey('organizations.org_uuid'))
    general_funding_stage = Column(Text)
    stage = Column(Text)
    investors = Column(ARRAY(Text()))
    lead_investors = Column(ARRAY(Text()))
    fundraise_amount_usd = Column(BigInteger)
    valuation_usd = Column(BigInteger)

    organization = relationship('Organization')

    
    def __repr__(self):
        return f"<FundingRound(uuid={self.funding_round_uuid}, org_uuid={self.org_uuid}, amount_raised={self.fundraise_amount_usd})>"

