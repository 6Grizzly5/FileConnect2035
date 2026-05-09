from app import db

class Service(db.Model):

    __tablename__ = 'service'

    id_service = db.Column(db.Integer, primary_key=True)

    nom = db.Column(db.String(100), nullable=False)

    duree_moyenne = db.Column(db.Integer, nullable=False)

    id_agence = db.Column(
        db.Integer,
        db.ForeignKey('agence.id_agence'),
        nullable=False
    )

    tickets = db.relationship('Ticket', backref='service', lazy=True)