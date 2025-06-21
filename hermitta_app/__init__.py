from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config_by_name, get_config_name

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """
    Application factory function.
    """
    if config_name is None:
        config_name = get_config_name()

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here to ensure they are registered with SQLAlchemy
    from models.user import User
    from models.property import Property
    from models.lease import Lease
    from models.financial_transaction import FinancialTransaction
    from models.maintenance_request import MaintenanceRequest
    # Import other models as they are created/converted

    # Register blueprints
    from hermitta_app.routes.user_routes import user_bp
    from hermitta_app.routes.property_routes import property_bp

    app.register_blueprint(user_bp) # url_prefix is defined in the blueprint itself
    app.register_blueprint(property_bp) # url_prefix is defined in the blueprint itself

    # Simple test route
    @app.route('/health')
    def health_check():
        return "OK"

    return app
