"""
Application configuration with different environments:
- Development: Debug mode, SQLite database
- Testing: Testing mode, separate test database
- Production: Production settings
"""

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(BASEDIR, db_name)


class Config:
    # For securing session data and tokens
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret key, just for testing"

    # SQLAlchemy settings
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True    # Automatically commit DB changes after request
    SQLALCHEMY_RECORD_QUERIES = True        # Enable query recording for debugging
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to improve performance

    @staticmethod
    def init_app(app):
        pass            # Hook for configuration-specific initialization


class DevelopmentConfig(Config):
    DEBUG = True        # Enables debug mode for detailed error pages
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("todolist-dev.db")      # Development database


class TestingConfig(Config):
    TESTING = True      # Enables testing mode
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("todolist-test.db")     # Test database
    WTF_CSRF_ENABLED = False     # Disables CSRF protection for testing
    import logging

    # Configures detailed logging for tests
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.DEBUG)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("todolist.db")      # Production database


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
