from typing import Annotated, Union
from datetime import datetime, timedelta

from fastapi import Depends, APIRouter, status, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

import os
from dotenv import load_dotenv

from ..main import fake_users_db
from ..models.Token import Token
from ..src.auth.manage_token import create_access_token
from ..src.auth.auth_user import authenticate_user

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

token_router = APIRouter(
    prefix='/token',
    tags=['Create auth token']
)

@token_router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
