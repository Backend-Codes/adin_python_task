from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..services import crud
from ..database.schemas import CampaignsResponse, ScoresResponse

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