from flask import Blueprint
from flask import jsonify
from flask import request

from datetime import datetime

from app.models.ticket import Ticket
from app.models.guichet import Guichet
from app import db

from app.structures.hash_table import (
    HashTable
)

from app.structures.tas_binaire import (
    TasBinaire
)

from app.structures.graphe_guichets import (
    GrapheGuichets
)

appel_bp = Blueprint(
    'appel_bp',
    __name__
)

# ==================================================
# STRUCTURES AVANCÉES
# ==================================================

historique_appels = HashTable()

file_prioritaire = TasBinaire()

graphe = GrapheGuichets()

# ==================================================
# INITIALISATION GRAPHE
# ==================================================

for i in range(1, 20):

    graphe.ajouter_guichet(
        f"G{i}"
    )

# connexions fictives

graphe.connecter("G1", "G2")
graphe.connecter("G2", "G3")
graphe.connecter("G3", "G4")

# ==================================================
# APPEL TICKET
# ==================================================

@appel_bp.route(
    '/appel_ticket',
    methods=['POST']
)
def appel_ticket():

    data = request.json

    id_guichet = data.get(
        'id_guichet'
    )

    guichet = Guichet.query.get(
        id_guichet
    )

    if not guichet:

        return jsonify({
            'error': 'Guichet introuvable'
        }), 404

    # -------------------------
    # CHERCHER TICKET
    # -------------------------

    ticket = (
        Ticket.query
        .filter_by(
            statut="En attente"
        )
        .order_by(
            Ticket.position.asc()
        )
        .first()
    )

    if not ticket:

        return jsonify({
            'message': 'Aucun ticket'
        })

    # -------------------------
    # TAS BINAIRE
    # -------------------------

    file_prioritaire.inserer(
        ticket.position,
        ticket.numero
    )

    prochain = (
        file_prioritaire
        .extraire_min()
    )

    # -------------------------
    # UPDATE TICKET
    # -------------------------

    ticket.statut = "En cours"

    ticket.id_guichet = guichet.id

    ticket.heure_debut = datetime.utcnow()

    db.session.commit()

    # -------------------------
    # HASH TABLE
    # -------------------------

    historique_appels.insert(

        ticket.numero,

        {
            "guichet": guichet.numero,
            "heure": str(datetime.utcnow())
        }
    )

    return jsonify({

        "ticket": ticket.numero,

        "guichet": guichet.numero,

        "historique": historique_appels.get(
            ticket.numero
        ),

        "graphe": graphe.afficher()

    })