from fastapi import APIRouter, Request, Depends, HTTPException
from seeders.db_seed import run_seed
from database.db import get_session
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/seed",
    tags=["Seed"]
)

@router.get("/run")
async def get_all(request: Request, db: Session = Depends(get_session)):
    return run_seed(db=db)
