from flask import Blueprint, jsonify

from app.models.ticket import Ticket

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/tickets', methods=['GET'])
def admin_tickets():

    tickets = Ticket.query.all()

    resultat = []

    for ticket in tickets:

        resultat.append({
            'numero': ticket.numero,
            'service': ticket.service.nom,
            'position': ticket.position_file,
            'temps': ticket.temps_estime
        })

    return jsonify(resultat)