from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..config import db
from ..config.db_tables import FundRequests
from ..utils.admin import get_all_users, upgrade_user_to_manager, remove_specific_user, add_need_type, get_specific_user_role

router = APIRouter(
    tags=['Administration'],
    prefix="/admin"
)

get_db = db.get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get('/get_all_users')
def read_all_users(token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return get_all_users(token, database)


@router.get('/get_specific_user_role/{user_id}')
def read_user_role(user_id: int, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return get_specific_user_role(user_id, token, database)


@router.patch('/give_manager_role/{user_id}')
def update_user_to_manager(user_id: int, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return upgrade_user_to_manager(user_id, token, database)


@router.delete('/remove_user/{user_id}')
def delete_user(user_id: int, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return remove_specific_user(user_id, token, database)


@router.post('/add_need_type')
def create_new_need_type(need_type_name: str, token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return add_need_type(need_type_name, token, database)
