from flask import Blueprint, request, jsonify
from models import Delivery, Rider
from extensions import db
from auth import role_required

deliveries_bp = Blueprint('deliveries', __name__, url_prefix='/deliveries')


@deliveries_bp.route('/', methods=['GET'])
def get_deliveries():
    deliveries = Delivery.query.all()
    result = []
    for d in deliveries:
        rider = Rider.query.get(d.rider_id)
        result.append({
            'id': d.id,
            'order_id': d.order_id,
            'rider_id': d.rider_id,
            'rider_name': rider.name if rider else None,
            'status': d.status,
            'tracking_id': d.tracking_id,
            'created_at': d.created_at
        })
    return jsonify(result)


@deliveries_bp.route('/<int:id>', methods=['GET'])
def get_delivery(id):
    delivery = Delivery.query.get(id)
    if not delivery:
        return jsonify({'error': 'Delivery not found'}), 404

    rider = Rider.query.get(delivery.rider_id)
    return jsonify({
        'id': delivery.id,
        'order_id': delivery.order_id,
        'rider_id': delivery.rider_id,
        'rider_name': rider.name if rider else None,
        'status': delivery.status,
        'tracking_id': delivery.tracking_id,
        'created_at': delivery.created_at
    })


@deliveries_bp.route('/', methods=['POST'])
@role_required('Admin')
def create_delivery():
    data = request.get_json()
    order_id = data.get('order_id')
    rider_id = data.get('rider_id')
    status = data.get('status')
    tracking_id = data.get('tracking_id')

    if not all([order_id, status, tracking_id]):
        return jsonify({'error': 'order_id, status, and tracking_id are required'}), 400

    if rider_id:
        rider = Rider.query.get(rider_id)
        if not rider:
            return jsonify({'error': 'Invalid rider_id'}), 404

    delivery = Delivery(
        order_id=order_id,
        rider_id=rider_id,
        status=status,
        tracking_id=tracking_id
    )
    db.session.add(delivery)
    db.session.commit()

    return jsonify({'message': 'Delivery created', 'id': delivery.id}), 201


@deliveries_bp.route('/<int:id>', methods=['PUT'])
@role_required('Admin')
def update_delivery(id):
    delivery = Delivery.query.get(id)
    if not delivery:
        return jsonify({'error': 'Delivery not found'}), 404

    data = request.get_json()
    delivery.order_id = data.get('order_id', delivery.order_id)
    delivery.rider_id = data.get('rider_id', delivery.rider_id)
    delivery.status = data.get('status', delivery.status)
    delivery.tracking_id = data.get('tracking_id', delivery.tracking_id)

    db.session.commit()
    return jsonify({'message': 'Delivery updated'})


@deliveries_bp.route('/<int:id>', methods=['DELETE'])
@role_required('Admin')
def delete_delivery(id):
    delivery = Delivery.query.get(id)
    if not delivery:
        return jsonify({'error': 'Delivery not found'}), 404

    db.session.delete(delivery)
    db.session.commit()
    return jsonify({'message': 'Delivery deleted'}), 204
