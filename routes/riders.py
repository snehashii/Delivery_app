from flask import Blueprint, request, jsonify
from models import Rider
from extensions import db

riders_bp = Blueprint('riders', __name__, url_prefix='/riders')


@riders_bp.route('/', methods=['GET'])
def get_riders():
    riders = Rider.query.all()
    result = [{
        'id': r.id,
        'name': r.name,
        'phone': r.phone,
        'status': r.status,
        'verified': r.verified,
        'locality': r.locality
    } for r in riders]
    return jsonify(result)


@riders_bp.route('/<int:id>', methods=['GET'])
def get_rider(id):
    rider = Rider.query.get(id)
    if not rider:
        return jsonify({'error': 'Rider not found'}), 404

    return jsonify({
        'id': rider.id,
        'name': rider.name,
        'phone': rider.phone,
        'status': rider.status,
        'verified': rider.verified,
        'locality': rider.locality
    })


@riders_bp.route('/', methods=['POST'])
def create_rider():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    locality = data.get('locality')

    if not all([name, phone, locality]):
        return jsonify({'error': 'Name, phone, and locality are required'}), 400

    rider = Rider(name=name, phone=phone, locality=locality)
    db.session.add(rider)
    db.session.commit()

    return jsonify({'message': 'Rider created', 'id': rider.id}), 201


@riders_bp.route('/<int:id>', methods=['PUT'])
def update_rider(id):
    rider = Rider.query.get(id)
    if not rider:
        return jsonify({'error': 'Rider not found'}), 404

    data = request.get_json()
    rider.name = data.get('name', rider.name)
    rider.phone = data.get('phone', rider.phone)
    rider.status = data.get('status', rider.status)
    rider.verified = data.get('verified', rider.verified)
    rider.locality = data.get('locality', rider.locality)

    db.session.commit()
    return jsonify({'message': 'Rider updated'})


@riders_bp.route('/<int:id>', methods=['DELETE'])
def delete_rider(id):
    rider = Rider.query.get(id)
    if not rider:
        return jsonify({'error': 'Rider not found'}), 404

    db.session.delete(rider)
    db.session.commit()
    return jsonify({'message': 'Rider deleted'}), 204
