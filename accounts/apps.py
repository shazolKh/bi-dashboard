from django.apps import AppConfig
from django.db.models.signals import post_save, post_migrate


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        """
        Runs when accounts app is ready. Imports HAS TO be here.
        """
        from .models import CustomUser
        from .signals import (
            create_staff_group,
            add_admin_permission,
            create_user_profile,
        )

        """Signals"""
        post_migrate.connect(create_staff_group, sender=self)
        post_save.connect(add_admin_permission, sender=CustomUser)
        post_save.connect(create_user_profile, sender=CustomUser)
