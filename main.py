from fastapi import FastAPI

from app.routers import auth, supplication, donation, management, admin

from app.config import db


app = FastAPI(
    title="DB Coursework",
    description="Donation System",
    version="1.0.0"
)

app.include_router(
    auth.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)


app.include_router(
    supplication.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)

app.include_router(
    donation.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)


app.include_router(
    management.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)


app.include_router(
    admin.router,
    responses={
        400: {"description": "Bad request"},
        401: {"description": "User not authenticated"},
        403: {"description": "Action forbidden"},
        404: {"description": "Not found"},
        409: {"description": "Email already in use"},
    }
)


@app.get('/')
def status_check():
    return {'status': 'OK'}
