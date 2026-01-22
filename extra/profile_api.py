## imports
from flask import jsonify
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app.models.users.schema_user import User
from app.web.auth import token_required
from app.web import session

## blueprint and prefix
profile_bp = Blueprint("profile", __name__, url_prefix = "/users")

## profile request api
@profile_bp.route('/profile', methods=['GET'])
@token_required
def profile(user_id):

    db_user_record = session.query(User).filter(User.id == user_id).first()
    
    if not db_user_record:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'user_id': db_user_record.id,
                    "user_email":db_user_record.email})
