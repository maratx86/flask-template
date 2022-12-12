import os

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '')


admins_email = os.environ.get('ADMINS_EMAIL')
if admins_email:
    admins_email = admins_email.split(';')
else:
    admins_email = []

environment = os.environ.get('ENVIRONMENT') or 'default'


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your_email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or MAIL_USERNAME


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
