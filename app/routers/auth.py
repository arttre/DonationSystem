from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..config import db
from ..models.auth import UserFullInfo
from ..utils.auth import register, login, get_current_user, get_current_user_role

router = APIRouter(
    tags=['Authentication'],
    prefix="/auth"
)

get_db = db.get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post('/register')
def user_registration(user: UserFullInfo, database: Session = Depends(get_db)):
    return register(user, database)


@router.post('/login')
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    return login(form_data, database)


@router.get('/who_am_i')
def who_am_i(token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return get_current_user(token, database)


@router.get('/my_role')
def my_role(token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    return get_current_user_role(token, database)
