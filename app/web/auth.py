from functools import wraps
from flask import request, jsonify
import jwt
from app.web import *

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
            data = jwt.decode(token, c.secret_key, algorithms=["HS256"])
            current_user_id = data['user_id']

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

        ## return to requested process
        return f(current_user_id, *args, **kwargs)
    return decorated
