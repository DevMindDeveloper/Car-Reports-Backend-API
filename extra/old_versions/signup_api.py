## imports
from flask import request, jsonify
from flask_smorest import Blueprint

from app.models.users.schema_user import User
from app.tasks.schema_validation import UserSchemaValidation
from app.web import session, bcrypt

## blueprint and prefix
sign_up_bp = Blueprint("sign_up", __name__, url_prefix= "/users")

## sign up api
@sign_up_bp.route("/sign_up",methods=['POST'])
@sign_up_bp.arguments(UserSchemaValidation())
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
