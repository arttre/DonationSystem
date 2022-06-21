import os
from dotenv import load_dotenv, find_dotenv

from fastapi import status, HTTPException

from datetime import datetime, timedelta

from jose import jwt, JWTError

load_dotenv(find_dotenv())


def create_access_token(data: dict, expires_delta: timedelta = None):
    data_to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(os.environ['JWT_ACCESS_TOKEN_EXPIRE_MINUTES']))

    data_to_encode.update({'exp': expire})
    encoded_data = jwt.encode(data_to_encode, os.environ['JWT_SECRET_KEY'], algorithm=os.environ['JWT_ALGORITHM'])
    return encoded_data


def get_data_from_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, os.environ['JWT_SECRET_KEY'], algorithms=[os.environ['JWT_ALGORITHM']])
        user_id, email = payload.get('id'), payload.get('email')
        if user_id is None or email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {
        'id': user_id,
        'email': email
    }
