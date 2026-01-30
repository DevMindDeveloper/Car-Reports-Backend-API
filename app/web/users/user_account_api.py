## imports
import datetime
from flask import request, jsonify
from flask_smorest import Blueprint
import jwt

from app.models.users.schema_user import User
from app.web.users.schema_validation import UserSchemaValidation
from app.web.auth import token_required
from app.web.users import session, app, bcrypt

## blueprint and prefix
users_pb = Blueprint("users", __name__, url_prefix= "/users")

## sign up api
@users_pb.route("/sign_up",methods=['POST'])
@users_pb.arguments(UserSchemaValidation)
def sign_up(user_input):

    EMAIL = user_input.get("email")
    PASSWORD = user_input.get("password")
    
    ## search already exist user
    db_result = session.query(User).filter(User.email == EMAIL).first()

    if db_result:
        return jsonify({"error":"the user with same email already exist"}), 400 # bad request
    
    ## add user
    insert_user_record = User(email = EMAIL, password = PASSWORD)
    session.add(insert_user_record)
    session.commit()

    return jsonify({"success":"user is added"}), 200 # success

## sign in api
@users_pb.route("/sign_in", methods=['POST'])
@users_pb.arguments(UserSchemaValidation)
def sign_in(user_record):

    EMAIL = user_record.get("email")
    PASSWORD = user_record.get("password")

    ## search already exist user
    db_result = session.query(User).filter(User.email == EMAIL).first()

    ## check password and email
    if not db_result:
        return jsonify({"success":"the email is incorrect"}), 400 # bad request
    
    elif not bcrypt.check_password_hash(db_result.password, PASSWORD):
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
