## imports
import datetime
from flask import request, jsonify
from flask_smorest import Blueprint
import jwt

from app.models.users.schema_user import User
from app.web.users.schema_validation import UserSchemaValidation
from app.web.auth import token_required
from app.web import session, bcrypt, app

## blueprint and prefix
users_pb = Blueprint("users", __name__, url_prefix= "/users")

## sign up api
@users_pb.route("/sign_up",methods=['POST'])
@users_pb.arguments(UserSchemaValidation())
def sign_up(user_input):

    email = user_input.get("email")
    password = user_input.get("password")
    
    ## search already exist user
    db_results = session.query(User).filter(User.email == email).all()

    if len(db_results) > 0:
        return jsonify({"error":"the user with same email already exist"}), 400 # bad request
    
    ## hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    ## add user
    insert_user_record = User(email = email, password = hashed_password)
    session.add(insert_user_record)
    session.commit()

    return jsonify({"success":"user is added"}), 200 # success

## sign in api
@users_pb.route("/sign_in", methods=['POST'])
@users_pb.arguments(UserSchemaValidation())
def sign_in(user_record):

    email = user_record.get("email")
    password = user_record.get("password")

    ## search already exist user
    db_result = session.query(User).filter(User.email == email).first()

    ## check password and email
    if not db_result:
        return jsonify({"success":"the email is incorrect"}), 400 # bad request
    
    if not bcrypt.check_password_hash(db_result.password, password):
        return jsonify({"success":"the password is incorrect"}), 400 # bad request
    
    ## token creation
    token = jwt.encode({
        "user_id" : str(db_result.id),
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    ## return the token to user
    return jsonify({"success": token}), 200 # success

## profile request api
@users_pb.route('/profile', methods=['GET'])
@token_required
def profile(user_id):

    db_user_record = session.query(User).filter(User.id == user_id).first()
    
    if not db_user_record:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'user_id': db_user_record.id,
                    "user_email":db_user_record.email})
