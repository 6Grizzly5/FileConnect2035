from app.models.ticket import Ticket
from app.models.service import Service

def calculer_position(id_service):

    tickets = Ticket.query.filter_by(
        id_service=id_service,
        statut='EN_ATTENTE'
    ).all()

    return len(tickets) + 1

def calculer_temps_estime(id_service):

    service = Service.query.get(id_service)

    tickets = Ticket.query.filter_by(
        id_service=id_service,
        statut='EN_ATTENTE'
    ).count()

    return tickets * service.duree_moyenne