# This script only use Pydantic Model for Structuring Request (not Response)

from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg import rows
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

try:
    # Connect to an existing database
    conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='p@s!gre&', port='5433', row_factory=rows.dict_row)
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

post_list = [{"topic": "sample topic", "contents": "sample post ka content", "published": "False", "id": 0}, {"topic": "sample2 topic", "contents": "sample2 post ka content", "published": "True", "rating": 7, "id": 1}]

def find_post(id):
    for post_item in post_list:
        if post_item['id'] == id:
            return post_item
    #else:
    #    return "Id doesn't Exist"
def find_post_index(id):
    for index, post_item in enumerate(post_list):
        if post_item['id'] == id:
            return index

@app.get("/")
def root():
    return {"message": "api demo"}

@app.get("/posts")
def get_posts():
    record = cur.execute(""" SELECT * FROM posts """).fetchall()
    #print(f"Data Retrieved from DB: {record}")
    return {"data": record}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payLoad: Post):
    record = cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (payLoad.title, payLoad.content, payLoad.published)).fetchone()
    conn.commit()
    #print(f"Data Created on DB: {record}")
    return {"data": record}

@app.get("/posts/{id}")
def get_post(id: int):
    record = cur.execute(""" SELECT * FROM posts WHERE id = %s """, (id,)).fetchone()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    #print(f"Data Retrieved from DB: {record}")
    return {"data": record}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    delete_record = cur.execute(""" DELETE FROM posts WHERE id = %s returning * """, (id,)).fetchone()
    #print(f"Post Deleted : {delete_record}")
    conn.commit()
    if not delete_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, payLoad: Post):
    update_record = cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (payLoad.title, payLoad.content, payLoad.published, id)).fetchone()
    #print(f"Updated Post in DB : {update_record}")
    conn.commit()
    if not update_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    else:
        return {"data": update_record}

