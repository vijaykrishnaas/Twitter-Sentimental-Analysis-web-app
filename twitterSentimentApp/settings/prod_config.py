import os
from .base_config import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = ['localhost']