from fastapi import status, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .jwt import get_data_from_access_token

from ..models.supplication import FundRequest
from ..config.db_tables import Users, FundRequests


def create_fund_request(fund_request_info: FundRequest, token: str, database: Session):
    try:
        payload = get_data_from_access_token(token)
        current_user_id = payload['id']

        current_user = database.query(Users).filter(Users.UserID == current_user_id).first()

        new_fund_request = FundRequests(StartAmount=fund_request_info.StartAmount,
                                        CurrentAmount=fund_request_info.StartAmount, recipient=current_user,
                                        Motivation=fund_request_info.Motivation, IBAN=fund_request_info.IBAN,
                                        Status=None)
        database.add(new_fund_request)
        database.commit()
        database.refresh(new_fund_request)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return new_fund_request
