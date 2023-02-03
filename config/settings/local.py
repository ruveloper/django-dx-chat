from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="77iajDsE7X6ofymkasdeeERqwg3#$3!356HDasdbQNrr9VBn9jVq4hLwML62OusyJN",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
# https://docs.djangoproject.com/en/stable/ref/settings/#internal-ips
INTERNAL_IPS = ALLOWED_HOSTS

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db_url("DATABASE_URL", default="sqlite:///db.sqlite3")}

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# * -------------------------- THIRD-PARTY CONFIG ------------------------------

# DJANGO CHANNELS
# ------------------------------------------------------------------------------
# https://channels.readthedocs.io/en/stable/
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# DAPHNE ASGI SERVER
# ------------------------------------------------------------------------------
# Allow Daphne’s ASGI version of the runserver management command
INSTALLED_APPS = [
    "daphne",
] + INSTALLED_APPS  # noqa F405

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405

# * Google reCaptcha v3
# * ------------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = env(
    "RECAPTCHA_PUBLIC_KEY", default="6mPas--PLACEHOLDER_KEY--3226_"
)
RECAPTCHA_PRIVATE_KEY = env(
    "RECAPTCHA_PRIVATE_KEY", default="6mPas--PLACEHOLDER_KEY--3226_"
)
RECAPTCHA_REQUIRED_SCORE = env.float("RECAPTCHA_REQUIRED_SCORE", default=0.85)
