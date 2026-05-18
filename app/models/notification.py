from app import db
from datetime import datetime


class Notification(db.Model):

    __tablename__ = 'notification'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    message = db.Column(db.Text)

    heure_envoi = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey('ticket.id'),
        nullable=False
    )
