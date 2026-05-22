from datetime import datetime

from app.models.ticket import Ticket
from app.models.guichet import Guichet

import heapq

def choisir_ticket_pour_guichet(id_guichet):

    guichet = Guichet.query.get(id_guichet)

    if not guichet:
        return None

    if guichet.statut != 'disponible':
        return None

    tickets = (
        Ticket.query
        .filter_by(statut='En attente')
        .all()
    )

    if not tickets:
        return None

    heap = []

    for ticket in tickets:

        score = calcul_score(
            ticket,
            id_guichet
        )

        heapq.heappush(
            heap,
            (score, ticket.id)
        )

    meilleur_score, id_ticket = heapq.heappop(heap)

    meilleur_ticket = Ticket.query.get(
        id_ticket
    )

    return meilleur_ticket

    # ─────────────────────────────
    # SCORE INTELLIGENT
    # ─────────────────────────────

def calcul_score(ticket, id_guichet):

    duree = (
        ticket.service.duree_moyenne
        if ticket.service else 999
    )

    attente = (
        datetime.utcnow()
        - ticket.heure_creation
    ).total_seconds() / 60

    priorite = getattr(
        ticket,
        'priorite',
        0
    )

    charge_guichet = (
        Ticket.query
        .filter_by(
            id_guichet=id_guichet,
            statut='En cours'
        )
        .count()
    )

    score = (
        duree
        - (attente * 0.5)
        - (priorite * 3)
        + (charge_guichet * 2)
    )

    return score