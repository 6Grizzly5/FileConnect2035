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
