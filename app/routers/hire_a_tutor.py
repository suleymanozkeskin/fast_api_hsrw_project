from turtle import title
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    tags=["Hire_A_Tutor"]
)



## WE WILL CREATE TUTOR PROFILES AND THIS PROFILES CAN BE FILTERED BY THEIR GPA , THEIR AVG REVIEW  , FACULTY_NAME WHICH IS GONNA BE SELECTED FROM A DROPDOWN MENU , HOURLY RATE etc..

## WE ALSO HAVE TO ADD A REVIEW COMMENT SECTION FOR PROFILES THAT IS VISIBLE TO EVERYONE.

## WE NEED TO IMPLEMENT A PAYMENT SYSTEM , SUCH AS STRIPE  





# @router.get("/tutor_profiles", response_model=List[schemas.TutorList]) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
#                                                               ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
# def get_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
#     # MAMIYE SOR, SEARCH ÖZELLIGI CALISMIYOR , GERISINDE PROBLEM YOK.
    
    

    
#     #if limit < int(all_existing_posts_count):
#     #    return posts + f"It seems like there are not that many posts yet."
    
#     profiles = db.query(models.Hire_Tutor).all()
#     print(type(profiles))
#     return profiles  




@router.get("/employer_profile/{id}", response_model=schemas.HireTutor) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                                 ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_tutor_profile(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
 
    post = db.query(models.Hire_Tutor).filter(models.Hire_Tutor.id == id).first()
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tutor profile with id: {id} was not found.")
        
    # if post.id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    return post

    


@router.post("/hire_tutor_posts",status_code=status.HTTP_201_CREATED, response_model=schemas.HireTutor)
def create_tutor_hiring_posts(post: schemas.HireTutor, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     
    
    if post.employer_email != current_user.email: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    new_post = models.Hire_Tutor(id = current_user.id,  **post.dict()) 
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post 
    return new_post





@router.put("/hire_tutor_posts/{id}",response_model=schemas.HireTutor)
def update_tutor_hiring_post(id: int , updated_post: schemas.HireTutor, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
   
    post_query = db.query(models.Hire_Tutor).filter(models.Hire_Tutor.id == id)
    
    post = post_query.first()
            
    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.employer_email != current_user.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail="Not authorized to perform requested action." )
    
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
        
    #''' post_dict = post.dict() # convert the data we get from "post: Post" to a dictionary 
    #post_dict["id"] = id  # we are gonna ad id to dictionary 
    #my_posts[index] = post_dict # and for that spesific id, index  we will replace with the new dictionary '''

   
    return post_query.first()



@router.delete("/hire_tutor_posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_tutor_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
 
    
    
    post_query = db.query(models.Hire_Tutor).filter(models.Hire_Tutor.id == id )   # we define the post here

    post = post_query.first() # then we find that post by using .first()
    
    if post == None:  # then we will check if the post is not there 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    
    post_query.delete(synchronize_session=False)  # and finally if everything checks out , we will let them to delete the post.
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 








# COME BACK LATER FOR GETTING A LIST OF ALL EXISTING TUTORS

@router.get("/employer_list", response_model=List[schemas.HireTutor]) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_tutors_list(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
   
    
    print(search)

    
    posts = db.query(models.Hire_Tutor).all()
    return posts  
    