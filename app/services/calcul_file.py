"""
calcul_file.py
==============
Algorithme de gestion intelligente de la file d'attente.

Règle appliquée : SPT — Shortest Processing Time (First)
---------------------------------------------------------
Principe : parmi les tickets "En attente", on trie par durée
du service demandé (croissant). Le client dont le service est
le plus court passe en premier, celui dont le service est le
plus long attend le plus. Cette règle minimise le temps
d'attente moyen global de tous les clients dans la file.

Exemple :
  - Client A : Virement bancaire (10 min)  → position 2
  - Client B : Paiement facture (5 min)    → position 1  ✓
  - Client C : Retrait d'argent (15 min)   → position 3

Résultat : temps d'attente moyen réduit au maximum.
"""

from app.models.ticket import Ticket
from app.models.service import Service


# ============================================================
# REORDONNER LA FILE (SPT)
# ============================================================

def reordonner_file():
    """
    Réordonne tous les tickets "En attente" selon la règle SPT :
    du service le plus court au plus long.
    Met à jour position et temps_estime pour chaque ticket.
    Retourne la liste ordonnée.
    """

    tickets_attente = (
        Ticket.query
        .filter_by(statut="En attente")
        .all()
    )

    # Trier par durée_moyenne du service (croissant = SPT)
    tickets_attente.sort(
        key=lambda t: _duree_service(t.service_id)
    )

    # Mise à jour positions et temps_estime
    for index, ticket in enumerate(tickets_attente):

        position = index + 1
        ticket.position = position

        duree = _duree_service(ticket.service_id)

        # Temps estimé = somme des durées des tickets devant soi
        temps = sum(
            _duree_service(tickets_attente[i].service_id)
            for i in range(index)
        ) + duree

        ticket.temps_estime = temps

    return tickets_attente


# ============================================================
# CALCULER POSITION D'UN NOUVEAU TICKET
# ============================================================

def calculer_position(service_id):
    """
    Retourne la position qu'occupera un nouveau ticket
    pour ce service selon la règle SPT.
    Les tickets dont le service est plus long sont repoussés.
    """

    duree_nouveau = _duree_service(service_id)

    tickets_attente = (
        Ticket.query
        .filter_by(statut="En attente")
        .all()
    )

    # Combien de tickets ont un service strictement plus court ?
    # Ce nouveau ticket se place juste après eux.
    position = sum(
        1 for t in tickets_attente
        if _duree_service(t.service_id) <= duree_nouveau
    ) + 1

    return position


# ============================================================
# CALCULER TEMPS ESTIMÉ D'UN NOUVEAU TICKET
# ============================================================

def calculer_temps_estime(service_id):
    """
    Retourne le temps d'attente estimé (en minutes) pour un
    nouveau ticket de ce service, en tenant compte de l'ordre SPT.
    """

    duree_nouveau = _duree_service(service_id)

    tickets_attente = (
        Ticket.query
        .filter_by(statut="En attente")
        .all()
    )

    # Durée des services qui passeront avant ce ticket
    temps = sum(
        _duree_service(t.service_id)
        for t in tickets_attente
        if _duree_service(t.service_id) <= duree_nouveau
    ) + duree_nouveau

    return temps


# ============================================================
# HELPER PRIVÉ
# ============================================================

def _duree_service(service_id):
    """Retourne la durée moyenne d'un service (0 si introuvable)."""

    service = Service.query.get(service_id)

    if service and service.duree_moyenne:
        return service.duree_moyenne

    return 0
