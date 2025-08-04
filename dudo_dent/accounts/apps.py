from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dudo_dent.accounts'

    def ready(self):
        import dudo_dent.accounts.signals