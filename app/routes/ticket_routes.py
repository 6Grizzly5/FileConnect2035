from flask import Blueprint, request, jsonify

from app import db

from app.models.ticket import Ticket
from app.models.service import Service

from app.services.calcul_file import (
    calculer_position,
    calculer_temps_estime
)

ticket_bp = Blueprint('ticket_bp', __name__)

@ticket_bp.route('/ticket', methods=['POST'])
def creer_ticket():

    data = request.get_json()

    id_service = data.get('id_service')

    service = Service.query.get(id_service)

    if not service:
        return jsonify({
            'message': 'Service introuvable'
        }), 404

    position = calculer_position(id_service)

    temps = calculer_temps_estime(id_service)

    numero = f"S{id_service}-{position}"

    ticket = Ticket(
        numero=numero,
        position_file=position,
        temps_estime=temps,
        statut='EN_ATTENTE',
        id_service=id_service
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        'id_ticket': ticket.id_ticket
    }), 201
    
from flask import render_template

@ticket_bp.route('/ticket/<int:id_ticket>', methods=['GET'])
def afficher_ticket(id_ticket):

    ticket = Ticket.query.get(id_ticket)

    if not ticket:
        return "Ticket introuvable", 404

    return render_template(
        'ticket.html',
        ticket=ticket
    )   