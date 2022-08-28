from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint



    

# HASHING THE PASSWORDS FOR SECURITY:  pip install passlib[bcrypt]

############### from zero 


    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    
    
    class Config:
        orm_mode = True 
        

class UserOut(BaseModel):
    id: int
    email: EmailStr         
    created_at: datetime
                            ## What to return as response 
                            # Without defining the "class Config: ", we will receive an error because pydantic does not know how to work with SqlAlchemy model. 
                            ## This class will tell pydantic to go ahead and conver it to a dictionary
    class Config:
        orm_mode = True
    
    
class UserCreate(BaseModel): # we are going to inherit from BaseModel
    email: EmailStr ## This is going to make sure its a valid email address // ## pip install email validator !
    password: str  
     

     
''' class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool= True
    
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr         
    created_at: datetime
                            ## What to return as response 
                            # Without defining the "class Config: ", we will receive an error because pydantic does not know how to work with SqlAlchemy model. 
                            ## This class will tell pydantic to go ahead and conver it to a dictionary
    class Config:
        orm_mode = True




class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class PostOut(BaseModel):
    Post: Post

    class Config:
        orm_mode = True
                        
class UserCreate(BaseModel): # we are going to inherit from BaseModel
    email: EmailStr ## This is going to make sure its a valid email address // ## pip install email validator !
    password: str 
    

     '''