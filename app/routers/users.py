# Path Operations for users

from fastapi import Response, status, HTTPException, APIRouter
from .. import schemas, database, utils

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payLoad: schemas.UserRequest):
    hashed_password = utils.hash_password(payLoad.password)
    payLoad.password = hashed_password
    create_record = database.cursor.execute(""" INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """, (payLoad.email, payLoad.password)).fetchone()
    database.conn.commit()
    return create_record

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int):
    record = database.cursor.execute(""" SELECT * FROM users WHERE id = %s """, (id,)).fetchone()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    #print(f"Data Retrieved from DB: {record}")
    return record   