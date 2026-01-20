## imports
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app.tasks.schema_validation import UserSchemaValidation
from app.models.users.schema_user import User
from app.web import *

schema = UserSchemaValidation()

## sign up
@app.route("/add_user",methods=['POST'])
def add_user():
    res = request.get_json()
    
    try:

        ## schema validation 
        user = schema_user.load({
            'email' : res.get("email"),
            "password" : res.get("password"),
        })
        user_input = schema.dump(user)
    
        ## search already exist user
        results = session.query(User).filter(User.email == user_input['email']).all()

        if len(results) > 0:
            return jsonify({"error":"the user with same email already exist"}), 400 # bad request
        
        ## hash the password
        hashed_password = bcrypt.generate_password_hash(user_input['password']).decode("utf-8")

        ## add user
        insert_user_record = User(email = user_input['email'], password = hashed_password)
        session.add(insert_user_record)
        session.commit()

        return jsonify({"success":"user is added"}), 200 # success

    except SQLAlchemyError as er:
        session.rollback()
        return jsonify({"error": er}), 501 # internal server error
    
    except ValidationError as er:
        return jsonify({"error": er}), 400 # bad request
    
    finally:
        ## close resources.
        session.close()
    