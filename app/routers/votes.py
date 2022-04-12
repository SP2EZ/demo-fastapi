# Path Operations for collecting votes

from fastapi import Depends, status, HTTPException, APIRouter
from .. import schemas, database, oauth2

router = APIRouter(prefix="/votes", tags=['Votes'])

@router.post("/")
def cast_vote(payLoad: schemas.VoteData, token_data: int = Depends(oauth2.get_current_user_id)):
    # Check if post exists
    existing_post_record = database.cursor.execute(""" SELECT * FROM posts where id = %s """, (payLoad.post_id,)).fetchone()
    if not existing_post_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post: {payLoad.post_id} Not Found")
    # Checking if the Vote Request is new
    existing_vote_record = database.cursor.execute(""" SELECT * FROM votes where post_id = %s AND user_id = %s """, (payLoad.post_id, token_data.id)).fetchone()
    if not existing_vote_record:
        # Casting New Up-Vote on a Post
        if payLoad.vote_dir:
            database.cursor.execute(""" INSERT INTO votes (post_id, user_id) VALUES (%s, %s) RETURNING * """, (payLoad.post_id, token_data.id)).fetchone()
            database.conn.commit()
            return {"message": "Post Voted"}
    # Else Removing Vote from Existing Post
    if not payLoad.vote_dir:
        # Deleting Entry from Votes Table
        database.cursor.execute(""" DELETE FROM votes WHERE post_id = %s AND user_id = %s RETURNING * """, (payLoad.post_id, token_data.id)).fetchone()
        database.conn.commit()
        return {"message": "Post Un-Voted"}
    # On receiving duplicate vote request Raise HTTP_409_CONFLICT 
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already Voted Post : {payLoad.post_id}")
    