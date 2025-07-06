from flask import Blueprint, request, jsonify
from models import Role
from extensions import db

roles_bp = Blueprint('roles', __name__, url_prefix='/roles')


@roles_bp.route('/', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{
        'id': role.id,
        'name': role.name,
        'description': role.description
    } for role in roles])


@roles_bp.route('/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    return jsonify({
        'id': role.id,
        'name': role.name,
        'description': role.description
    })


@roles_bp.route('/', methods=['POST'])
def create_role():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    new_role = Role(name=name, description=description)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({
        'message': 'Role created',
        'id': new_role.id
    }), 201


@roles_bp.route('/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404

    data = request.get_json()
    role.name = data.get('name', role.name)
    role.description = data.get('description', role.description)

    db.session.commit()
    return jsonify({'message': 'Role updated'})


@roles_bp.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404

    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted'}), 204
