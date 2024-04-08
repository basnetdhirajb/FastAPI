from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
    

#Connecting to the database
while True:
    try:
        #Real Dict Cursor is used to view the data with columns which we don't get by default
        #Establishing the connection
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'password', cursor_factory= RealDictCursor)
        #cursor to execute SQL queries
        cur = conn.cursor()
        print('Database connection successful!')
        break
    except Exception as error:
        print("Could not connect to the database!")
        print("Error: ",error)
        time.sleep(5)


@app.get("/", status_code= status.HTTP_200_OK)
def read_root(response: Response):
     raise HTTPException(status_code= status.HTTP_200_OK, detail = "Welcome to FASTAPI")

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(response: Response):
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    return {'data': posts}

@app.get("/posts/{id}", status_code= status.HTTP_200_OK)
def get_post(id:int):
    
    cur.execute("SELECT * FROM posts WHERE id = %s",(str(id)))
    postById = cur.fetchone()
    
    if postById:
        return {'data':postById}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"No Post was found with id of {id}") 

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(newPost: Post, response: Response):
    #inPost = {"Id": newPost.id , "title": newPost.title, "content" : newPost.content, "published" : newPost.published, "rating" : newPost.rating}
    cur.execute("INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) returning *", (newPost.title, newPost.content, newPost.published))
    createdPost = cur.fetchone()
    # conn.commit()
    # cur.close()
    conn.close()
    return {'data':createdPost}

@app.delete('/posts/{id}')
def delete_post(id:int): #FAST API validates the id to be passed into query quarameter
    cur.execute("DELETE FROM posts WHERE id = %s returning *",(str(id),))
    deletedPost = cur.fetchone()
    conn.commit()
    if deletedPost:
        return {'data': deletedPost}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'Could not find post with ID of {id}')

@app.put("/posts/{id}")
def update_post(post: Post, id: int):
    cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *", (post.title, post.content, post.published, str(id)))
    updatedPost = cur.fetchone()
    conn.commit()
    if updatedPost:
        return {'data': updatedPost}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'Post with id of {id} not found')