from fastapi import status, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .jwt import get_data_from_access_token

from ..config.db_tables import UserRoles, Users, Needs


def get_all_users(token: str, database: Session):
    if not check_admin_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")

    try:
        users_list = database.query(Users).all()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return users_list


def get_specific_user_role(user_id: int, token: str, database: Session):
    if not check_admin_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")

    try:
        user_role = database.query(UserRoles).filter(UserRoles.User == user_id).first().role.RoleName
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return {'user_role': user_role}


def upgrade_user_to_manager(user_id: int, token: str, database: Session):
    if not check_admin_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")

    try:
        current_user_role_query = database.query(UserRoles).filter(UserRoles.User == user_id)

        current_user_role = current_user_role_query.first()

        if current_user_role.Role == 2:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user is manager already")

        current_user_role_query.update({
            'Role': 2
        })

        current_user_role = current_user_role_query.first()

        database.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return current_user_role.user


def remove_specific_user(user_id: int, token: str, database: Session):
    if not check_admin_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")

    try:
        current_user_query = database.query(Users).filter(Users.UserID == user_id)

        current_user_copy = current_user_query.first()
        current_user_query.delete()

        database.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Something wrong with the provided data')

    return current_user_copy


def add_need_type(need_type_name: str, token, database: Session):
    if not check_admin_role_by_token(token, database):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")

    try:
        new_need_type = Needs(NeedName=need_type_name)

        database.add(new_need_type)
        database.commit()
        database.refresh(new_need_type)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"This need type is already in use")
    return new_need_type


def check_admin_role_by_token(token: str, database: Session):
    payload = get_data_from_access_token(token)
    user_id = payload['id']

    current_user = database.query(UserRoles).filter(UserRoles.User == user_id).first()

    if current_user.Role == 3:
        return True
    else:
        return False
