import os

# Default config
class BaseConfig(object):
	DEBUG = False

	SECRET_KEY = 'secret_key'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False