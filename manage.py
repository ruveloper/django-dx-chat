#!/usr/bin/env python
import sys
from pathlib import Path

from config.settings.base import env

if __name__ == "__main__":

    # GET SETTINGS MODULE
    # ---------------------------------------------------------------------------
    # If DJANGO_SETTINGS_MODULE is unset, default to the local settings
    env("DJANGO_SETTINGS_MODULE", default="config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # apps directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "apps"))

    execute_from_command_line(sys.argv)
