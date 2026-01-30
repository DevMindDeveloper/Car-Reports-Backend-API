## imports
from functools import wraps
from flask import request, jsonify
import jwt

from app.web import app

## Decorator to protect routes
def token_required(f):
    @wraps(f) # copies metadata from "f"
    def decorated(*args, **kwargs):
        TOKEN = None

        ## check token
        if 'x-access-token' in request.headers:
            TOKEN = request.headers['x-access-token']
        if not TOKEN:
            return jsonify({'message': 'Token is missing!'}), 401

        ## decode and check the expiration of token
        try:
            data = jwt.decode(TOKEN, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

        ## return to requested process
        return f(current_user_id, *args, **kwargs)
    return decorated
