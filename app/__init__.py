from flask import Flask
from flask_session import Session
from config import config
import os

# Initialize Flask-Session
sess = Session()

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    sess.init_app(app)
    
    # Register blueprints
    from app.auth import auth_bp
    from app.users import users_bp
    from app.groups import groups_bp
    from app.computers import computers_bp
    from app.main import main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(groups_bp, url_prefix='/groups')
    app.register_blueprint(computers_bp, url_prefix='/computers')
    
    return app
