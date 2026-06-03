from flask import Flask

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config.from_object(
        'app.config.Config'
    )

    db.init_app(app)

    # -------------------------
    # IMPORT ROUTES
    # -------------------------

    from app.routes.agence_routes import (
        agence_bp
    )

    from app.routes.service_routes import (
        service_bp
    )

    from app.routes.ticket_routes import (
        ticket_bp
    )

    from app.routes.display_routes import (
        display_bp
    )
    
    from app.routes.admin_routes import (
        admin_bp
    )
    
    from app.routes.guichet_routes import (
        guichet_bp
    )
    
    from app.routes.appel_routes import (
        appel_bp
    )

    # -------------------------
    # REGISTER
    # -------------------------

    app.register_blueprint(
        agence_bp
    )

    app.register_blueprint(
        service_bp
    )

    app.register_blueprint(
        ticket_bp
    )

    app.register_blueprint(
        display_bp
    )
    
    app.register_blueprint(
        admin_bp
    )
    
    app.register_blueprint(
        guichet_bp
    )
    
    app.register_blueprint(
        appel_bp
    )
    
    return app
