## imports
import bcrypt
import datetime
import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import CarReportCredential
from app.models.users.schema_user import User
from app.web.users.schema_validation import UserSchemaValidation, SuccessModel, FailureModel
from app.web.auth import token_required
from app.web.users import app
from app.web.users.utils import get_db

## blueprint and prefix
users_pb = APIRouter(prefix= "/users")

## sign up api
@users_pb.post("/sign_up",response_model=SuccessModel, status_code = 200, responses={400:{"model":FailureModel}})
async def sign_up(user_input: UserSchemaValidation, session: AsyncSession = Depends(get_db)):

    email = user_input.email
    password = user_input.password
    
    ## search already exist user
    db_result = await session.execute(select(User).where(User.email == email))
    user_record = db_result.scalar_one_or_none()

    if user_record:
        raise HTTPException(status_code=400, detail="the user with same email already exists")
    
    ## add user
    insert_user_record = User(email = email, password = password)
    session.add(insert_user_record)
    await session.commit()
    await session.refresh(insert_user_record)

    return {"success":"user is added"} # success

## sign in api
@users_pb.post("/sign_in", response_model=SuccessModel, status_code = 200, responses={400:{"model":FailureModel}})
async def sign_in(user_record: UserSchemaValidation,session: AsyncSession = Depends(get_db)):

    email = user_record.email
    password = user_record.password

    ## search already exist user
    db_result = await session.execute(select(User).where(User.email == email))
    db_user_record = db_result.scalar_one_or_none()

    ## check password and email
    if not db_user_record:
        raise HTTPException (status_code=400, detail="the email is incorrect")
    
    elif not bcrypt.checkpw(password.encode("utf-8"), db_user_record.password.encode("utf-8")):
        raise HTTPException (status_code=400, detail="the password is incorrect")
    
    ## token creation
    token = jwt.encode({
        "user_id" : str(db_user_record.id),
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    },CarReportCredential.APP_SECRET_KEY, algorithm="HS256")

    ## return the token to user
    return {"success": token}

## profile request api
@users_pb.get('/profile')
async def profile(user_id: int = Depends(token_required), session: AsyncSession = Depends(get_db)):

    db_result = await session.execute(select(User).where(User.id == user_id))
    db_user_record = db_result.scalar_one_or_none()
    
    if not db_user_record:
        return {'message': 'User not found'}, 404

    return {'user_id': db_user_record.id,
            "user_email":db_user_record.email}
