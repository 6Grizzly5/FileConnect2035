from app import db

class Agence(db.Model):

    __tablename__ = 'agence'

    id_agence = db.Column(db.Integer, primary_key=True)

    nom = db.Column(db.String(100), nullable=False)

    type = db.Column(db.String(50), nullable=False)

    adresse = db.Column(db.Text)

    services = db.relationship('Service', backref='agence', lazy=True)