from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    topic: str
    contents: str
    published: bool = True
    rating: Optional[int] = None

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
    return {"data": post_list}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payLoad: Post):
    post_dict = payLoad.dict()
    post_dict['id'] = randrange(0, 9999999)
    post_list.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post_item = find_post(id)
    if not post_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    return {"data": post_item}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_item = find_post(id)
    if not post_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    else:
        post_list.pop(find_post_index(id))
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, payLoad: Post):
    post_item = find_post(id)
    if not post_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} not found")
    else:
        post_update = payLoad.dict()
        post_update['id'] = id
        post_list[find_post_index(id)] = post_update
        return {"data": post_update}


@app.post("/createposts_sample1")
def create_posts(payLoad: dict = Body(...)):
    print(f"DEV sample1:    payLoad received - {payLoad}")
    return {"Post Created": f"topic :{payLoad['topic']} || contents :{payLoad['contents']}"}

@app.post("/createposts_sample2")
def create_posts(payLoad: Post):
    print(f"DEV sample2:    payLoad received - {payLoad}")
    return {"data": payLoad}