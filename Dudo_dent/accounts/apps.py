from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dudo_dent.accounts'

    def ready(self):
        import Dudo_dent.accounts.signals