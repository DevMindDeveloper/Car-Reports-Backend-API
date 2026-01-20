## imports
from flask import request, Flask, jsonify
from  flask_bcrypt import Bcrypt
import mysql.connector as mc
import datetime
import jwt

from app import config as c

## db configs
db_configs = {
    'host' : c.host,
    'user' : c.user,
    'password' : c.password,
    'database' : c.database
}

## initialization
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'yourpassword' 

## sign in
@app.route("/check_user", methods=['POST'])
def check_user():
    res = request.get_json()
    email = res.get("email")
    password = res.get("password")
    
    ## db initialization
    conn = mc.connect(**db_configs)
    cursor = conn.cursor(buffered=True)

    ## check both fields are avaliable
    if not email or not password:
        return jsonify({"error":"email or password is not given"}), 400 # bad request
    
    try:
        ## search already exist user
        search_sql_query = "select * from users_cred where email = %s"
        cursor.execute(search_sql_query, (email,))
        result = cursor.fetchone()

        ## check password and email
        if not result or not bcrypt.check_password_hash(result[2], password):
            return jsonify({"success":"the email or password is incorrect"}), 400 # bad request
        
        ## token creation
        token = jwt.encode({
            "user_id" : str(result[0]),
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config["SECRET_KEY"], algorithm="HS256")


        ## return the token to user
        return jsonify({"success": token}), 200 # success

    except mc.Error as er:
        return jsonify({"error": f"{er}"}), 501 # internal server error
    
    finally:
        ## close resources.
        cursor.close()
        conn.close()
    
if __name__ == "__main__":
    app.run(host = "127.0.0.1", port=1278)

