from flask import Blueprint, request, jsonify
from models import ThirdPartyService
from extensions import db

third_party_bp = Blueprint('third_party_service', __name__, url_prefix='/third-party')


@third_party_bp.route('/', methods=['GET'])
def get_services():
    services = ThirdPartyService.query.all()
    result = [
        {
            "id": s.id,
            "name": s.name,
            "contact_info": s.contact_info,
            "areas_covered": s.areas_covered
        } for s in services
    ]
    return jsonify(result)


@third_party_bp.route('/<int:id>', methods=['GET'])
def get_service(id):
    service = ThirdPartyService.query.get(id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    return jsonify({
        "id": service.id,
        "name": service.name,
        "contact_info": service.contact_info,
        "areas_covered": service.areas_covered
    })


@third_party_bp.route('/', methods=['POST'])
def add_service():
    data = request.get_json()
    name = data.get('name')
    contact_info = data.get('contact_info')
    areas_covered = data.get('areas_covered')

    if not all([name, contact_info, areas_covered]):
        return jsonify({'error': 'All fields are required'}), 400

    new_service = ThirdPartyService(name=name, contact_info=contact_info, areas_covered=areas_covered)
    db.session.add(new_service)
    db.session.commit()

    return jsonify({'message': 'Third-party service added', 'id': new_service.id}), 201


@third_party_bp.route('/<int:id>', methods=['PUT'])
def update_service(id):
    service = ThirdPartyService.query.get(id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    data = request.get_json()
    service.name = data.get('name', service.name)
    service.contact_info = data.get('contact_info', service.contact_info)
    service.areas_covered = data.get('areas_covered', service.areas_covered)

    db.session.commit()
    return jsonify({'message': 'Service updated'})


@third_party_bp.route('/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = ThirdPartyService.query.get(id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted'}), 204
