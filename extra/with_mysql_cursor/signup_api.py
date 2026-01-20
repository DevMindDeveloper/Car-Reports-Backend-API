## imports
from flask import request, Flask, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector as mc
from marshmallow import ValidationError

from app import config as c
from app.tasks.schema_validation import userSchemaValidation

## db creds
db_configs = {
    'host' : c.host,
    'user' : c.user,
    'password' : c.password,
    'database' : c.database
}

## initialization
app = Flask(__name__)
bcrypt = Bcrypt(app)

schema = userSchemaValidation()

## sign up
@app.route("/add_user",methods=['POST'])
def add_user():
    res = request.get_json()
    email = res.get("email")
    password = res.get("password")

    ## db initialization
    conn = mc.connect(**db_configs)
    cursor = conn.cursor()

    ## check both fields are avaliable
    if not email or not password:
        return jsonify({"error":"email or password is not given"}), 400 # bad request
    
##-------------------------------------------------------------------------------------------------------
    # ## check the length of the password
    # if len(password)<8:
    #     return jsonify({"error":"the length of password should greater than 8"}), 400 # bad request
##-------------------------------------------------------------------------------------------------------
    
    try:

        ## schema validation 
        user = schema.load({
            'email' : email,
            'password' : password
        })
    
        ## search already exist user
        search_sql_query = "select * from users_cred where email = %s"
        cursor.execute(search_sql_query, (email,))
        results = cursor.fetchall()

        if len(results) > 0:
            return jsonify({"error":"the user with same email already exist"}), 400 # bad request
        
        user_input = schema.dump(user)

        ## hash the password
        hashed_password = bcrypt.generate_password_hash(user_input['password']).decode("utf-8")

        ## add user
        insert_sql_query = "insert into users_cred (email, password) values (%s, %s)"
        cursor.execute(insert_sql_query, (user_input['email'], hashed_password))
        conn.commit()

        return jsonify({"success":"user is added"}), 200 # success

    except mc.Error as er:
        return jsonify({"error": er}), 501 # internal server error
    
    except ValidationError as er:
        return jsonify({"error": er}), 400 # bad request
    
    finally:
        ## close resources.
        cursor.close()
        conn.close()
    
if __name__ == "__main__":
    app.run(host = "127.0.0.1", port=2243)
