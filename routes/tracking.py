from flask import Blueprint, request, jsonify
from models import Tracking, Delivery
from extensions import db
from auth import role_required

tracking_bp = Blueprint('tracking', __name__, url_prefix='/tracking')

@tracking_bp.route('/', methods=['GET'])
def get_tracking():
    tracking_entries = Tracking.query.all()
    result = []
    for entry in tracking_entries:
        delivery = Delivery.query.get(entry.delivery_id)
        result.append({
            'id': entry.id,
            'delivery_id': entry.delivery_id,
            'order_id': delivery.order_id if delivery else None,
            'current_location': entry.current_location,
            'timestamp': entry.timestamp,
            'status_update': entry.status_update
        })
    return jsonify(result)

@tracking_bp.route('/<int:id>', methods=['GET'])
def get_tracking_entry(id):
    entry = Tracking.query.get(id)
    if not entry:
        return jsonify({'error': 'Tracking entry not found'}), 404

    delivery = Delivery.query.get(entry.delivery_id)
    return jsonify({
        'id': entry.id,
        'delivery_id': entry.delivery_id,
        'order_id': delivery.order_id if delivery else None,
        'current_location': entry.current_location,
        'timestamp': entry.timestamp,
        'status_update': entry.status_update
    })

@tracking_bp.route('/', methods=['POST'])
@role_required('Admin')
def add_tracking():
    data = request.get_json()
    delivery_id = data.get('delivery_id')
    current_location = data.get('current_location')
    status_update = data.get('status_update')

    if not all([delivery_id, current_location, status_update]):
        return jsonify({'error': 'All fields are required'}), 400

    delivery = Delivery.query.get(delivery_id)
    if not delivery:
        return jsonify({'error': 'Invalid delivery_id'}), 404

    new_tracking = Tracking(
        delivery_id=delivery_id,
        current_location=current_location,
        status_update=status_update
    )
    db.session.add(new_tracking)
    db.session.commit()

    return jsonify({'message': 'Tracking entry added', 'id': new_tracking.id}), 201

@tracking_bp.route('/<int:id>', methods=['PUT'])
@role_required('Admin')
def update_tracking(id):
    entry = Tracking.query.get(id)
    if not entry:
        return jsonify({'error': 'Tracking entry not found'}), 404

    data = request.get_json()
    entry.current_location = data.get('current_location', entry.current_location)
    entry.status_update = data.get('status_update', entry.status_update)

    db.session.commit()
    return jsonify({'message': 'Tracking entry updated'})

@tracking_bp.route('/<int:id>', methods=['DELETE'])
@role_required('Admin')
def delete_tracking(id):
    entry = Tracking.query.get(id)
    if not entry:
        return jsonify({'error': 'Tracking entry not found'}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Tracking entry deleted'}), 204
