## imports
import datetime
from flask import request, jsonify
from flask_smorest import Blueprint
import jwt

from app.models.users.schema_user import User
from app.tasks.schema_validation import  UserSchemaValidation
from app.web import app, session, bcrypt

## blueprint and prefix
sign_in_bp = Blueprint("sign_in", __name__, url_prefix="/users")

## sign in api
@sign_in_bp.route("/sign_in", methods=['POST'])
@sign_in_bp.arguments(UserSchemaValidation())
def sign_in(user_record):

    email = user_record.get("email")
    password = user_record.get("password")

    ## search already exist user
    db_result = session.query(User).filter(User.email == email).first()

    ## check password and email
    if not db_result or not bcrypt.check_password_hash(db_result.password, password):
        return jsonify({"success":"the email or password is incorrect"}), 400 # bad request
    
    ## token creation
    token = jwt.encode({
        "user_id" : str(db_result.id),
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    ## return the token to user
    return jsonify({"success": token}), 200 # success