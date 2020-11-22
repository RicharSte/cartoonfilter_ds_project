from datetime import timedelta
import os

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''

basedir = os.path.abspath(os.path.dirname(__file__))
PATH_TO_DOWNLOADS = os.path.join(
os.path.abspath(os.path.dirname(__file__)), 'static', 'images', 'downloads')

SECRET_KEY = ''
ALLOWED_EXTENSIONS = {'jpg'}
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

REMEMBER_COOKIE_DURATION = timedelta(days=5)

SQLALCHEMY_TRACK_MODIFICATIONS = False

#список фотографий для каруселм
name_photo_example = ['liuyifei4.jpg', 'mountain4.jpg', 'photo1_cartoon.jpg',
                              'photo2_cartoon.jpg']

PHOTO_PATH = os.path.join('static', 'images', 'downloads')