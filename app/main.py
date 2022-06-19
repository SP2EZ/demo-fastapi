# This script uses Pydantic Model for Structuring HTTP Request and Response

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, users, auth, votes
import socket

app = FastAPI()

origins = ["*"]
#origins = ["https://www.google.com"]

# test middleware by running the following from a browser console after loading google.com
# fetch('http://localhost:8000/').then(res=>res.json()).then(console.log)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router) # /posts
app.include_router(users.router) # /users
app.include_router(auth.router) # /login
app.include_router(votes.router) # /votes

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

#print(local_ip)

@app.get("/")
def root():
    return {"message": f"Hello, you have reached API Default Path for Instance: {local_ip}"}


 