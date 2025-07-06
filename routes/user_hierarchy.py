from flask import Blueprint, request, jsonify
from models import UserHierarchy, User
from extensions import db
from auth import role_required

user_hierarchy_bp = Blueprint('user_hierarchy', __name__, url_prefix='/user-hierarchy')

@user_hierarchy_bp.route('/', methods=['GET'])
def get_user_hierarchy():
    hierarchy = UserHierarchy.query.all()
    result = []
    for uh in hierarchy:
        manager = User.query.get(uh.manager_id)
        subordinate = User.query.get(uh.subordinate_id)
        result.append({
            'id': uh.id,
            'manager_id': uh.manager_id,
            'manager_name': manager.name if manager else None,
            'subordinate_id': uh.subordinate_id,
            'subordinate_name': subordinate.name if subordinate else None
        })
    return jsonify(result)

@user_hierarchy_bp.route('/', methods=['POST'])
@role_required('Admin')
def add_user_hierarchy():
    data = request.get_json()
    manager_id = data.get('manager_id')
    subordinate_id = data.get('subordinate_id')

    if not all([manager_id, subordinate_id]):
        return jsonify({'error': 'Both manager_id and subordinate_id are required'}), 400

    manager = User.query.get(manager_id)
    subordinate = User.query.get(subordinate_id)

    if not manager or not subordinate:
        return jsonify({'error': 'Invalid manager_id or subordinate_id'}), 404

    new_hierarchy = UserHierarchy(manager_id=manager_id, subordinate_id=subordinate_id)
    db.session.add(new_hierarchy)
    db.session.commit()

    return jsonify({'message': 'User hierarchy created', 'id': new_hierarchy.id}), 201

@user_hierarchy_bp.route('/<int:id>', methods=['PUT'])
@role_required('Admin')
def update_user_hierarchy(id):
    hierarchy = UserHierarchy.query.get(id)
    if not hierarchy:
        return jsonify({'error': 'UserHierarchy not found'}), 404

    data = request.get_json()
    manager_id = data.get('manager_id', hierarchy.manager_id)
    subordinate_id = data.get('subordinate_id', hierarchy.subordinate_id)

    manager = User.query.get(manager_id)
    subordinate = User.query.get(subordinate_id)
    if not manager or not subordinate:
        return jsonify({'error': 'Invalid manager_id or subordinate_id'}), 404

    hierarchy.manager_id = manager_id
    hierarchy.subordinate_id = subordinate_id
    db.session.commit()

    return jsonify({'message': 'UserHierarchy updated'})

@user_hierarchy_bp.route('/<int:id>', methods=['DELETE'])
@role_required('Admin')
def delete_user_hierarchy(id):
    hierarchy = UserHierarchy.query.get(id)
    if not hierarchy:
        return jsonify({'error': 'UserHierarchy not found'}), 404

    db.session.delete(hierarchy)
    db.session.commit()

    return jsonify({'message': 'UserHierarchy deleted'}), 204
