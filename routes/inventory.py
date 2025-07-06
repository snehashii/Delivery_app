from flask import Blueprint, request, jsonify
from models import Inventory
from extensions import db

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')


@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    items = Inventory.query.all()
    result = [{
        'id': item.id,
        'item_name': item.item_name,
        'quantity_available': item.quantity_available,
        'location': item.location
    } for item in items]
    return jsonify(result)


@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    item = Inventory.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    return jsonify({
        'id': item.id,
        'item_name': item.item_name,
        'quantity_available': item.quantity_available,
        'location': item.location
    })


@inventory_bp.route('/', methods=['POST'])
def add_inventory():
    data = request.get_json()
    item_name = data.get('item_name')
    quantity_available = data.get('quantity_available')
    location = data.get('location')

    if not all([item_name, quantity_available, location]):
        return jsonify({'error': 'All fields are required'}), 400

    new_item = Inventory(
        item_name=item_name,
        quantity_available=quantity_available,
        location=location
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Inventory item added', 'id': new_item.id}), 201


@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory_item(id):
    item = Inventory.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    data = request.get_json()
    item.item_name = data.get('item_name', item.item_name)
    item.quantity_available = data.get('quantity_available', item.quantity_available)
    item.location = data.get('location', item.location)

    db.session.commit()
    return jsonify({'message': 'Inventory item updated'})


@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory_item(id):
    item = Inventory.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Inventory item deleted'}), 204
