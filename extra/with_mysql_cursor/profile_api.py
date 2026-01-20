## imports
from flask import request, Flask, jsonify
import mysql.connector as mc
from functools import wraps
import jwt

from app import config as c

## db creds
db_configs = {
    'host' : c.host,
    'user' : c.user,
    'password' : c.password,
    'database' : c.database
}

## initialization
app = Flask(__name__)

app.config['SECRET_KEY'] = c.secret_key

## Decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        ## check token
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        ## decode and check the expiration of token
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

        ## return to requested process
        return f(current_user_id, *args, **kwargs)
    return decorated

## profile request
@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user_id):

    ## db initialization
    conn = mc.connect(**db_configs)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users_cred WHERE id=%s", (current_user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'user': user})

    except mc.Error as err:
        return jsonify({'message': 'Database error', 'error': str(err)}), 500
    
    finally:
        ## close resources
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=1112)