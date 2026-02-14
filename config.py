import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session configuration
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT', 'False').lower() == 'true'
    SESSION_USE_SIGNER = os.environ.get('SESSION_USE_SIGNER', 'True').lower() == 'true'
    PERMANENT_SESSION_LIFETIME = int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600))
    
    # Active Directory configuration
    AD_SERVER = os.environ.get('AD_SERVER', 'ldap://localhost')
    AD_DOMAIN = os.environ.get('AD_DOMAIN', 'DOMAIN')
    AD_BASE_DN = os.environ.get('AD_BASE_DN', 'DC=domain,DC=com')
    AD_BIND_USER = os.environ.get('AD_BIND_USER', '')
    AD_BIND_PASSWORD = os.environ.get('AD_BIND_PASSWORD', '')
    AD_USE_SSL = os.environ.get('AD_USE_SSL', 'False').lower() == 'true'
    AD_PORT = int(os.environ.get('AD_PORT', 636 if os.environ.get('AD_USE_SSL', 'False').lower() == 'true' else 389))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
