from sqlalchemy.orm import Session
from ..database import models
from datetime import datetime
from fastapi import HTTPException
from ..database.schemas import SummaryResponse, CampaignCard, PerformanceMetrics, CurrentMetrics, VolumeUnitCostTrend, ImpressionsCpm, CampaignTable

def get_campaigns(db: Session, campaign_id: str = None):
    if campaign_id:
        return db.query(models.DailyCampaign).filter(models.DailyCampaign.campaign_id == campaign_id).all()
    else:
        return db.query(models.DailyCampaign).all()

def get_scores(db: Session, campaign_id: str = None):
    if campaign_id:
        return db.query(models.DailyScore).filter(models.DailyScore.campaign_id == campaign_id).all()
    else:
        return db.query(models.DailyScore).all()

def get_summary(db: Session, campaign_id: str = None, start_date: str = None, end_date: str = None):
    start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

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

    campaign_name = campaigns[0].campaign_name if campaign_id else "All"
    date_range = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}" if start_date and end_date else "All"
    total_days = (end_date - start_date).days + 1 if start_date and end_date else "All"

    impressions = sum(campaign.impressions for campaign in campaigns)
    clicks = sum(campaign.clicks for campaign in campaigns)
    views = sum(campaign.views for campaign in campaigns)

    impression_trend = {datetime.strptime(campaign.date, '%Y-%m-%d').strftime('%Y-%m-%d'): campaign.impressions for campaign in campaigns}
    cpm_trend = {datetime.strptime(campaign.date, '%Y-%m-%d').strftime('%Y-%m-%d'): campaign.cpm for campaign in campaigns}

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