from flask import Blueprint, request, jsonify
from models import Permission
from extensions import db
from auth import role_required

permissions_bp = Blueprint('permissions', __name__, url_prefix='/permissions')

@permissions_bp.route('/', methods=['GET'])
def get_permissions():
    permissions = Permission.query.all()
    return jsonify([
        {'id': p.id, 'page_name': p.page_name, 'access_level': p.access_level}
        for p in permissions
    ])

@permissions_bp.route('/', methods=['POST'])
@role_required('Admin')
def create_permission():
    data = request.get_json()
    page_name = data.get('page_name')
    access_level = data.get('access_level')

    if not all([page_name, access_level]):
        return jsonify({'error': 'Missing page_name or access_level'}), 400

    new_permission = Permission(page_name=page_name, access_level=access_level)
    db.session.add(new_permission)
    db.session.commit()

    return jsonify({
        'message': 'Permission created',
        'permission_id': new_permission.id
    }), 201

# Update a permission
@permissions_bp.route('/<int:id>', methods=['PUT'])
@role_required('Admin')
def update_permission(id):
    permission = Permission.query.get(id)
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404

    data = request.get_json()
    permission.page_name = data.get('page_name', permission.page_name)
    permission.access_level = data.get('access_level', permission.access_level)

    db.session.commit()
    return jsonify({'message': 'Permission updated'})


# Delete a permission
@permissions_bp.route('/<int:id>', methods=['DELETE'])
@role_required('Admin')
def delete_permission(id):
    permission = Permission.query.get(id)
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404

    db.session.delete(permission)
    db.session.commit()
    return jsonify({'message': 'Permission deleted'}), 204
