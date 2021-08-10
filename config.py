import os

from environs import Env

env = Env()
env.read_env(os.path.abspath('./all.env'))


class Config:
    """Flask App configuration"""
    TESTING: bool
    DEBUG: bool

    SECRET_KEY = 'super-secret-key'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductConfig(Config):
    """Product configuration"""
    ENV = 'production'
    DEBUG = False

    POSTGRES_USER = env.str('POSTGRES_USER')
    POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
    POSTGRES_DB = env.str('POSTGRES_DB')
    POSTGRES_HOST = env.str('POSTGRES_HOST')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'


class TestConfig(Config):
    """Test configuration"""

    ENV = 'development'

    TESTING = True
    DEBUG = True


class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(Config.APP_DIR, "app.db")}'

