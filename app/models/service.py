from app import db


class Service(db.Model):

    __tablename__ = "service"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    duree_moyenne = db.Column(
        db.Integer
    )

    agence_id = db.Column(
        db.Integer,
        db.ForeignKey("agence.id")
    )