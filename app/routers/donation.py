from fastapi import APIRouter, Depends

from .auth import oauth2_scheme

from sqlalchemy.orm import Session

from ..config import db
from ..models.donation import Donation
from ..models.supplication import NeedType
from ..utils.donation import create_donation, get_all_uncompleted_fund_requests, \
    filter_fund_requests_by_given_need_types, filter_fund_requests_by_need_type

router = APIRouter(
    tags=['Donation'],
    prefix="/donation"
)

get_db = db.get_db


@router.get('/get_fund_requests')
def read_all_completed_fund_requests(database: Session = Depends(get_db)):
    return get_all_uncompleted_fund_requests(database)


@router.post('/filter_fund_requests_by_given_need_type')
def read_fund_requests_by_given_need_type(need_types: NeedType, database: Session = Depends(get_db)):
    return filter_fund_requests_by_given_need_types(need_types, database)


@router.get('/filter_fund_requests_by_need_type')
def read_fund_requests_by_need_types(database: Session = Depends(get_db)):
    return filter_fund_requests_by_need_type(database)


@router.post('/create_donation/{fund_request_id}')
def request_funds(fund_request_id: int, donation_info: Donation, token: str = Depends(oauth2_scheme),
                  database: Session = Depends(get_db)):
    return create_donation(fund_request_id, donation_info, token, database)
