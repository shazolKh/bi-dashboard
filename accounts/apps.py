from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    """
    Account app config to store signals.
    """

    name = "accounts"

    def ready(self):
        """
        Runs when accounts app is ready. Imports HAS TO be here.
        """
        from .models import CustomUser
        from .signals import (
            change_user_profile,
            store_login_information,
            login_signal,
        )

        """Signals"""
        post_save.connect(change_user_profile, sender=CustomUser)
        login_signal.connect(store_login_information)