from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Loan
from backend.app.schemas.loan import LoanResponse

router = APIRouter()

@router.get("", response_model=List[LoanResponse])
def get_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()

@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan_by_id(loan_id: str, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
