from flask import Blueprint
from flask import render_template

from app.models.ticket import Ticket
from app.models.agence import Agence

display_bp = Blueprint(
    'display_bp',
    __name__
)

@display_bp.route('/display')
def display():

    # =========================
    # TICKETS EN COURS
    # =========================

    tickets = (
        Ticket.query
        .filter_by(statut="En cours")
        .all()
    )

    appels = []

    for ticket in tickets:

        appels.append({

            "ticket": ticket.numero,

            "guichet": (
                ticket.guichet.numero
                if ticket.guichet else "?"
            )

        })

    # =========================
    # AGENCE
    # =========================

    agence = Agence.query.first()

    if not agence:

        class FakeAgence:
            nom = "Agence Centrale"

        agence = FakeAgence()

    # =========================
    # RENDER
    # =========================

    return render_template(

        'display.html',

        appels=appels,

        agence=agence

    )