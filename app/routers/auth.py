from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Response 
from sqlalchemy.orm import  Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from .. import database, schemas, models,utils, oauth2


router = APIRouter(
    
    tags = ['Authentication']
)

@router.post('/login', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    

  
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Email or password is not correct")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"email or password is not correct")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
