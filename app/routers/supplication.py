from fastapi import APIRouter, Depends

from .auth import oauth2_scheme

from sqlalchemy.orm import Session

from ..config import db
from ..models.supplication import FundRequest
from ..utils.supplication import create_fund_request

router = APIRouter(
    tags=['Supplication'],
    prefix="/supplication"
)

get_db = db.get_db


@router.post('/create_fund_request')
def request_funds(fund_request_info: FundRequest, token: str = Depends(oauth2_scheme),
                  database: Session = Depends(get_db)):
    return create_fund_request(fund_request_info, token, database)
