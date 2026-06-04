import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, APIRouter
from fastapi.security import OAuth2PasswordBearer
from core.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(username):
    ## Create a temp token which expire in 1hr

    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def current_user(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Authentication Token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired. Please log in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Authentication Token")
