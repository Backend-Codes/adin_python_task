from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from ..database.database import get_db
from ..services import crud
from ..database import models
from ..database.schemas import CampaignsResponse, ScoresResponse, SummaryResponse, CampaignCard, PerformanceMetrics, CurrentMetrics, VolumeUnitCostTrend, ImpressionsCpm, CampaignTable

router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"]
)

@router.get("/", response_model=CampaignsResponse)
def read_campaigns(campaign_id: str = None, db: Session = Depends(get_db)):
    campaigns = crud.get_campaigns(db, campaign_id=campaign_id)
    if not campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"campaigns": campaigns}

@router.get("/scores", response_model=ScoresResponse)
def read_scores(campaign_id: str = None, db: Session = Depends(get_db)):
    scores = crud.get_scores(db, campaign_id=campaign_id)
    if not scores:
        raise HTTPException(status_code=404, detail="Scores not found")
    return {"scores": scores}

@router.get("/summary", response_model=SummaryResponse)
def get_summary(campaign_id: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    # Fetch campaign data
    campaigns_query = db.query(models.DailyCampaign)
    scores_query = db.query(models.DailyScore)

    if start_date:
        campaigns_query = campaigns_query.filter(models.DailyCampaign.date >= start_date)
        scores_query = scores_query.filter(models.DailyScore.date >= start_date)

    if end_date:
        campaigns_query = campaigns_query.filter(models.DailyCampaign.date <= end_date)
        scores_query = scores_query.filter(models.DailyScore.date <= end_date)

    if campaign_id:
        campaigns_query = campaigns_query.filter(models.DailyCampaign.campaign_id == campaign_id)
        scores_query = scores_query.filter(models.DailyScore.campaign_id == campaign_id)

    campaigns = campaigns_query.all()
    scores = scores_query.all()

    if not campaigns or not scores:
        raise HTTPException(status_code=404, detail="No data found for the given criteria")

    # Calculate summary
    campaign_name = campaigns[0].campaign_name if campaign_id else "All"
    date_range = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}" if start_date and end_date else "All"
    total_days = (end_date - start_date).days + 1 if start_date and end_date else "All"

    impressions = sum(campaign.impressions for campaign in campaigns)
    clicks = sum(campaign.clicks for campaign in campaigns)
    views = sum(campaign.views for campaign in campaigns)

    impression_trend = {datetime.strptime(campaign.date, '%Y-%m-%d').strftime('%Y-%m-%d'): campaign.impressions for campaign in campaigns}
    cpm_trend = {datetime.strptime(campaign.date, '%Y-%m-%d').strftime('%Y-%m-%d'): campaign.cpm for campaign in campaigns}

    # Compile response
    response = SummaryResponse(
        campaignCard=CampaignCard(
            campaignName=campaign_name,
            range=date_range,
            days=total_days
        ),
        performanceMetrics=PerformanceMetrics(
            currentMetrics=CurrentMetrics(
                impressions=impressions,
                clicks=clicks,
                views=views
            )
        ),
        volumeUnitCostTrend=VolumeUnitCostTrend(
            impressionsCpm=ImpressionsCpm(
                impression=impression_trend,
                cpm=cpm_trend
            )
        ),
        campaignTable=CampaignTable(
            start_date=[datetime.strptime(score.start_date, '%Y-%m-%d').strftime('%Y-%m-%d') for score in scores],
            end_date=[datetime.strptime(score.end_date, '%Y-%m-%d').strftime('%Y-%m-%d') for score in scores],
            adin_id=[score.campaign_id for score in scores],
            campaign=[score.campaign_name for score in scores],
            effectiveness=[score.effectiveness for score in scores],
            media=[score.media for score in scores],
            creative=[score.creative for score in scores]
        )
    )

    return response