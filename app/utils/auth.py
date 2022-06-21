import os
from dotenv import load_dotenv, find_dotenv

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from jose import jwt, JWTError

from ..models.auth import UserFullInfo, UserLogin
from ..schemas.user import UserConvert
from ..utils.hashing import hash_password, verify_password
from ..utils.jwt import create_access_token, get_data_from_access_token
from ..config.db_tables import Users, Roles, UserRoles

load_dotenv(find_dotenv())


def register(user: UserFullInfo, database: Session):
    try:
        new_user = Users(Email=user.email, PhoneNumber=user.phone_number, FirstName=user.first_name,
                         LastName=user.last_name, Password=hash_password(user.password))
        role = database.query(Roles).filter(Roles.RoleID == 1).first()
        user_role = UserRoles(user=new_user, role=role)

        database.add(new_user, user_role)
        database.commit()
        database.refresh(new_user)
    except IntegrityError as err:
        print(err.args)
        if "users.PhoneNumber" in str(err.args):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Phone number {user.phone_number} is already in use")
        elif "users.Email" in str(err.args):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Email {user.email} is already in use")
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Something wrong with credentials")

    return new_user


def login(form_data: OAuth2PasswordRequestForm, database: Session):
    try:
        current_user = database.query(Users).filter(Users.Email == form_data.username).first()

        user_role_id_list = []

        for user_role_id in current_user.users:
            user_role_id_list.append(user_role_id.role.RoleName)

        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Invalid Credentials")
        if not verify_password(current_user.Password, form_data.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Incorrect password")

        jwt_token = create_access_token(data={
            'role': user_role_id_list,
            'id': current_user.UserID
        })
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with credentials')

    return {'access_token': jwt_token, 'token_type': 'bearer'}


def get_current_user(token: str, database: Session):
    try:
        payload = get_data_from_access_token(token)
        current_user_id = payload['id']

        current_user = database.query(Users).filter(Users.UserID == current_user_id).first()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with credentials')

    return current_user


def get_current_user_role(token: str, database: Session):
    try:
        payload = get_data_from_access_token(token)
        current_user_id = payload['id']

        current_user_role = database.query(UserRoles).filter(UserRoles.User == current_user_id).first().role.RoleName

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with credentials')

    return {'user_role': current_user_role}
