#!/usr/bin/env python

"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """change settings according to DJANGO_ENV"""
    if os.environ.get("DJANGO_ENV") == "production":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.prod_settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.base_settings")

    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
