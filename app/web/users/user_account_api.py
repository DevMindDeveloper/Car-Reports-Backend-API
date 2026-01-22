## imports
import bcrypt
import datetime
import jwt
from fastapi import APIRouter, Depends

from app.models.users.schema_user import User
from app.tasks.schema_validation import UserInput
from app.config import CarReportCredential
from app.web.auth import token_required
from app.web import session

## blueprint and prefix
users_pb = APIRouter(prefix="/users")

## sign up api
@users_pb.post("/sign_up")
def sign_up(user_input : UserInput):

    email = user_input.email
    password = user_input.password
    
    ## search already exist user
    db_results = session.query(User).filter(User.email == email).all()

    if len(db_results) > 0:
        return {"error":"the user with same email already exist"}, 400 # bad request
    
    ## hash the password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    ## add user
    insert_user_record = User(email = email, password = hashed_password)
    session.add(insert_user_record)
    session.commit()

    return {"success":"user is added"}, 200 # success

## sign in api
@users_pb.post("/sign_in")
def sign_in(user_record : UserInput):

    email = user_record.email
    password = user_record.password

    ## search already exist user
    db_result = session.query(User).filter(User.email == email).first()

    ## check password and email
    if not db_result or not bcrypt.checkpw(password.encode("utf-8"), db_result.password.encode("utf-8")):
        return {"success":"the email or password is incorrect"}, 400 # bad request
    
    ## token creation
    token = jwt.encode({
        "user_id" : str(db_result.id),
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, CarReportCredential().app_secret_key, algorithm="HS256")

    ## return the token to user
    return {"success": token}, 200 # success

## profile request api
@users_pb.get('/profile')
def profile(user_id : int = Depends(token_required)):

    db_user_record = session.query(User).filter(User.id == user_id).first()
    
    if not db_user_record:
        return {'message': 'User not found'}, 404

    return {'user_id': db_user_record.id,
                    "user_email":db_user_record.email}
