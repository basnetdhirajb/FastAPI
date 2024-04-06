from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

myPosts = []
postID = 0

#Using pydantic library to create a schema. This structure is what is expected to be in the JSON.
#The data received in the request will be validated against this schema.
class Post(BaseModel):
    id : Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None
    
@app.get("/", status_code= status.HTTP_200_OK)
def read_root(response: Response):
     raise HTTPException(status_code= status.HTTP_200_OK, detail = "Welcome to FASTAPI")

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(response: Response):
    return {'data': myPosts}

@app.get("/posts/{id}", status_code= status.HTTP_200_OK)
def get_post(id:int):
    
    for post in myPosts:
        if post['id'] == id:
            return {'data':post}
   
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"No Post was found with id of {id}") 

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(newPost: Post, response: Response):
    #inPost = {"Id": newPost.id , "title": newPost.title, "content" : newPost.content, "published" : newPost.published, "rating" : newPost.rating}
    postDict = newPost.model_dump()
    postDict['id'] = randrange(0,100000)
    myPosts.append(postDict)
    return {'data':postDict}

@app.delete('/posts/{id}')
def delete_post(id:int): #FAST API validates the id to be passed into query quarameter
    for post in myPosts:
        if post['id'] == id:
            myPosts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'Could not find post with ID of {id}')

@app.put("/posts/{id}")
def update_post(updatedPost: Post, id: int):
    for i, post in enumerate(myPosts):
        if post['id'] == id:
            postDict = updatedPost.model_dump()
            postDict['id'] = id
            myPosts[i] = postDict
            return {'detail':'Post has been updated'}
        
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'Post with id of {id} not found')