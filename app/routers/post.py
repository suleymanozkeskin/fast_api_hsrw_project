from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    tags=["Posts"]
)



@router.get("/posts", response_model=List[schemas.PostVoteOut]) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # MAMIYE SOR, SEARCH ÖZELLIGI CALISMIYOR , GERISINDE PROBLEM YOK.
    
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    # .offset(skip) means whatever number is assigned to skip in the defined function , will be skipped while retrieving posts.
    
    # search: [Optional]str = ""   means that users can make a search for something specific. From title ,content etc. 
    # In this case its gonna be title with the following code: .filter(models.Post.title.contains(search))
    
    print(search)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()                       #.filter(models.Post.owner_id == current_user.id).all()
    
    
    #if limit < int(all_existing_posts_count):
    #    return posts + f"It seems like there are not that many posts yet."
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts  
    
    
    # posts = db.query(models.Post, func.count(models.Post.id).label("votes").group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())
    # return posts  
    
    
    # left outer join -> .join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True)
    # count and name as -> func.count(models.Vote.post_id).label("votes"))
   
    # print(results)
    # return results
# WHICH TRANSLATES INTO SQL QUERY AS FOLLOWING:

    
    



@router.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """ , (post.title, post.content, post.published)) ##  placeholders , this way we avoid SQL INJECTION! 
    # new_post = cursor.fetchone()
    # conn.commit() ## this is going to push those changes that we do in the postman to the actual database 
    
    
    
    new_post = models.Post(owner_id=current_user.id,  **post.dict()) ## this method will take the post as dictionary and automatically import it from there as opposed to manual typing version below:
    # new_post = models.Post(title=post.title, content=post.content , published= post.published)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post 
    return new_post





### ''' @app.post("/posts",status_code=status.HTTP_201_CREATED)
###         def create_posts(post: Post):
###             post_dict = post.dict()
###             post_dict["id"] = randrange(0,100000)
###             my_posts.append(post_dict)
###             return{"data": post_dict} '''




''' @router.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}
     '''
@router.get("/posts/{id}", response_model=schemas.Post) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #post = post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")
        
    if post.owner_id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action." )
    
    return post

# @router.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session = Depends(get_db)):
    
#     # IMPORTANT NOTE !!
#     # Issue: In order to avoid receiving id numbers in a non-integer form like this: http://127.0.0.1:8000/posts/asdjsdsfds , 
#     # We need to first validate it as a number and convert into an integer as we define in the get_post function.
#     # Then we have to convert back in to a string when we want execute our SQL Query, OTHERWISE there will be a " TypeError: 'int' object does not support indexing. "
    
#    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)) ) 
#    # post = cursor.fetchone()
#    # print(post)
    

    
#     if not post: # if we didnt find the post, we will raise an exception using Fast-Api's HTTPException method.
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail= f"post with id: {id} was not found. ")
    
#     return{post}





@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # deleting posts
    # find the index in the array that has the required ID
    # my_posts.pop(index)
    
    #cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING* """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    
    post_query = db.query(models.Post).filter(models.Post.id == id )   # we define the post here

    post = post_query.first() # then we find that post by using .first()
    
    if post == None:  # then we will check if the post is not there 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.owner_id != current_user.id: # then we will check if the user who is logged in , actually owns the post 
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED,detail="Not authorized to perform requested action." )
    
    
    post_query.delete(synchronize_session=False)  # and finally if everything checks out , we will let them to delete the post.
    db.commit()
      
    # IMPORTANT NOTE ON     @app.delete and HTTP_204_NO_CONTENT : 
    # if we delete something , we can not return a data like this: 
    # return{"post_detail": post}
    # instead we have to use FAST-API's Response feature 
    # and return whatever the status code is.
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 



@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int , updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    #cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s  RETURNING* """ , (post.title, post.content,post.published,(str(id))) )
    #post_updated = cursor.fetchone() 
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
            
    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail="Not authorized to perform requested action." )
    
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
        
    #''' post_dict = post.dict() # convert the data we get from "post: Post" to a dictionary 
    #post_dict["id"] = id  # we are gonna ad id to dictionary 
    #my_posts[index] = post_dict # and for that spesific id, index  we will replace with the new dictionary '''

   
    return post_query.first()



# testing sqlalchemy Db session with depends
@router.get("/sqlalchemy_test_post")
def test_post(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    
    return posts 



