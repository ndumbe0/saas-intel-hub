from sqlalchemy import Column, Integer, String, BigInteger, Numeric, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class SaaSIdea(Base):
    __tablename__ = "saas_ideas"

    id = Column(Integer, primary_key=True, index=True)
    idea = Column(String, index=True)
    monthly_revenue = Column(Numeric(15, 2))
    monthly_traffic = Column(BigInteger)
    revenue_per_visitor = Column(Numeric(10, 4))
    starting_costs = Column(Numeric(15, 2))
    solopreneur_score = Column(Integer)
    icp = Column(Text)
    growth_tactics = Column(Text)  # JSON array stored as text
    source_file = Column(String)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())
