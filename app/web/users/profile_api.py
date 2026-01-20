## imports
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps

from app.models.users.schema_user import User
from app.web import *

## profile request
@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user_id):

    try:
        user = session.query(User).filter(User.id == current_user_id).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'user_id': user.id,
                        "user_email":user.email})

    except SQLAlchemyError as err:
        session.rollback()
        return jsonify({'message': 'Database error', 'error': str(err)}), 500
    
    finally:
        ## close resources
        session.close()
    