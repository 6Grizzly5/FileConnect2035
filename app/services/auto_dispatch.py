from datetime import datetime

from app import db

from app.models.guichet import Guichet
from app.models.ticket import Ticket

from app.services.dispatch_algo import (
    choisir_ticket_pour_guichet
)


def verifier_guichets():

    guichets = Guichet.query.all()

    for guichet in guichets:

        if guichet.statut != "disponible":
            continue

        # Ticket actuel du guichet
        ticket_en_cours = Ticket.query.filter_by(
            id_guichet=guichet.id,
            statut="En cours"
        ).first()

        # SI AUCUN TICKET
        if not ticket_en_cours:

            attribuer_ticket(guichet)

            continue

        # VERIFIER SI TEMPS DEPASSE
        service = ticket_en_cours.service

        if not service:
            continue

        duree = service.duree_moyenne
        if not ticket_en_cours.heure_debut_service:
            continue

        temps_ecoule = (
            datetime.utcnow() -
            ticket_en_cours.heure_debut_service
        ).total_seconds() / 60

        # SERVICE TERMINE
        if temps_ecoule >= duree:

            ticket_en_cours.statut = "Terminé"

            db.session.commit()

            attribuer_ticket(guichet)


def attribuer_ticket(guichet):

    ticket = choisir_ticket_pour_guichet(
        guichet.id
    )

    if not ticket:
        return

    ticket.statut = "En cours"

    ticket.id_guichet = guichet.id

    ticket.heure_debut_service = datetime.utcnow()

    db.session.commit()