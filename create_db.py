from app import create_app, db

from app.models.agence import Agence
from app.models.service import Service
from app.models.ticket import Ticket
from app.models.notification import Notification

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de données créée avec succès.")