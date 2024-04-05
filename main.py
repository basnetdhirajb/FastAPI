from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

#Using pydantic library to create a schema. This structure is what is expected to be in the JSON.
#The data received in the request will be validated against this schema.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None
    

    
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"message":"These are the posts"}

@app.post("/createpost")
def create_post(newPost: Post):
    return newPost.model_dump()