from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class DailyCampaignBase(BaseModel):
    campaign_id: str
    date: date
    impressions: Optional[int] = None
    clicks: Optional[int] = None
    campaign_name: Optional[str] = None
    cpm: Optional[float] = None
    views: Optional[int] = None

    class Config:
        orm_mode = True

class DailyScoreBase(BaseModel):
    campaign_id: str
    date: date
    media: Optional[float] = None
    campaign_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    effectiveness: Optional[float] = None
    status: Optional[str] = None
    creative: Optional[float] = None

    class Config:
        orm_mode = True

class CampaignsResponse(BaseModel):
    campaigns: List[DailyCampaignBase]

class ScoresResponse(BaseModel):
    scores: List[DailyScoreBase]