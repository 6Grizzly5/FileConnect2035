from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)

    from app.routes.ticket_routes import ticket_bp
    from app.routes.service_routes import service_bp
    from app.routes.web_routes import web_bp
    from app.routes.agence_routes import agence_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(ticket_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(agence_bp)
    app.register_blueprint(admin_bp)

    return app