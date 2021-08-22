import os
from .base_config import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = ['localhost', '18.116.100.58', '18.116.100.58:8001', 'analysis.twittersentiment.tech']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
