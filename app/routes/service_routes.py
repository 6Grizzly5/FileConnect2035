from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models.service import Service
from app.models.ticket import Ticket
from app.models.agence import Agence

service_bp = Blueprint('service_bp', __name__)


# ─────────────────────────────
# CREATE SERVICE
# ─────────────────────────────

@service_bp.route('/create_service', methods=['POST'])
def create_service():
    data = request.json

    if not data:
        return jsonify({'error': 'Pas de données JSON'}), 400

    nom      = data.get('nom', '').strip()
    duree    = data.get('duree')
    agence_id = data.get('id_agence')

    # Validations
    if not nom:
        return jsonify({'error': 'Le nom est obligatoire'}), 400

    if duree is None:
        return jsonify({'error': 'La durée est obligatoire'}), 400

    try:
        duree = int(duree)
    except (ValueError, TypeError):
        return jsonify({'error': 'La durée doit être un entier'}), 400

    if not agence_id:
        return jsonify({'error': 'id_agence manquant'}), 400

    agence = Agence.query.get(agence_id)
    if not agence:
        return jsonify({'error': f'Agence {agence_id} introuvable'}), 404

    service = Service(
        nom=nom,
        duree_moyenne=duree,
        agence_id=agence_id
    )

    db.session.add(service)
    db.session.commit()

    return jsonify({
        'message': 'Service créé',
        'id': service.id,
        'nom': service.nom
    }), 201


# ─────────────────────────────
# GET ALL SERVICES
# ─────────────────────────────

@service_bp.route('/services')
def get_all_services():
    services = Service.query.all()

    result = []
    for s in services:
        ticket_count = Ticket.query.filter_by(service_id=s.id).count()
        result.append({
            'id':         s.id,
            'nom':        s.nom,
            'duree':      s.duree_moyenne or 0,
            'agence_id':  s.agence_id,
            'tickets':    ticket_count
        })

    return jsonify(result)


# ─────────────────────────────
# GET SERVICES PAR AGENCE
# ─────────────────────────────

@service_bp.route('/agence/<int:id>')
def get_services_agence(id):
    services = Service.query.filter_by(agence_id=id).all()

    result = [{'id': s.id, 'nom': s.nom} for s in services]
    return jsonify(result)


# ─────────────────────────────
# DELETE SERVICE
# ─────────────────────────────

@service_bp.route('/service/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)

    if not service:
        return jsonify({'error': 'Service introuvable'}), 404

    db.session.delete(service)
    db.session.commit()

    return jsonify({'message': 'Service supprimé'})


# ─────────────────────────────
# PAGE MOBILE
# ─────────────────────────────

@service_bp.route('/mobile/<int:id>')
def mobile_page(id):
    services = Service.query.filter_by(agence_id=id).all()
    return render_template('mobile.html', services=services, agence_id=id)
