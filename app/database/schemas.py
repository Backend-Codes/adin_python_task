from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict

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

class CampaignCard(BaseModel):
    campaignName: str
    range: str
    days: int

class CurrentMetrics(BaseModel):
    impressions: int
    clicks: int
    views: int

class PerformanceMetrics(BaseModel):
    currentMetrics: CurrentMetrics

class ImpressionsCpm(BaseModel):
    impression: Dict[str, int]
    cpm: Dict[str, float]

class VolumeUnitCostTrend(BaseModel):
    impressionsCpm: ImpressionsCpm

class CampaignTable(BaseModel):
    start_date: List[str]
    end_date: List[str]
    adin_id: List[str]
    campaign: List[str]
    effectiveness: List[float]
    media: List[float]
    creative: List[float]

class SummaryResponse(BaseModel):
    campaignCard: CampaignCard
    performanceMetrics: PerformanceMetrics
    volumeUnitCostTrend: VolumeUnitCostTrend
    campaignTable: CampaignTable