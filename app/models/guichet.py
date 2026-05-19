from app import db


class Guichet(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    numero = db.Column(
        db.Integer,
        nullable=False
    )

    statut = db.Column(
        db.String(30),
        default='disponible'
    )

    id_agence = db.Column(
        db.Integer,
        db.ForeignKey('agence.id')
    )
    
    agence = db.relationship(
        'Agence',
        backref='guichets'
    )