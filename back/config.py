from os import path

basedir = path.abspath(path.dirname(__file__))

# FIX D8 : jamais de debug en production
DEBUG = False
TESTING = False

CORS_ORIGINS = ["http://localhost:9000"]

SQLALCHEMY_DATABASE_URI = "sqlite:///./database.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False
