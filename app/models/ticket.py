from app import db
from datetime import datetime

class Ticket(db.Model):

    __tablename__ = 'ticket'

    id_ticket = db.Column(db.Integer, primary_key=True)

    numero = db.Column(db.String(20), nullable=False)

    heure_arrivee = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    position_file = db.Column(db.Integer)

    temps_estime = db.Column(db.Integer)

    statut = db.Column(
        db.String(20),
        default='EN_ATTENTE'
    )

    id_service = db.Column(
        db.Integer,
        db.ForeignKey('service.id_service'),
        nullable=False
    )