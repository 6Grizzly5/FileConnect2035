from app import db


class Agence(db.Model):

    __tablename__ = 'agence'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    ville = db.Column(
        db.String(100)
    )

    adresse = db.Column(
        db.String(255)
    )

    telephone = db.Column(
        db.String(30)
    )
    
    qr_image = db.Column(
        db.String(255)
    )