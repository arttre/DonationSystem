from fastapi import APIRouter, Depends

from .auth import oauth2_scheme

from sqlalchemy.orm import Session

from ..config import db
from ..models.supplication import FundRequest, NeedType
from ..utils.management import get_all_unconfirmed_fund_request, get_all_fund_request, \
    confirm_fund_request, reject_fund_request, get_all_completed_fund_requests, get_all_uncompleted_fund_requests, \
    confirm_donation_request, get_all_donation_request, get_all_unapproved_donation_request, \
    get_all_approved_donation_requests, get_all_rejected_donation_requests, reject_donation_request, \
    return_donation_request, get_all_need_types, set_need_types

router = APIRouter(
    tags=['Management'],
    prefix="/management"
)

get_db = db.get_db


@router.get('/get_all_need_types')
def read_all_need_types(token: str = Depends(oauth2_scheme),
                        database: Session = Depends(get_db)):
    return get_all_need_types(token, database)


@router.post('/set_need_types/{fund_request_id}')
def update_fund_request(fund_request_id: int, need_types: NeedType, token: str = Depends(oauth2_scheme),
                        database: Session = Depends(get_db)):
    return set_need_types(fund_request_id, need_types, token, database)


@router.get('/fund_requests/get_all_fund_requests')
def read_all_fund_requests(token: str = Depends(oauth2_scheme),
                           database: Session = Depends(get_db)):
    return get_all_fund_request(token, database)


@router.get('/fund_requests/get_all_unconfirmed_fund_requests')
def read_all_unconfirmed_fund_requests(token: str = Depends(oauth2_scheme),
                                       database: Session = Depends(get_db)):
    return get_all_unconfirmed_fund_request(token, database)


@router.get('/fund_requests/get_all_completed_fund_requests')
def read_all_completed_fund_requests(token: str = Depends(oauth2_scheme),
                                     database: Session = Depends(get_db)):
    return get_all_completed_fund_requests(token, database)


@router.get('/fund_requests/get_all_uncompleted_fund_requests')
def read_all_uncompleted_fund_requests(token: str = Depends(oauth2_scheme),
                                       database: Session = Depends(get_db)):
    return get_all_uncompleted_fund_requests(token, database)


@router.patch('/fund_requests/confirm_fund_request/{fund_request_id}')
def update_unconfirmed_fund_request(fund_request_id: int, token: str = Depends(oauth2_scheme),
                                    database: Session = Depends(get_db)):
    return confirm_fund_request(fund_request_id, token, database)


@router.delete('/fund_requests/reject_fund_request/{fund_request_id}')
def remove_fund_request(fund_request_id: int, token: str = Depends(oauth2_scheme),
                        database: Session = Depends(get_db)):
    return reject_fund_request(fund_request_id, token, database)


@router.get('/donation_requests/get_all_donation_requests')
def read_all_donation_requests(token: str = Depends(oauth2_scheme),
                               database: Session = Depends(get_db)):
    return get_all_donation_request(token, database)


@router.get('/donation_requests/get_all_unapproved_donation_requests')
def read_all_unapproved_donation_requests(token: str = Depends(oauth2_scheme),
                                          database: Session = Depends(get_db)):
    return get_all_unapproved_donation_request(token, database)


@router.get('/donation_requests/get_all_approved_donation_requests')
def read_all_approved_donation_requests(token: str = Depends(oauth2_scheme),
                                        database: Session = Depends(get_db)):
    return get_all_approved_donation_requests(token, database)


@router.get('/donation_requests/get_all_rejected_fund_requests')
def read_all_rejected_donation_requests(token: str = Depends(oauth2_scheme),
                                        database: Session = Depends(get_db)):
    return get_all_rejected_donation_requests(token, database)


@router.patch('/donation_requests/approve_donation_request/{donation_request_id}')
def update_unapproved_donation_request(donation_request_id: int, token: str = Depends(oauth2_scheme),
                                       database: Session = Depends(get_db)):
    return confirm_donation_request(donation_request_id, token, database)


@router.patch('/donation_requests/reject_donation_request/{donation_request_id}')
def update_unapproved_donation_request(donation_request_id: int, token: str = Depends(oauth2_scheme),
                                       database: Session = Depends(get_db)):
    return reject_donation_request(donation_request_id, token, database)


@router.delete('/donation_requests/return_donation_request/{donation_request_id}')
def remove_unapproved_donation_request(donation_request_id: int, token: str = Depends(oauth2_scheme),
                                       database: Session = Depends(get_db)):
    return return_donation_request(donation_request_id, token, database)