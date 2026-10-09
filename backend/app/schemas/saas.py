from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class SaaSIdeaBase(BaseModel):
    idea: Optional[str] = None
    monthly_revenue: Optional[float] = None
    monthly_traffic: Optional[int] = None
    revenue_per_visitor: Optional[float] = None
    starting_costs: Optional[float] = None
    solopreneur_score: Optional[int] = None
    icp: Optional[str] = None
    growth_tactics: Optional[Any] = None

class SaaSIdeaCreate(SaaSIdeaBase):
    pass

class SaaSIdea(SaaSIdeaBase):
    id: int
    source_file: Optional[str] = None
    ingested_at: Optional[datetime] = None

    class Config:
        from_attributes = True
