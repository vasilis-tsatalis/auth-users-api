from typing import Annotated, Union
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status


from jose import JWTError, jwt

import os
from dotenv import load_dotenv

from .models.User import User, UserInDB
from .models.Token import Token, TokenData
from .src.auth.hashpass import verify_password, get_password_hash
from .src.auth.auth_schema import oauth2_scheme, pwd_context
from .src.auth.manage_token import create_access_token
from .src.auth.auth_user import get_user, authenticate_user, get_current_active_user
from .routes.token import token_router

# Load the stored environment variables
load_dotenv()

# Get env the values
BASE_URL= os.getenv("BASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

################## TO BE CHANGED #####################################################################
import json
with open('./api/assets/sample_db.json') as db_file:
  db_data = db_file.read()

fake_users_db = json.loads(db_data)
######################################################################################################

app = FastAPI()

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


# Main Routes of API
app.include_router(token_router, prefix=BASE_URL)