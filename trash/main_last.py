from typing import Union

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()



## BUILDING POSTGRES DATABASE CONNECTION WITH  <PSYCOPG2>

while True:
    
    try:
# Connect to your postgres DB
        conn = psycopg2.connect(host='localhost' ,database="fastapi", user="postgres", password ="1234", cursor_factory=RealDictCursor)
    
# Open a cursor to perform database operations
        cursor = conn.cursor()
    
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Connection to database failed.")
        print("Error:" , error)
        time.sleep(2) ## gonna sleep for 2 seconds before trying connecting again.
        
# Execute a query
    #cur.execute("SELECT * FROM my_data")

# Retrieve query results
    #records = cur.fetchall()


my_posts = [{"title": "title of the post 1", "content": " content of post 1","id": 1}, 
            {"title": "title of the post 2", "content": " content of post 2","id": 1}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
        



@app.get("/") # "/" this is path that we have to decorate.
def root():
    return {"message": "Welcome to my API"}




## uvicorn main:app 

@app.get("/posts")
def get_posts():
    return {"data:" , "This is your post "}



@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO  posts (title, content,published) VALUES (%s,%s,%s)  RETURNING * """,
                  (post.title ,post.content, post.published))
    new_post= cursor.fetchone()

    return{"data" : new_post}
    

@app.get("get_post")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": my_posts}   
