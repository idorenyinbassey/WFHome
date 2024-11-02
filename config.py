class Config:
    """Configuration class for the Flask application."""
    SECRET_KEY = 'your_secret_key_here'  # Replace with a secure random key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Path to your SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable overhead of SQLAlchemy events
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing