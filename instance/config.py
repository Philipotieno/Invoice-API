"""
Contains general settings for environments to have by default
"""
import os

#config.py
class Config(object):
    """Parent/default configutaion"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Development configuration"""
    DEBUG = False

app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}