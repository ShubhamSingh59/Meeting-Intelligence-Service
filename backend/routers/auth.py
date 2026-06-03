from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.security import create_access_token

router = APIRouter()

MOCK_USER = {"username": "singhshubham", "password": "singh123"}

@router.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != MOCK_USER["username"] or form_data.password != MOCK_USER["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(username=form_data.username)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }