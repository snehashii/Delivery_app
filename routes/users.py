from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from auth import role_required
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__, url_prefix='/users')

# ✅ Get all users
@users_bp.route('/', methods=['GET'])
@role_required('Admin')  # Optional
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role_id': user.role_id,
            'role_name': user.role.name if user.role else None
        } for user in users
    ])

# ✅ Get single user by ID (used during login!)
@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role_id': user.role_id,
        'role_name': user.role.name if user.role else None
    })

# ✅ Create user (Admin only)
@users_bp.route('/', methods=['POST'])
@role_required('Admin')
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    if not all([name, email, password, role_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    # ❗ Check for duplicate email
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already in use'}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password=hashed_password, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user_id': new_user.id
    }), 201

# ✅ Update user
@users_bp.route('/<int:id>', methods=['PUT'])
@role_required('Admin')
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    password = data.get('password')
    if password:
        user.password = generate_password_hash(password)
    user.role_id = data.get('role_id', user.role_id)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# ✅ Delete user (Admin only)
@users_bp.route('/<int:id>', methods=['DELETE'])
@role_required('Admin')
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 204
