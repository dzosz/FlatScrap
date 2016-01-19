import os

# FLASK APP
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))

# WSGI
HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS','localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME','flatscrap')
IP = os.environ.get('OPENSHIFT_PYTHON_IP','127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT',8080))

# DATABASE
REDIS_HOST = os.environ.get('OPENSHIFT_REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('OPENSHIFT_REDIS_PORT', 6379)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')

# WEBSCRAPER
MAX_PAGE_NUMBER = 10
