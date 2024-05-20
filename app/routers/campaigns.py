from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from sqlalchemy import func
from ..services import crud
from ..database.schemas import CampaignsResponse, ScoresResponse, SummaryResponse

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
    summary = crud.get_summary(campaign_id=campaign_id, start_date=start_date, end_date=end_date, db=db)
    if not summary:
        raise HTTPException(status_code=404, detail="No summary data found")
    return summary