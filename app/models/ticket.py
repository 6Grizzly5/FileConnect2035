from app import db
from datetime import datetime


class Ticket(db.Model):

    __tablename__ = "ticket"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    numero = db.Column(
        db.String(20),
        nullable=False
    )

    client = db.Column(
        db.String(100)
    )

    position = db.Column(
        db.Integer
    )

    # Temps estimé d'attente en minutes (rempli par calcul_file)
    temps_estime = db.Column(
        db.Integer
    )

    statut = db.Column(
        db.String(50),
        default="En attente"
    )

    heure_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("service.id")
    )

    # Relation pour accès facile au service
    service = db.relationship(
        "Service",
        backref="tickets_list",
        lazy=True
    )
    
    id_guichet = db.Column(
        db.Integer,
        db.ForeignKey('guichet.id')
    )
