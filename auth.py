from flask import request, jsonify
from functools import wraps
from extensions import db 
from models import User

def get_current_user():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return None
    return db.session.get(User, int(user_id))  # Modern SQLAlchemy usage

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user or user.role.name != required_role:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
