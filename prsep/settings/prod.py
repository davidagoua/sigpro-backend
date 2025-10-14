import os
from .base import *



SECRET_KEY = os.environ.get('SECRET_KEY','my_secret_key')
ALLOWED_HOSTS = ['*','https://sigpro-mena.com']

TRUSTED_ORIGINS = ['https://sigpro-mena.com','http://sigpro-mena.com','https://test.localhost']
CSRF_TRUSTED_ORIGINS = ['https://sigpro-mena.com','http://sigpro-mena.com','http://*.sigpro-mena.com','https://test.localhost']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "mydatabase"),
        "USER": os.environ.get("POSTGRES_USER", "mydatabaseuser"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "mypassword"),
        "HOST": os.environ.get("DB_HOST", "postgis"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
