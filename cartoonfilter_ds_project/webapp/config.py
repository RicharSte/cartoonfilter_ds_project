from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'Your secret key'
ALLOWED_EXTENSIONS = {'jpg'}
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

REMEMBER_COOKIE_DURATION = timedelta(days=5)

SQLALCHEMY_TRACK_MODIFICATIONS = False
