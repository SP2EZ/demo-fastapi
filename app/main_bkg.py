# This script uses Pydantic Model for Structuring HTTP Request and Response

from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg import rows
from . import schemas, utils

app = FastAPI()

try:
    # Connect to an existing database
    conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='p@s!gre&', port='5432', row_factory=rows.dict_row)
    cur = conn.cursor()
    print("Database Connected !!!")
except Exception as error:
    print("Database Connection Failed, Error Encountered :")
    print(error)
    #conn.rollback()
#else:
#    conn.commit()
#finally:
#    conn.close()


@app.get("/")
def root():
    return {"message": "api demo"}



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payLoad: schemas.UserRequest):
    hashed_password = utils.hash_password(payLoad.password)
    payLoad.password = hashed_password
    create_record = cur.execute(""" INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """, (payLoad.email, payLoad.password)).fetchone()
    conn.commit()
    return create_record

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int):
    record = cur.execute(""" SELECT * FROM users WHERE id = %s """, (id,)).fetchone()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    #print(f"Data Retrieved from DB: {record}")
    return record    