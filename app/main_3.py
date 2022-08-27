from typing import Optional
from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi import status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

import models

from database import engine,SessionLocal 






#INTEGRATION OF "models.py" to create database tables: 

models.Base.metadata.create_all(bind=engine)




app = FastAPI()


#We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.
# And then a new session will be created for the next request.This is much more efficient than keeping one open.
# For that, we will create a new dependency with yield


def get_db():
    db = SessionLocal()
    try:
        yield db # The yielded value is what is injected into path operations and other dependencies
    finally: 
        db.close()
        
    

## IN ORDER TO START THE APP WE WILL USE THE FOLLOWING:
## uvicorn app.main_3:app --reload
##         app.main_3 specifies that  the  python file called as "main_3.py" within the folder named "app"


#-------------------------------------------------------------------------------------




## BUILDING POSTGRES DATABASE CONNECTION WITH  <PSYCOPG2>

''' 
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
 '''
 
#-------------------------------------------------------------------------------------

class Post(BaseModel):
    title: str
    content: str
    published: bool= True
    rating: Optional[int] = None
    
my_posts = [{"title": "title of post_1 ", "content": "content of post_1", "id": 1},
            {"title": "title of post_2 ", "content": "content of post_2", "id": 2}]        


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i 

@app.get("/")
def root():
    return{"message": "welcome to my page 1 "}



@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return{"data": posts}



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """ , (post.title, post.content, post.published)) ##  placeholders , this way we avoid SQL INJECTION! 
    new_post = cursor.fetchone()
    conn.commit() ## this is going to push those changes that we do in the postman to the actual database 
    return{"data": new_post}





### ''' @app.post("/posts",status_code=status.HTTP_201_CREATED)
###         def create_posts(post: Post):
###             post_dict = post.dict()
###             post_dict["id"] = randrange(0,100000)
###             my_posts.append(post_dict)
###             return{"data": post_dict} '''




@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}
    


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    # IMPORTANT NOTE !!
    # Issue: In order to avoid receiving id numbers in a non-integer form like this: http://127.0.0.1:8000/posts/asdjsdsfds , 
    # We need to first validate it as a number and convert into an integer as we define in the get_post function.
    # Then we have to convert back in to a string when we want execute our SQL Query, OTHERWISE there will be a " TypeError: 'int' object does not support indexing. "
    
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)) ) 
    post = cursor.fetchone()
    print(post)
    
    post = find_post(int(id))
    if not post: # if we didnt find the post, we will raise an exception using Fast-Api's HTTPException method.
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found. ")
    return{"post_detail": post}





@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    # deleting posts
    # find the index in the array that has the required ID
    # my_posts.pop(index)
    
    cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING* """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
    
   
      
    # IMPORTANT NOTE ON     @app.delete and HTTP_204_NO_CONTENT : 
    # if we delete something , we can not return a data like this: 
    # return{"post_detail": post}
    # instead we have to use FAST-API's Response feature 
    # and return whatever the status code is.
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 



@app.put("/posts/{id}")
def update_post(id: int , post: Post):
    
    cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s  RETURNING* """ , (post.title, post.content,post.published,(str(id))) )
    post_updated = cursor.fetchone() 
    conn.commit()
    
    if post_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
        
        
    #''' post_dict = post.dict() # convert the data we get from "post: Post" to a dictionary 
    #post_dict["id"] = id  # we are gonna ad id to dictionary 
    #my_posts[index] = post_dict # and for that spesific id, index  we will replace with the new dictionary '''

   
    return{"message": post_updated}



# testing sqlalchemy Db session with depends
@app.get("/sqlalchemy_test_post")
def test_post(db: Session = Depends(get_db)):
    return{"status": "success"}

