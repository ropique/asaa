from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from app import oauth2
from ..import models, schemas, oauth2, database
from sqlalchemy.orm import  Session 
from ..database import get_db
from typing import List, Optional 

router = APIRouter(
    prefix= "/vote", 
    tags = ['Vote']
)

@router.post("/", status_code= status.HTTP_200_OK)

def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"There is not post with {vote.post_id} id")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id) 
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail = f"You already voted for post with {vote.post_id} id")
        
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist")   

        vote_query.delete(synchronize_session= False)    
        db.commit()

        return {"message": "Successfully deleted vote"}