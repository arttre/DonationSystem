from fastapi import status, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .jwt import get_data_from_access_token

from ..models.supplication import FundRequest, NeedType
from ..config.db_tables import Users, UserRoles, FundRequests, DonationRequests, Needs, NeedFundRequests


def get_all_fund_request(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        fund_requests_lists = database.query(FundRequests).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return fund_requests_lists


def get_all_unconfirmed_fund_request(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        fund_requests_lists = database.query(FundRequests).filter(FundRequests.Status == None).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return fund_requests_lists


def get_all_completed_fund_requests(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        fund_requests_lists = database.query(FundRequests).filter(FundRequests.Status == 1).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return fund_requests_lists


def get_all_uncompleted_fund_requests(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        fund_requests_lists = database.query(FundRequests).filter(FundRequests.Status == 0).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return fund_requests_lists


def confirm_fund_request(fund_request_id: int, token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        current_fund_request_query = database.query(FundRequests).filter(FundRequests.RequestID == fund_request_id)
        current_fund_request_query.update({
            'Status': 0
        })
        database.commit()

        current_fund_request = current_fund_request_query.first()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return current_fund_request


def reject_fund_request(fund_request_id: int, token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        current_fund_request_query = database.query(FundRequests).filter(FundRequests.RequestID == fund_request_id)

        current_fund_request_copy = current_fund_request_query.first()
        current_fund_request_query.delete()

        database.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return current_fund_request_copy


def get_all_donation_request(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        donation_requests_lists = database.query(DonationRequests).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return donation_requests_lists


def get_all_unapproved_donation_request(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        donation_requests_lists = database.query(DonationRequests).filter(DonationRequests.Status == None).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return donation_requests_lists


def get_all_approved_donation_requests(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        donation_requests_lists = database.query(DonationRequests).filter(DonationRequests.Status == 1).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return donation_requests_lists


def get_all_rejected_donation_requests(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        donation_requests_lists = database.query(DonationRequests).filter(DonationRequests.Status == 0).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return donation_requests_lists


def confirm_donation_request(donation_request_id: int, token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        current_donation_request_query = database.query(DonationRequests).\
            filter(DonationRequests.DonationID == donation_request_id)

        current_donation_request = current_donation_request_query.first()

        if current_donation_request.Status == 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This donation request is approved')

        related_fund_request_query = database.query(FundRequests). \
            filter(FundRequests.RequestID == current_donation_request.FundRequest)

        related_fund_request = related_fund_request_query.first()

        if related_fund_request.Status == 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This fund request is completed')

        current_donation_request_query.update({
            'Status': 1
        })

        related_fund_request_query.update({
            'CurrentAmount': related_fund_request.CurrentAmount - current_donation_request.Amount
        })

        if related_fund_request.CurrentAmount <= 0:
            related_fund_request_query.update({
                'Status': 1
            })

        database.commit()

        database.refresh(current_donation_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return current_donation_request


def reject_donation_request(donation_request_id: int, token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        current_donation_request_query = database.query(DonationRequests). \
            filter(DonationRequests.DonationID == donation_request_id)

        current_donation_request = current_donation_request_query.first()

        current_donation_request_query.update({
            'Status': 0
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return current_donation_request


def return_donation_request(donation_request_id: int, token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        current_donation_request_query = database.query(DonationRequests).\
            filter(DonationRequests.DonationID == donation_request_id)

        current_donation_request_copy = current_donation_request_query.first()
        current_donation_request_query.delete()

        database.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return current_donation_request_copy


def get_all_need_types(token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        need_types_list = database.query(Needs).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return need_types_list


def set_need_types(fund_request_id: int, need_types: NeedType, token: str, database: Session):
    if not check_manager_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a manager")
    try:
        confirm_fund_request(fund_request_id, token, database)

        need_type_ids_list = database.query(Needs.NeedID).all()

        for need_type in set(need_types.Needs):
            if (need_type,) not in need_type_ids_list:
                continue

            if database.query(NeedFundRequests).\
                    filter(NeedFundRequests.Need == need_type, NeedFundRequests.FundRequest == fund_request_id).first():
                continue

            new_need_fund_request = NeedFundRequests(Need=need_type, FundRequest=fund_request_id)

            database.add(new_need_fund_request)

        database.commit()

        need_type_fund_request_list = database.query(NeedFundRequests).\
            filter(NeedFundRequests.FundRequest == fund_request_id).all()

        result_list = []

        for need_type_fund_request in need_type_fund_request_list:
            result_list.append({
                'need_type': need_type_fund_request.need.NeedName,
                'fund_request': need_type_fund_request.fund_request
            })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return result_list


def check_manager_role_by_token(token: str, database: Session):
    payload = get_data_from_access_token(token)

    if 'manager' in payload['role'] or 'admin' in payload['role']:
        return True
    else:
        return False
