from flask import Blueprint, request, jsonify
from models import RolePermission, Role, Permission
from extensions import db

role_permissions_bp = Blueprint('role_permissions', __name__, url_prefix='/role-permissions')

@role_permissions_bp.route('/', methods=['GET'])
def get_role_permissions():
    role_permissions = RolePermission.query.all()
    return jsonify([
        {
            'id': rp.id,
            'role_id': rp.role_id,
            'role': rp.role.name if rp.role else None,
            'permission_id': rp.permission_id,
            'permission': rp.permission.page_name if rp.permission else None
        }
        for rp in role_permissions
    ])

@role_permissions_bp.route('/', methods=['POST'])
def assign_permission_to_role():
    data = request.get_json()
    role_id = data.get('role_id')
    permission_id = data.get('permission_id')

    if not all([role_id, permission_id]):
        return jsonify({'error': 'Missing role_id or permission_id'}), 400

    new_assignment = RolePermission(role_id=role_id, permission_id=permission_id)
    db.session.add(new_assignment)
    db.session.commit()

    return jsonify({
        'message': 'Permission assigned to role',
        'assignment_id': new_assignment.id
    }), 201

@role_permissions_bp.route('/<int:id>', methods=['PUT'])
def update_role_permission(id):
    rp = RolePermission.query.get(id)
    if not rp:
        return jsonify({'error': 'RolePermission not found'}), 404

    data = request.get_json()
    rp.role_id = data.get('role_id', rp.role_id)
    rp.permission_id = data.get('permission_id', rp.permission_id)

    db.session.commit()
    return jsonify({'message': 'RolePermission updated'})


@role_permissions_bp.route('/<int:id>', methods=['DELETE'])
def delete_role_permission(id):
    rp = RolePermission.query.get(id)
    if not rp:
        return jsonify({'error': 'RolePermission not found'}), 404

    db.session.delete(rp)
    db.session.commit()
    return jsonify({'message': 'RolePermission deleted'}), 204
