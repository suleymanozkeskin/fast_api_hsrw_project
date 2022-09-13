from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models,oauth2
router = APIRouter(tags=["Vote"] )


@router.post("/vote", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote , db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    
    # so if we wanna make a vote, we will check whether there is an already existing vote or not.
    # then we are gonna filter by Vote.post_id and see if there is already a vote for this  specific post_id 
    # however this is not enough because multiple people can vote on the same post
    # so we have to do a second check: models.Vote.user_id == current_user.id
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() # We are gonna take query the post and if the post does not exist , user can not vote on it.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist.")
     
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()
      
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id} .")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        
        
        db.add(new_vote)
        db.commit()
        return{"message": "successfully added vote"}   
        
    
    if (vote.dir == -1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id} .")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
       
            
        
        
        
        db.add(new_vote)
        db.commit()
        return{"message": "successfully added vote"}
    
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist.")
        
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "successfully deleted vote."}
            
    