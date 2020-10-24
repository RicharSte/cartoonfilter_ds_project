import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = ''
ALLOWED_EXTENSIONS = {'jpg'}
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False