from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import User

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))

def user_exists(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "user not found"}), 404
        return f(*args, **kwargs)
    return decorated
