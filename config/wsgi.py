import os

from django.core.wsgi import get_wsgi_application

"""change settings according to DJANGO_ENV"""
if os.environ.get("DJANGO_ENV") == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.prod_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.base_settings")

application = get_wsgi_application()
