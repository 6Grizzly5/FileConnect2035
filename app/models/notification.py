from app import db
from datetime import datetime

class Notification(db.Model):

    __tablename__ = 'notification'

    id_notification = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text)

    heure_envoi = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    id_ticket = db.Column(
        db.Integer,
        db.ForeignKey('ticket.id_ticket'),
        nullable=False
    )