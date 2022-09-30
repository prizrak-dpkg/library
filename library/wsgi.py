"""
WSGI config for library project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os, sys
import django
from pathlib import Path
from django.core.wsgi import get_wsgi_application


os.environ["DJANGO_SETTINGS_MODULE"] = "library.settings.local_settings"
django.setup()

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
application = get_wsgi_application()
