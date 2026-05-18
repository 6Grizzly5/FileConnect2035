from flask import Blueprint
from flask import render_template

from app.models.ticket import Ticket

display_bp = Blueprint(
    'display_bp',
    __name__
)

# =========================
# DISPLAY SCREEN
# =========================

@display_bp.route(
    '/display'
)
def display():

    current = Ticket.query.filter_by(
        statut="En cours"
    ).first()

    waiting = Ticket.query.filter_by(
        statut="En attente"
    ).order_by(
        Ticket.position.asc()
    ).limit(5).all()

    return render_template(

        'display.html',

        current=current,

        waiting=waiting
    )