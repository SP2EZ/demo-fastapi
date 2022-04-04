# Path Operations for Authorization

from fastapi import Depends, status, APIRouter, HTTPException
from .. import database, utils, schemas, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(prefix="/login", tags=['Login'])

@router.post("/", response_model=schemas.Token)
def verify_login(payLoad: OAuth2PasswordRequestForm = Depends()):
    record = database.cursor.execute(""" SELECT * FROM users WHERE email = %s """, (payLoad.username,)).fetchone()
    #print(f"User Details type: {type(record)}\n User Details: {record['password']}")
    if not record:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify_password(payLoad.password, record['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token with expiration time
    # below create_access_token() will take parameter as User Data which can be anything like user_id or user_role, etc
    print(f"User Details type: {type(record)}\n User Details: {record['id']}")
    access_token  = oauth2.create_access_token(payLoad={"user_id": record['id']})

    #return generated token
    #return{"token": "API token"}
    return {"access_token": access_token, "token_type": "Bearer"}
