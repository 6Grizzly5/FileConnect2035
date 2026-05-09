from flask import Blueprint, jsonify

from app.models.service import Service

service_bp = Blueprint('service_bp', __name__)

@service_bp.route('/services', methods=['GET'])
def get_services():

    services = Service.query.all()

    resultat = []

    for service in services:

        resultat.append({
            'id': service.id_service,
            'nom': service.nom,
            'duree_moyenne': service.duree_moyenne
        })

    return jsonify(resultat)

from flask import request

from app import db

@service_bp.route('/service', methods=['POST'])
def creer_service():

    data = request.get_json()

    service = Service(
        nom=data['nom'],
        duree_moyenne=data['duree'],
        id_agence=data['id_agence']
    )

    db.session.add(service)
    db.session.commit()

    return jsonify({
        'message': 'Service ajouté'
    }), 201