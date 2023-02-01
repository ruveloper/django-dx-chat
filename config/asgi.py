"""
ASGI config for Django HTMX Chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# apps directory.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "apps"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# * WEBSOCKETS
# ------------------------------------------------------------------------------
# Import websocket application here, so apps from django_application are loaded first
from apps.chat import routing  # noqa isort:skip
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa isort:skip
from channels.security.websocket import AllowedHostsOriginValidator  # noqa isort:skip
from channels.auth import AuthMiddlewareStack  # noqa isort:skip

# ProtocolTypeRouter determines which application should handle incoming requests based on their protocol type
application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": AllowedHostsOriginValidator(
            # https://channels.readthedocs.io/en/latest/topics/security.html#security
            AuthMiddlewareStack(
                # https://channels.readthedocs.io/en/latest/topics/authentication.html#django-authentication
                URLRouter(
                    # https://channels.readthedocs.io/en/latest/topics/routing.html#routing
                    routing.websocket_urlpatterns
                ),
            )
        ),
    }
)
