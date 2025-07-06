from flask import Blueprint, request, jsonify
from models import User
from extensions import db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role_id': user.role_id
        } for user in users
    ])

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    if not all([name, email, password, role_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_user = User(name=name, email=email, password=password, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user_id': new_user.id
    }), 201

# Update a user
@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.role_id = data.get('role_id', user.role_id)

    db.session.commit()
    return jsonify({'message': 'User updated'})


# Delete a user
@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 204
