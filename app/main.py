from typing import Optional, List
from urllib import response
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
import schemas
import utils

from database import engine,SessionLocal ,get_db

import user, post




#INTEGRATION OF "models.py" to create database tables: 

models.Base.metadata.create_all(bind=engine)




app = FastAPI()



        
    

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


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return{"message": "welcome to my page 1 "}


