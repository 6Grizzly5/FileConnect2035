from datetime import datetime

from app.models.ticket import Ticket
from app.models.guichet import Guichet


def choisir_ticket_pour_guichet(id_guichet):

    guichet = Guichet.query.get(id_guichet)

    if not guichet:
        return None

    # Guichet fermé/pause
    if guichet.statut != 'disponible':
        return None

    # Tickets en attente
    tickets = (
        Ticket.query
        .filter_by(statut='En attente')
        .all()
    )

    if not tickets:
        return None

    # ─────────────────────────────
    # SCORE INTELLIGENT
    # ─────────────────────────────

    def calcul_score(ticket):

        # durée du service
        duree = (
            ticket.service.duree_moyenne
            if ticket.service else 999
        )

        # attente réelle
        maintenant = datetime.utcnow()

        attente = (
            maintenant - ticket.heure_creation
        ).total_seconds() / 60

        # priorité future possible
        priorite = getattr(ticket, 'priorite', 0)

        # charge du guichet
        charge_guichet = (
            Ticket.query
            .filter_by(
                id_guichet=id_guichet,
                statut='En cours'
            )
            .count()
        )

        # ─────────────────────────
        # FORMULE
        # ─────────────────────────

        score = (
            duree
            - (attente * 0.5)
            - (priorite * 3)
            + (charge_guichet * 2)
        )

        return score

    # TRI FINAL
    tickets = sorted(
        tickets,
        key=lambda t: calcul_score(t)
    )

    return tickets[0]