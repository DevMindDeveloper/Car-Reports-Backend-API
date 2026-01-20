## imports
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import datetime
import jwt

from app.models.users.schema_user import User
from app.web import *

## sign in
@app.route("/check_user", methods=['POST'])
def check_user():
    res = request.get_json()
    
    ## check both fields are avaliable using schema validation
    user = schema_user.load({
        'email' : res.get("email"),
        "password" : res.get("password"),
    })
    
    user_record = schema_user.dump(user)
    
    try:
        ## search already exist user
        result = session.query(User).filter(User.email == user_record['email']).first()

        ## check password and email
        if not result or not bcrypt.check_password_hash(result.password, user_record['password']):
            return jsonify({"success":"the email or password is incorrect"}), 400 # bad request
        
        ## token creation
        token = jwt.encode({
            "user_id" : str(result.id),
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config["SECRET_KEY"], algorithm="HS256")

        ## return the token to user
        return jsonify({"success": token}), 200 # success

    except SQLAlchemyError as er:
        session.rollback()
        return jsonify({"error": f"{er}"}), 501 # internal server error
    
    finally:
        ## close resources.
        session.close()
    