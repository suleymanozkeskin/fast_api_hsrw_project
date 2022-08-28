import models, schemas
from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter
from fastapi import status
from sqlalchemy.orm import Session
from database import engine, get_db
from typing import List

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post]) ## here we have to import "List" from "typing" library that so we can convert the posts into a list.
                                                              ## Otherwise it will try to put all posts into the shape one of post therefore it won't work!
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()

    return posts



@router.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """ , (post.title, post.content, post.published)) ##  placeholders , this way we avoid SQL INJECTION! 
    # new_post = cursor.fetchone()
    # conn.commit() ## this is going to push those changes that we do in the postman to the actual database 
    
    
    new_post = models.Post(**post.dict()) ## this method will take the post as dictionary and automatically import it from there as opposed to manual typing version below:
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


@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    
    # IMPORTANT NOTE !!
    # Issue: In order to avoid receiving id numbers in a non-integer form like this: http://127.0.0.1:8000/posts/asdjsdsfds , 
    # We need to first validate it as a number and convert into an integer as we define in the get_post function.
    # Then we have to convert back in to a string when we want execute our SQL Query, OTHERWISE there will be a " TypeError: 'int' object does not support indexing. "
    
   # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)) ) 
   # post = cursor.fetchone()
   # print(post)
    
    print(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    
     # post = find_post(int(id))
    
    if not post: # if we didnt find the post, we will raise an exception using Fast-Api's HTTPException method.
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found. ")
  
    return{"post_detail": post}





@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db)):
    # deleting posts
    # find the index in the array that has the required ID
    # my_posts.pop(index)
    
    #cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING* """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    
    post_query = db.query(models.Post).filter(models.Post.id == id )

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
    post_query.delete(synchronize_session=False) 
    db.commit()
      
    # IMPORTANT NOTE ON     @app.delete and HTTP_204_NO_CONTENT : 
    # if we delete something , we can not return a data like this: 
    # return{"post_detail": post}
    # instead we have to use FAST-API's Response feature 
    # and return whatever the status code is.
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 



@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int , updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    #cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s  RETURNING* """ , (post.title, post.content,post.published,(str(id))) )
    #post_updated = cursor.fetchone() 
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
            
    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist.")
        
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



