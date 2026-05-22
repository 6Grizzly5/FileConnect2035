from flask import Blueprint, jsonify

from app.models.ticket import Ticket
from app.models.service import Service

admin_bp = Blueprint('admin_bp', __name__)


# =========================
# DASHBOARD STATS
# =========================

@admin_bp.route('/dashboard_stats')
def dashboard_stats():

    total = Ticket.query.count()

    active = Ticket.query.filter_by(statut='En attente').count()

    en_cours = Ticket.query.filter_by(statut='En cours').count()

    finished = Ticket.query.filter_by(statut='Terminé').count()

    # Temps moyen réel depuis les services
    services = Service.query.all()

    if services:
        durees = [
            s.duree_moyenne for s in services
            if s.duree_moyenne
        ]
        moyenne = round(sum(durees) / len(durees)) if durees else 0
    else:
        moyenne = 0

    return jsonify({
        'clients_today': total,
        'active_tickets': active,
        'en_cours': en_cours,
        'finished_tickets': finished,
        'average_time': moyenne
    })
    
@admin_bp.route('/guichet_stats')
def guichet_stats():

    from app.models.guichet import Guichet
    from app.models.ticket import Ticket

    result = []

    guichets = Guichet.query.all()

    for g in guichets:

        total = (
            Ticket.query
            .filter_by(
                id_guichet=g.id,
                statut='Terminé'
            )
            .count()
        )

        result.append({

            'guichet': f'Guichet {g.numero}',

            'tickets': total

        })

    return jsonify(result)
