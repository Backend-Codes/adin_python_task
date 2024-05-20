from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
from fastapi import HTTPException
from ..database import models
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
    if not start_date:
        start_date = "2023-03-20"
    if not end_date:
        end_date = "2023-12-30"

    start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=422, detail="Invalid date range: start_date must be before end_date")

    start_date_minus_one = start_date - timedelta(days=1) if start_date else None

    campaigns_query = db.query(models.DailyCampaign)
    scores_query = db.query(models.DailyScore)

    if start_date_minus_one:
        campaigns_query = campaigns_query.filter(models.DailyCampaign.date >= start_date_minus_one)
        scores_query = scores_query.filter(models.DailyScore.date >= start_date_minus_one)

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

    for campaign in campaigns:
        if isinstance(campaign.date, str):
            campaign.date = datetime.strptime(campaign.date, '%Y-%m-%d')

    campaign_name = campaigns[0].campaign_name if campaign_id else "All"
    date_range = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}" if start_date and end_date else "All"
    total_days = (end_date - start_date).days + 1 if start_date and end_date else "All"

    impressions = sum(campaign.impressions for campaign in campaigns)
    clicks = sum(campaign.clicks for campaign in campaigns)
    views = sum(campaign.views for campaign in campaigns)

    impression_trend = { (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(total_days)}
    cpm_trend = { (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(total_days)}

    for campaign in campaigns:
        date_str = campaign.date.strftime('%Y-%m-%d')
        impression_trend[date_str] += campaign.impressions
        cpm_trend[date_str] += campaign.cpm

    for score in scores:
        if isinstance(score.start_date, str):
            score.start_date = datetime.strptime(score.start_date, '%Y-%m-%d')
        if isinstance(score.end_date, str):
            score.end_date = datetime.strptime(score.end_date, '%Y-%m-%d')

    unique_start_dates = list({score.start_date for score in scores})
    unique_end_dates = list({score.end_date for score in scores})
    unique_campaign_ids = list({score.campaign_id for score in scores})
    unique_campaign_names = list({score.campaign_name for score in scores})
    unique_effectiveness = [score.effectiveness for score in scores]
    unique_media = [score.media for score in scores]
    unique_creative = [score.creative for score in scores]

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
            start_date=[date.strftime('%Y-%m-%d') for date in unique_start_dates],
            end_date=[date.strftime('%Y-%m-%d') for date in unique_end_dates],
            adin_id=unique_campaign_ids,
            campaign=unique_campaign_names,
            effectiveness=unique_effectiveness,
            media=unique_media,
            creative=unique_creative
        )
    )

    return response