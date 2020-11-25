from django.apps import AppConfig
from django.db.models.signals import post_save, post_migrate
from allauth.account.signals import user_logged_in


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
            create_staff_group,
            add_admin_permission,
            change_user_profile,
            store_login_information,
            login_signal,
        )

        """Signals"""
        post_migrate.connect(create_staff_group, sender=self)
        post_save.connect(add_admin_permission, sender=CustomUser)
        post_save.connect(change_user_profile, sender=CustomUser)
        login_signal.connect(store_login_information)