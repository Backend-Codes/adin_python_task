from sqlalchemy.orm import Session
from ..database import models

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