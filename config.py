import os
_basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'srr9KJ8IHElAZF869w'

MONGODB_DATABASE = "dlop"
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

CELERY_BROKER_URL = 'mongodb://localhost:27017/dlop'
CELERY_BROKER_BACKEND = 'mongodb://localhost:30000/'
CELERY_BROKER_BACKEND_SETTINGS = {
    'database': 'dlop',
    'taskmeta_collection': 'my_taskmeta_collection',
    'CELERY_TIMEZONE': 'CHINA/ShangHai'
}
