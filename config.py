import os, datetime
from configparser import ConfigParser
from server.tools.assists import getconfig

basedir = os.path.abspath(os.path.dirname(__file__))


config = ConfigParser()
config.read('config.cfg')


database_path = os.getenv('DATABASE_URL')
database_path = getconfig(
    config, 'DATABASE', 'database_url') if not database_path else database_path
database_path = 'sqlite:///../server/db/sqlite.db' if not database_path else database_path


class Config:
    DEFAULT_SECRET_KEY = os.urandom(32)
    DEFAULT_SECRET_KEY = 'secret key'
    SECRET_KEY = os.environ.get("SECRET_KEY", DEFAULT_SECRET_KEY)
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class ApplicationConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = database_path

    # SESSION_TYPE = "filesystem"
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True

    CORS_HEADERS = 'Content-Type'
    PROPAGATE_EXCEPTIONS = True


    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES_WHEN_REMEMBER = datetime.timedelta(days=30)

    EXP_TIME_INVITATION_LINK_OF_COMPANY = datetime.timedelta(minutes=30)

    ENDPOINT_MAKE_USER_OFFLINE_AFTER_N_SECONDS = 5

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = 'public'
    RECAPTCHA_PRIVATE_KEY = 'private'
    RECAPTCHA_OPTIONS = {'theme': 'white'}

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'aliyutimileyin@gmail.com'
    MAIL_PASSWORD = 'jnhizfbhsbtuqaxi'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = 'R-I Software <ri-team@ri.website.com>'


    LOG_FOLDER = 'server/logs/'   
    LOG_FILE_MAIN_NAME = LOG_FOLDER + 'main.error.log'
    LOG_FILE_END_MAIN_NAME = LOG_FOLDER + 'end.error.log'



class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    DEBUG = True
    SQLALCHEMY_ECHO=True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    DEBUG = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS= False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_ECHO = False
    TESTING = True


