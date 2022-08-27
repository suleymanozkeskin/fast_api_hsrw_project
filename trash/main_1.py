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




        



@app.get("/") # "/" this is path that we have to decorate.
def root():
    return {"message": "Welcome to my API"}




## uvicorn main:app 

@app.get("/posts")
def get_posts():
    return {"data:" , "This is your post "}



    
@app.post("/create_posts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return{"new_post": f"title {payload['title']} content:{payload['content']}"}



