from flask import Blueprint
from flask import request
from flask import jsonify
from flask import render_template

from app import db

from app.models.ticket import Ticket
from app.models.service import Service
from app.services.calcul_file import (
    calculer_position,
    calculer_temps_estime,
    reordonner_file
)

ticket_bp = Blueprint(
    'ticket_bp',
    __name__
)

# =========================
# CREATE TICKET
# =========================

@ticket_bp.route(
    '/create_ticket',
    methods=['POST']
)
def create_ticket():

    data = request.json

    service = Service.query.get(data['service_id'])

    if not service:
        return jsonify({'error': 'Service introuvable'}), 404

    # Numéro séquentiel global
    total = Ticket.query.count()
    numero = f"T-{total + 1}"

    # Position et temps selon SPT AVANT insertion
    position = calculer_position(service.id)
    temps = calculer_temps_estime(service.id)

    ticket = Ticket(
        numero=numero,
        client=data.get('client', 'Anonyme'),
        position=position,
        temps_estime=temps,
        service_id=service.id,
        statut="En attente"
    )

    db.session.add(ticket)
    db.session.flush()   # obtenir l'id avant reordonner

    # Réordonner toute la file avec le nouveau ticket inclus
    reordonner_file()

    db.session.commit()

    return jsonify({
        'numero': ticket.numero,
        'client': ticket.client,
        'position': ticket.position,
        'temps_estime': ticket.temps_estime,
        'service': service.nom
    })


# =========================
# NEXT TICKET
# =========================

@ticket_bp.route(
    '/next_ticket',
    methods=['POST']
)
def next_ticket():

    # Terminer le ticket en cours
    current = Ticket.query.filter_by(
        statut="En cours"
    ).first()

    if current:
        current.statut = "Terminé"
        current.position = 0

    # Appeler le prochain (ordre SPT = position 1)
    prochain = (
        Ticket.query
        .filter_by(statut="En attente")
        .order_by(Ticket.position.asc())
        .first()
    )

    if prochain:
        prochain.statut = "En cours"
        prochain.position = 0

    # Réordonner le reste de la file
    reordonner_file()

    db.session.commit()

    return jsonify({'message': 'Ticket suivant appelé'})


# =========================
# ADMIN TICKETS
# =========================

@ticket_bp.route('/admin/tickets')
def admin_tickets():

    tickets = (
        Ticket.query
        .order_by(Ticket.position.asc(), Ticket.id.asc())
        .all()
    )

    result = []

    for ticket in tickets:

        service = Service.query.get(ticket.service_id)
        service_nom = service.nom if service else "—"
        duree = service.duree_moyenne if service else 0

        result.append({
            'id': ticket.id,
            'numero': ticket.numero,
            'client': ticket.client or 'Anonyme',
            'service': service_nom,
            'duree_service': duree,
            'position': ticket.position or 0,
            'temps_estime': ticket.temps_estime or 0,
            'statut': ticket.statut or 'En attente',
            'heure_creation': (
                ticket.heure_creation.strftime('%H:%M')
                if ticket.heure_creation else '—'
            )
        })

    return jsonify(result)


# =========================
# TICKET PAGE (mobile)
# =========================

@ticket_bp.route('/ticket_page')
def ticket_page():

    return render_template(
        'ticket.html',
        numero=request.args.get('numero'),
        position=request.args.get('position'),
        temps=request.args.get('temps')
    )


# =========================
# TICKET STATUS (mobile)
# =========================

@ticket_bp.route('/ticket_status/<numero>')
def ticket_status(numero):

    ticket = Ticket.query.filter_by(numero=numero).first()

    if not ticket:
        return jsonify({'error': 'Ticket introuvable'})

    service = Service.query.get(ticket.service_id)
    duree = service.duree_moyenne if service else 0

    temps_restant = (ticket.temps_estime or 0)

    return jsonify({
        'numero': ticket.numero,
        'client': ticket.client or 'Anonyme',
        'position': ticket.position or 0,
        'statut': ticket.statut,
        'temps_restant': f"{temps_restant} min",
        'service': service.nom if service else '—'
    })
