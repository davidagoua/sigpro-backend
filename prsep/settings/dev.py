from .base import *

INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

PUSHER_APP_ID='some-id'
PUSHER_KEY='some-key'
PUSHER_SECRET='app-secret'
PUSHER_HOST='sigpro-mena.com'