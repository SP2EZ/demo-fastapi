# Path Operations for posts

from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import schemas, database, oauth2
from typing import List

router = APIRouter(prefix="/posts", tags=['Posts'])

# By adding -> limit: int = 5 in our get_posts, we are setting up Query Paramater
# Anything after the question mark in the website "www.website.com/posts?limit=3" is key value pair that allows users to filter the results of a request
# In our case "limit", "skip" & "search" is the Query Paramater
# int = 5 means we setting default value of limit
@router.get("/", response_model=List[schemas.PostResponseWithLikes])
def get_posts(token_data: int = Depends(oauth2.get_current_user_id), limit: int = 5, skip: int = 0, search: str = ""):
    search = "%"+search+"%"
    #record = database.cursor.execute(""" SELECT * FROM posts WHERE user_id = %s AND title ILIKE %s LIMIT %s OFFSET %s """, (token_data.id, search, limit, skip)).fetchall()
    record = database.cursor.execute(""" 
    SELECT P.*, COUNT(V.post_id) likes FROM posts P LEFT JOIN votes V 
    ON P.id = V.post_id
    WHERE P.user_id = %s AND P.title ILIKE %s
    GROUP BY P.id
    LIMIT %s OFFSET %s 
    """, (token_data.id, search, limit, skip)).fetchall()

    #print(f"Typeof Data Received {type(record)} \n Data Retrieved from DB: {record}")
    return record

# Adding token_data: int = Depends(oauth2.get_current_user_id) in the below function forces user to provide Token so they are Authorized before they can create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payLoad: schemas.PostRequest, token_data: int = Depends(oauth2.get_current_user_id)):
    # Getting Email using User ID from DB
    # current_user = oauth2.get_current_user(token_data.id)

    record = database.cursor.execute(""" INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING * """, (payLoad.title, payLoad.content, payLoad.published, token_data.id)).fetchone()
    database.conn.commit()
    #print(f"Data Created in DB for User - {current_user} : {record}")
    return record

@router.get("/{id}", response_model=schemas.PostResponseWithLikes)
def get_post(id: int, token_data: int = Depends(oauth2.get_current_user_id)):
    #record = database.cursor.execute(""" SELECT * FROM posts WHERE id = %s AND user_id = %s """, (id, token_data.id)).fetchone()
    record = database.cursor.execute(""" 
    SELECT P.*, COUNT(V.post_id) likes FROM posts P LEFT JOIN votes V
    ON P.id = V.post_id
    WHERE P.id = %s AND P.user_id = %s
    GROUP BY P.id 
    """, (id, token_data.id)).fetchone()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    #print(f"Data Retrieved from DB: {record}")
    return record

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, token_data: int = Depends(oauth2.get_current_user_id)):
    delete_record = database.cursor.execute(""" DELETE FROM posts WHERE id = %s AND user_id = %s returning * """, (id, token_data.id)).fetchone()
    #print(f"Post Deleted : {delete_record}")
    database.conn.commit()
    if not delete_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, payLoad: schemas.PostRequest, token_data: int = Depends(oauth2.get_current_user_id)):
    update_record = database.cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s AND user_id = %s RETURNING *""", (payLoad.title, payLoad.content, payLoad.published, id, token_data.id)).fetchone()
    #print(f"Updated Post in DB : {update_record}")
    database.conn.commit()
    if not update_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    else:
        return update_record