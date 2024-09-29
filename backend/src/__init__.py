# src/__init__.py
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from .utils.logger import setup_logger
##from .routes.debug import debug_bp

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    
    # Load environment variables
    load_dotenv()

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "filmflow.db")}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    # Setup logger
    setup_logger()

    # Import models to register them with SQLAlchemy
    from .models import User, Script

    # Import blueprints
    from .routes.generate_text import generate_text_bp
    from .routes.auth import auth_bp
    from .routes.scripts import scripts_bp
    from .routes.home import home_bp

    # Register blueprints
    app.register_blueprint(generate_text_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(scripts_bp, url_prefix='/scripts')
    app.register_blueprint(home_bp)
    ##app.register_blueprint(debug_bp)  # Register the debug blueprint

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "An internal error occurred.", "details": str(error)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
