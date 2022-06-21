from fastapi import status, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .jwt import get_data_from_access_token

from ..models.donation import Donation
from ..models.supplication import NeedType
from ..config.db_tables import Users, FundRequests, DonationRequests, Needs, NeedFundRequests


def create_donation(fund_request_id: int, donation_info: Donation, token: str, database: Session):
    try:
        payload = get_data_from_access_token(token)
        current_user_id = payload['id']

        current_user = database.query(Users).filter(Users.UserID == current_user_id).first()

        current_fund_request_query = database.query(FundRequests).filter(FundRequests.RequestID == fund_request_id)

        current_fund_request = current_fund_request_query.first()

        if current_fund_request.Status == 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This fund request is completed')
        elif current_fund_request.Status == None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This fund request is unapproved')

        new_donation_request = DonationRequests(Amount=donation_info.Amount, benefactor=current_user,
                                                fund_request=current_fund_request, Message=donation_info.Message,
                                                Status=None)

        database.add(new_donation_request)
        database.commit()
        database.refresh(new_donation_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return new_donation_request


def get_all_uncompleted_fund_requests(database: Session):
    try:
        fund_requests_lists = database.query(FundRequests).filter(FundRequests.Status == 0).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return fund_requests_lists


def filter_fund_requests_by_given_need_types(need_types: NeedType, database: Session):
    try:
        filtered_need_fund_requests = database.query(NeedFundRequests).filter(NeedFundRequests.Need.in_(need_types.Needs)).all()

        result_list = []

        for need_fund_request in filtered_need_fund_requests:
            result_list.append({
                'need_type': need_fund_request.need.NeedName,
                'fund_request': need_fund_request.fund_request
            })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return result_list


def filter_fund_requests_by_need_type(database: Session):
    try:
        result_dict = {}

        need_types = database.query(Needs).all()

        for need_type in need_types:
            result_dict[need_type.NeedName] = []
            need_fund_requests_list = database.query(NeedFundRequests).filter(NeedFundRequests.Need == need_type.NeedID).all()
            for need_fund_request in need_fund_requests_list:
                result_dict[need_type.NeedName].append(need_fund_request.fund_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return result_dict
