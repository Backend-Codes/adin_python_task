from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class DailyCampaign(Base):
    __tablename__ = "tbl_daily_campaigns"

    campaign_id = Column(String, primary_key=True, index=True)
    date = Column(Date, primary_key=True)
    impressions = Column(Integer)
    clicks = Column(Integer)
    campaign_name = Column(String)
    cpm = Column(Float)
    views = Column(Integer)

class DailyScore(Base):
    __tablename__ = "tbl_daily_scores"

    campaign_id = Column(String, primary_key=True, index=True)
    date = Column(Date, primary_key=True)
    media = Column(Float)
    campaign_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    effectiveness = Column(Float)
    status = Column(String)
    creative = Column(Float)